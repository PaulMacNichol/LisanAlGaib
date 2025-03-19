# src/cogs/info.py

import discord
from discord.ext import commands
import platform
import datetime

from utils.logger import get_logger
from utils.helpers import format_time  # Use helper to format time

logger = get_logger(__name__)


class Info(commands.Cog):
    """Cog for displaying bot information and general help commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    @commands.command(name="info")
    async def info(self, ctx: commands.Context):
        """
        Display detailed information about the bot, such as version, uptime,
        Python version, and operating system.
        """
        uptime_delta = datetime.datetime.utcnow() - self.start_time
        uptime_seconds = int(uptime_delta.total_seconds())
        # Format uptime using helper
        formatted_uptime = format_time(uptime_seconds)

        embed = discord.Embed(
            title="Bot Information",
            description="Details about this Discord Music Bot",
            color=discord.Color.blue()
        )
        embed.add_field(name="Version", value="1.0.0", inline=False)
        embed.add_field(name="Uptime", value=formatted_uptime, inline=False)
        embed.add_field(
            name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="Platform", value=platform.system(), inline=True)
        embed.set_footer(text="Powered by discord.py")
        logger.info("Executed info command")
        await ctx.send(embed=embed)

    @commands.command(name="helpinfo")
    async def helpinfo(self, ctx: commands.Context):
        """
        Provide a list of available commands and their descriptions.
        """
        embed = discord.Embed(
            title="Help Information",
            description="Here is a list of available commands:",
            color=discord.Color.green()
        )
        embed.add_field(
            name="!info", value="Displays detailed bot information.", inline=False)
        embed.add_field(name="!play <query>",
                        value="Searches and plays a track from Tidal, Spotify, or YouTube.", inline=False)
        embed.add_field(
            name="!skip", value="Skips the currently playing track.", inline=False)
        embed.add_field(
            name="!pause", value="Pauses the current track.", inline=False)
        embed.add_field(
            name="!resume", value="Resumes playback.", inline=False)
        embed.set_footer(
            text="For additional details, refer to the bot's documentation.")
        logger.info("Executed helpinfo command")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
    logger.info("Info cog loaded successfully")
