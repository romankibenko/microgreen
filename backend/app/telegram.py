from html import escape

import httpx

from app.config import settings
from app.models import Order, OrderStatus

TELEGRAM_API = "https://api.telegram.org"


async def send_message(chat_id: int, text: str) -> None:
    """Отправляет сообщение через Bot API. Молча выходит без токена и не падает на ошибках —
    сбой уведомления не должен ронять оформление заказа."""
    if not settings.bot_token:
        return
    url = f"{TELEGRAM_API}/bot{settings.bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(url, json=payload)
    except httpx.HTTPError:
        pass


def build_admin_message(order: Order) -> str:
    lines = [
        f"🌱 <b>Новый заказ №{order.id}</b>",
        "",
        f"📞 {escape(order.customer_phone)}",
    ]
    if order.customer_name:
        lines.append(f"👤 {escape(order.customer_name)}")
    if order.comment:
        lines.append(f"💬 {escape(order.comment)}")
    lines.append("")
    for item in order.items:
        lines.append(
            f"• {escape(item.product_name)} × {item.quantity} — "
            f"{item.unit_price * item.quantity:.0f} ₽"
        )
    lines.append("")
    lines.append(f"<b>Итого: {order.total:.0f} ₽</b>")
    return "\n".join(lines)


def build_client_message(order: Order) -> str:
    return (
        f"🌱 Спасибо за заказ №{order.id}!\n\n"
        f"Мы получили его на сумму <b>{order.total:.0f} ₽</b> и скоро свяжемся "
        f"по номеру {escape(order.customer_phone)}, чтобы согласовать время.\n\n"
        f"Свежей зелени! 🥬"
    )


# Тексты статусов для клиента. new не уведомляем — это начальное состояние.
_STATUS_PHRASE = {
    OrderStatus.assembled: "📦 собран и готов к доставке",
    OrderStatus.delivered: "✅ доставлен. Спасибо, что выбрал нас — свежей зелени! 🥬",
    OrderStatus.cancelled: "❌ отменён. Если это ошибка — напиши нам.",
}


def build_status_message(order: Order) -> str | None:
    """Сообщение клиенту о новом статусе. None — если по статусу не уведомляем."""
    phrase = _STATUS_PHRASE.get(order.status)
    if phrase is None:
        return None
    return f"🌱 Заказ №{order.id} {phrase}"


async def dispatch_order_notifications(
    admin_text: str,
    client_text: str | None,
    client_chat_id: int | None,
) -> None:
    if settings.admin_chat_id is not None:
        await send_message(settings.admin_chat_id, admin_text)
    if client_chat_id is not None and client_text is not None:
        await send_message(client_chat_id, client_text)
