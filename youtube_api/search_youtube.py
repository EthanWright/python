"""
= Youtube Search Using API =
Iterate through songs in saved folder
Search Youtube for the song
Can also search a specific Channel

Why use an API call to do this?
This API is rate limited, use standard HTTP GET instead lol

https://developers.google.com/youtube/v3/docs/
"""

import json
import os

from call_youtube_api import call_youtube_api
from paths import MUSIC_DIR

url_prefix = 'https://www.googleapis.com/youtube/v3'


def search_for_song(file_name, channel_id=None):
    title = os.path.splitext(file_name)[0]
    params = {
        'q': title,
        'part': 'snippet',
    }
    if channel_id:
        params['channelId'] = channel_id

    result = call_youtube_api(url_base, api_endpoint, params)

    write_results_to_file(result.get('items', []))


def format_search_result(search_result):
    video_id = search_result.get('id', {}).get('videoId')
    if not video_id:
        return ''

    snippet = search_result.get('snippet', {})
    channel_name = snippet.get('channelTitle', '')
    video_title = snippet.get('title', '').replace('&amp;', 'and').replace('&#39;', '\'')

    output_string = f'{video_id} {channel_name} | {video_title}'
    output_string_formatted = ''.join([char for char in output_string if 128 >= ord(char) >= 32 and char.isascii()]) + '\r\n'

    return output_string_formatted.encode('utf-8')


def write_results_to_file(search_results):

    with open('search_results.txt', 'ab+') as out_file:
        for search_result in search_results:
            output_string_formatted = format_search_result(search_result)
            if output_string_formatted:
                out_file.write(output_string_formatted)

        out_file.write('\r\n'.encode('utf-8'))


def iterate_through_song_files_on_computer(music_dir):
    for file_name in list_music_files(music_dir):
        search_for_song(file_name)


def list_music_files(directory):
    files = [file_name for file_name in os.listdir(directory) if os.path.isfile(os.path.join(directory, file_name))]
    return [file_name for file_name in files if file_name.rsplit('.', 1)[-1] not in ['jpg', 'txt']]


if __name__ == '__main__':
    sub_dir = r'to_sort\to_sort_old'
    # sub_dir = r'liked\missing'
    music_dir = os.path.join(MUSIC_DIR, sub_dir)

    iterate_through_song_files_on_computer(music_dir)
    # sheepy_channel_id = 'UC5nc_ZtjKW1htCVZVRxlQAQ'
