import re


def normalize_phone(raw: str) -> str:
    """Приводит телефон к цифрам в формате 7XXXXXXXXXX.

    Лендинг и Telegram-контакт присылают телефон по-разному (+7…, 8…, с пробелами).
    Единый формат нужен, чтобы матчить заказ с привязанным Telegram-аккаунтом.
    """
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits[0] == "8":
        digits = "7" + digits[1:]
    return digits
