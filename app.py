import logging
from flask import Flask, request
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

application = Application.builder().token("6589718266:AAHKFM9wwTTPCFCcwtiblLATHccCPLMHU1w").build()


async def set_webhook():
    webhook_url = "https://r-render-test.onrender.com/webhook"  # Replace with your server's domain and endpoint
    await application.bot.setWebhook(webhook_url)
    print("Webhook set successfully")

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    """Handle incoming webhook updates."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    print("update : ", update)
    # Process the update using the application's dispatcher
    application.process_update(update)
    print("web ok")
    update.message.reply_text("456789")
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
    print("help")
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print("echo ok")
    await update.message.reply_text(update.message.text)


if __name__ == "__main__":
    # app.run(debug=True)  # Replace with the port you want to use (usually 443 for HTTPS)

    loop = asyncio.get_event_loop()

    # Set the webhook
    loop.run_until_complete(set_webhook())

    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


    print("run ok")
    app.run(debug=True)  # Replace with the port you want to use (usually 443 for HTTPS)
