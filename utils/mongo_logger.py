import os
import datetime
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("LOG_DB_NAME", "bot_logs")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db["logs"]

async def save_log(
    level: str,
    message: str,
    *,
    guild_id: int | None = None,
    guild_name: str | None = None,
    user_id: int | None = None,
    user_name: str | None = None,
    source: str | None = None
):
    if level not in ("WARNING", "ERROR", "CRITICAL"):
        return

    doc = {
        "level": level,
        "message": message,
        "guild": {
            "id": guild_id,
            "name": guild_name
        },
        "user": {
            "id": user_id,
            "name": user_name
        },
        "source": source,
        "timestamp": datetime.datetime.utcnow()
    }

    await collection.insert_one(doc)
