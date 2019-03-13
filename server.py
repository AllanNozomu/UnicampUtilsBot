import requests
import os
from flask import Flask, request

app = Flask(__name__)

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")

def get_url(method):
  return "https://api.telegram.org/bot{}/{}".format(bot_token,method)

def process_message(update):
    data = {}
    data["chat_id"] = update["message"]["from"]["id"]
    data["text"] = "I can hear you!"
    r = requests.post(get_url("sendMessage"), data=data)

@app.route("/", methods=["POST"])
def process_update():
    if request.method == "POST":
        update = request.get_json()
        if "message" in update:
            process_message(update)
    return "ok!", 200
