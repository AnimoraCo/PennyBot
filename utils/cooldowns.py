import time
from collections import defaultdict

class CooldownManager:
    def __init__(self):
        self.global_cd = defaultdict(float)
        self.command_cd = defaultdict(lambda: defaultdict(float))

    def is_on_global_cooldown(self, user_id: int, cooldown: float) -> float:
        now = time.time()
        remaining = self.global_cd[user_id] - now
        if remaining > 0:
            return remaining

        self.global_cd[user_id] = now + cooldown
        return 0.0

    def is_on_command_cooldown(
        self,
        user_id: int,
        command: str,
        cooldown: float
    ) -> float:
        now = time.time()
        remaining = self.command_cd[user_id][command] - now
        if remaining > 0:
            return remaining

        self.command_cd[user_id][command] = now + cooldown
        return 0.0


# ✅ INSTÂNCIA GLOBAL (ISSO ESTAVA FALTANDO)
cooldowns = CooldownManager()
