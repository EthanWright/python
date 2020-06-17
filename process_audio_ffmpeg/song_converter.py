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
from paths import MUSIC_DIR


def run(file_path):
    metadata, stdout_data = get_metadata(file_path)
    title = parse_metadata_for_field(metadata, 'title').strip()
    convert_file_to_opus(file_path, title)


def parse_metadata_for_field(metadata, field):
    search_string = field + '='
    for line in metadata.split('\n'):
        line_clean = line.strip()
        if line_clean.startswith(search_string):
            return line_clean.replace(search_string, '')
    return None


def convert_file_to_opus(source_file_path, new_name):

    source_directory, source_file_name = source_file_path.rsplit('\\', 1)
    new_file_name = new_name + '.opus'
    output_path = os.path.join(source_directory, new_file_name)

    command = f'ffmpeg -i "{source_file_path}" -c:a libopus -b:a 48000 "{output_path}"'
    # command = f'ffmpeg -i "{source_file_path}" -c:a libopus -b:a 320000 "{output_path}"'
    print('Running command:\n' + command)
    result, stdout = call_ffmpeg(command)

    return result


if __name__ == '__main__':

    input_subdirectory = r'post_rock\to_sort\original'
    directory = os.path.join(MUSIC_DIR, input_subdirectory)
    # files = os.listdir(directory)
    # for file_name in files:
    run(os.path.join(directory, file_name))
