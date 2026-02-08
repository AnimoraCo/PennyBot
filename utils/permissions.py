from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["penny"]
collection = db["permissions"]

PERMISSION_LEVELS = {
    "OWNER": 100,
    "DEV": 80,
    "STAFF": 50,
    "USER": 0
}

async def get_user_level(user_id: int) -> int:
    owner_id = os.getenv("BOT_OWNER_ID")
    if owner_id and int(owner_id) == user_id:
        return PERMISSION_LEVELS["OWNER"]

    doc = await collection.find_one({"user_id": user_id})
    if not doc:
        return PERMISSION_LEVELS["USER"]

    return PERMISSION_LEVELS.get(doc["role"], 0)
