from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Product
from app.schemas import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate, session: AsyncSession = Depends(get_session)
) -> Product:
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.get("", response_model=list[ProductOut])
async def list_products(
    session: AsyncSession = Depends(get_session),
) -> list[Product]:
    result = await session.execute(
        select(Product).where(Product.is_active.is_(True)).order_by(Product.id)
    )
    return list(result.scalars().all())


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int, session: AsyncSession = Depends(get_session)
) -> Product:
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
    return product
