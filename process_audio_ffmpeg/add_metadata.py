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

from call_ffmpeg import call_ffmpeg
from paths import MUSIC_DIR


def add_metadata_from_file(directory, file_name):
    song_file_path = os.path.join(directory, file_name)
    # metadata_path_base = os.path.join(directory, 'metadata')
    metadata_path_base = directory
    metadata_input_path = os.path.join(metadata_path_base, file_name + '.txt')
    metadata_output_path = os.path.join(metadata_path_base, 'metadata_' + file_name + '.txt')

    file_data = open(metadata_input_path, 'r').readlines()
    parse_file_data_into_metadata_file(file_data, metadata_output_path)
    add_metadata(song_file_path, metadata_output_path)


def parse_file_data_into_metadata_file(input_data, output_file):
    if input_data[0].startswith(';FFMETADATA1'):
        return input_data
    track_data_list = []
    for track_data in input_data:
        start_time, end_time, title = parse_string(track_data)
        track_data_list.append((start_time, end_time, title))
    track_data_list.append((None, None, None))

    # for item in track_data_list:
    #     print(item)
    with io.open(output_file, 'wt', encoding='utf-8') as f:
        def ffmpeg_escape(text):
            return re.sub(r'(=|;|#|\\|\n)', r'\\\1', text)

        metadata_file_content = ';FFMETADATA1\n'
        for x in range(len(track_data_list) - 1):
            start, end, title = track_data_list[x]
            if not end:
                end = track_data_list[x + 1][0]
            metadata_file_content += '[CHAPTER]\nTIMEBASE=1/1000\n'
            metadata_file_content += 'START=%s\n' % str(start)
            metadata_file_content += 'END=%s\n' % str(end)
            metadata_file_content += 'title=%s\n' % ffmpeg_escape(title)
        f.write(metadata_file_content)


def parse_string(data_string):
    timestamps = extract_timestamps(data_string)
    milliseconds = convert_timestamp_to_milliseconds(timestamps[0])
    title = data_string.replace(timestamps[0], '')

    milliseconds2 = None
    if len(timestamps) == 2:
        milliseconds2 = convert_timestamp_to_milliseconds(timestamps[1])
        title = title.replace(timestamps[1], '')
    title = clean_title(title)

    return milliseconds, milliseconds2, title


def extract_timestamps(data_string):
    regex = '([0-9][0-9]?:[0-9][0-9])'
    return re.findall(regex, data_string)


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
    title = title.strip('-: \n')
    return title


def add_metadata(source_file_path, metadata_file_path):
    source_directory, source_file_name = source_file_path.rsplit('\\', 1)
    print(f'Adding metadata to File: {source_file_name}')
    output_path = os.path.join(source_directory, 'added_metadata_' + source_file_name)
    command = f'ffmpeg -i "{source_file_path}" -f ffmetadata -i "{metadata_file_path}" -c copy -map_metadata 1 "{output_path}"'
    # command = f'ffmpeg -i "{source_file_path}" -c copy -map_metadata -1 -fflags +bitexact -flags:a +bitexact "{output_path}"'
    print(command)
    result, stdout = call_ffmpeg(command)
    # print(result)
    # print(stdout)
    print('--- Done!\n')


def run(directory):
    directory = os.path.join(MUSIC_DIR, directory)

    files = os.listdir(directory)
    for file_name in files:
        if not os.path.isdir(os.path.join(directory, file_name)) and not file_name.startswith('added_metadata'):
            add_metadata_from_file(directory, file_name)


if __name__ == '__main__':
    input_subdirectory = r'post_rock\full_albums\to_listen_to\add_metadata'
    # input_subdirectory = r'post_rock\full_albums\liked\no_metadata'
    # input_subdirectory = r'post_rock\full_albums\liked_plus\no_metadata'
    run(input_subdirectory)
