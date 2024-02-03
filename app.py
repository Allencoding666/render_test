import asyncio
import logging
from http import HTTPStatus

import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, Response, make_response, request

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import command_funcs
import message_funcs
import filter_funcs
from init import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def main() -> None:
    """Set up PTB application and a web application for handling the incoming requests."""

    application = (
        Application.builder().token(BOT_TOKEN).updater(None).context_types(ContextTypes()).build()
    )

    # register handlers
    application.add_handler(CommandHandler("start", command_funcs.start))
    application.add_handler(CommandHandler("weather", command_funcs.weather))

    filter_msg_test = filter_funcs.FilterMsgTest()
    application.add_handler(MessageHandler(filter_msg_test, message_funcs.msg_test))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_funcs.echo))

    # Pass webhook settings to telegram
    await application.bot.set_webhook(url=f"{SEVER_URL}/telegram", allowed_updates=Update.ALL_TYPES)

    # Set up webserver
    flask_app = Flask(__name__)

    @flask_app.post("/telegram")  # type: ignore[misc]
    async def telegram() -> Response:
        """Handle incoming Telegram updates by putting them into the `update_queue`"""
        await application.update_queue.put(Update.de_json(data=request.json, bot=application.bot))
        return Response(status=HTTPStatus.OK)

    @flask_app.get("/healthcheck")  # type: ignore[misc]
    async def health() -> Response:
        """For the health endpoint, reply with a simple plain text message."""
        response = make_response("The bot is still running fine :)", HTTPStatus.OK)
        response.mimetype = "text/plain"
        return response

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=WsgiToAsgi(flask_app),
            port=PORT,
            use_colors=False,
            host="0.0.0.0"
        )
    )

    # Run application and webserver together
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()


if __name__ == "__main__":
    asyncio.run(main())
