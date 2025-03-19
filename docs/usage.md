# Usage Guide for Lisan Al Gaib Discord Music Bot

This document provides a comprehensive guide on how to install, configure, and use the **Lisan Al Gaib** Discord Music Bot. Follow the steps below to transform your Discord server into a sanctuary of celestial harmonies.

---

## Installation and Configuration

### 1. Clone the Repository

Begin by cloning the repository to your local machine:

```bash
git clone https://github.com/yourusername/discord-music-bot.git
cd discord-music-bot
```

## 2. Set Up a Virtual Environment

Create a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 3. Install Dependencies

Install the required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 4. Configure the Bot

**Bot Settings**
Open the config/config.yaml file to adjust general bot settings such as the command prefix and logging options.

**API Keys**
Insert your API credentials for Tidal, Spotify, and YouTube into the config/api_keys.json file.

    **Security Tip:** Ensure that these keys remain secure and are not exposed in public repositories.

**Discord Bot Token**
Set your Discord bot token as an environment variable:

```bash
export DISCORD_BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN"
```

## 5. Run the Bot

Start the bot by executing:

```bash
python src/main.py
```

## Bot Commands

Once the bot is running and invited to your Discord server, you can control it using the following commands:

### General Information Commands

- `!info`
  Displays detailed information about the bot, including version, uptime, Python version, and operating system.

- `!helpinfo`
  Provides a list of all available commands along with their descriptions.

## Music Playback Commands

- `!play <query>`
  Searches for a track across Tidal, Spotify, and YouTube based on your query and plays the first matching result.
  Example: `!play House of the Rising Sun`

- `!skip`
  Skips the currently playing track and starts the next one in the queue.

- `!pause`
  Pauses the current track.

- `!resume`
  Resumes playback of a paused track.

- `!stop`
  Stops the music session, clears the queue, and disconnects the bot from the voice channel

## How to Use the Bot

**Join a Voice Channel**
Ensure you are connected to a voice channel on your Discord server.

**Start Playing Music**
In any text channel where the bot has permissions, type:

```bash
!play <song or artist name>
```

The bot will perform a unified search across supported platforms and begin playback.

**Control Playback**
Use `!skip` to move to the next track.
Use `!pause` to pause and `!resume` to continue the current track.
Use `!stop` to end the music session and have the bot leave the voice channel.

Get More Information
For a list of commands and detailed info about the bot, type:

```bash
!helpinfo
```

```bash
!info
```

Troubleshooting and Tips
Bot Not Responding
Ensure the bot is online.
Check your Discord bot token.
Make sure the bot has the necessary permissions on your server.
Voice Connection Issues
Confirm that you are connected to a voice channel before issuing music commands.
The bot will only join a channel if the command author is connected.
API Key Errors
Double-check that your API keys in config/api_keys.json are valid.
Invalid or expired keys can prevent the bot from fetching music.
Logging
The bot uses a centralized logging system.
Check the logs for error messages that can help diagnose issues.
Extending Functionality
The modular architecture of Lisan Al Gaib makes it easy to add new features or integrate additional platforms. Refer to the project documentation in the docs/ folder for design details and best practices.

Final Note
Step into the realm of sound and prophecy. Let Lisan Al Gaib be your guide through the sonic dunes of Arrakis, where every beat is a sacred scripture and every melody a divine commandment. Embrace the sacred cadence of the Spice and elevate your spirit with every note.

May your musical pilgrimage be ever transcendent.
