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

    # Let people assign themselves tickets: @arvis !assignme ticket #123456
    # search_obj = re.search(r'!assignme .* #(\d{6,})', incoming_json['text'])
    # if search_obj:
    #     message = connectwise.assign_sr(search_obj.group(1))
        '''
        team_member_email = get_team_members_email(message_from)
        member = connectwise.get_member_by_email(team_member_email)
        assign_sr(ticket_id, member.identifier)
        '''

    # Get Team ID
    search_obj = re.search(r'(!team)', incoming_json['text'])
    if search_obj:
        team_id = incoming_json['channelData']['team']['id']
        from_name = incoming_json['from']['name']
        print('Team ', team_id)
        print('User ', from_name)

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
