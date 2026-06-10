from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Order, OrderItem, Product
from app.schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate, session: AsyncSession = Depends(get_session)
) -> Order:
    product_ids = [item.product_id for item in data.items]
    result = await session.execute(select(Product).where(Product.id.in_(product_ids)))
    products = {p.id: p for p in result.scalars().all()}

    order = Order(
        customer_phone=data.customer_phone,
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
    return order


@router.get("", response_model=list[OrderOut])
async def list_orders(
    session: AsyncSession = Depends(get_session),
) -> list[Order]:
    result = await session.execute(select(Order).order_by(Order.id.desc()))
    return list(result.scalars().all())


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int, session: AsyncSession = Depends(get_session)
) -> Order:
    order = await session.get(Order, order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Заказ не найден")
    return order
