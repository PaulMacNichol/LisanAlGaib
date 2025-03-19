# src/cogs/music.py

import discord
from discord.ext import commands
import asyncio

from utils.logger import get_logger
from utils.helpers import sanitize_text  # Import helper to sanitize text
from music.player import MusicPlayer
from music.search import unified_search

logger = get_logger(__name__)


class Music(commands.Cog):
    """Cog for music commands: play, skip, pause, resume, and stop."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Maintain a dictionary mapping guild IDs to their MusicPlayer instances.
        self.players = {}

    def get_player(self, ctx: commands.Context) -> MusicPlayer:
        """
        Retrieve the MusicPlayer for the current guild or create one if it doesn't exist.
        """
        player = self.players.get(ctx.guild.id)
        if not player:
            player = MusicPlayer(self.bot, ctx)
            self.players[ctx.guild.id] = player
            logger.info(f"Created new MusicPlayer for guild: {ctx.guild.name}")
        return player

    @commands.command(name="play", help="Play a song by searching Tidal, Spotify, and YouTube.")
    async def play(self, ctx: commands.Context, *, query: str):
        # Ensure the user is in a voice channel.
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You must be connected to a voice channel to play music.")
            return

        player = self.get_player(ctx)

        await ctx.send(f"Searching for: {sanitize_text(query)}")
        results = await unified_search(query)
        if not results:
            await ctx.send(f"No results found for: {sanitize_text(query)}")
            return

        # Select the first result from the combined search.
        track = results[0]
        player.add_to_queue(track)
        await ctx.send(f"Added to queue: {sanitize_text(track.get('title', 'Unknown Title'))}")
        logger.info(
            f"User {ctx.author} requested track '{sanitize_text(track.get('title', 'Unknown Title'))}' in guild '{ctx.guild.name}'.")

    @commands.command(name="skip", help="Skip the current track.")
    async def skip(self, ctx: commands.Context):
        player = self.players.get(ctx.guild.id)
        if player:
            player.skip()
            await ctx.send("Skipped the current track.")
            logger.info(f"Track skipped in guild '{ctx.guild.name}'.")
        else:
            await ctx.send("No active music session to skip.")

    @commands.command(name="pause", help="Pause the current track.")
    async def pause(self, ctx: commands.Context):
        player = self.players.get(ctx.guild.id)
        if player:
            player.pause()
            await ctx.send("Paused the track.")
            logger.info(f"Track paused in guild '{ctx.guild.name}'.")
        else:
            await ctx.send("No active music session to pause.")

    @commands.command(name="resume", help="Resume the paused track.")
    async def resume(self, ctx: commands.Context):
        player = self.players.get(ctx.guild.id)
        if player:
            player.resume()
            await ctx.send("Resumed the track.")
            logger.info(f"Track resumed in guild '{ctx.guild.name}'.")
        else:
            await ctx.send("No active music session to resume.")

    @commands.command(name="stop", help="Stop the music and leave the voice channel.")
    async def stop(self, ctx: commands.Context):
        player = self.players.get(ctx.guild.id)
        if player:
            # Stop playback and disconnect from the voice channel.
            player.skip()  # This stops the current track.
            await player.leave()
            del self.players[ctx.guild.id]
            await ctx.send("Stopped the music and left the voice channel.")
            logger.info(f"Music session stopped in guild '{ctx.guild.name}'.")
        else:
            await ctx.send("No active music session to stop.")


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
    logger.info("Music cog loaded successfully.")
