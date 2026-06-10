from fastapi import FastAPI

from app.routers import orders, products

app = FastAPI(title="Microgreen API")

app.include_router(products.router)
app.include_router(orders.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
