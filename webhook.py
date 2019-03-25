import requests
import os
import json
import sys

with open('settings/env.json') as f:
    data = json.load(f)
    for k in data:
        os.environ[k] = data[k]

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

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