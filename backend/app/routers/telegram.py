from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.models import TelegramUser
from app.phone import normalize_phone
from app.schemas import TelegramLinkIn, TelegramUserOut

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/link", response_model=TelegramUserOut)
async def link_account(
    data: TelegramLinkIn, session: AsyncSession = Depends(get_session)
) -> TelegramUser:
    """Привязывает телефон к Telegram-аккаунту (бот вызывает при расшаривании контакта)."""
    user = await session.get(TelegramUser, data.chat_id)
    if user is None:
        user = TelegramUser(chat_id=data.chat_id)
        session.add(user)
    user.phone = normalize_phone(data.phone)
    user.username = data.username
    user.first_name = data.first_name
    await session.commit()
    await session.refresh(user)
    return user


@router.get("/users/{chat_id}", response_model=TelegramUserOut)
async def get_user(
    chat_id: int, session: AsyncSession = Depends(get_session)
) -> TelegramUser:
    user = await session.get(TelegramUser, chat_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Аккаунт не привязан")
    return user


@router.get("/config")
async def public_config() -> dict[str, str]:
    """Публичные настройки для бота (URL магазина под кнопку Mini App)."""
    return {"shop_url": settings.shop_url}
