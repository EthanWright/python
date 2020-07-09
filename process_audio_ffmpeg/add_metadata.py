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

import argparse
import io
import os
import re

from call_ffmpeg import call_ffmpeg
from common import list_music_files, clean_file_name
from paths import MUSIC_DIR, POST_ROCK_FULL_ALBUMS_DIR


# Parsing Functions
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

        metadata_file_content = ';FFMETADATA1\n'
        for x in range(len(track_data_list) - 1):
            start, end, title = track_data_list[x]
            if not end:
                end = track_data_list[x + 1][0]
            metadata_file_content += '[CHAPTER]\nTIMEBASE=1/1000\n'
            metadata_file_content += 'START=%s\n' % str(start)
            metadata_file_content += 'END=%s\n' % str(end)
            metadata_file_content += 'title=%s\n' % title  # ffmpeg_escape(title)
        f.write(metadata_file_content)


def parse_string(data_string):
    timestamps = extract_timestamps(data_string)
    milliseconds = convert_timestamp_to_milliseconds(timestamps[0])
    title = data_string.replace(timestamps[0], '')

    milliseconds2 = None
    if len(timestamps) == 2:
        milliseconds2 = convert_timestamp_to_milliseconds(timestamps[1])
        title = title.replace(timestamps[1], '')

    title = clean_file_name(title)  # TODO Too strict?

    return milliseconds, milliseconds2, title


def extract_timestamps(data_string):
    regex = r'([0-9]{1,3}:[0-9][0-9]\.?[0-9]*)'
    return re.findall(regex, data_string)


def convert_timestamp_to_milliseconds(timestamp):
    minutes, seconds = timestamp.split(':')
    return (float(minutes) * 60.0 + float(seconds)) * 1000.0


def add_metadata_from_file(directory, file_name, remove_first=False, verbose=0, commit=False):

    song_file_path = os.path.join(directory, file_name)
    metadata_input_path = song_file_path + '.txt'
    metadata_output_path = song_file_path + '_metadata.txt'

    purl = None
    if remove_first:
        song_file_path, purl = remove_metadata(directory, file_name, verbose=verbose, commit=commit)

    file_data = open(metadata_input_path, 'r').readlines()
    parse_file_data_into_metadata_file(file_data, metadata_output_path)

    add_metadata(song_file_path, metadata_output_path, purl=purl, verbose=verbose, commit=commit)


def add_metadata(source_file_path, metadata_file_path, purl=None, verbose=0, commit=False):
    source_directory, source_file_name = source_file_path.rsplit('\\', 1)
    print(f'Adding metadata to File: {source_file_name}')
    output_path = os.path.join(source_directory, 'added_metadata_' + source_file_name)

    cli_options = [
        ('-i', '"' + source_file_path + '"'),
        ('-f', 'ffmetadata'),
        ('-i', '"' + metadata_file_path + '"'),
        ('-c', 'copy'),
        ('-map_metadata', '1'),
    ]
    if purl:
        cli_options.append(('-metadata', f'purl={purl}'))

    cli_options_string = ' '.join([flag + ' ' + value for flag, value in cli_options])
    command = f'ffmpeg {cli_options_string} "{output_path}"'
    # command = f'ffmpeg -i "{source_file_path}" -f ffmetadata -i "{metadata_file_path}" -c copy -map_metadata 1 -metadata purl={purl} "{output_path}"'
    call_ffmpeg(command, verbose=verbose, commit=commit)


def remove_metadata(source_directory, source_file_name, verbose=0, commit=False):
    print(f'Removing metadata from File: {source_file_name}')
    source_file_path = os.path.join(source_directory, source_file_name)
    output_file_name = 'removed_metadata_' + source_file_name
    output_path = os.path.join(source_directory, output_file_name)
    # Remove ALL metadata
    command = f'ffmpeg -i "{source_file_path}" -c copy -map_metadata -1 -fflags +bitexact -flags:a +bitexact "{output_path}"'
    result, stdout = call_ffmpeg(command, verbose=verbose, commit=commit)
    purl = 'No PURL!'
    if stdout:
        purl = extract_field_from_stdout(stdout, 'purl')

    return output_path, purl


def extract_field_from_stdout(stdout, stdout_field):
    for line in stdout.split('\n'):
        line_clean = line.strip()
        if stdout_field in line_clean:
            return line_clean.rsplit(' ', 1)[1]


def run(sub_directory, verbose=0, commit=False, remove_first=False):
    directory = os.path.join(MUSIC_DIR, sub_directory)
    for file_name in list_music_files(directory):
        if not (file_name.startswith('added_metadata') or file_name.startswith('removed_metadata')):
            add_metadata_from_file(directory, file_name, remove_first=remove_first, verbose=verbose, commit=commit)


if __name__ == '__main__':
    default_path = os.path.join(POST_ROCK_FULL_ALBUMS_DIR, 'needs_metadata')

    parser = argparse.ArgumentParser(description='Add Metadata to Song Files')
    parser.add_argument('directory', nargs='?', default=default_path, help='Target Directory')
    parser.add_argument('--commit', action='store_true', help='Rename Files')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    parser.add_argument('--remove-first', action='store_true', help='Remove ALL metadata')

    args = parser.parse_args()
    run(args.directory, args.verbose, args.commit, remove_first=args.remove_first)

r"""
python add_metadata.py
"""