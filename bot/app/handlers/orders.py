import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message

from app import api
from app.keyboards import main_menu

logger = logging.getLogger(__name__)
router = Router()

STATUS_LABELS = {
    "new": "🆕 Принят",
    "assembled": "📦 Собран",
    "delivered": "✅ Доставлен",
    "cancelled": "❌ Отменён",
}


def _format_date(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime("%d.%m %H:%M")
    except ValueError:
        return value


def _format_total(value: str | float) -> str:
    number = float(value)
    text = f"{number:.2f}".rstrip("0").rstrip(".")
    return text


@router.message(F.text == "🧾 Мои заказы")
async def show_orders(message: Message) -> None:
    try:
        orders = await api.get_orders_by_chat(message.chat.id)
    except Exception:
        logger.exception("get_orders_by_chat failed")
        await message.answer("Не получилось загрузить заказы, попробуй позже 🙏")
        return

    if not orders:
        await message.answer(
            "У тебя пока нет заказов на привязанный номер.\n\n"
            "Если заказывал с сайта — поделись телефоном кнопкой "
            "«📱 Поделиться телефоном», чтобы я нашёл твои заказы.",
            reply_markup=main_menu(),
        )
        return

    blocks = []
    for order in orders[:10]:
        status = STATUS_LABELS.get(order["status"], order["status"])
        header = (
            f"<b>Заказ #{order['id']}</b> · {_format_date(order['created_at'])}\n"
            f"Статус: {status}"
        )
        items = "\n".join(
            f"  • {item['product_name']} × {item['quantity']}"
            for item in order["items"]
        )
        total = f"Сумма: <b>{_format_total(order['total'])} ₽</b>"
        blocks.append(f"{header}\n{items}\n{total}")

    await message.answer("\n\n".join(blocks))
