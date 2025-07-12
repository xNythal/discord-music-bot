"""Constants for the Discord Music Bot"""

import discord
import os
from dotenv import load_dotenv

# Loading .env file
load_dotenv()

# The secret key that authenticates your bot with the Discord API.
# Insert your own token in your `.env` file before running the bot. Never share or publish it.
BOT_TOKEN: str = os.getenv("BOT_TOKEN")

# The number of minutes the bot will wait before leaving a voice channel if no users are connected.
# Negative value means no timeout, 0 means immediate timeout.
IDLE_TIMEOUT_MINUTES: int = 0

# The path to the log file where the bot will write its logs.
# This file will be created if it does not exist.
LOG_FILE_PATH: str = "logs.log"

# The length of the separator line in the log file.
# This is used to visually separate different sessions in the log file.
LOG_SEPARATOR_LENGTH: int = 50

# The activity that the bot will display when it is online.
# This can be a game, a streaming status, or any other activity.
BOT_ACTIVITY: discord.Activity = discord.Game(name="Music 🎵")

# The URL to the support server for the bot.
# Replace with your own support server URL.
# If you don't have a support server, you can set this to None.
SUPPORT_SERVER_URL: str|None = "https://discord.gg/your-support-server"

# The command prefix that the bot will respond to.
# This is the character or string that users will type before commands.
# This will not affect slash commands.
COMMAND_PREFIX: str = "$"

# The file where DJ roles are stored.
# DJ roles are roles that have special permissions to use certain music commands.
DJ_ROLES_FILE_PATH: str = "data/dj_roles.txt"