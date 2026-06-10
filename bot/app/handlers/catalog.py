import logging

from aiogram import F, Router
from aiogram.types import Message

from app import api
from app.keyboards import shop_markup

logger = logging.getLogger(__name__)
router = Router()


def _format_price(value: str | float) -> str:
    # Цена приходит строкой (Decimal). Показываем без лишних нулей: "150" / "150.50".
    number = float(value)
    text = f"{number:.2f}".rstrip("0").rstrip(".")
    return text


@router.message(F.text == "📋 Каталог")
async def show_catalog(message: Message) -> None:
    try:
        products = await api.get_products()
    except Exception:
        logger.exception("get_products failed")
        await message.answer("Каталог временно недоступен, загляни попозже 🙏")
        return

    active = [p for p in products if p.get("is_active", True)]
    if not active:
        await message.answer("Сейчас всё распродано 🌱 Скоро будет свежий посев!")
        return

    lines = ["🌱 <b>В наличии</b>\n"]
    for product in active:
        unit = product.get("unit")
        unit_suffix = f" / {unit}" if unit else ""
        lines.append(
            f"• <b>{product['name']}</b> — {_format_price(product['price'])} ₽{unit_suffix}"
        )
        description = product.get("description")
        if description:
            lines.append(f"  <i>{description}</i>")

    lines.append("\nОформить заказ удобнее на сайте 👇")
    await message.answer("\n".join(lines), reply_markup=shop_markup())
