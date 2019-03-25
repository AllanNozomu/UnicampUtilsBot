# -*- coding: utf-8 -*-
import boto3
import os
import requests
from src.pdf_parser import pdf_handler

import src.database as database

SEND_MESSAGE = "sendMessage"
GET_FILE = "getFile"

ALLOWED_METHOS = (
    SEND_MESSAGE,
    GET_FILE,
)

def get_url(method):
    if method not in ALLOWED_METHOS:
        raise Exception('Not valid method')

    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", None)
    return "https://api.telegram.org/bot{}/{}".format(BOT_TOKEN, method)


def get_url_prepare_download():
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", None)
    return "https://api.telegram.org/bot{}/getFile".format(BOT_TOKEN)


def get_url_download(filename):
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", None)
    return "https://api.telegram.org/file/bot{}/{}".format(BOT_TOKEN,filename)


def send_message(chat_id, text):
    data = {}
    data["chat_id"] = chat_id
    data["text"] = text
    r = requests.post(get_url(SEND_MESSAGE), data=data)
    return r.json()


def process_message(message):
    try:
        if "document" in message:
            data = {}
            data["file_id"]=message["document"]["file_id"]
            fileData = requests.post(get_url_prepare_download(), data=data).json()

            send_message(message["from"]["id"], "Recebemos seu arquivo. Estamos processando-o")
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
                database.save_user_data(message["from"]["id"], res)
                send_message(message["from"]["id"], "File received {}".format(str(res)))
                r = requests.post(get_url(SEND_MESSAGE), data=data)
            except Exception as e:
                print(e)
                send_message(message["from"]["id"], "Falha no recebimento {}".format(str(e)))
                r = requests.post(get_url(SEND_MESSAGE), data=data)
            finally:
                os.remove('/tmp/test.pdf')

        else:
            if (message['text'] == '/lista'):
                r = database.get_user_data(message['from']['id'])
                data = {}
                if 'Item' in r:
                    classes = []
                    for c in r['Item']['data']:
                        classes.append(c['code'])
                    msg = 'Voce tem as seguintes aulas cadastradas:\n{}'.format('\n'.join(classes))
                else:
                    msg = "Voce nao tem nenhuma aula cadastrada ainda. Para cadastrar, basta fazer um upload de seu relatorio de matricula disponivel em https://www1.sistemas.unicamp.br/altmatr/autenticarusuario.do"
                send_message(message["from"]["id"], msg)
            else:
                send_message(message["from"]["id"], "/lista para ver suas materias")
    except Exception as e:
        data = {}
        data["chat_id"] = message["from"]["id"]
        data["text"] = "ERROR {}".format(str(e))
        r = requests.post(get_url(SEND_MESSAGE), data=data)