from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.database import get_session
from app.models import Order, Planting
from app.schemas import (
    OrderOut,
    OrderStatusUpdate,
    PlantingCreate,
    PlantingOut,
    PlantingUpdate,
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


@router.patch("/orders/{order_id}/status", response_model=OrderOut)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    session: AsyncSession = Depends(get_session),
) -> Order:
    order = await session.get(Order, order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Заказ не найден")
    order.status = data.status
    await session.commit()
    await session.refresh(order)
    return order


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


@router.delete("/plantings/{planting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_planting(
    planting_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    planting = await session.get(Planting, planting_id)
    if planting is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Посадка не найдена")
    await session.delete(planting)
    await session.commit()
