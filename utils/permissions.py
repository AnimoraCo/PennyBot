from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging

log = logging.getLogger("penny.permissions")

# ========================
# Mongo
# ========================
MONGO_URI = os.getenv("MONGODB_URL")  # 🔥 corrigido

client = None
db = None
collection = None

if MONGO_URI:
    client = AsyncIOMotorClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )
    db = client["penny"]
    collection = db["permissions"]
else:
    log.warning("MONGODB_URL não definida, permissões via DB desativadas")

# ========================
# Níveis
# ========================
PERMISSION_LEVELS = {
    "OWNER": 100,
    "DEV": 80,
    "STAFF": 50,
    "USER": 0
}

async def get_user_level(user_id: int) -> int:
    # OWNER sempre tem acesso
    owner_id = os.getenv("BOT_OWNER_ID")
    if owner_id and int(owner_id) == user_id:
        return PERMISSION_LEVELS["OWNER"]

    # Mongo desligado? usuário comum
    if not collection:
        return PERMISSION_LEVELS["USER"]

    try:
        doc = await collection.find_one({"user_id": user_id})
    except Exception as e:
        log.error(f"Erro ao buscar permissão do usuário {user_id}: {e}")
        return PERMISSION_LEVELS["USER"]

    if not doc:
        return PERMISSION_LEVELS["USER"]

    role = doc.get("role", "USER")
    return PERMISSION_LEVELS.get(role, PERMISSION_LEVELS["USER"])
