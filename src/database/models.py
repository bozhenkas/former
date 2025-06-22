from typing import Optional, List, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field
from bson import ObjectId
from uuid import uuid4

# Pydantic models
class UserModel(BaseModel):
    telegram_id: int
    telegram_username: str
    access: str = "undefined"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GoogleAccountModel(BaseModel):
    user_tg_id: int
    email: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class IntegrationModel(BaseModel):
    user_tg_id: int
    integration_name: str
    webhook_token: str = Field(default_factory=lambda: str(uuid4()))
    form_id: str
    google_sheet_id: str
    google_account_id: ObjectId
    field_mapping: Dict[str, str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {"arbitrary_types_allowed": True}

class FormResponseModel(BaseModel):
    integration_id: ObjectId
    form_id: str
    response_data: Dict[str, Any]
    received_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "success"
    error_message: Optional[str] = None
    
    model_config = {"arbitrary_types_allowed": True}

# CRUD and index setup
async def setup_indexes(db: AsyncIOMotorDatabase):
    await db.users.create_index("tg_id", unique=True)
    await db.google_accounts.create_index("user_tg_id")
    await db.integrations.create_index([("user_tg_id", 1), ("form_id", 1)])
    await db.form_responses.create_index("integration_id")
    await db.form_responses.create_index("received_at")

# USERS
async def create_user(db: AsyncIOMotorDatabase, user: UserModel):
    await db.users.insert_one(user.dict())

async def get_user_by_telegram_id(db: AsyncIOMotorDatabase, telegram_id: int) -> Optional[dict]:
    return await db.users.find_one({"telegram_id": telegram_id})

# GOOGLE ACCOUNTS
async def add_google_account(db: AsyncIOMotorDatabase, account: GoogleAccountModel):
    await db.google_accounts.insert_one(account.dict())

async def get_google_accounts_by_user(db: AsyncIOMotorDatabase, telegram_id: int) -> List[dict]:
    return await db.google_accounts.find({"user_tg_id": telegram_id}).to_list(length=None)

# INTEGRATIONS
async def create_integration(db: AsyncIOMotorDatabase, integration: IntegrationModel):
    await db.integrations.insert_one(integration.dict())

async def get_integrations_by_user(db: AsyncIOMotorDatabase, telegram_id: int) -> List[dict]:
    return await db.integrations.find({"user_tg_id": telegram_id}).to_list(length=None)

# FORM RESPONSES
async def add_form_response(db: AsyncIOMotorDatabase, response: FormResponseModel):
    await db.form_responses.insert_one(response.dict())

async def get_responses_by_integration(db: AsyncIOMotorDatabase, integration_id: ObjectId) -> List[dict]:
    return await db.form_responses.find({"integration_id": integration_id}).to_list(length=None)

# Проверка связей
async def check_user_google_accounts(db: AsyncIOMotorDatabase, telegram_id: int) -> List[dict]:
    user = await get_user_by_telegram_id(db, telegram_id)
    if not user:
        return []
    return await get_google_accounts_by_user(db, telegram_id)

async def check_integration_google_account(db: AsyncIOMotorDatabase, integration_id: ObjectId) -> Optional[dict]:
    integration = await db.integrations.find_one({"_id": integration_id})
    if not integration:
        return None
    google_account = await db.google_accounts.find_one({"_id": integration["google_account_id"]})
    return google_account 