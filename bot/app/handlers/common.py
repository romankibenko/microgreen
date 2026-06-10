import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app import api
from app.keyboards import main_menu, shop_markup

logger = logging.getLogger(__name__)
router = Router()

WELCOME = (
    "🌱 <b>Микрозелень у дома</b>\n\n"
    "Привет, {name}! Я бот, который держит тебя в курсе заказов.\n\n"
    "• 📋 <b>Каталог</b> — что есть в наличии\n"
    "• 🧾 <b>Мои заказы</b> — статусы твоих заказов\n"
    "• 📱 <b>Поделиться телефоном</b> — чтобы я узнавал тебя по заказам с сайта "
    "и присылал уведомления\n\n"
    "Жми кнопки внизу 👇"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    name = message.from_user.first_name if message.from_user else "сосед"
    await message.answer(WELCOME.format(name=name), reply_markup=main_menu())
    shop = shop_markup()
    if shop is not None:
        await message.answer("Открыть магазин:", reply_markup=shop)


@router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    # Нужно Роме, чтобы вписать свой chat_id в ADMIN_CHAT_ID.
    await message.answer(f"Твой chat_id: <code>{message.chat.id}</code>")


@router.message(F.contact)
async def on_contact(message: Message) -> None:
    contact = message.contact
    # Пользователь может прислать чужой контакт — берём только свой.
    if contact.user_id != message.from_user.id:
        await message.answer(
            "Это чужой контакт 🙃 Поделись, пожалуйста, своим номером — "
            "кнопкой «📱 Поделиться телефоном»."
        )
        return
    try:
        await api.link_account(
            chat_id=message.chat.id,
            phone=contact.phone_number,
            username=message.from_user.username,
            first_name=contact.first_name,
        )
    except Exception:
        logger.exception("link_account failed")
        await message.answer("Не получилось привязать номер, попробуй чуть позже 🙏")
        return
    await message.answer(
        "Готово ✅ Теперь я буду присылать тебе статусы заказов, "
        "оформленных на этот номер."
    )
