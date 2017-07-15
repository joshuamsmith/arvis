#!/usr/bin/python

from flask import Flask, request, jsonify
import requests

import arvis
app = Flask(__name__)


@app.route('/api/messages', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        incoming_json = request.get_json()
        if incoming_json and incoming_json['type'] == 'message':
            # prep response message
            reply = arvis.process_message(incoming_json['text'])

            return_json = {
                "type": "message",
                "from": {
                    "id": incoming_json['recipient']['id'],
                    "name": incoming_json['recipient']['name']
                },
                "conversation": {
                    "id": incoming_json['conversation']['id']
                },
                "recipient": {
                    "id": incoming_json['from']['id'],
                    "name": incoming_json['from']['name']
                },
                "text": reply,
                "replyToId": incoming_json['id']
            }
            url = incoming_json['serviceUrl'] + '/v3/conversations/' + incoming_json['conversation'][
                'id'] + '/activities/' + incoming_json['id']

            # send request
            if url and return_json:
                _ = requests.post(url, json=return_json)
            return jsonify({"id": incoming_json['conversation']['id']})
    return ''


if __name__ == "__main__":
    app.run(debug=True)
