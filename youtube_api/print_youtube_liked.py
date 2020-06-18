"""
Print Youtube Liked Videos
Requires OAuth 2.0 to be set up via the googleapi console

Ethan Wright - 06/05/20
"""

import json
import requests
import os
import urllib.parse

from call_youtube_api import call_youtube_api, get_client_id_and_secret

token = 'ya29.a0AfH6SMBow9OfFLapK5dIJ6JXr2B-qHi_PHymM0eQ1JnaWssXRx_g1S7Bk7xS5DFeMrbU8PxsnoSwSemVU-BzEEnXuX0tsqnwp4LwAOAXr40HhfS4ekKxvFkTEGOgJdj5D7snhHpgzJo7ioOjkWMAJOpFNT4ELZl4Lvk'


def get_oauth_token():
    """
    Generates an authorization link that you must follow in a BROWSER.
    Consent to the terms, and it should generate the `access_token` as
    part of the url string after it tries and fails to redirect you.
    """
    oauth_endpoint = 'https://accounts.google.com/o/oauth2/auth'
    client_id, client_secret = get_client_id_and_secret()
    params = {
        'client_id': client_id,
        # 'client_secret': client_secret,
        'scope': 'https://www.googleapis.com/auth/youtube',
        'response_type': 'token',  # What does 'code' do?
        'redirect_uri': 'https://localhost'  # Does't really matter
    }
    encoded_url_params = urllib.parse.urlencode(params)
    exit(f'Go here:\n{oauth_endpoint}?{encoded_url_params}')


def get_liked_videos():
    video_ids = []
    results_per_page = 50

    url_base = 'https://www.googleapis.com/youtube/v3'
    api_endpoint = 'videos'
    params = {
        'part': 'snippet',
        'myRating': 'like',
        'maxResults': results_per_page,
        # 'accessToken': token  # TODO Needed?
    }

    while 'pageToken' not in params or params.get('pageToken'):
        headers = {'Authorization': f'Bearer {token}'}
        result = call_youtube_api(url_base, api_endpoint, params, headers=headers)
        import pdb;pdb.set_trace()
        for video in result.get('items', []):
            video_ids.append(video.get('id'))

        params['pageToken'] = result.get('nextPageToken')
        break
    return video_ids


def write_to_txt(video_ids):
    output_file = r'output\video_ids.txt'
    with open(output_file, 'w+') as out_file:
        for video_id in video_ids:
            out_file.write(video_id + '\n')


if __name__ == '__main__':
    # Need to get a new access_token every hour(?) or so
    # get_oauth_token()
    liked_video_ids = get_liked_videos()
    write_to_txt(liked_video_ids)
