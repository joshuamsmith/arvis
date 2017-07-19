#!/usr/bin/python
import requests
import time

import config

###
# This module handles the authentication between the bot and MSA/AAD v2 login service
# Built from: https://docs.microsoft.com/en-us/bot-framework/rest-api/bot-framework-rest-connector-authentication
##

auth_header = None
timeout = time.time()


# Authenticate requests from your bot to the Bot Connector service
def return_auth_header():
    global auth_header, timeout

    # Step 0: Check if last auth token is still valid
    # TODO: check timeout value against current time, if still fresh return previous header
    # if timeout > time.time(): return auth_header ELSE print('Refreshing Auth Token')

    # Step 1: Request an access token from the MSA/AAD v2 login service
    microsoft_app_id = config.app_id
    microsoft_app_pass = config.app_pass
    post_url = 'https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token'
    host = 'login.microsoftonline.com'
    content_type = 'application/x-www-form-urlencoded'
    token_request = 'grant_type=client_credentials&client_id={}&client_secret={}&' \
                    'scope=https%3A%2F%2Fapi.botframework.com%2F.default'.format(microsoft_app_id, microsoft_app_pass)
    headers = {'Content-Type': content_type, 'Host': host}
    r = requests.post(post_url, data=token_request, headers=headers)

    # Step 2: Obtain the JWT token from the MSA/AAD v2 login service response
    # TODO: handle errors
    if r.status_code == requests.codes.ok:
        token_response = r.json()

    # Step 3: Specify the JWT token in the Authorization header of requests
    auth_header = {'Authorization': '{} {}'.format(token_response['token_type'], token_response['access_token'])}

    if __name__ != '__main__':
        timeout += token_response['expires_in']
        return auth_header
    else:
        print(timeout)
        print(token_response)
        print(timeout + token_response['expires_in'])
        # print(k + ': ' + v for k, v in token_response)

# Authenticate requests from the Bot Connector service to your bot

# Step 2: Get the OpenID metadata document

# Step 3: Get the list of valid signing keys

# Step 4: Verify the JWT token

# Authenticate requests from the Bot Framework Emulator to your bot

# Step 2: Get the MSA OpenID metadata document

# Step 3: Get the list of valid signing keys

# Step 4: Verify the JWT token

if __name__ == '__main__':
    return_auth_header()
