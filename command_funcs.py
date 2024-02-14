from init import *
import html
from telegram import Update
from telegram.ext import (
    CallbackContext,
)
import aiohttp
from urllib.parse import quote
from datetime import datetime, timedelta
import pytz


async def start(update: Update, context: CallbackContext) -> None:
    """Display a message with instructions on how to use this bot."""
    server_url = SEVER_URL

    payload_url = html.escape(f"{server_url}/submitpayload?user_id=<your user id>&payload=<payload>")
    text = (
        f"To check if the bot is still running, call <code>{server_url}/healthcheck</code>.\n\n"
        f"To post a custom update, call <code>{payload_url}</code>."
    )
    await update.message.reply_html(text=text)


async def weather(update: Update, context: CallbackContext) -> None:
    """取得台中市-西屯區近24小時的天氣預報"""
    current_time = datetime.now(pytz.timezone('Asia/Taipei'))
    eight_hours_later_time = current_time + timedelta(hours=24)
    encoded_current_time = quote(current_time.strftime("%Y-%m-%dT%H:%M:%S"))
    encoded_eight_hours_later_time = quote(eight_hours_later_time.strftime("%Y-%m-%dT%H:%M:%S"))

    url = (f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-073"
           f"?Authorization={WEATHER_AUTH_CODE}"
           f"&locationName=%E8%A5%BF%E5%B1%AF%E5%8D%80"
           f"&elementName=WeatherDescription"
           f"&timeFrom={encoded_current_time}"
           f"&timeTo={encoded_eight_hours_later_time}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as rsp:
            rsp_json = await rsp.json()

    city = rsp_json["records"]["locations"][0]["locationsName"]
    district = rsp_json["records"]["locations"][0]["location"][0]["locationName"]
    description = rsp_json["records"]["locations"][0]["location"][0]["weatherElement"][0]["description"]

    all_data = rsp_json["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"]
    result = (f"{city} : {district}\n"
              f"{description}\n"
              f"撈取時間 : {current_time.strftime('%Y-%m-%d %H:%M:%S')} ~ "
              f"{eight_hours_later_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    for data in all_data:
        start_time = data["startTime"]
        end_time = data["endTime"]
        value = data["elementValue"][0]["value"]
        result += f"{start_time} ~ {end_time}\n - 天氣預報 : {value}\n\n"

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=result)
