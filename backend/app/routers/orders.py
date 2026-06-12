from decimal import Decimal

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Order, OrderItem, Product, TelegramUser
from app.phone import normalize_phone
from app.schemas import OrderCreate, OrderOut
from app.telegram import (
    build_admin_message,
    build_client_message,
    dispatch_order_notifications,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    background: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
) -> Order:
    product_ids = [item.product_id for item in data.items]
    result = await session.execute(select(Product).where(Product.id.in_(product_ids)))
    products = {p.id: p for p in result.scalars().all()}

    order = Order(
        customer_phone=normalize_phone(data.customer_phone),
        customer_name=data.customer_name,
        comment=data.comment,
    )
    total = Decimal("0")
    for item in data.items:
        product = products.get(item.product_id)
        if product is None or not product.is_active:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Товар {item.product_id} недоступен",
            )
        order.items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=item.quantity,
            )
        )
        total += product.price * item.quantity
    order.total = total

    session.add(order)
    await session.commit()
    await session.refresh(order)

    # уведомления — в фоне, чтобы Telegram не задерживал и не ронял ответ
    client_chat_id = await session.scalar(
        select(TelegramUser.chat_id).where(
            TelegramUser.phone == order.customer_phone
        )
    )
    background.add_task(
        dispatch_order_notifications,
        build_admin_message(order),
        build_client_message(order),
        client_chat_id,
    )
    return order


@router.get("", response_model=list[OrderOut])
async def list_orders(
    phone: str | None = None,
    chat_id: int | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[Order]:
    # Публичный эндпоинт обслуживает только бота/клиента — строго по своему телефону.
    # Полный список (с чужими телефонами) доступен лишь админке через /admin/orders.
    if phone is None and chat_id is None:
        return []
    if chat_id is not None:
        phone = await session.scalar(
            select(TelegramUser.phone).where(TelegramUser.chat_id == chat_id)
        )
        if phone is None:
            return []

    stmt = select(Order)
    if phone is not None:
        stmt = stmt.where(Order.customer_phone == normalize_phone(phone))
    stmt = stmt.order_by(Order.id.desc())

    result = await session.execute(stmt)
    return list(result.scalars().all())


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int, session: AsyncSession = Depends(get_session)
) -> Order:
    order = await session.get(Order, order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Заказ не найден")
    return order
