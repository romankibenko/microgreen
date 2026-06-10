from typing import Any

import httpx

from app.config import settings


def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(base_url=settings.backend_url, timeout=10)


async def get_products() -> list[dict[str, Any]]:
    async with _client() as client:
        response = await client.get("/products")
        response.raise_for_status()
        return response.json()


async def link_account(
    chat_id: int, phone: str, username: str | None, first_name: str | None
) -> None:
    async with _client() as client:
        response = await client.post(
            "/telegram/link",
            json={
                "chat_id": chat_id,
                "phone": phone,
                "username": username,
                "first_name": first_name,
            },
        )
        response.raise_for_status()


async def get_orders_by_chat(chat_id: int) -> list[dict[str, Any]]:
    async with _client() as client:
        response = await client.get("/orders", params={"chat_id": chat_id})
        response.raise_for_status()
        return response.json()
