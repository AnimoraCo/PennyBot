from discord import app_commands
from utils.permissions import get_user_level
from utils.permissions import get_user_level, PERMISSION_LEVELS
from utils.maintenance import is_maintenance
from utils.cooldowns import CooldownManager
from utils.permissions import get_user_level, PERMISSION_LEVELS

cooldowns = CooldownManager()


def maintenance_check():
    async def predicate(interaction):
        if not await is_maintenance():
            return True

        level = await get_user_level(interaction.user.id)
        if level >= PERMISSION_LEVELS["DEV"]:
            return True

        raise app_commands.CheckFailure(
            "🛠️ O bot está em manutenção no momento."
        )
    return app_commands.check(predicate)

def require_level(min_level: int):
    async def predicate(interaction):
        level = await get_user_level(interaction.user.id)
        if level < min_level:
            raise app_commands.CheckFailure(
                "Você não tem permissão para usar este comando."
            )
        return True
    return app_commands.check(predicate)

def cooldown(global_cd: float = 2.0, command_cd: float | None = None):
    async def predicate(interaction):
        level = await get_user_level(interaction.user.id)
        if level >= PERMISSION_LEVELS["DEV"]:
            return True

        remaining = cooldowns.is_on_global_cooldown(
            interaction.user.id,
            global_cd
        )

        if remaining > 0:
            raise app_commands.CheckFailure(
                f"⏳ Aguarde `{remaining:.1f}s` antes de usar outro comando."
            )

        if command_cd:
            remaining_cmd = cooldowns.is_on_command_cooldown(
                interaction.user.id,
                interaction.command.name,
                command_cd
            )
            if remaining_cmd > 0:
                raise app_commands.CheckFailure(
                    f"⏳ Aguarde `{remaining_cmd:.1f}s` para usar este comando novamente."
                )

        return True
    return app_commands.check(predicate)
