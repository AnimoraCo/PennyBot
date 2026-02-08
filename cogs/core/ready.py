from discord.ext import commands

class Ready(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Bot conectado ao Discord")
        print(f"🤖 Usuário: {self.bot.user}")
        print(f"📡 Servidores: {len(self.bot.guilds)}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Ready(bot))
