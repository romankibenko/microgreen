from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

from app.config import settings


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📋 Каталог"),
                KeyboardButton(text="🧾 Мои заказы"),
            ],
            [KeyboardButton(text="📱 Поделиться телефоном", request_contact=True)],
        ],
        resize_keyboard=True,
    )


def shop_markup() -> InlineKeyboardMarkup | None:
    # Заглушка под будущий Mini App. Telegram принимает web_app только по HTTPS,
    # поэтому в локальной разработке (http://localhost) кнопку не показываем.
    if not settings.shop_url.startswith("https://"):
        return None
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Магазин",
                    web_app=WebAppInfo(url=settings.shop_url),
                )
            ]
        ]
    )
