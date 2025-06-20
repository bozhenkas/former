import asyncio
from datetime import datetime, timedelta
from bson import ObjectId
from database import db, init_db, UserModel, GoogleAccountModel, IntegrationModel, FormResponseModel, \
    create_user, get_user_by_telegram_id, add_google_account, get_google_accounts_by_user, \
    create_integration, get_integrations_by_user, add_form_response, get_responses_by_integration, \
    check_user_google_accounts, check_integration_google_account

async def main():
    await init_db()
    print("[DB] Индексы инициализированы.")

    telegram_id = 123456789
    username = "testuser"
    email = "user@gmail.com"
    form_id = "form123"
    sheet_id = "sheet123"

    # 1. Создать пользователя
    await create_user(db, UserModel(telegram_id=telegram_id, telegram_username=username, access="allowed"))
    user = await get_user_by_telegram_id(db, telegram_id)
    print("[User]", user)

    # 2. Добавить Google-аккаунт
    expires = datetime.utcnow() + timedelta(hours=1)
    await add_google_account(db, GoogleAccountModel(
        user_tg_id=telegram_id,
        email=email,
        access_token="test_access_token",
        refresh_token="test_refresh_token",
        expires_at=expires
    ))
    accounts = await get_google_accounts_by_user(db, telegram_id)
    print("[Google Accounts]", accounts)

    # 3. Создать интеграцию
    google_account_id = accounts[0]['_id']
    await create_integration(db, IntegrationModel(
        user_tg_id=telegram_id,
        integration_name="Test Integration",
        form_id=form_id,
        google_sheet_id=sheet_id,
        google_account_id=google_account_id,
        field_mapping={"field1": "col1"}
    ))
    integrations = await get_integrations_by_user(db, telegram_id)
    print("[Integrations]", integrations)

    # 4. Добавить ответ формы
    integration_id = integrations[0]['_id']
    await add_form_response(db, FormResponseModel(
        integration_id=integration_id,
        form_id=form_id,
        response_data={"field1": "value1"},
        status="success"
    ))
    responses = await get_responses_by_integration(db, integration_id)
    print("[Form Responses]", responses)

    # 5. Проверить связи
    user_accounts = await check_user_google_accounts(db, telegram_id)
    print("[Связанные Google-аккаунты пользователя]", user_accounts)

    integration_account = await check_integration_google_account(db, integration_id)
    print("[Google-аккаунт интеграции]", integration_account)

if __name__ == "__main__":
    asyncio.run(main()) 