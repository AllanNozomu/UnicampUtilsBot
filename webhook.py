# -*- coding: utf-8 -*-
import requests
import os
import json
import sys

from settings import settings

BOT_TOKEN = settings.getenv("TELEGRAM_BOT_TOKEN", None)

def get_url(method):
    return "https://api.telegram.org/bot{}/{}".format(BOT_TOKEN,method)

def main(argv):
    if len(argv) != 1:
        print("Excepting a parameter")
        sys.exit(2)

    url = argv[0]
    r = requests.get(get_url("setWebhook"), data={"url": url})
    r = requests.get(get_url("getWebhookInfo"))
    if 'ok' in r.json() and r.json()['ok'] == True:
        print('All set')
    else:
        print("setWebhook failed")
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])