from datetime import date, datetime, timedelta
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

from app.models import OrderStatus


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    unit: str | None = Field(default=None, max_length=40)
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool = True
    stock: int = Field(ge=0, default=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    unit: str | None = Field(default=None, max_length=40)
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None
    stock: int | None = Field(default=None, ge=0)


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: Decimal
    unit: str | None
    image_url: str | None
    is_active: bool
    stock: int
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
    shade_days: int = Field(ge=0, default=3)
    trays: int = Field(gt=0, default=1)
    note: str | None = None
    product_id: int | None = None

    @model_validator(mode="after")
    def check_shade_within_grow(self) -> "PlantingCreate":
        if self.shade_days > self.grow_days:
            raise ValueError("shade_days не может превышать grow_days")
        return self


class PlantingUpdate(BaseModel):
    note: str | None = None


class HarvestRequest(BaseModel):
    product_id: int
    qty: int = Field(gt=0)


class PlantingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int | None
    culture: str
    sown_at: date
    grow_days: int
    shade_days: int
    trays: int
    note: str | None
    harvested_at: date | None
    harvested_qty: int | None

    @computed_field
    @property
    def ready_at(self) -> date:
        return self.sown_at + timedelta(days=self.grow_days)

    @computed_field
    @property
    def stage(self) -> str:
        """Текущий этап партии по сегодняшней дате: тень → свет → готово."""
        today = date.today()
        if today < self.sown_at + timedelta(days=self.shade_days):
            return "shade"
        if today < self.sown_at + timedelta(days=self.grow_days):
            return "light"
        return "ready"
