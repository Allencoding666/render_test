import os
from telegram.ext import (
    CallbackContext,
)

# Define configuration constants
SEVER_URL = os.environ.get("SEVER_URL")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
PORT = 5000
BOT_TOKEN = os.getenv("TOKEN")

