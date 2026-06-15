"""Ежедневный дайджест по посадкам — раз в день Роме в Telegram.

Считает по датам, что требует внимания сегодня: пора выносить на свет,
готово к сбору, готово завтра. Если событий нет — не шлёт (без спама).
"""

from datetime import date, timedelta
from html import escape

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import SessionLocal
from app.models import Planting
from app.telegram import send_message


def _item(p: Planting, suffix: str = "") -> str:
    return f"• {escape(p.culture)} — {p.trays} лот.{suffix}"


async def build_digest_text(session: AsyncSession) -> str | None:
    """Текст дайджеста по несобранным посадкам. None — если показывать нечего."""
    today = date.today()
    rows = (
        await session.scalars(
            select(Planting).where(Planting.harvested_at.is_(None))
        )
    ).all()

    ready: list[str] = []
    to_light: list[str] = []
    tomorrow: list[str] = []
    for p in rows:
        ready_day = p.sown_at + timedelta(days=p.grow_days)
        light_day = p.sown_at + timedelta(days=p.shade_days)
        if today >= ready_day:
            overdue = (today - ready_day).days
            ready.append(_item(p, f" (ждёт {overdue} дн.)" if overdue else ""))
        elif ready_day == today + timedelta(days=1):
            tomorrow.append(_item(p))
        if light_day == today:
            to_light.append(_item(p))

    sections: list[str] = []
    if ready:
        sections.append("✅ <b>Готово к сбору:</b>\n" + "\n".join(ready))
    if to_light:
        sections.append("🌤 <b>Сегодня выносим на свет:</b>\n" + "\n".join(to_light))
    if tomorrow:
        sections.append("⏳ <b>Готово завтра:</b>\n" + "\n".join(tomorrow))

    if not sections:
        return None
    header = f"🌱 <b>Дайджест посадок на {today:%d.%m.%Y}</b>"
    return header + "\n\n" + "\n\n".join(sections)


async def send_daily_digest() -> None:
    """Задача планировщика: формирует дайджест и шлёт админу, если есть что слать."""
    if settings.admin_chat_id is None:
        return
    async with SessionLocal() as session:
        text = await build_digest_text(session)
    if text is not None:
        await send_message(settings.admin_chat_id, text)
