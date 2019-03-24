# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, request
from src.bot import process_message

app = Flask(__name__)

if os.path.isfile('env.json'):
    with open('env.json') as f:
        data = json.load(f)
        for k in data:
            os.environ[k] = data[k]

@app.route("/", methods=["POST"])
def process_update():
    if request.method == "POST":
        update = request.get_json()
        if "message" in update:
            process_message(update["message"])
    return "ok!", 200
