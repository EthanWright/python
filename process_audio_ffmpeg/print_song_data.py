"""
Use ffmpeg CLI commands to print song data

Ethan Wright - 6/11/20
"""

import argparse
import io
import os
import re

from call_ffmpeg import call_ffmpeg, get_metadata
from common import list_music_files
from paths import MUSIC_DIR, POST_ROCK_TO_SORT_DIR, POST_ROCK_DUPES_DIR

MEGA = 1024 * 1024


class Output(object):
    def __init__(self, write_file_name=None):
        self.write_to_file = False
        if write_file_name:
            if not os.path.exists(write_file_name):
                self.write_to_file = True
                self.write_file = open(write_file_name, 'w')
            else:
                print('FILE EXISTS\n')

    def output(self, data):
        if self.write_to_file:
            self.write_file.write(data)
        else:
            print(data)


def format_metadata(metadata):
    return_list = []
    for chapter in metadata.split('[CHAPTER]'):
        regex = 'START=([0-9]+)\nEND=([0-9]+)\ntitle=(.+)\n'
        result = re.search(regex, chapter)
        if result:
            data = result.groups()

            if len(data) == 3:
                start_time_value = float(data[0].strip()) / 1000.0
                end_time_value = float(data[1].strip()) / 1000.0
                title = data[2].strip()

                start_timestamp = format_time_value(start_time_value)
                end_timestamp = format_time_value(end_time_value)

                return_list.append(f'{title} {start_timestamp} - {end_timestamp}')

    return '\n'.join(return_list)


def format_time_value(time_value):
    timestamp_minutes = int(time_value / 60)
    timestamp_seconds = time_value % 60

    timestamp_seconds_int = int(timestamp_seconds)
    timestamp_seconds_str = str(timestamp_seconds_int)
    if timestamp_seconds_int < 10:
        timestamp_seconds_str = '0' + timestamp_seconds_str

    # TODO Is this wise?
    # timestamp_seconds_decimal = timestamp_seconds - float(timestamp_seconds_int)
    # if timestamp_seconds_decimal:
    #     timestamp_seconds_str = timestamp_seconds_str + '.' + str(timestamp_seconds_decimal)[2:5]

    return f'{timestamp_minutes}:{timestamp_seconds_str}'


def print_song_data(directory, file_name, export_metadata=False):
    source_file_path = os.path.join(directory, file_name)
    metadata, stdout = get_metadata(source_file_path)
    if export_metadata:
        formatted_metadata = format_metadata(metadata)
        printer = Output(source_file_path + '.txt')
        printer.output(formatted_metadata)
    print_data_from_stdout(stdout)
    print_file_size(source_file_path)
    print('---')


def print_file_size(source_file_path):
    size = str(os.path.getsize(source_file_path) / MEGA)
    integer_digits, decimal_digits = size.split('.')
    print(f'File Size: {integer_digits}.{decimal_digits[:2]} MB')


def print_data_from_stdout(stdout):
    prepared_for_data = False

    for line in stdout.split('\n'):
        line_clean = line.strip()

        if line_clean.startswith('Output #0,'):
            return
        if line_clean.startswith('Input #0,'):
            file_name = line_clean.rsplit('\\', 1)[1]
            if file_name.endswith('\':'):
                file_name = file_name[:-2]
            print(file_name)
            prepared_for_data = True
            continue

        if prepared_for_data and line_clean.startswith('purl'):
            print(line_clean.rsplit(' ', 1)[1])

        if prepared_for_data and line_clean.startswith('Duration'):
            # 'Duration: 00:07:11.02, start: 0.019000, bitrate: 130 kb/s'
            # regex = r'Duration: (([0-9]{2}:){2}([0-9]{2}[\.]?){2}), start: ([0-9]\.[0-9]+), bitrate: ([0-9]{2,3}) kb/s'
            regex = r'Duration: ([0-9:\.]+), start: -?([0-9]\.[0-9]+), bitrate: ([0-9]{2,3}) kb/s'
            search = re.search(regex, line_clean)
            if search:
                length, start, bitrate = search.groups()
                print(f'Length: {length} Bitrate: {bitrate}')
            else:
                raise Exception(f'Problem with input: {line_clean}')


def run(input_directory, export_metadata=False):
    directory = os.path.join(MUSIC_DIR, input_directory)
    for file_name in list_music_files(directory):
        print_song_data(directory, file_name, export_metadata=export_metadata)


if __name__ == '__main__':
    default_path = POST_ROCK_DUPES_DIR
    parser = argparse.ArgumentParser(description='Print Audio/Video file details')
    parser.add_argument('directory', nargs='?', default=default_path, help='Target Directory')
    # parser.add_argument('--commit', action='store_true', help='Rename Files')
    # parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    parser.add_argument('--export-metadata', action='store_true', help='Export Track metadata to a file')

    args = parser.parse_args()
    run(args.directory, export_metadata=args.export_metadata)

"""
python print_song_data.py
"""