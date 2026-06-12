from datetime import date, datetime, timedelta
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, computed_field

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


class TelegramLinkIn(BaseModel):
    chat_id: int
    phone: str = Field(min_length=5, max_length=20)
    username: str | None = Field(default=None, max_length=64)
    first_name: str | None = Field(default=None, max_length=120)


class TelegramUserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_id: int
    phone: str | None
    username: str | None
    first_name: str | None


class LoginIn(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class PlantingCreate(BaseModel):
    culture: str = Field(min_length=1, max_length=120)
    sown_at: date
    grow_days: int = Field(gt=0)
    note: str | None = None
    product_id: int | None = None


class PlantingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int | None
    culture: str
    sown_at: date
    grow_days: int
    note: str | None

    @computed_field
    @property
    def ready_at(self) -> date:
        return self.sown_at + timedelta(days=self.grow_days)
