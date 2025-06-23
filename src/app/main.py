from fastapi import FastAPI
from app.api.v1.endpoints import webhook
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Yandex Forms Webhook Handler")

app.include_router(webhook.router, prefix="/api/v1/yandex", tags=["Yandex.Forms"])

@app.get("/")
async def read_root():
    return {"message": "Webhook handler is running"} 