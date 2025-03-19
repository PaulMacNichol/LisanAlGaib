#!/bin/bash

# run.sh: Script to start the Lisan Al Gaib Discord Music Bot

# Check if the DISCORD_BOT_TOKEN environment variable is set
if [ -z "$DISCORD_BOT_TOKEN" ]; then
  echo "Error: DISCORD_BOT_TOKEN environment variable is not set."
  echo "Please set it using: export DISCORD_BOT_TOKEN='YOUR_DISCORD_BOT_TOKEN'"
  exit 1
fi

# Optionally activate the virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
  echo "Activating virtual environment..."
  source venv/bin/activate
fi

echo "Starting Lisan Al Gaib Discord Music Bot..."
python src/main.py
