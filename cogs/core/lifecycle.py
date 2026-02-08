from discord.ext import commands

class Lifecycle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"➕ Entrei no servidor: {guild.name} ({guild.id})")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"➖ Sai do servidor: {guild.name} ({guild.id})")

async def setup(bot: commands.Bot):
    await bot.add_cog(Lifecycle(bot))
