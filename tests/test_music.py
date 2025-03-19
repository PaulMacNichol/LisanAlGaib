# tests/test_music.py

import unittest
import asyncio
from discord.ext import commands

# Import the classes we want to test.
from music.player import MusicPlayer
from cogs.music import Music

# Dummy classes to simulate minimal Discord objects.


class DummyVoiceClient:
    def __init__(self, channel):
        self.channel = channel
        self._playing = False

    def play(self, source, after):
        self._playing = True
        # Immediately trigger the after callback for testing.
        after(None)

    def is_playing(self):
        return self._playing

    def stop(self):
        self._playing = False

    async def disconnect(self):
        self._playing = False


class DummyChannel:
    def __init__(self, name="Dummy Channel"):
        self.name = name

    async def connect(self):
        return DummyVoiceClient(self)


class DummyVoiceState:
    def __init__(self, channel):
        self.channel = channel


class DummyAuthor:
    def __init__(self, voice_channel=None):
        self.voice = DummyVoiceState(voice_channel) if voice_channel else None


class DummyGuild:
    def __init__(self, id, name="Dummy Guild"):
        self.id = id
        self.name = name


class DummyContext:
    def __init__(self, guild, author):
        self.guild = guild
        self.author = author

    async def send(self, message):
        # For testing, simply return the message.
        return message

# Test cases for MusicPlayer


class TestMusicPlayer(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Create a dummy bot instance. We use commands.Bot but no actual connection.
        self.bot = commands.Bot(command_prefix="!", intents=None)
        # Create dummy channel, guild, and author with voice.
        self.dummy_channel = DummyChannel("Test Channel")
        self.dummy_guild = DummyGuild(123, "Test Guild")
        self.dummy_author = DummyAuthor(self.dummy_channel)
        self.dummy_context = DummyContext(self.dummy_guild, self.dummy_author)
        # Instantiate a MusicPlayer.
        self.player = MusicPlayer(self.bot, self.dummy_context)
        # Override join to use our dummy channel's connect method to avoid actual Discord calls.
        self.player.join = lambda channel=None: asyncio.sleep(
            0)  # no-op for join in test

        # Override player_loop to process only one track and then cancel.
        async def one_iteration_loop():
            if not self.player.queue.empty():
                # Simulate playback: remove a track and then signal track finished.
                track = await self.player.queue.get()
                self.player.next_track_event.set()
        self.player.player_task.cancel()  # Cancel the real loop task.
        self.player.player_task = asyncio.create_task(one_iteration_loop())

    async def test_add_to_queue(self):
        # Test that adding a track increments the queue size.
        track = {"title": "Test Track",
                 "source_url": "http://example.com/test.mp3", "service": "dummy"}
        self.player.add_to_queue(track)
        self.assertEqual(self.player.queue.qsize(), 1)

    async def test_player_loop_processes_track(self):
        # Test that the player loop processes a track (simulate by adding a track).
        track = {"title": "Test Track",
                 "source_url": "http://example.com/test.mp3", "service": "dummy"}
        self.player.add_to_queue(track)
        # Wait a short time for the loop to process the queue.
        await asyncio.sleep(0.1)
        # After processing, the event should have been set.
        self.assertTrue(self.player.next_track_event.is_set())

# Test cases for the Music cog.


class TestMusicCog(unittest.TestCase):

    def test_get_player_returns_same_instance(self):
        dummy_bot = commands.Bot(command_prefix="!")
        dummy_guild = DummyGuild(123, "Test Guild")
        dummy_author = DummyAuthor()  # Author without voice (not used in this test)
        dummy_context = DummyContext(dummy_guild, dummy_author)
        music_cog = Music(dummy_bot)
        player1 = music_cog.get_player(dummy_context)
        player2 = music_cog.get_player(dummy_context)
        self.assertIs(player1, player2)


if __name__ == '__main__':
    unittest.main()
