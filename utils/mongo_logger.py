from utils.mongo import get_collection
import datetime
import logging

logger = logging.getLogger("penny")


async def save_log(collection: str, data: dict):
    db = get_db()
    if db is None:
        return

    try:
        data["created_at"] = datetime.datetime.utcnow()
        await db[collection].insert_one(data)
    except Exception as e:
        logger.error(f"Erro ao salvar log no MongoDB: {e}")
