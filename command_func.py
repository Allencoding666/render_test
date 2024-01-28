import html
from telegram import Update
from telegram.ext import (
    CallbackContext,
)


async def start(update: Update, context: CallbackContext) -> None:
    """Display a message with instructions on how to use this bot."""
    server_url = context.bot_data.get["SEVER_URL"]
    payload_url = html.escape(f"{server_url}/submitpayload?user_id=<your user id>&payload=<payload>")
    text = (
        f"To check if the bot is still running, call <code>{server_url}/healthcheck</code>.\n\n"
        f"To post a custom update, call <code>{payload_url}</code>."
    )
    await update.message.reply_html(text=text)
