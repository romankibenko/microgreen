from fastapi import FastAPI

app = FastAPI(title="Microgreen API")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
