# -*- coding: utf-8 -*-
import json
import os
import re
import html
from datetime import datetime
from xml.etree import ElementTree as ET

import requests

from color_normalizer import normalize_color, find_color_param, COLOR_PARAM_NAMES

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

HTML_TAG_RE = re.compile(r"<[^>]+>")
MULTI_SPACE_RE = re.compile(r"\s+")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_html(text):
    if not text:
        return ""
    text = HTML_TAG_RE.sub(" ", text)
    text = html.unescape(text)
    text = MULTI_SPACE_RE.sub(" ", text)
    return text.strip()[:5000]


def calc_markup(cost, tiers, min_markup_uah):
    tier = next((t for t in tiers if t["min"] <= cost <= t["max"]), None)
    if tier is None:
        return None, False
    if not tier.get("available", True):
        fallback = next((t for t in tiers if t.get("available", True)), None)
        if fallback:
            price = round(cost * (1 + fallback["percent"] / 100.0) + fallback["fixed"])
            if price - cost < min_markup_uah:
                price = round(cost + min_markup_uah)
            return price, False
        return None, False
    percent = tier["percent"]
    fixed = tier["fixed"]
    price = round(cost * (1 + percent / 100.0) + fixed)
    if price - cost < min_markup_uah:
        price = round(cost + min_markup_uah)
    return price, True


def build_kasta_xml(config):
    cfg = config
    resp = requests.get(cfg["source_url"], timeout=300)
    source_bytes = resp.content
    root_in = ET.fromstring(source_bytes)
    offers_in = root_in.find("shop/offers")
    categories_in = root_in.find("shop/categories")

    yml = ET.Element("yml_catalog", {"date": datetime.now().strftime("%Y-%m-%d %H:%M")})
    shop = ET.SubElement(yml, "shop")

    currs = ET.SubElement(shop, "currencies")
    ET.SubElement(currs, "currency", {"id": "UAH", "rate": "1"})

    cats = ET.SubElement(shop, "categories")
    cat_ids = set()
    if categories_in is not None:
        for cat in categories_in.findall("category"):
            cid = cat.get("id")
            if cid and cid not in cat_ids:
                cat_ids.add(cid)
                new = ET.SubElement(cats, "category", {"id": cid})
                parent = cat.get("parentId")
                if parent:
                    new.set("parentId", parent)
                new.text = cat.text or ""

    offers = ET.SubElement(shop, "offers")
    markup_cfg = cfg["markup"]
    tiers = markup_cfg["tiers"]
    min_markup = markup_cfg["min_markup_uah"]
    old_mul = markup_cfg["old_price_multiplier"]
    promo_mul = markup_cfg["promo_price_multiplier"]
    stock_qty = markup_cfg.get("stock_quantity", 6)

    cnt = 0
    for offer in offers_in.findall("offer"):
        offer_id = offer.get("id")
        group_id = offer.get("group_id", "")
        price_src = float(offer.findtext("price", "0"))

        final_price, available = calc_markup(price_src, tiers, min_markup)

        offer_attrs = {"id": offer_id, "available": "true" if available else "false"}
        if group_id:
            offer_attrs["group_id"] = group_id
        o = ET.SubElement(offers, "offer", offer_attrs)

        ET.SubElement(o, "currencyId").text = "UAH"
        ET.SubElement(o, "categoryId").text = offer.findtext("categoryId", "")

        if final_price is not None:
            final_price = round(final_price)
            ET.SubElement(o, "price").text = str(final_price)

            if available:
                old_price = round(final_price * old_mul)
                if old_price <= final_price:
                    old_price = final_price + 1
                ET.SubElement(o, "old_price").text = str(old_price)

                promo_price = round(final_price * promo_mul)
                ET.SubElement(o, "price_promo").text = str(promo_price)

                ET.SubElement(o, "stock_quantity").text = str(stock_qty)
        else:
            ET.SubElement(o, "price").text = "0"

        for pic in offer.findall("picture"):
            if pic.text:
                ET.SubElement(o, "picture").text = pic.text

        vendor = offer.findtext("vendor", "")
        if vendor:
            ET.SubElement(o, "vendor").text = vendor

        ET.SubElement(o, "article").text = offer.findtext("vendorCode", offer_id)

        name_ua = offer.findtext("name_ua", "")
        if name_ua:
            ET.SubElement(o, "name_ua").text = name_ua
        name_en = offer.findtext("name", "")
        if name_en:
            ET.SubElement(o, "name").text = name_en

        desc_ua = offer.findtext("description_ua", "")
        if desc_ua:
            ET.SubElement(o, "description_ua").text = clean_html(desc_ua)
        desc_en = offer.findtext("description", "")
        if desc_en:
            ET.SubElement(o, "description").text = clean_html(desc_en)

        barcode = offer.findtext("barcode", "")
        if barcode:
            ET.SubElement(o, "barcode").text = barcode

        color_found = False
        for param in offer.findall("param"):
            pname = param.get("name", "")
            if pname:
                pname_lower = pname.strip().lower()
                pvalue = param.text or ""
                if pname_lower in COLOR_PARAM_NAMES:
                    color_found = True
                    normalized = normalize_color(pvalue)
                    ET.SubElement(o, "param", {"name": "Колір"}).text = normalized
                else:
                    ET.SubElement(o, "param", {"name": pname}).text = pvalue

        if not color_found:
            ET.SubElement(o, "param", {"name": "Колір"}).text = "Комбінований"

        cnt += 1
        if cnt % 5000 == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed {cnt} offers...")

    xml_decl = '<?xml version="1.0" encoding="UTF-8"?>\n'
    body = ET.tostring(yml, encoding="unicode")
    return xml_decl + body, cnt


def main():
    cfg = load_config()
    xml_str, total = build_kasta_xml(cfg)
    out_path = os.path.join(SCRIPT_DIR, cfg["output_file"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"Done. Total offers: {total}. Output: {out_path}")


if __name__ == "__main__":
    main()