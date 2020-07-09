import os

from common import list_music_files
from paths import MUSIC_DIR, MUSIC_SCRIPT_DIR

youtube_search_url = 'https://www.youtube.com/results'


def search_for_song(search_string):

    params = {
        'search_query': format_search_string(search_string),
    }

    # Query youtube
    response = requests.get(youtube_search_url, params=params)

    if response.status_code == 200:
        result = response.json()
    else:
        import pdb;pdb.set_trace()
        result = ''

    response.close()

    return result


def format_html_and_write_to_file(search_result_html, write_file):

    #
    # TODO Parse video HTML
    #

    for TODO in search_result_html:
        video_id = ''
        channel_name = ''
        video_title = ''.replace('&amp;', 'and').replace('&#39;', '\'')

        output_string = f'{video_id} {channel_name} | {video_title}'
        output_string_formatted = ''.join([char for char in output_string if 128 >= ord(char) >= 32 and char.isascii()]) + '\r\n'
        # results.append(output_string_formatted.encode('utf-8'))
        write_file.write(output_string_formatted.encode('utf-8'))


def format_search_string(search_string):
    formatted_string = search_string

    replace_list = [
        ('&', 'and'),
        ('?', ''), ('\'', ''),
        ('.mp3', ''), ('.ogg', ''),
    ]
    for find_val, replace_val in replace_list:
        formatted_string = formatted_string.replace(find_val, replace_val)

    return ''.join(filter(lambda x: ord(x) < 128, formatted_string)).strip()


def search_for_multiple_songs(song_list, output_file):
    with open(output_file, 'w') as write_file:
        for title in song_list:
            result_html = search_for_song(title)
            format_html_and_write_to_file(result_html, write_file)


def iterate_through_songs_in_file(input_file, output_file):
    with open(input_file, 'r') as read_file:
        data = read_file.readlines()
    search_for_multiple_songs(data, output_file)


def iterate_through_songs_in_directory(music_dir, output_file):
    search_for_multiple_songs(list_music_file_titles(music_dir), output_file)


def list_music_file_titles(directory):
    return [file_name.rsplit('.', 1)[0] for file_name in list_music_files(directory)]


def run_for_directory():
    output_file = 'songs_list_parsed.txt'

    sub_dir = r'liked'
    iterate_through_songs_in_directory(
        os.path.join(MUSIC_DIR, sub_dir),
        os.path.join(MUSIC_SCRIPT_DIR, output_file),
    )


def run_for_file():
    output_file = 'output\songs_list_parsed.txt'

    input_file = r'input\songs_list.txt'
    iterate_through_songs_in_file(
        os.path.join(MUSIC_SCRIPT_DIR, input_file),
        os.path.join(MUSIC_SCRIPT_DIR, output_file),
    )


if __name__ == '__main__':
    # run_for_directory()
    run_for_file()
