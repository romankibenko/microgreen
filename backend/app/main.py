from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import orders, products, telegram

app = FastAPI(title="Microgreen API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(telegram.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
