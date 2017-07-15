#!/usr/bin/python

from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)


@app.route('/api/messages', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        # print(request.headers)
        incoming_json = request.get_json()
        print(incoming_json['type'])
    message = ''
    # return generic message
    if incoming_json and incoming_json['type'] == 'message':
        # prep response message

        text = incoming_json['text']
        if text.isdigit() and int(text) in range(1, 5):
            # test REST site
            test_url = "https://jsonplaceholder.typicode.com/posts/1/comments?id=" + text
            r = requests.get(test_url)
            text = json.loads(r.text)[0]
            # print(text['email'])
            message = incoming_json['text'] + '\'s email is ' + text['email']
        else:
            message = text + ', really?'
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
            "text": message,
            "replyToId": incoming_json['id']
        }
        url = incoming_json['serviceUrl'] + '/v3/conversations/' + incoming_json['conversation'][
            'id'] + '/activities/' + incoming_json['id']

        # send request
        _ = requests.post(url, json=return_json)
        return jsonify({"id": incoming_json['conversation']['id']})
    return message


if __name__ == "__main__":
    app.run(debug=True)
