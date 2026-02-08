from discord.ext import commands
import datetime

class BotInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    @commands.Cog.listener()
    async def on_ready(self):
        uptime = datetime.datetime.utcnow() - self.start_time
        print(f"⏱️ Uptime inicial: {uptime}")

async def setup(bot: commands.Bot):
    await bot.add_cog(BotInfo(bot))
