import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import PERMISSION_LEVELS
from utils.checks import require_level

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Recarrega um cog")
    @require_level(PERMISSION_LEVELS["DEV"])
    async def reload(self, interaction: discord.Interaction, cog: str):
        try:
            await self.bot.reload_extension(cog)
            await interaction.response.send_message(
                f"🔄 Cog `{cog}` recarregado com sucesso.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erro ao recarregar `{cog}`:\n```py\n{e}\n```",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Reload(bot))
