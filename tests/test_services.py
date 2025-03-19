# tests/test_services.py

import unittest
import asyncio

# Import the service modules to test their search functionality.
from services import tidal, spotify, youtube


class TestServices(unittest.IsolatedAsyncioTestCase):
    async def test_tidal_search(self):
        query = "Test Query"
        results = await tidal.search(query)
        # Verify that the results is a list with at least one entry.
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        track = results[0]
        # Check that the expected keys exist.
        self.assertIn("title", track)
        self.assertIn("source_url", track)
        self.assertIn("service", track)
        # Validate that the service is correctly reported.
        self.assertEqual(track["service"], "tidal")
        # Verify that the query string appears in the dummy result.
        self.assertIn(query, track["title"])
        self.assertIn(query, track["source_url"])

    async def test_spotify_search(self):
        query = "Test Query"
        results = await spotify.search(query)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        track = results[0]
        self.assertIn("title", track)
        self.assertIn("source_url", track)
        self.assertIn("service", track)
        self.assertEqual(track["service"], "spotify")
        self.assertIn(query, track["title"])
        self.assertIn(query, track["source_url"])

    async def test_youtube_search(self):
        query = "Test Query"
        results = await youtube.search(query)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        track = results[0]
        self.assertIn("title", track)
        self.assertIn("source_url", track)
        self.assertIn("service", track)
        self.assertEqual(track["service"], "youtube")
        self.assertIn(query, track["title"])
        self.assertIn(query, track["source_url"])


if __name__ == '__main__':
    unittest.main()
