from init import *
from telegram import Update
from telegram.ext import (
    ContextTypes
)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def msg_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle custom updates."""
    text = "測試"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
