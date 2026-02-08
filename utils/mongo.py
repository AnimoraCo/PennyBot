import os
from motor.motor_asyncio import AsyncIOMotorClient

_client = None
_db = None


def init_mongo():
    global _client, _db

    if os.getenv("MONGO_ENABLED", "false").lower() != "true":
        return

    uri = os.getenv("MONGODB_URL")
    db_name = os.getenv("LOG_DB_NAME", "penny")

    _client = AsyncIOMotorClient(uri)
    _db = _client[db_name]


def get_collection(name: str):
    if _db is None:
        raise RuntimeError("MongoDB não inicializado")
    return _db[name]
