"""
Print Youtube Playlist
https://developers.google.com/youtube/v3/docs/playlistItems/list
"""

import json
import os

from call_youtube_api import call_youtube_api, get_api_key

url_base = 'https://www.googleapis.com/youtube/v3'
youtube_video_url = r'https://www.youtube.com/watch?v='


def get_videos_by_playlist_id(playlist_id):
    api_endpoint = 'playlistItems'

    results_per_page = 50
    videos = []

    params = {
        'api_key': get_api_key(),
        'part': 'snippet',
        'playlistId': playlist_id,
        'maxResults': results_per_page,
    }
    while 'pageToken' not in params or params.get('pageToken'):

        result = call_youtube_api(url_base, api_endpoint, params)
        for video in result.get('items', []):
            snippet = video.get('snippet', {})
            videos.append((snippet.get('resourceId', {}).get('videoId', {}), snippet.get('title')))

        params['pageToken'] = result.get('nextPageToken')

    output_excel_format(videos)
    return


def get_upload_playlist_id(channel_name):
    api_endpoint = 'channels'

    params = {
        'part': 'contentDetails',
        'forUsername': channel_name,
    }

    result = call_youtube_api(url_base, api_endpoint, params)

    playlists = result.get('items')
    if len(playlists) > 0:
        return playlists[0].get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads', {})


def output_html_format(video_data):
    output_file = 'video_playlist_html.html'
    # TODO Format for HTML


def output_excel_format(video_data):
    output_file = r'output\video_playlist_excel.txt'
    with open(output_file, 'w+') as out_file:
        for video_id, title in video_data:
            link = youtube_video_url + video_id
            out_file.write("=HYPERLINK(\"%s\"; \"%s\")\n" % (link, title))


def run():
    channel_name = 'everyframeapainting'
    upload_playlist_id = get_upload_playlist_id(channel_name)
    get_videos_by_playlist_id(upload_playlist_id)


if __name__ == '__main__':
    run()
