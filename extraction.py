import re


keywords = [
    "яккасарай", "мирабад", "mirabad", "госпит", "нукус", "nukus",
    "шота", "shota", "бабур", "бобур", "babur", "bobur",
    "глин", "glin", "аски", "муки", "muki", "фидо", "fido",
    "саид", "said", "тарас", "taras", "шахри", "shahri",
    "бешаг", "тараб", "тароб", "tarob", "абду", "abdu",
    "новострой", "жк", "жилой комплекс", "жилом комплексе",
    "жилого комплекса", "жилым комплексом", "oybek", "ойбек", "айбек"
]

pattern_keywords = re.compile('|'.join(re.escape(word) for word in keywords), re.IGNORECASE)


async def check_text(text):
    if not text:
        return False

    if not pattern_keywords.search(text): # Words checking
        return False

    price_pattern = r'(?:\((\d{3})\)|(\d[\d\s]*)\s*(?:\$|usd|USD|долл|дол)|\b(\d{3})\b(?=\s|$))'
    match = re.search(price_pattern, text)
    if not match:
        return False

    price_str = match.group(1) or match.group(2) or match.group(3)
    price = int(price_str.replace(" ", ""))

    if 650 <= price <= 850:
        return True
    else:
        return False
