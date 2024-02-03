from init import *
import html
from telegram import Update
from telegram.ext import (
    CallbackContext,
)
import requests


async def start(update: Update, context: CallbackContext) -> None:
    """Display a message with instructions on how to use this bot."""
    server_url = SEVER_URL
    print("update : ", update)
    print("update.message : ", update.message)
    print("update.api_kwargs : ", update.api_kwargs)
    print(context)

    payload_url = html.escape(f"{server_url}/submitpayload?user_id=<your user id>&payload=<payload>")
    text = (
        f"To check if the bot is still running, call <code>{server_url}/healthcheck</code>.\n\n"
        f"To post a custom update, call <code>{payload_url}</code>."
    )
    await update.message.reply_html(text=text)


async def weather(update: Update, context: CallbackContext, location_name: str = "西屯區") -> None:
    """取得台中市天氣預報"""
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-073?Authorization=CWA-55E41616-4DFC-494F-8D12-2121983E8639&limit=1&locationName=%E8%A5%BF%E5%B1%AF%E5%8D%80&elementName=WeatherDescription"
    rsp = requests.get(url)
    rsp_json = rsp.json()
    city = rsp_json["records"]["locations"][0]["locationsName"]
    district = rsp_json["records"]["locations"][0]["location"][0]["locationName"]
    description = rsp_json["records"]["locations"][0]["location"][0]["weatherElement"][0]["description"]

    all_data = rsp_json["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"]
    result = f"{city} : {district}\n{description}\n\n"
    for data in all_data:
        start_time = data["startTime"]
        end_time = data["endTime"]
        value = data["elementValue"][0]["value"]
        result += f"{start_time} ~ {end_time}\n - 天氣預報 : {value}\n"

    await update.message.reply_html(text=result)
