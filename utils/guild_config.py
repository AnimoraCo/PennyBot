from motor.motor_asyncio import AsyncIOMotorClient
import os

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["penny"]
collection = db["guild_configs"]

DEFAULT_CONFIG = {
    "economy_enabled": True,
    "language": "pt-BR"
}

async def get_guild_config(guild_id: int) -> dict:
    doc = await collection.find_one({"guild_id": guild_id})
    if not doc:
        doc = {"guild_id": guild_id, **DEFAULT_CONFIG}
        await collection.insert_one(doc)
    return doc

async def update_guild_config(guild_id: int, data: dict):
    await collection.update_one(
        {"guild_id": guild_id},
        {"$set": data},
        upsert=True
    )
