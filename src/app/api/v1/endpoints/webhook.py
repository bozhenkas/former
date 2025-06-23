from fastapi import APIRouter, Depends, HTTPException, Request
from database.db_methods import get_integration_by_webhook_token, log_form_response
import logging

router = APIRouter()

@router.post("/webhook")
async def process_yandex_webhook(request: Request, token: str):
    """
    Принимает вебхук от Яндекс.Формы.

    - **token**: Уникальный токен для идентификации интеграции.
    """
    integration = await get_integration_by_webhook_token(token)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found for the provided token")

    try:
        response_data = await request.json()
        await log_form_response(
            integration_id=integration["_id"],
            form_id=integration["form_id"],
            status="success",
            response_data=response_data
        )
        # Здесь будет логика для отправки данных в Google Sheets
        logging.info(f"Successfully processed webhook for integration: {integration['integration_name']}")
        return {"status": "ok", "message": "Webhook processed successfully"}

    except Exception as e:
        logging.error(f"Failed to process webhook for integration {integration.get('integration_name')}: {e}")
        await log_form_response(
            integration_id=integration["_id"],
            form_id=integration["form_id"],
            status="failed",
            error_message=str(e),
            response_data=await request.json()
        )
        raise HTTPException(status_code=500, detail="Internal Server Error") 