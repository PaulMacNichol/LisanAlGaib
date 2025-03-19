# src/music/player.py

import asyncio
import discord
from discord.ext import commands

from utils.logger import get_logger
# Import URL validation and sanitization
from utils.helpers import is_valid_url, sanitize_text

logger = get_logger(__name__)


class MusicPlayer:
    """
    A MusicPlayer class for managing audio playback in a Discord guild.
    It handles queue management, connecting to voice channels, and streaming audio.
    """

    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self.ctx = ctx
        self.guild = ctx.guild
        self.voice_client: discord.VoiceClient = None
        self.queue = asyncio.Queue()
        self.current_track = None
        self.next_track_event = asyncio.Event()
        # Start the background task for playing queued tracks.
        self.player_task = bot.loop.create_task(self.player_loop())

    async def join(self, channel: discord.VoiceChannel = None):
        """
        Connect to a voice channel.
        If no channel is provided, the bot will join the voice channel
        that the command author is currently in.
        """
        if channel is None:
            if self.ctx.author.voice:
                channel = self.ctx.author.voice.channel
            else:
                raise Exception(
                    "Author is not connected to any voice channel.")
        self.voice_client = await channel.connect()
        logger.info(f"Connected to voice channel: {channel.name}")

    async def leave(self):
        """
        Disconnect the bot from the voice channel.
        """
        if self.voice_client:
            await self.voice_client.disconnect()
            logger.info("Disconnected from voice channel")
            self.voice_client = None

    async def player_loop(self):
        """
        The main loop that waits for tracks in the queue and plays them sequentially.
        It automatically joins a voice channel if not connected.
        """
        while True:
            self.next_track_event.clear()
            self.current_track = await self.queue.get()

            # Validate the source URL using the helper.
            source_url = self.current_track.get('source_url')
            if not is_valid_url(source_url):
                logger.error(
                    f"Invalid URL for track: {sanitize_text(self.current_track.get('title', 'Unknown Title'))}")
                continue

            # Join the author's voice channel if not already connected.
            if not self.voice_client:
                if self.ctx.author.voice:
                    await self.join(self.ctx.author.voice.channel)
                else:
                    logger.error(
                        "Command author is not connected to any voice channel.")
                    continue

            # Prepare the audio source.
            source = discord.FFmpegPCMAudio(source_url, options='-vn')

            def after_playback(error):
                if error:
                    logger.error(f"Error during playback: {error}")
                # Signal that the track has finished playing.
                self.bot.loop.call_soon_threadsafe(self.next_track_event.set)

            # Play the audio and send a message about the current track.
            self.voice_client.play(source, after=after_playback)
            await self.ctx.send(f"Now playing: {sanitize_text(self.current_track.get('title', 'Unknown Title'))}")

            # Wait until the track finishes.
            await self.next_track_event.wait()
            # Optional: short delay between tracks.
            await asyncio.sleep(1)

    def add_to_queue(self, track: dict):
        """
        Add a track to the queue.
        The track should be a dictionary with at least 'source_url' and 'title' keys.
        """
        self.queue.put_nowait(track)
        logger.info(
            f"Added track to queue: {sanitize_text(track.get('title', 'Unknown Title'))}")

    def skip(self):
        """
        Skip the currently playing track.
        """
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            logger.info("Skipped the current track")

    def pause(self):
        """
        Pause the currently playing track.
        """
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            logger.info("Paused the track")

    def resume(self):
        """
        Resume playback if paused.
        """
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            logger.info("Resumed the track")
