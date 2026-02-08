import os
from utils.mongo import get_collection

MONGO_ENABLED = os.getenv("MONGO_ENABLED", "false").lower() == "true"


async def is_maintenance() -> bool:
    if not MONGO_ENABLED:
        return False

    collection = get_collection("config")
    doc = await collection.find_one({"_id": "maintenance"})
    return bool(doc and doc.get("enabled"))


async def set_maintenance(enabled: bool, reason: str | None = None):
    if not MONGO_ENABLED:
        return

    collection = get_collection("config")

    await collection.update_one(
        {"_id": "maintenance"},
        {
            "$set": {
                "enabled": enabled,
                "reason": reason,
            }
        },
        upsert=True
    )


async def get_maintenance_reason() -> str | None:
    if not MONGO_ENABLED:
        return None

    collection = get_collection("config")
    doc = await collection.find_one({"_id": "maintenance"})
    return doc.get("reason") if doc else None
