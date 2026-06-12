from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.auth import hash_password
from app.config import settings
from app.database import SessionLocal
from app.models import User
from app.routers import admin, auth, orders, products, telegram


async def seed_admin() -> None:
    """Создаёт первого админа из .env, если его ещё нет. Идемпотентно."""
    if not settings.admin_username or not settings.admin_password:
        return
    async with SessionLocal() as session:
        exists = await session.scalar(
            select(User).where(User.username == settings.admin_username)
        )
        if exists is None:
            session.add(
                User(
                    username=settings.admin_username,
                    password_hash=hash_password(settings.admin_password),
                )
            )
            await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_admin()
    yield


app = FastAPI(title="Microgreen API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(telegram.router)
app.include_router(auth.router)
app.include_router(admin.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
