import discord
from discord.ext import commands
from discord import app_commands

from utils.maintenance import (
    is_maintenance,
    set_maintenance,
    get_maintenance_reason
)
from utils.permissions import PERMISSION_LEVELS, get_user_level


class Maintenance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="maintenance",
        description="Ativa ou desativa o modo manutenção do bot"
    )
    @app_commands.describe(
        estado="on para ativar, off para desativar",
        motivo="Motivo da manutenção (opcional)"
    )
    async def maintenance(
        self,
        interaction: discord.Interaction,
        estado: str,
        motivo: str | None = None
    ):
        estado = estado.lower()

        if estado not in ("on", "off"):
            return await interaction.response.send_message(
                "❌ Use `on` ou `off`.",
                ephemeral=True
            )


            if level < PERMISSION_LEVELS["DEV"]:
                return await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando.",
                ephemeral=True
    )

        enabled = estado == "on"
        await set_maintenance(enabled, motivo)

        if enabled:
            msg = "🛠️ **Modo manutenção ativado**"
            if motivo:
                msg += f"\n📌 Motivo: {motivo}"
        else:
            msg = "✅ **Modo manutenção desativado**"

        await interaction.response.send_message(
            msg,
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Maintenance(bot))
