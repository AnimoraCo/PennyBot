import os
import logging

logger = logging.getLogger("penny")

async def load_cogs(bot):
    for root, _, files in os.walk("cogs"):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                path = os.path.join(root, file)
                module = path.replace("\\", ".").replace("/", ".")[:-3]

                try:
                    await bot.load_extension(module)
                    logger.info(f"📦 Cog carregado: {module}")
                except Exception as e:
                    logger.error(f"❌ Erro ao carregar {module}: {e}")
