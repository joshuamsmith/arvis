#!/usr/bin/python
import re
import requests

import auth
import connectwise


def process_message(incoming_json):
    message = None

    # Did someone mention an SR#?
    search_obj = re.search(r'(\d{6,})', incoming_json['text'])
    if search_obj:
        # Lookup and return SR# details if found
        message = connectwise.return_sr_summary(search_obj.group(1))

    # Did they do something else? Look for it in the TEXT value
    # search_obj = re.search(r'(FOO)', incoming_json['text'])
    # if search_obj:
    #   message = connectwise.????(search_obj.group(1))

    if message:
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

        reply = {'json': return_json, 'url': url}
        # send request
        if isinstance(reply, dict) and 'url' in reply.keys() and 'json' in reply.keys():
            headers = auth.return_auth_header()
            _ = requests.post(reply['url'], headers=headers, json=reply['json'])
    else:
        reply = 'Error: unsure how to handle.'

    return reply

