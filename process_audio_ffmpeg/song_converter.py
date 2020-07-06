"""
Use ffmpeg CLI commands to convert audio files
Only converts to opus right now

TODO
Configurable bitrate

Ethan Wright 6/10/20
"""
import os
import re

from call_ffmpeg import call_ffmpeg, get_metadata
from common import list_music_files
from paths import MUSIC_DIR, POST_ROCK_TO_SORT_DIR, POST_ROCK_FULL_ALBUMS_DIR


def run(file_path, commit=False):
    metadata, stdout_data = get_metadata(file_path)
    title = parse_metadata_for_field(metadata, 'title')
    if not title:
        title = file_path.rsplit('\\', 1)[1].rsplit('.', 1)[0]
    convert_file_to_opus(file_path, title, commit=commit)


def parse_metadata_for_field(metadata, field):
    search_string = field + '='
    for line in metadata.split('\n'):
        line_clean = line.strip()
        if line_clean.startswith(search_string):
            return line_clean.replace(search_string, '').strip()
    return None


def convert_file_to_opus(source_file_path, new_name, commit=False):

    source_directory, source_file_name = source_file_path.rsplit('\\', 1)
    new_file_name = new_name + '.opus'
    output_path = os.path.join(source_directory, new_file_name)

    command = f'ffmpeg -i "{source_file_path}" -c:a libopus -b:a 48000 "{output_path}"'
    # command = f'ffmpeg -i "{source_file_path}" -c:a libopus -b:a 320000 "{output_path}"'
    print('Running command:\n' + command)
    result, stdout = call_ffmpeg(command, commit=commit)

    return result


if __name__ == '__main__':

    # directory = POST_ROCK_TO_SORT_DIR
    # directory = POST_ROCK_FULL_ALBUMS_DIR
    # file_name = r''

    commit = False

    for file_name in list_music_files(directory):
        run(os.path.join(directory, file_name), commit=commit)
