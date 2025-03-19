# src/main.py

import os
from bot import bot, load_extensions
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    # Load all the required extensions (cogs).
    load_extensions()

    # Retrieve the bot token from an environment variable.
    TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_BOT_TOKEN")
    if TOKEN == "YOUR_DISCORD_BOT_TOKEN":
        logger.error(
            "Please set your Discord bot token in the environment variable 'DISCORD_BOT_TOKEN'")
        return

    # Run the bot.
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
