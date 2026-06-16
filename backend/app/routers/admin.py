from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.config import settings
from app.database import get_session
from app.digest import build_digest_text
from app.models import Order, OrderStatus, Planting, Product, TelegramUser
from app.telegram import build_status_message, send_message
from app.schemas import (
    HarvestRequest,
    OrderOut,
    OrderStatusUpdate,
    PlantingCreate,
    PlantingOut,
    PlantingUpdate,
    ProductCreate,
    ProductOut,
    ProductReorder,
    ProductUpdate,
)

# Весь роутер закрыт JWT — без валидного токена сюда не пройти.
router = APIRouter(
    prefix="/admin", tags=["admin"], dependencies=[Depends(get_current_user)]
)


@router.get("/orders", response_model=list[OrderOut])
async def list_all_orders(
    session: AsyncSession = Depends(get_session),
) -> list[Order]:
    result = await session.execute(select(Order).order_by(Order.id.desc()))
    return list(result.scalars().all())


async def _shift_stock(session: AsyncSession, order: Order, sign: int) -> None:
    """Меняет наличие товаров по позициям заказа. sign=-1 списать, +1 вернуть.
    Списание не уводит наличие в минус (цифра могла отставать)."""
    for item in order.items:
        product = await session.get(Product, item.product_id)
        if product is None:
            continue
        if sign < 0:
            product.stock = max(0, product.stock - item.quantity)
        else:
            product.stock += item.quantity


@router.patch("/orders/{order_id}/status", response_model=OrderOut)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    background: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
) -> Order:
    order = await session.get(Order, order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Заказ не найден")
    # списываем наличие при доставке, возвращаем при отмене — однократно (флаг)
    if data.status == OrderStatus.delivered and not order.stock_deducted:
        await _shift_stock(session, order, sign=-1)
        order.stock_deducted = True
    elif data.status == OrderStatus.cancelled and order.stock_deducted:
        await _shift_stock(session, order, sign=1)
        order.stock_deducted = False
    order.status = data.status
    await session.commit()
    await session.refresh(order)

    # уведомляем клиента о новом статусе, если его телефон привязан к боту
    text = build_status_message(order)
    if text is not None:
        chat_id = await session.scalar(
            select(TelegramUser.chat_id).where(
                TelegramUser.phone == order.customer_phone
            )
        )
        if chat_id is not None:
            background.add_task(send_message, chat_id, text)
    return order


@router.get("/products", response_model=list[ProductOut])
async def list_all_products(
    session: AsyncSession = Depends(get_session),
) -> list[Product]:
    # в отличие от публичного каталога — отдаём и неактивные товары
    result = await session.execute(
        select(Product).order_by(Product.sort_order, Product.id)
    )
    return list(result.scalars().all())


@router.post(
    "/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED
)
async def create_product(
    data: ProductCreate, session: AsyncSession = Depends(get_session)
) -> Product:
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.put("/products/reorder", response_model=list[ProductOut])
async def reorder_products(
    data: ProductReorder, session: AsyncSession = Depends(get_session)
) -> list[Product]:
    """Принимает id товаров в желаемом порядке и проставляет sort_order по индексу."""
    position = {pid: i for i, pid in enumerate(data.ids)}
    result = await session.execute(
        select(Product).where(Product.id.in_(position))
    )
    for product in result.scalars():
        product.sort_order = position[product.id]
    await session.commit()
    ordered = await session.execute(
        select(Product).order_by(Product.sort_order, Product.id)
    )
    return list(ordered.scalars().all())


@router.patch("/products/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    session: AsyncSession = Depends(get_session),
) -> Product:
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    await session.commit()
    await session.refresh(product)
    return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
    await session.delete(product)
    await session.commit()


@router.get("/plantings", response_model=list[PlantingOut])
async def list_plantings(
    session: AsyncSession = Depends(get_session),
) -> list[Planting]:
    result = await session.execute(
        select(Planting).order_by(Planting.sown_at.desc(), Planting.id.desc())
    )
    return list(result.scalars().all())


@router.post(
    "/plantings", response_model=PlantingOut, status_code=status.HTTP_201_CREATED
)
async def create_planting(
    data: PlantingCreate, session: AsyncSession = Depends(get_session)
) -> Planting:
    planting = Planting(**data.model_dump())
    session.add(planting)
    await session.commit()
    await session.refresh(planting)
    return planting


@router.patch("/plantings/{planting_id}", response_model=PlantingOut)
async def update_planting(
    planting_id: int,
    data: PlantingUpdate,
    session: AsyncSession = Depends(get_session),
) -> Planting:
    planting = await session.get(Planting, planting_id)
    if planting is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Посадка не найдена")
    planting.note = data.note
    await session.commit()
    await session.refresh(planting)
    return planting


@router.post("/plantings/{planting_id}/harvest", response_model=PlantingOut)
async def harvest_planting(
    planting_id: int,
    data: HarvestRequest,
    session: AsyncSession = Depends(get_session),
) -> Planting:
    planting = await session.get(Planting, planting_id)
    if planting is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Посадка не найдена")
    if planting.harvested_at is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Партия уже собрана")
    product = await session.get(Product, data.product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
    planting.product_id = product.id
    planting.harvested_at = date.today()
    planting.harvested_qty = data.qty
    product.stock += data.qty
    await session.commit()
    await session.refresh(planting)
    return planting


@router.delete("/plantings/{planting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_planting(
    planting_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    planting = await session.get(Planting, planting_id)
    if planting is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Посадка не найдена")
    await session.delete(planting)
    await session.commit()


@router.post("/digest/test")
async def trigger_digest(
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Ручной прогон ежедневного дайджеста — формирует текст и шлёт админу.
    preview отдаём всегда, чтобы видеть результат прямо в ответе."""
    text = await build_digest_text(session)
    if text is None:
        return {"sent": False, "preview": None, "reason": "На сегодня событий нет"}
    sent = settings.admin_chat_id is not None
    if sent:
        await send_message(settings.admin_chat_id, text)
    return {"sent": sent, "preview": text}
