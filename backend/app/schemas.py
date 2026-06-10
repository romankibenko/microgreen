from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import OrderStatus


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    unit: str | None = Field(default=None, max_length=40)
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool = True


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: Decimal
    unit: str | None
    image_url: str | None
    is_active: bool
    created_at: datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_phone: str = Field(min_length=5, max_length=20)
    customer_name: str | None = Field(default=None, max_length=120)
    comment: str | None = None
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_phone: str
    customer_name: str | None
    comment: str | None
    status: OrderStatus
    total: Decimal
    created_at: datetime
    items: list[OrderItemOut]
