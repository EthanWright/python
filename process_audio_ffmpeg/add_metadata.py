"""
Use ffmpeg CLI commands to add metadata to a song
The metadata should be supplied in a txt file named
the same name as the song file + '.txt'

Expected format of metadata is:
;FFMETADATA1
[CHAPTER]
TIMEBASE=1/1000
START=0
END=274000
title=On Fire
[CHAPTER]
...

With each [CHAPTER] delineating track info.
Timestamps are in milliseconds (?)

Ethan Wright - 6/11/20
"""

import io
import os
import re

from call_ffmpeg import call_ffmpeg, get_metadata
from paths import MUSIC_DIR


def add_metadata_from_file(directory, file_name):
    song_file_path = os.path.join(directory, file_name)
    metadata_path_base = os.path.join(directory, 'metadata')
    metadata_input_path = os.path.join(metadata_path_base, file_name + '.txt')
    metadata_output_path = os.path.join(metadata_path_base, 'metadata_' + file_name + '.txt')

    file_data = open(metadata_input_path, 'r').readlines()
    parse_file_data_into_metadata_file(file_data, metadata_output_path)
    add_metadata(song_file_path, metadata_output_path)


def parse_file_data_into_metadata_file(input_data, output_file):
    track_data_list = []
    for track_data in input_data:
        start_time, title = parse_string(track_data)
        track_data_list.append((start_time, title))
    track_data_list.append(('eof', None))
    for item in track_data_list:
        print(item)
    # import pdb;pdb.set_trace()
    with io.open(output_file, 'wt', encoding='utf-8') as f:
        def ffmpeg_escape(text):
            return re.sub(r'(=|;|#|\\|\n)', r'\\\1', text)

        metadata_file_content = ';FFMETADATA1\n'
        for x in range(len(track_data_list) - 1):
            start, title = track_data_list[x]
            metadata_file_content += '[CHAPTER]\nTIMEBASE=1/1000\n'
            metadata_file_content += 'START=%s\n' % str(start)
            metadata_file_content += 'END=%s\n' % str(track_data_list[x + 1][0])
            metadata_file_content += 'title=%s\n' % ffmpeg_escape(track_data_list[x][1])
        f.write(metadata_file_content)


def parse_string(data_string):
    timestamp = extract_timestamp(data_string)
    if not timestamp:
        import pdb;pdb.set_trace()
    title = data_string.replace(timestamp, '')
    title = clean_title(title)
    milliseconds = convert_timestamp_to_milliseconds(timestamp)
    return milliseconds, title


def extract_timestamp(data_string):
    regex = '([0-9][0-9]?:[0-9][0-9])'
    result = re.search(regex, data_string)
    if result:
        return result.group(1)


def convert_timestamp_to_milliseconds(timestamp):
    minutes, seconds = timestamp.split(':')
    return (int(minutes) * 60 + int(seconds)) * 1000


def clean_title(title):

    # Remove Track Title Prefixes ('1.' or '01.')
    if re.match(r'[0-9][0-9]?\..*', title):
        title = title.split('.', 1)[1].strip()

    # Remove characters that mess with ffmpeg cli commands
    bad_chars = '?"`#*<>|\'\\'
    for char in bad_chars:
        title = title.replace(char, '')
    title = title.replace('/', ' ')
    title = title.strip(': \n')
    return title


def add_metadata(source_file_path, metadata_file_path):
    source_directory, source_file_name = source_file_path.rsplit('\\', 1)
    print(f'Adding metadata to File: {source_file_name}')
    output_path = os.path.join(source_directory, 'added_metadata_' + source_file_name)
    command = f'ffmpeg -i "{source_file_path}" -f ffmetadata -i "{metadata_file_path}" -c copy -map_metadata 1 "{output_path}"'
    print(command)
    call_ffmpeg(command)
    print('--- Done!\n')


def run(directory):
    directory = os.path.join(MUSIC_DIR, directory)

    files = os.listdir(directory)
    for file_name in files:
        if not os.path.isdir(os.path.join(directory, file_name)) and not file_name.startswith('added_metadata'):
            add_metadata_from_file(directory, file_name)


if __name__ == '__main__':
    input_subdirectory = r'post_rock\full_albums\to_listen_to\no_metadata'
    # input_subdirectory = r'post_rock\full_albums\liked\no_metadata'
    # input_subdirectory = r'post_rock\full_albums\liked_plus\no_metadata'
    run(input_subdirectory)
