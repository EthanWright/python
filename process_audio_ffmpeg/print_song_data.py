"""
Use ffmpeg CLI commands to print song data

Ethan Wright - 6/11/20
"""

import argparse
import io
import os
import re

from call_ffmpeg import call_ffmpeg, get_metadata
from file_scripts_common import list_music_files
from paths import Paths
from utils import get_track_data_from_metadata, format_into_timestamp, convert_float_to_str_safe

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


def format_track_data(track_data):
    return_data = ''
    for item in track_data:
        start_timestamp = format_into_timestamp(item.get('start_timestamp'))
        end_timestamp = format_into_timestamp(item.get('end_timestamp'))
        title = item.get('title')
        return_data += f'{title} {start_timestamp} - {end_timestamp}\n'

    return return_data


def print_song_data(directory, file_name, export_metadata=False):
    source_file_path = os.path.join(directory, file_name)
    metadata, stdout = get_metadata(source_file_path)

    # Write data to file
    if export_metadata:
        track_data = get_track_data_from_metadata(metadata)
        formatted_track_data = format_track_data(track_data)
        printer = Output(source_file_path + '.txt')
        printer.output(formatted_track_data)

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
            file_name = os.path.split(line_clean)[1]
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


def run(directory, export_metadata=False):
    for file_name in list_music_files(directory):
        print_song_data(directory, file_name, export_metadata=export_metadata)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print Audio/Video file details')
    parser.add_argument('directory', nargs='?', help='Target Directory')
    parser.add_argument('--dupes', '-d', action='store_true', default=False, help='Renaming Albums')
    parser.add_argument('--needs-metadata', '-n', action='store_true', default=False, help='Renaming Songs')
    parser.add_argument('--export-metadata', action='store_true', help='Export Track metadata to a file')
    # parser.add_argument('--commit', action='store_true', help='Commit')
    # parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    args = parser.parse_args()

    if args.dupes:
        music_directory = Paths.DUPES
    elif args.needs_metadata:
        music_directory = Paths.NEEDS_METADATA
    elif args.directory:
        music_directory = args.directory
    else:  # Default
        music_directory = Paths.DUPES

    run(music_directory, export_metadata=args.export_metadata)

"""
python print_song_data.py
python print_song_data.py --needs-metadata --export-metadata
"""
