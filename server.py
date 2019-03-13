import requests
import os
from flask import Flask, request
from pdfParser import pdf_handler

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

SEND_MESSAGE="sendMessage"
GET_FILE="getFile"

def get_url(method):
  return "https://api.telegram.org/bot{}/{}".format(BOT_TOKEN,method)

def get_url_prepare_download():
  return "https://api.telegram.org/bot{}/getFile".format(BOT_TOKEN)

def get_url_download(filename):
  return "https://api.telegram.org/file/bot{}/{}".format(BOT_TOKEN,filename)

def process_message(message):
    try:
        if "document" in message:
            data = {}
            data["file_id"]=message["document"]["file_id"]
            fileData = requests.post(get_url_prepare_download(), data=data).json()

            data = {}
            data["chat_id"] = message["from"]["id"]
            data["text"] = "File received"
            r = requests.post(get_url(SEND_MESSAGE), data=data)

            data = {}
            with requests.get(get_url_download(fileData['result']['file_path']), stream=True) as r:
                with open('/tmp/test.pdf', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                            f.flush()
            res = pdf_handler()
            data = {}
            data["chat_id"] = message["from"]["id"]
            data["text"] = "File received {}".format(str(res))
            r = requests.post(get_url(SEND_MESSAGE), data=data)
        else:
	        data = {}
	        data["chat_id"] = message["from"]["id"]
	        data["text"] = "I can hear you!"
	        r = requests.post(get_url(SEND_MESSAGE), data=data)
    except Exception as e:
        data = {}
        data["chat_id"] = message["from"]["id"]
        data["text"] = "ERROR {}".format(str(e))
        r = requests.post(get_url(SEND_MESSAGE), data=data)

@app.route("/", methods=["POST"])
def process_update():
    if request.method == "POST":
        update = request.get_json()
        if "message" in update:
            process_message(update["message"])
    return "ok!", 200
