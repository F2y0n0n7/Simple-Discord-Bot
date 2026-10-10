import os
import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv
from uitils.config import get_cog_config, setup_config


# .env liegt im Hauptverzeichnis (einen Ordner höher als src/)
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

TOKEN = os.getenv("BOT_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")

if not TOKEN:
    raise ValueError("[Main] Error: No BOT_TOKEN found in the .env file.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def load_extensions():
    cogs_dir = Path(__file__).resolve().parent / "cogs"
    config_dir = Path(__file__).resolve().parent / "config.json"
    if not config_dir.exists():
        try:
            setup_config()
            print("[Main] Config setup successfully.")
        except Exception as e:
            print(f"[Main] Error setting up config: {e}")

    if not cogs_dir.exists():
        cogs_dir.mkdir(parents=True, exist_ok=True)
        print("[Main] Folder 'src/cogs' created.")
        return

    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            cog_name = filename[:-3]
            if not get_cog_config(cog_name)["enabled"]:
                print(f"[Main] ⚠️ cogs.{cog_name} is disabled in the config.")
                continue
            try:
                bot.load_extension(f"cogs.{cog_name}")
            except discord.ExtensionFailed as e:
                print(f"[Main] ❌ cogs.{cog_name} failed in its code: {type(e.original).__name__}: {e.original}")
            except discord.ExtensionNotFound:
                print(f"[Main] ❌ cogs.{cog_name} not found.")
            except discord.NoEntryPointError:
                print(f"[Main] ❌ cogs.{cog_name} has no 'setup' function.")
            except discord.ExtensionAlreadyLoaded:
                print(f"[Main] ⚠️ cogs.{cog_name} is already loaded.")
            else:
                print(f"[Main] ✅ Extension loaded: cogs.{cog_name}")

@bot.event
async def on_ready():
    print("----------------------------------------")
    print(f"[Main] 🤖 Bot online as: {bot.user.name}")
    print(f"[Main] ⚙️  Prefix: {PREFIX}")
    print("----------------------------------------")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())