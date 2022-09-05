"""
= Youtube Search Using API =
Iterate through songs in saved folder or a list
Search Youtube for the song
Can also search a specific Channel

This API is rate limited, for large amounts of songs,
just call the standard youtube search with HTTP GET

https://developers.google.com/youtube/v3/docs/
"""

import json
import os

from call_youtube_api import call_youtube_api, get_api_key
from paths import MUSIC_DIR, PYTHON_DIR

api_base = 'https://www.googleapis.com/youtube/v3'


# Search using youtube's built in search with HTTP GET
def search_for_song_http(song_name):

    search_url = 'https://www.youtube.com/results?search_query=' + song_name
    out_file_name = os.path.join(PYTHON_DIR, 'youtube_api', 'output', 'search_queries.html')

    with open(out_file_name, 'a') as out_file:
        out_file.write('<a href="' + search_url + '">' + song_name + '</a><br>\r\n')

    # TODO Perform the youtube search request and parse the results
    # result = call_youtube_http(search_url)
    # write_results_to_file(title, result.get('items', []))


def search_for_song(song_name, channel_id=None):
    api_endpoint = 'search'
    params = {
        'key': get_api_key(),
        'q': song_name,
        'part': 'snippet',
    }
    if channel_id:
        params['channelId'] = channel_id

    result = call_youtube_api(api_base, api_endpoint, params)
    title = ''  # TODO
    write_results_to_file(title, result.get('items', []))


def format_search_result(search_result):
    video_id = search_result.get('id', {}).get('videoId')
    if not video_id:
        return ''

    snippet = search_result.get('snippet', {})
    channel_name = snippet.get('channelTitle', '')
    video_title = snippet.get('title', '').replace('&amp;', 'and').replace('&#39;', '\'')

    output_string = f'{video_id} | {channel_name} | {video_title}'
    output_string_formatted = ''.join([char for char in output_string if 128 >= ord(char) >= 32 and char.isascii()]) + '\r\n'

    return output_string_formatted.encode('utf-8')


def write_results_to_file(query_string, search_results):
    query_string = 'Search Query: "' + query_string.strip() + '"\r\n'
    out_file_name = os.path.join(PYTHON_DIR, 'youtube_api', 'output', 'search_results.txt')

    with open(out_file_name, 'ab+') as out_file:
        out_file.write(query_string.encode('utf-8'))
        for search_result in search_results:
            output_string_formatted = format_search_result(search_result)
            if output_string_formatted:
                out_file.write(output_string_formatted)

        out_file.write('\r\n'.encode('utf-8'))


def iterate_through_songs_in_file(input_file):
    with open(input_file, 'r') as read_file:
        data = read_file.readlines()
    for song_name in data:
        #song_name = os.path.splitext(file_name)[0].strip()
        #search_for_song(song_name.strip())
        search_for_song_http(song_name.strip())


def iterate_through_song_files_in_directory(music_dir):
    for file_name in list_music_files(music_dir):
        search_for_song(file_name)


def list_music_files(directory):
    files = [file_name for file_name in os.listdir(directory) if os.path.isfile(os.path.join(directory, file_name))]
    return [file_name for file_name in files if file_name.rsplit('.', 1)[-1] not in ['jpg', 'txt']]


if __name__ == '__main__':
    music_file = os.path.join(PYTHON_DIR, 'youtube_api', 'input', 'songs_list.txt')
    iterate_through_songs_in_file(music_file)

    # Use song files in dir on computer
    # music_dir = os.path.join(MUSIC_DIR, r'to_sort\to_sort_old')
    # iterate_through_song_files_in_directory(music_dir)

