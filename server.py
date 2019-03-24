import requests
import os
import json
import boto3
from flask import Flask, request
from pdfParser import pdf_handler

app = Flask(__name__)

if os.path.isfile('env.json'):
    with open('env.json') as f:
        data = json.load(f)
        for k in data:
            os.environ[k] = data[k]

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", None)

SEND_MESSAGE="sendMessage"
GET_FILE="getFile"

def save(user, data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('unicamp_utils_bot')
    table.put_item(Item={ 'user_id' : user, 'data' : data})

def get(user):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('unicamp_utils_bot')
    r = table.get_item(Key={ 'user_id' : user})

    data = {}
    data["chat_id"] = user
    
    if 'Item' in r:
        classes = []
        for c in r['Item']['data']:
            classes.append(c['code'])
        data["text"] = 'Voce tem as seguintes aulas cadastradas:\n {}'.format('\n'.join(classes))
    else:
        data["text"] = "Voce nao tem nenhuma aula cadastrada ainda. Para cadastrar, basta fazer um upload de seu relatorio de matricula disponivel em https://www1.sistemas.unicamp.br/altmatr/autenticarusuario.do"
    r = requests.post(get_url(SEND_MESSAGE), data=data)

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
            data["text"] = "Recebemos seu arquivo. Estamos processando-o"
            r = requests.post(get_url(SEND_MESSAGE), data=data)

            data = {}
            with requests.get(get_url_download(fileData['result']['file_path']), stream=True) as r:
                with open('/tmp/test.pdf', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        if chunk:
                            f.write(chunk)
                            f.flush()

            data = {}
            try:
                res = pdf_handler()
                save(message["from"]["id"], res)
                data["chat_id"] = message["from"]["id"]
                data["text"] = "File received {}".format(str(res))
                r = requests.post(get_url(SEND_MESSAGE), data=data)
            except Exception as e:
                print(e)
                data["chat_id"] = message["from"]["id"]
                data["text"] = "Falha no recebimento {}".format(str(e))
                r = requests.post(get_url(SEND_MESSAGE), data=data)
            finally:
                os.remove('/tmp/test.pdf')

        else:
            if (message['text'] == '\\lista'):
                get(message['from']['id'])
            else:
                data = {}
                data["chat_id"] = message["from"]["id"]
                data["text"] = "\lista para ver suas materias"
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
