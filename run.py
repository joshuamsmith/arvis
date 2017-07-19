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
            reply = arvis.process_message(incoming_json)

            # send request
            if isinstance(reply, dict) and 'url' in reply.keys() and 'json' in reply.keys():
                _ = requests.post(reply['url'], json=reply['json'])
            return jsonify({"id": incoming_json['conversation']['id']})
    return ''


if __name__ == "__main__":
    app.run(debug=True)
