from flask import Flask, request
import requests
import json
import traceback
import random
import os
import sys

from urllib.parse import urlencode
from urllib.request import Request, urlopen

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.getenv("VERIFY_TOKEN"):
            return "Verification token mismatch"
        return request.args["hub.challenge"]

    return "hello world!! get", 200


@app.route('/', methods=['POST'])
def webhook():
    url = 'https://graph.facebook.com/v2.6/me/messages'

    req_data = request.data

    data = json.loads(req_data)

    sender_id = data["entry"][0]["messaging"][0]["sender"]["id"]
    sender_msg = data["entry"][0]["messaging"][0]["message"]["text"]

    send_back_to_fb = {
        "recipient": {
            "id": sender_id
        },
        "message": {
            # "text": sender_msg,
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "https://i.pinimg.com/564x/f8/09/07/f809070515b2489cf4297f81daf267e9--rick-and-morty.jpg",
                    "is_reusable": "true"
                }
            }
        }
    }

    headers = {'Content-type': 'application/json'}

    params_input = {"access_token": os.getenv('PAGE_ACCESS_TOKEN')}

    if check_conditions(sender_msg):
        fb_response = requests.post(url,
                                    data=json.dumps(send_back_to_fb),
                                    headers=headers,
                                    params=params_input
                                    )

        # handle the response to the subrequest you made
        if not fb_response.ok:
            # log some useful info for yourself, for debugging
            print ('--- BEGIN ERROR ---')
            print ('fb_response: ', fb_response)
            print ('fb_response.json(): ', fb_response.json())
            print ('---  END  ERROR ---')

    else:
        print (sender_msg)
        print (check_conditions(sender_msg))




    return "OK", 200

def check_conditions(message):
    message = message.lower()
    if (message.find('yes') != -1 and message.find('or') != -1 and message.find('no') != -1 and message.find('?') != -1) or (message.find('yon?') != -1):
        return True
    else:
        return False


if __name__ == '__main__':
    app.run()
