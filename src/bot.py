# src/bot.py

import os
import discord
from discord.ext import commands
from utils.logger import get_logger

logger = get_logger(__name__)

# Configure bot intents (adjust based on your needs)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Initialize the bot with a command prefix and the defined intents.
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Bot is online as {bot.user} (ID: {bot.user.id})")
    print(f"Bot is online as {bot.user}")


def load_extensions():
    """
    Load the bot extensions (cogs) from the cogs folder.
    """
    # List of cog modules to load.
    extensions = [
        "cogs.info",
        "cogs.music",
    ]
    for ext in extensions:
        try:
            bot.load_extension(ext)
            logger.info(f"Loaded extension: {ext}")
        except Exception as e:
            logger.error(f"Failed to load extension {ext}: {e}")


if __name__ == '__main__':
    load_extensions()

    # Retrieve your bot token from an environment variable or configuration file.
    # For this example, replace 'YOUR_DISCORD_BOT_TOKEN' with your actual bot token.
    TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_BOT_TOKEN")

    if TOKEN == "YOUR_DISCORD_BOT_TOKEN":
        logger.error(
            "Please set your Discord bot token in the environment variable 'DISCORD_BOT_TOKEN'")
    else:
        bot.run(TOKEN)
