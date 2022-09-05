"""
Execute calls to Youtube's API
Requires an API key to be available to the Credentials object

Ethan Wright - 6/11/20
"""
import requests

from credentials import Credentials

SLASH = '/'


def get_api_key():
    credentials = Credentials('youtube')
    return credentials.get('api_key')


def get_client_id_and_secret():
    credentials = Credentials('youtube')
    return credentials.get('client_id'), credentials.get('client_secret')


def call_youtube_api(url_base, api_endpoint, params, headers=None):

    api_endpoint = api_endpoint.replace(SLASH, '')
    if url_base[-1] != SLASH:
        url_base += SLASH

    response = requests.get(url_base + api_endpoint, params=params, headers=headers)

    if response.status_code == 200:
        result = response.json()
    else:
        #import pdb;pdb.set_trace()
        raise Exception(response.text)

    response.close()
    return result
