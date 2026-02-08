import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

from utils.cog_loader import load_cogs
from utils.logger import setup_logger

# ========================
# Logger
# ========================
logger = setup_logger()
logger.info("Inicializando Penny...")

# ========================
# ENV
# ========================
load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
ENV = os.getenv("ENV", "prod")
DEV_SERVER_ID = os.getenv("DEV_SERVER_ID")

if not BOT_TOKEN:
    raise RuntimeError("DISCORD_TOKEN não encontrado no .env")

# ========================
# Intents
# ========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

SYNC_FILE = ".synced"

# ========================
# Bot
# ========================
class Penny(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )
        self._status_started = False  # proteção contra múltiplos loops

    async def setup_hook(self):
        # 1️⃣ Carrega cogs primeiro
        load_cogs(self)
        logger.info("Cogs carregados com sucesso")

        # 2️⃣ Sincronização de slash commands
        if ENV == "dev" and DEV_SERVER_ID:
            guild = discord.Object(id=int(DEV_SERVER_ID))
            await self.tree.sync(guild=guild)
            logger.info("Slash commands sincronizados (DEV)")

        elif ENV == "prod" and not os.path.exists(SYNC_FILE):
            await self.tree.sync()
            open(SYNC_FILE, "w").close()
            logger.info("Slash commands sincronizados globalmente (PROD)")

    async def on_ready(self):
        logger.info(f"Bot online como {self.user} ({self.user.id})")

        # 3️⃣ Inicia o task APENAS quando o bot estiver pronto
        if not self._status_started:
            self.status_task.start()
            self._status_started = True
            logger.info("Status task iniciado")

    @tasks.loop(minutes=5)
    async def status_task(self):
        from utils.status import get_random_status
        await self.change_presence(
            activity=get_random_status(self)
        )

bot = Penny()
bot.run(BOT_TOKEN)
