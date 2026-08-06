# -*- coding: utf-8 -*-
import re

# KASTA-compatible color list (from kasta.xlsx)
KASTA_COLORS = [
    "Лайм", "Сірий", "Синій", "Бузковий", "Сливовий",
    "Темно-бежевий", "Темно-бірюзовий", "Темно-бордовий", "Темно-вишневий",
    "Темно-блакитний", "Темно-зелений", "Темно-золотистий", "Темно-коричневий",
    "Темно-червоний", "Темно-рожевий", "Темно-сірий", "Темно-синій",
    "Темно-фіолетовий", "Теракотовий", "Фіолетовий", "Айворі", "Темно-ліловий",
    "Хакі", "Чорний", "Фуксія", "Кавовий", "Сіро-голубий", "Яскраво-червоний",
    "Бежевий", "Білосніжний", "Білий", "Безбарвний", "Бірюзовий", "Бордовий",
    "Бронзовий", "Блакитний", "Гірчичний", "Жовтий", "Перловий", "Зелений",
    "Золотий", "Смарагдовий", "Індиго", "Кораловий", "Коричневий", "Червоний",
    "Лавандовий", "Лососевий", "Малиновий", "Мідний", "Молочний",
    "Морської хвилі", "М'ятний", "Оливковий", "Помаранчевий", "Персиковий",
    "Охра", "Пурпурний", "Пісочний", "Рожево-ліловий", "Прозорий",
    "Рожево-коричневий", "Рожевий", "Салатовий", "Світло-бірюзовий",
    "Світло-вишневий", "Світло-бордовий", "Світло-жовтий", "Світло-коричневий",
    "Світло-червоний", "Світло-оранжевий", "Світло-ліловий", "Світло-рожевий",
    "Світло-сірий", "Світло-синій", "Світло-фіолетовий", "Срібний",
    "Сіро-синій", "Комбінований", "Пудровий", "Вишневий", "Ліловий",
    "Світло-пурпурний", "Темно-пурпурний", "Фісташковий", "Сіро-бежевий",
    "Сіро-коричневий", "Кислотно-жовтий", "Кислотно-рожевий",
    "Кислотно-оранжевий", "Кислотно-зелений", "Сіро-зелений", "Чорно-білий",
    "Сіро-червоний", "Синьо-жовтий", "Метал", "Графітовий", "Нержавіюча сталь",
    "Золотистий", "Койот", "Світло-бежевий", "Світло-зелений",
    "Світло-блакитний", "Кремовий", "Пляшковий зелений", "Волошковий",
    "Рудий", "Бурштиновий", "Блідо-рожевий", "Цегляний",
    "Помаранчево-червоний", "Сріблястий",
]

COLOR_PARAM_NAMES = {
    "колір", "color", "colour", "цвіт", "цвет", "кольор",
    "забарвлення", "окрас", "відтінок", "колірна гама", "палітра",
}

SEPARATOR_RE = re.compile(r"[/\\,;+]+|\s+з\s+|\s+та\s+|\s+і\s+|\s+й\s+|\s*&\s*")
WITH_SEPARATOR_RE = re.compile(r"\s+с\s+|\s+со\s+|\s+з\s+|\s+із\s+")
MULTI_HYPHEN_RE = re.compile(r"(.+)-(.+)-(.+)")

RU_UA_COLORS = {
    "белый": "Білий", "чёрный": "Чорний", "черный": "Чорний",
    "серый": "Сірий", "красный": "Червоний", "синий": "Синій",
    "зелёный": "Зелений", "зеленый": "Зелений", "жёлтый": "Жовтий",
    "желтый": "Жовтий", "коричневый": "Коричневий", "розовый": "Рожевий",
    "оранжевый": "Помаранчевий", "фиолетовый": "Фіолетовий",
    "голубой": "Блакитний", "бежевый": "Бежевий", "бирюзовый": "Бірюзовий",
    "золотой": "Золотий", "золотистый": "Золотистий",
    "серебристый": "Сріблястий", "серебряный": "Срібний",
    "бордовый": "Бордовий", "салатовый": "Салатовий",
    "прозрачный": "Прозорий", "кремовый": "Кремовий",
    "песочный": "Пісочний", "хаки": "Хакі", "графитовый": "Графітовий",
    "вишневый": "Вишневий", "бронзовый": "Бронзовий",
    "лиловый": "Ліловий", "малиновый": "Малиновий",
    "оливковый": "Оливковий", "фисташковый": "Фісташковий",
    "персиковый": "Персиковий", "пурпурный": "Пурпурний",
    "лавандовый": "Лавандовий", "мятный": "М'ятний",
    "коралловый": "Кораловий", "изумрудный": "Смарагдовий",
    "сиреневый": "Бузковий", "бирюза": "Бірюзовий",
    "терракотовый": "Теракотовий", "фуксия": "Фуксія",
    "морская волна": "Морської хвилі", "слоновая кость": "Айворі",
    "охра": "Охра", "индиго": "Індиго", "металлик": "Метал",
    "стальной": "Метал", "нержавейка": "Нержавіюча сталь",
    "лососевый": "Лососевий", "лосось": "Лососевий",
    "медный": "Мідний", "молочный": "Молочний",
    "горчичный": "Гірчичний", "жемчужный": "Перловий",
    "пудровый": "Пудровий", "кислотный": "Кислотний",
    "дымчатый": "Сірий", "кофе с молоком": "Кавовий",
    "кофейный": "Кавовий", "камуфляж": "Хакі",
    "мультикам": "Хакі", "пиксель": "Хакі",
    "разные цвета": "Комбінований", "разноцветный": "Комбінований",
    "мультиколор": "Комбінований", "multicolor": "Комбінований",
    "микс": "Комбінований", "ассорти": "Комбінований",
    "бесцветный": "Безбарвний", "янтарный": "Бурштиновий",
    "огненный": "Червоний", "морской": "Блакитний",
    "матовый черный": "Чорний", "matte black": "Чорний",
    "золото": "Золотий", "серебро": "Срібний", "бронза": "Бронзовий",
    "розовое золото": "Комбінований", "коралл": "Кораловий",
    "шоколад": "Коричневий", "шоколадный": "Коричневий",
    "лайм": "Лайм", "лаймовый": "Лайм",
    "слива": "Сливовий", "сливовый": "Сливовий",
    "мокрый асфальт": "Графітовий", "асфальт": "Графітовий",
    "васильковый": "Волошковий", "кирпичный": "Цегляний",
    "рыжий": "Рудий", "болотный": "Оливковий",
    "цветной": "Комбінований", "в ассортименте": "Комбінований",
    "navy": "Темно-синій", "blue": "Синій", "red": "Червоний",
    "green": "Зелений", "white": "Білий", "black": "Чорний",
    "grey": "Сірий", "gray": "Сірий", "yellow": "Жовтий",
    "pink": "Рожевий", "orange": "Помаранчевий",
    "brown": "Коричневий", "purple": "Фіолетовий",
    "gold": "Золотий", "silver": "Срібний",
    "beige": "Бежевий", "coral": "Кораловий",
    "mint": "М'ятний", "olive": "Оливковий",
    "khaki": "Хакі", "burgundy": "Бордовий",
    "teal": "Бірюзовий", "turquoise": "Бірюзовий",
    "cream": "Кремовий", "ivory": "Айворі",
    "clear": "Прозорий", "transparent": "Прозорий",
    "multicoloured": "Комбінований", "multi": "Комбінований",
    "camouflage": "Хакі", "camo": "Хакі",
    "walnut": "Коричневий", "oak": "Коричневий",
    "maple": "Бежевий", "cherry": "Вишневий",
    "violet": "Фіолетовий", "lilac": "Ліловий",
    "lavender": "Лавандовий", "peach": "Персиковий",
    "sand": "Пісочний", "champagne": "Бежевий",
    "graphite": "Графітовий", "steel": "Метал",
    "plum": "Сливовий", "wine": "Бордовий",
    "salmon": "Лососевий", "copper": "Мідний",
    "bronze": "Бронзовий", "emerald": "Смарагдовий",
    "nude": "Бежевий", "sky blue": "Блакитний",
    "light blue": "Блакитний", "dark blue": "Темно-синій",
    "черно-белый": "Чорно-білий", "бело-черный": "Чорно-білий",
    "черно-серый": "Чорно-білий", "бело-серый": "Чорно-білий",
    "черно-красный": "Чорно-білий", "красно-черный": "Чорно-білий",
    "сине-желтый": "Синьо-жовтий", "желто-синий": "Синьо-жовтий",
    "красно-белый": "Чорно-білий", "сине-белый": "Чорно-білий",
    "серо-черный": "Чорно-білий",
}

RU_UA_PREFIXES = {
    "темно": "Темно-", "тёмно": "Темно-",
    "светло": "Світло-", "ярко": "Яскраво-",
    "бледно": "Блідо-", "нежно": "Світло-",
    "кислотно": "Кислотно-", "насыщенно": "Яскраво-",
    "dark": "Темно-", "light": "Світло-",
    "bright": "Яскраво-", "pale": "Блідо-",
    "deep": "Темно-", "soft": "Світло-",
    "нежно-": "Світло-", "блідо-": "Блідо-",
}


def _build_map():
    kasta_map = {}
    for c in KASTA_COLORS:
        kasta_map[c.lower()] = c
        kasta_map[c.lower().replace("-", " ")] = c
        kasta_map[c.lower().replace("-", "")] = c
    return kasta_map


KASTA_MAP = _build_map()


def _simple_translate(word):
    w = word.lower().strip()
    if w in KASTA_MAP:
        return KASTA_MAP[w]
    if w in RU_UA_COLORS:
        return RU_UA_COLORS[w]
    return None


def normalize_color(raw_value):
    if not raw_value or not str(raw_value).strip():
        return "Комбінований"
    val = str(raw_value).strip()
    val_lower = val.lower()

    if WITH_SEPARATOR_RE.search(val_lower):
        parts = WITH_SEPARATOR_RE.split(val_lower)
        parts = [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]
        if len(parts) > 1:
            distinct = set()
            for part in parts:
                if part in KASTA_MAP:
                    distinct.add(KASTA_MAP[part])
                elif part in RU_UA_COLORS:
                    distinct.add(RU_UA_COLORS[part])
            if len(distinct) > 1:
                return "Комбінований"
            if len(distinct) == 1 and len(parts) > 1:
                return "Комбінований"

    if val_lower in KASTA_MAP:
        return KASTA_MAP[val_lower]

    if val_lower in RU_UA_COLORS:
        return RU_UA_COLORS[val_lower]

    for prefix_ru, prefix_ua in RU_UA_PREFIXES.items():
        plen = len(prefix_ru)
        if val_lower.startswith(prefix_ru + "-") or val_lower.startswith(prefix_ru + " "):
            suffix = val_lower[plen:].lstrip("- ").strip()
            if suffix in KASTA_MAP:
                base = KASTA_MAP[suffix]
            elif suffix in RU_UA_COLORS:
                base = RU_UA_COLORS[suffix]
            else:
                continue
            candidate = prefix_ua + base
            if candidate.lower() in KASTA_MAP:
                return KASTA_MAP[candidate.lower()]
            return "Комбінований"

    val_no_hyphen = val_lower.replace("-", " ")
    if val_no_hyphen in KASTA_MAP:
        return KASTA_MAP[val_no_hyphen]

    val_compact = val_lower.replace("-", "").replace(" ", "")
    if val_compact in KASTA_MAP:
        return KASTA_MAP[val_compact]

    parts = SEPARATOR_RE.split(val_lower)
    parts = [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]
    if len(parts) > 1 or (len(parts) == 1 and parts[0] != val_lower.replace(" ", "")):
        distinct_colors = set()
        for part in parts:
            if part in KASTA_MAP:
                distinct_colors.add(KASTA_MAP[part])
            elif part in RU_UA_COLORS:
                distinct_colors.add(RU_UA_COLORS[part])
            elif part.replace(" ", "") in KASTA_MAP:
                distinct_colors.add(KASTA_MAP[part.replace(" ", "")])
            elif part.replace(" ", "") in RU_UA_COLORS:
                distinct_colors.add(RU_UA_COLORS[part.replace(" ", "")])
        if len(distinct_colors) == 1:
            return distinct_colors.pop()
        if len(distinct_colors) > 1:
            return "Комбінований"
        if len(parts) > 1:
            return "Комбінований"

    m = MULTI_HYPHEN_RE.match(val_lower)
    if m:
        combined = set()
        for g in m.groups():
            if g in KASTA_MAP:
                combined.add(KASTA_MAP[g])
            elif g in RU_UA_COLORS:
                combined.add(RU_UA_COLORS[g])
        if len(combined) == 1:
            return combined.pop()
        if len(combined) > 1:
            return "Комбінований"

    if "-" in val_lower and val_lower.count("-") == 1:
        left, right = val_lower.split("-", 1)
        left_ua = _simple_translate(left)
        right_ua = _simple_translate(right)
        if left_ua and right_ua:
            candidate = left_ua + "-" + right_ua
            if candidate.lower() in KASTA_MAP:
                return KASTA_MAP[candidate.lower()]
            candidate2 = left_ua + "-" + right_ua.lower()
            if candidate2.lower() in KASTA_MAP:
                return KASTA_MAP[candidate2.lower()]
        return "Комбінований"

    words = val_lower.replace("-", " ").split()
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            sub = " ".join(words[i:j])
            if sub in KASTA_MAP:
                return KASTA_MAP[sub]
            if sub in RU_UA_COLORS:
                return RU_UA_COLORS[sub]

    return "Комбінований"


def find_color_param(params):
    for p in params:
        name = (p.get("name", "") or "").strip().lower()
        value = (p.text or "").strip() if hasattr(p, "text") else ""
        if name in COLOR_PARAM_NAMES and value:
            return value
    for p in params:
        name = (p.get("name", "") or "").strip().lower()
        value = (p.text or "").strip() if hasattr(p, "text") else ""
        for cn in COLOR_PARAM_NAMES:
            if cn in name and value:
                return value
    return None
