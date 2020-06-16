"""
Execute calls to Youtube's API
Requires an API key to be available to the Credentials object

Ethan Wright - 6/11/20
"""
import requests

from credentials import Credentials

SLASH = '/'


def call_youtube_api(url_base, api_endpoint, params, headers=None):
    # Add API key
    credentials = Credentials('youtube')
    params['key'] = credentials.get('api_key')

    api_endpoint = api_endpoint.replace(SLASH, '')
    if url_base[-1] != SLASH:
        url_base += SLASH

    response = requests.get(url_base + api_endpoint, params=params, headers=headers)

    if response.status_code == 200:
        result = response.json()
    else:
        import pdb;pdb.set_trace()
        result = ''

    response.close()
    return result
