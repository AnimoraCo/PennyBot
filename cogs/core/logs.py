import discord
from discord.ext import commands
import logging
import traceback

from utils.webhook_logger import send_webhook_log
from utils.mongo_logger import save_log


logger = logging.getLogger("penny")

class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ===== BOT =====
    @commands.Cog.listener()
    async def on_ready(self):
        msg = f"Bot online como `{self.bot.user}` | Servidores: {len(self.bot.guilds)}"
        logger.info(msg)
        await send_webhook_log("INFO", "🟢 Bot Online", msg)

    # ===== SERVIDORES =====
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        msg = f"Entrou em {guild.name} ({guild.id})"
        logger.info(msg)
        await send_webhook_log("INFO", "➕ Novo Servidor", msg)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        msg = f"Saiu de {guild.name} ({guild.id})"
        logger.warning(msg)

        await save_log(
            level="WARNING",
            message=msg,
            guild_id=guild.id,
            guild_name=guild.name,
            source="on_guild_remove"
        )

        await send_webhook_log("WARNING", "➖ Servidor Removido", msg)

    # ===== ERRO SLASH COMMAND =====
    @commands.Cog.listener()
    async def on_app_command_error(self, interaction, error):
        tb = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )

        logger.error(tb)

        await save_log(
            level="ERROR",
            message=tb,
            guild_id=interaction.guild.id if interaction.guild else None,
            guild_name=interaction.guild.name if interaction.guild else None,
            user_id=interaction.user.id,
            user_name=str(interaction.user),
            source="slash_command"
        )

        await send_webhook_log(
            "ERROR",
            "🚨 Erro em Slash Command",
            f"Servidor: `{interaction.guild}`\n"
            f"Usuário: `{interaction.user}`\n"
            f"```py\n{tb[:3000]}\n```"
        )

        if not interaction.response.is_done():
            await interaction.response.send_message(
                "❌ Ocorreu um erro. A equipe já foi notificada.",
                ephemeral=True
            )

    # ===== ERRO GLOBAL =====
    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        tb = traceback.format_exc()
        logger.critical(tb)

        await save_log(
            level="CRITICAL",
            message=tb,
            source=f"event:{event}"
        )

        await send_webhook_log(
            "CRITICAL",
            f"🔥 Erro Crítico ({event})",
            f"```py\n{tb[:3000]}\n```"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Logs(bot))
