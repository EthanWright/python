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

from call_ffmpeg import call_ffmpeg
from music_file_scripts_common import list_music_files
from paths import Paths
from utils import SPACED_HYPHEN, get_track_data_from_file, convert_float_to_str_safe, extract_field_from_stdout


def parse_track_data_into_metadata(track_data_list):

    # base_num = 0  # Only for stupid formats
    metadata_file_content = ';FFMETADATA1\n'
    chapter_start = '[CHAPTER]\nTIMEBASE=1/1000\n'
    len_list = len(track_data_list)

    for x in range(len_list):
        track_data = track_data_list[x]
        start = track_data.get('start_timestamp')
        end = track_data.get('end_timestamp')
        title = track_data.get('title')

        # end = start + base_num  # Only for stupid formats
        # start = base_num  # Only for stupid formats
        # base_num = end  # Only for stupid formats

        if not end:
            if x < len_list - 1:
                end = track_data_list[x + 1].get('start')
            else:
                end = 100000000.0

        # TODO Did I need this?
        # start = convert_float_to_str_safe(start).rsplit('.', 1)[0]
        # end = convert_float_to_str_safe(end).rsplit('.', 1)[0]

        # print(f'{start}{SPACED_HYPHEN}{end} | {title}')
        metadata_file_content += f'{chapter_start}START={start}\nEND={end}\ntitle={title}\n'

    return metadata_file_content


def add_metadata_from_file(directory, file_name, remove_first=False, verbose=0, commit=False):

    song_file_path = os.path.join(directory, file_name)
    metadata_input_path = song_file_path + '.txt'
    metadata_output_path = song_file_path + '_metadata.txt'

    purl = None
    if remove_first:
        song_file_path, purl = remove_metadata(directory, file_name, verbose=verbose, commit=commit)

    track_data_list = get_track_data_from_file(metadata_input_path)

    metadata_file_content = parse_track_data_into_metadata(track_data_list)

    if metadata_file_content and commit:
        with io.open(metadata_output_path, 'wt', encoding='utf-8') as f:
            f.write(metadata_file_content)

    call_add_metadata(song_file_path, metadata_output_path, purl=purl, verbose=verbose, commit=commit)


def call_add_metadata(source_file_path, metadata_file_path, purl=None, verbose=0, commit=False):
    source_directory, source_file_name = os.path.split(source_file_path)
    print(f'Adding metadata to File: {source_file_name}')
    output_path = os.path.join(source_directory, 'added_metadata_' + source_file_name)

    command = [
        'ffmpeg',
        '-i', source_file_path,
        '-f', 'ffmetadata',
        '-i', metadata_file_path,
        '-c', 'copy',
        '-map_metadata', '1',
    ]
    if purl:
        command.extend(['-metadata', 'purl=' + purl])
    command.append(output_path)
    # windows_command = ' '.join(command)

    result, stdout = call_ffmpeg(command, verbose=verbose, commit=commit)


def remove_metadata(source_directory, source_file_name, verbose=0, commit=False):
    print(f'Removing metadata from File: {source_file_name}')
    source_file_path = os.path.join(source_directory, source_file_name)
    output_file_name = 'removed_metadata_' + source_file_name
    output_path = os.path.join(source_directory, output_file_name)
    # Remove ALL metadata
    # command = f'ffmpeg -i "{source_file_path}" -c copy -map_metadata -1 -fflags +bitexact -flags:a +bitexact "{output_path}"'
    command = [
        'ffmpeg',
        '-i', source_file_path,
        '-c', 'copy',
        '-map_metadata', '-1',
        '-fflags', '+bitexact',
        '-flags:a', '+bitexact',
        output_path
    ]
    result, stdout = call_ffmpeg(command, verbose=verbose, commit=commit)
    purl = 'No PURL!'
    if stdout:
        purl = extract_field_from_stdout(stdout, 'purl')

    return output_path, purl


def run(sub_directory, verbose=0, commit=False, remove_first=False):
    directory = os.path.join(Paths.MUSIC, sub_directory)
    for file_name in list_music_files(directory):
        if not (file_name.startswith('added_metadata') or file_name.startswith('removed_metadata')):
            add_metadata_from_file(directory, file_name, remove_first=remove_first, verbose=verbose, commit=commit)


if __name__ == '__main__':
    default_path = Paths.NEEDS_METADATA

    parser = argparse.ArgumentParser(description='Add Metadata to Song Files')
    parser.add_argument('directory', nargs='?', default=default_path, help='Target Directory')
    parser.add_argument('--commit', action='store_true', help='Rename Files')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    parser.add_argument('--remove-first', action='store_true', help='Remove ALL metadata')

    args = parser.parse_args()
    run(args.directory, args.verbose, args.commit, remove_first=args.remove_first)

"""
python add_metadata.py
"""
