import os
from os.path import expanduser

USER_HOME_DIR = expanduser("~")

REFRESH_GOOGLE_API_TOKEN_TIME = 86400
DRY_SHEET_RUN = False
CHECK_ON_EMPTY_VOICE_CHANNEL = True

PERMITTED_COMMANDS_ROLE = "root"
BOT_COMMAND_PREFIX = "ai-"

BOT_CONFIG_DIR = ".discord-iu4-bot"

BOT_CONFIG_PATH = os.path.join(USER_HOME_DIR, BOT_CONFIG_DIR)

DISCORD_TOKEN_FILEPATH = os.path.join(BOT_CONFIG_PATH, "discord.json")
GOOGLE_CREDENTIALS_FILEPATH = os.path.join(BOT_CONFIG_PATH, "credentials.json")
GOOGLE_TOKEN_FILEPATH = os.path.join(BOT_CONFIG_PATH, "google.json")
