import os

def load_cogs(bot, base_path="cogs"):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                module = (
                    root.replace("/", ".")
                        .replace("\\", ".")
                    + f".{file[:-3]}"
                )
                bot.load_extension(module)
                print(f"📦 Cog carregado: {module}")
