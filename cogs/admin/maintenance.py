import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import PERMISSION_LEVELS
from utils.checks import require_level
from utils.maintenance import set_maintenance

class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="maintenance", description="Ativa/desativa manutenção")
    @require_level(PERMISSION_LEVELS["DEV"])
    async def maintenance(self, interaction: discord.Interaction, state: bool):
        await set_maintenance(state)
        status = "ativada" if state else "desativada"
        await interaction.response.send_message(
            f"🛠️ Manutenção {status}.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Maintenance(bot))
