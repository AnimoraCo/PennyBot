import aiohttp
import os
import datetime

WEBHOOK_URL = os.getenv("LOG_WEBHOOK_URL")
ROLE_ID = os.getenv("LOG_ROLE_ID")

COLORS = {
    "INFO": 0x2ECC71,     
    "WARNING": 0xF1C40F,   
    "ERROR": 0xE74C3C,     
    "CRITICAL": 0x8E44AD,
}

async def send_webhook_log(level: str, title: str, description: str):
    if not WEBHOOK_URL:
        return

    mention = ""
    if level in ("WARNING", "ERROR", "CRITICAL") and ROLE_ID:
        mention = f"<@&{ROLE_ID}>"

    embed = {
        "title": title,
        "description": description[:4000],
        "color": COLORS.get(level, 0x95A5A6),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "footer": {"text": f"Nível: {level}"}
    }

    payload = {
        "content": mention,
        "embeds": [embed]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=payload):
            pass
