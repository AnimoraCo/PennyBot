import discord
import random

CUSTOM_STATUSES = [
    "Se divertindo em {servers} servidores!",
    "Brincando com {users} usuários!",
    "Utilize /ajuda para ver todos os meus comandos!",
]

def get_random_status(bot: discord.Client) -> discord.CustomActivity:
    status = random.choice(CUSTOM_STATUSES)

    status = status.format(
        servers=len(bot.guilds),
        users=sum(guild.member_count or 0 for guild in bot.guilds)
    )

    return discord.CustomActivity(name=status)
