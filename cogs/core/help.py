import discord
from discord.ext import commands
from discord import app_commands


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ajuda",
        description="Mostra informações sobre o bot"
    )
    async def ajuda(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Penny • Ajuda",
            description=(
                "Bem-vindo à **Penny**!\n\n"
                "📌 **Principais comandos**\n"
                "• `/ajuda` — Mostra esta mensagem\n"
                "• `/maintenance` — Ativa/desativa manutenção\n"
                "• `/reload` — Recarrega módulos do bot\n\n"
                "ℹ️ Mais comandos serão adicionados em breve."
            ),
            color=discord.Color.blurple()
        )

        embed.set_footer(text="Penny • Em desenvolvimento")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
