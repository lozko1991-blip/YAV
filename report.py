# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from xml.etree import ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
STATE_PATH = os.path.join(SCRIPT_DIR, "state.json")
FEED_PATH = os.path.join(SCRIPT_DIR, "kasta_feed.xml")
REPORT_PATH = os.path.join(SCRIPT_DIR, "report.html")


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"runs": []}


def save_state(state):
    state["updated"] = datetime.now().isoformat()
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def parse_feed():
    tree = ET.parse(FEED_PATH)
    root = tree.getroot()
    shop = root.find("shop")
    categories = {}
    for cat in shop.find("categories").findall("category"):
        cid = cat.get("id")
        parent = cat.get("parentId", "")
        name = (cat.text or "").strip()
        categories[cid] = {"name": name, "parent": parent}

    offers = []
    for o in shop.find("offers").findall("offer"):
        item = {
            "id": o.get("id"),
            "available": o.get("available") == "true",
            "group_id": o.get("group_id", ""),
            "categoryId": o.findtext("categoryId", ""),
            "price": int(o.findtext("price", "0")),
            "old_price": o.findtext("old_price"),
            "price_promo": o.findtext("price_promo"),
            "vendor": (o.findtext("vendor") or "").strip(),
            "has_name_ua": bool((o.findtext("name_ua") or "").strip()),
            "has_name": bool((o.findtext("name") or "").strip()),
            "has_desc_ua": bool((o.findtext("description_ua") or "").strip()),
            "has_desc": bool((o.findtext("description") or "").strip()),
        }
        if item["old_price"]:
            item["old_price"] = int(item["old_price"])
        if item["price_promo"]:
            item["price_promo"] = int(item["price_promo"])
        offers.append(item)
    return offers, categories


def build_report(offers, categories, state):
    now = datetime.now()
    offer_ids = {o["id"] for o in offers}
    avail = sum(1 for o in offers if o["available"])
    unavail = sum(1 for o in offers if not o["available"])

    prev_ids = set()
    week_ago_ids = set()
    for run in state.get("runs", []):
        run_ids = set(run.get("offer_ids", []))
        if run.get("date", "").startswith(now.strftime("%Y-%m-%d")):
            prev_ids = run_ids
        run_dt = datetime.fromisoformat(run["date"]) if run.get("date") else None
        if run_dt and run_dt >= now - timedelta(days=7):
            week_ago_ids |= run_ids

    new_today = offer_ids - prev_ids if prev_ids else offer_ids
    removed_today = prev_ids - offer_ids if prev_ids else set()
    new_week = offer_ids - week_ago_ids if week_ago_ids else offer_ids

    cat_counts = Counter(o["categoryId"] for o in offers)
    cat_avail = Counter(o["categoryId"] for o in offers if o["available"])
    cat_table = []
    for cid, cnt in cat_counts.most_common():
        cat_info = categories.get(cid, {})
        name = cat_info.get("name", cid)
        parent_name = categories.get(cat_info.get("parent", ""), {}).get("name", "")
        cat_table.append((cid, name[:60], parent_name[:40], cnt, cat_avail.get(cid, 0)))

    name_ua_only = sum(1 for o in offers if o["has_name_ua"] and not o["has_name"])
    name_both = sum(1 for o in offers if o["has_name_ua"] and o["has_name"])
    name_only = sum(1 for o in offers if not o["has_name_ua"] and o["has_name"])
    desc_ua_only = sum(1 for o in offers if o["has_desc_ua"] and not o["has_desc"])
    desc_both = sum(1 for o in offers if o["has_desc_ua"] and o["has_desc"])
    desc_only = sum(1 for o in offers if not o["has_desc_ua"] and o["has_desc"])

    prices = [o["price"] for o in offers if o["available"] and o["price"] > 0]
    price_min = min(prices) if prices else 0
    price_max = max(prices) if prices else 0
    price_avg = sum(prices) // len(prices) if prices else 0

    vendors = Counter(o["vendor"] for o in offers if o["vendor"])
    top_vendors = vendors.most_common(20)

    with_group = sum(1 for o in offers if o["group_id"])
    without_group = len(offers) - with_group

    html = _render_html(
        now=now,
        total=len(offers),
        avail=avail,
        unavail=unavail,
        new_today=new_today,
        removed_today=removed_today,
        new_week=new_week,
        cat_table=cat_table,
        name_ua_only=name_ua_only,
        name_both=name_both,
        name_only=name_only,
        desc_ua_only=desc_ua_only,
        desc_both=desc_both,
        desc_only=desc_only,
        price_min=price_min,
        price_max=price_max,
        price_avg=price_avg,
        top_vendors=top_vendors,
        with_group=with_group,
        without_group=without_group,
        total_cats=len(cat_table),
    )
    return html


def _render_html(**d):
    now_str = d["now"].strftime("%Y-%m-%d %H:%M:%S")

    cat_rows = ""
    for cid, name, parent, cnt, acnt in d["cat_table"][:100]:
        cat_rows += f"<tr><td>{cid}</td><td>{name}</td><td>{parent}</td><td>{cnt}</td><td>{acnt}</td></tr>"

    vendor_rows = ""
    for vname, vcnt in d["top_vendors"]:
        vendor_rows += f"<tr><td>{vname[:50]}</td><td>{vcnt}</td></tr>"

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YAVSHOKE — KASTA Feed Report</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f4f6f9; color: #1a1a2e; padding: 20px; }}
.container {{ max-width: 1200px; margin: 0 auto; }}
h1 {{ font-size: 1.6em; margin-bottom: 4px; }}
.subtitle {{ color: #666; font-size: 0.9em; margin-bottom: 24px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.card {{ background: #fff; border-radius: 10px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
.card .value {{ font-size: 2em; font-weight: 700; }}
.card .label {{ font-size: 0.85em; color: #888; margin-top: 2px; }}
.green {{ color: #10b981; }}
.red {{ color: #ef4444; }}
.blue {{ color: #3b82f6; }}
.purple {{ color: #8b5cf6; }}
.orange {{ color: #f59e0b; }}
.section {{ background: #fff; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
.section h2 {{ font-size: 1.15em; margin-bottom: 14px; color: #374151; }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.88em; }}
th, td {{ padding: 8px 10px; text-align: left; border-bottom: 1px solid #e5e7eb; }}
th {{ background: #f9fafb; font-weight: 600; color: #6b7280; font-size: 0.8em; text-transform: uppercase; }}
tr:hover {{ background: #f9fafb; }}
.bar {{ display: inline-block; height: 8px; border-radius: 4px; background: #3b82f6; vertical-align: middle; margin-right: 6px; }}
.lang-table td:first-child {{ font-weight: 500; }}
footer {{ text-align: center; color: #999; font-size: 0.8em; margin-top: 30px; }}
</style>
</head>
<body>
<div class="container">
<h1>YAVSHOKE — KASTA Feed Report</h1>
<p class="subtitle">Generated: {now_str} (UTC)</p>

<div class="grid">
<div class="card"><div class="value">{d["total"]:,}</div><div class="label">Total offers</div></div>
<div class="card"><div class="value green">{d["avail"]:,}</div><div class="label">Available</div></div>
<div class="card"><div class="value red">{d["unavail"]:,}</div><div class="label">Unavailable</div></div>
<div class="card"><div class="value blue">{len(d["new_today"]):,}</div><div class="label">New today</div></div>
<div class="card"><div class="value purple">{len(d["removed_today"]):,}</div><div class="label">Removed today</div></div>
<div class="card"><div class="value orange">{len(d["new_week"]):,}</div><div class="label">New this week</div></div>
<div class="card"><div class="value">{d["total_cats"]}</div><div class="label">Categories</div></div>
<div class="card"><div class="value">{d["price_min"]:,} грн</div><div class="label">Min price</div></div>
<div class="card"><div class="value">{d["price_max"]:,} грн</div><div class="label">Max price</div></div>
<div class="card"><div class="value">{d["price_avg"]:,} грн</div><div class="label">Avg price</div></div>
<div class="card"><div class="value">{d["with_group"]:,}</div><div class="label">With variants</div></div>
<div class="card"><div class="value">{d["without_group"]:,}</div><div class="label">Without variants</div></div>
</div>

<div class="section">
<h2>Language Coverage</h2>
<table class="lang-table">
<tr><th>Field</th><th>Count</th><th>%</th></tr>
<tr><td>name_ua only (Ukrainian name)</td><td>{d["name_ua_only"]:,}</td><td>{_pct(d["name_ua_only"], d["total"])}</td></tr>
<tr><td>name + name_ua (both)</td><td>{d["name_both"]:,}</td><td>{_pct(d["name_both"], d["total"])}</td></tr>
<tr><td>name only (no Ukrainian)</td><td>{d["name_only"]:,}</td><td>{_pct(d["name_only"], d["total"])}</td></tr>
<tr><td>description_ua only</td><td>{d["desc_ua_only"]:,}</td><td>{_pct(d["desc_ua_only"], d["total"])}</td></tr>
<tr><td>description + description_ua (both)</td><td>{d["desc_both"]:,}</td><td>{_pct(d["desc_both"], d["total"])}</td></tr>
<tr><td>description only (no Ukrainian)</td><td>{d["desc_only"]:,}</td><td>{_pct(d["desc_only"], d["total"])}</td></tr>
</table>
</div>

<div class="section">
<h2>Categories (top 100)</h2>
<table>
<tr><th>ID</th><th>Name</th><th>Parent</th><th>Total</th><th>Available</th></tr>
{cat_rows}
</table>
</div>

<div class="section">
<h2>Top Vendors</h2>
<table>
<tr><th>Vendor</th><th>Offers</th></tr>
{vendor_rows}
</table>
</div>

<footer>YAVSHOKE KASTA Feed — auto-generated every ~5 hours</footer>
</div>
</body>
</html>"""


def _pct(part, total):
    if total == 0:
        return "0%"
    return f"{part / total * 100:.1f}%"


def main():
    offers, categories = parse_feed()
    state = load_state()

    now = datetime.now()
    state.setdefault("runs", []).append({
        "date": now.isoformat(),
        "total": len(offers),
        "available": sum(1 for o in offers if o["available"]),
        "offer_ids": sorted(list({o["id"] for o in offers})),
    })

    # Keep last 14 runs max
    if len(state["runs"]) > 14:
        state["runs"] = state["runs"][-14:]

    save_state(state)
    html = build_report(offers, categories, state)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    new_today = 0
    prev_ids = set()
    for run in state["runs"][:-1]:
        if run.get("date", "").startswith(now.strftime("%Y-%m-%d")):
            prev_ids = set(run.get("offer_ids", []))
    if prev_ids:
        current = {o["id"] for o in offers}
        new_today = len(current - prev_ids)

    print(f"Report generated: {REPORT_PATH}")
    print(f"Total: {len(offers)}, Available: {sum(1 for o in offers if o['available'])}, New today: {new_today}")


if __name__ == "__main__":
    main()