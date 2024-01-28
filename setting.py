import os
from telegram.ext import (
    CallbackContext,
)

# Define configuration constants
bot_callbackcontext = CallbackContext
bot_callbackcontext.bot_data["SEVER_URL"] = os.environ.get("SEVER_URL")
SEVER_URL = bot_callbackcontext.bot_data["SEVER_URL"]
# SEVER_URL = os.environ.get("SEVER_URL")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
PORT = 5000
BOT_TOKEN = os.getenv("TOKEN")

