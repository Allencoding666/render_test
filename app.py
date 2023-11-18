import logging
from flask import Flask, request
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

application = Application.builder().token("TOKEN").build()


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    """Handle incoming webhook updates."""
    update = Update.de_json(request.get_json(force=True), application.bot)

    # Process the update using the application's dispatcher
    application.process_update(update)

    return "ok"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


if __name__ == "__main__":
    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Set the webhook URL
    webhook_url = "https://r-telegram-bot.onrender.com/webhook"  # Replace with your server's domain and endpoint
    application.bot.setWebhook(webhook_url)

    # Run the Flask app
    app.run(port=8443)  # Replace with the port you want to use (usually 443 for HTTPS)