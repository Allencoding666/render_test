import os
from telegram.ext import (
    CallbackContext,
)

# Define configuration constants
SEVER_URL = os.environ.get("SEVER_URL", "https://r-render-test.onrender.com")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
PORT = 5000
BOT_TOKEN = os.getenv("TOKEN", "6589718266:AAHKFM9wwTTPCFCcwtiblLATHccCPLMHU1w")

