from motor.motor_asyncio import AsyncIOMotorClient
import os

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["penny"]
collection = db["system"]

async def is_maintenance() -> bool:
    doc = await collection.find_one({"_id": "maintenance"})
    return doc["enabled"] if doc else False

async def set_maintenance(state: bool):
    await collection.update_one(
        {"_id": "maintenance"},
        {"$set": {"enabled": state}},
        upsert=True
    )
