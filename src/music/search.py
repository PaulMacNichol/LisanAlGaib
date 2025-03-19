# src/music/search.py

import asyncio
from utils.logger import get_logger
from utils.helpers import sanitize_text  # Import helper to sanitize text

# Import the service modules. These modules should each implement an async search(query: str) function.
from services import tidal, spotify, youtube

logger = get_logger(__name__)


async def search_tidal(query: str):
    """
    Search Tidal for tracks matching the query.
    """
    try:
        results = await tidal.search(query)
        logger.info(
            f"Found {len(results)} results on Tidal for query '{sanitize_text(query)}'")
        return results
    except Exception as e:
        logger.error(f"Error searching Tidal: {e}")
        return []


async def search_spotify(query: str):
    """
    Search Spotify for tracks matching the query.
    """
    try:
        results = await spotify.search(query)
        logger.info(
            f"Found {len(results)} results on Spotify for query '{sanitize_text(query)}'")
        return results
    except Exception as e:
        logger.error(f"Error searching Spotify: {e}")
        return []


async def search_youtube(query: str):
    """
    Search YouTube for tracks matching the query.
    """
    try:
        results = await youtube.search(query)
        logger.info(
            f"Found {len(results)} results on YouTube for query '{sanitize_text(query)}'")
        return results
    except Exception as e:
        logger.error(f"Error searching YouTube: {e}")
        return []


async def unified_search(query: str):
    """
    Perform a unified search across Tidal, Spotify, and YouTube.
    Returns a combined list of track dictionaries.
    """
    tidal_results, spotify_results, youtube_results = await asyncio.gather(
        search_tidal(query),
        search_spotify(query),
        search_youtube(query),
    )
    combined_results = tidal_results + spotify_results + youtube_results

    # Sanitize track titles for all results.
    for track in combined_results:
        if 'title' in track:
            track['title'] = sanitize_text(track['title'])

    logger.info(
        f"Unified search for query '{sanitize_text(query)}' returned {len(combined_results)} total results")
    return combined_results

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python search.py <query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    async def main():
        results = await unified_search(query)
        # For demonstration, print out the title and source URL of each result.
        for idx, track in enumerate(results, 1):
            title = track.get('title', 'Unknown Title')
            url = track.get('source_url', 'No URL')
            print(f"{idx}. {title} - {url}")

    asyncio.run(main())
