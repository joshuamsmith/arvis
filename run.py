#!/usr/bin/python

from flask import Flask, request, jsonify

import arvis
app = Flask(__name__)


@app.route('/api/messages', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        incoming_json = request.get_json()
        if incoming_json and incoming_json['type'] == 'message':
            # prep response message
            _ = arvis.process_message(incoming_json)
            return jsonify({"id": incoming_json['conversation']['id']})
    return ''


if __name__ == "__main__":
    app.run(debug=True, port=6643)
