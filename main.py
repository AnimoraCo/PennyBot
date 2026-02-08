import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

from utils.cog_loader import load_cogs
from utils.logger import setup_logger
from utils.mongo import init_mongo

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


class Penny(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )
        self._status_started = False

    async def setup_hook(self):
        # Mongo
        init_mongo()

        # Cogs
        await load_cogs(self)
        logger.info("Cogs carregados com sucesso")


        if ENV == "dev" and DEV_SERVER_ID:
            guild = discord.Object(id=int(DEV_SERVER_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info("Slash commands sincronizados (DEV)")

        commands = self.tree.get_commands()
        logger.info(f"Slash commands carregados: {len(commands)}")

        for cmd in commands:
            logger.info(f" - /{cmd.name}")

    async def on_ready(self):
        logger.info(
            f"Bot online como {self.user} | Servidores: {len(self.guilds)}"
        )

        if not self._status_started:
            self.status_task.start()
            self._status_started = True
            logger.info("Status task iniciado")

    @tasks.loop(minutes=1)
    async def status_task(self):
        from utils.status import get_random_status
        await self.change_presence(
            activity=get_random_status(self)
        )


bot = Penny()
bot.run(BOT_TOKEN)
