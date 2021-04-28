"""
Use ffmpeg CLI commands to split songs based on their chapter metadata

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

Ethan Wright 6/15/20
"""
import argparse
import os
import re

from call_ffmpeg import call_ffmpeg, get_metadata
from file_scripts_common import list_music_files
from paths import Paths
from utils import (
    SPACED_HYPHEN,
    get_track_data_from_metadata, get_track_data_from_file,
    extract_field_from_stdout, convert_float_to_str_safe
)


class SongSplitter(object):

    def __init__(
        self,
        album_done_dir=None,
        song_output_dir=None,
        album_error_dir=None,
        verbose=0, commit=False
    ):
        self.song_output_dir = song_output_dir
        self.album_error_dir = album_error_dir
        self.album_done_dir = album_done_dir
        self.verbose = verbose
        self.commit = commit

    def split_songs_in_directory(self, directory, split_using_file=False):
        for file_name in list_music_files(directory):
            self.call_split_file(directory, file_name, split_using_file)

    def call_split_file(self, directory, file_name, split_using_file):

        full_path = os.path.join(directory, file_name)
        metadata, stdout = get_metadata(full_path, verbose=-1)
        purl = extract_field_from_stdout(stdout, 'purl', default_return='')

        if split_using_file:
            track_data = get_track_data_from_file(full_path + '.txt')
        else:
            track_data = get_track_data_from_metadata(metadata)

        if len(track_data) == 0:
            return move_to_subdir(full_path, file_name, self.album_error_dir, commit=self.commit, print_error_msg=True)

        split_file(
            full_path, file_name, track_data, purl,
            output_directory=self.song_output_dir, verbose=self.verbose, commit=self.commit
        )
        move_to_subdir(full_path, file_name, self.album_done_dir, commit=self.commit)


def move_to_subdir(source_file_path, file_name, output_directory, commit=False, print_error_msg=False):
    if print_error_msg:
        print(f'Can not split file. Marking as error: {source_file_path}')
    target_file_path = os.path.join(output_directory, file_name)
    if commit:
        os.rename(source_file_path, target_file_path)


def format_timestamp(_timestamp):

    if not isinstance(_timestamp, float):
        _timestamp = float(_timestamp)

    return convert_float_to_str_safe(_timestamp / 1000.0)


def split_file(source_file_path, source_file_name, track_data, purl, output_directory=None, verbose=0, commit=False):

    if not output_directory:
        output_directory = os.path.split(source_file_path)[0]
    if not os.path.exists(output_directory):
        raise Exception(f'Output directory does not exist: {output_directory}')

    extension = source_file_name.rsplit('.', 1)[1]
    artist = extract_artist(source_file_name)

    print(f'Splitting File: {source_file_name}')

    def generate_file_name_safe_inline(new_name):
        if 'livestream' in source_file_name.lower():
            new_name += ' (Live)'

        if artist:
            new_name = f'{artist}{SPACED_HYPHEN}{new_name}'

        new_file_name = f'{new_name}.{extension}'
        output_full_path = os.path.join(output_directory, new_file_name)
        suffix = 1
        while os.path.isfile(output_full_path):
            suffix += 1
            print('File already exists, appending _' + str(suffix))
            new_file_name = f'{new_name}_{suffix}.{extension}'
            output_full_path = os.path.join(output_directory, new_file_name)

        print(f'Creating File: {new_file_name}')
        return output_full_path

    for data in track_data:

        start_timestamp = data.get('start_timestamp')
        end_timestamp = data.get('end_timestamp')
        start_timestamp = format_timestamp(start_timestamp)
        end_timestamp = format_timestamp(end_timestamp)

        if verbose > 0:
            print(f'Start Timestamp: {start_timestamp}')
            print(f'End Timestamp: {end_timestamp}')

        # end_timestamp -= 1.0  # milliseconds  # TODO ?

        title = clean_file_name(data.get('title'))

        output_path = generate_file_name_safe_inline(title)

        # if 'livestream' in source_file_name.lower():
        #     title += ' (Live)'
        # if artist:
        #     title = f'{artist}{SPACED_HYPHEN}{title}'
        # output_path = generate_file_name_safe(output_directory, title, extension)

        command = [
            'ffmpeg',
            '-i', source_file_path,
            '-acodec', 'copy',
            '-metadata', 'purl=' + purl,
            '-ss', start_timestamp,
            '-to', end_timestamp,
            output_path
        ]
        # command_2 = [
        #     'ffmpeg',
        #     '-ss', str(start_timestamp),
        #     '-to', str(end_timestamp),
        #     '-i', source_file_path,
        #     '-acodec', 'copy',
        #     '-metadata', 'purl=' + purl,
        #     output_path

        # TODO Quote file names?
        # windows_command = ' '.join(command)
        # windows_command_2 = ' '.join(command_2)

        call_ffmpeg(command, verbose=-1, commit=commit)

    if not commit:
        print(f'~~~ NOT Committing Changes ~~~\n')
    else:
        print('--- Done!\n')


# def generate_file_name_safe(output_directory, title, extension):
#     new_file_name = f'{title}.{extension}'
#     output_path = os.path.join(output_directory, new_file_name)
#     suffix = 1
#     while os.path.isfile(output_path):
#         suffix += 1
#         print('File already exists, appending _' + str(suffix))
#         new_file_name = f'{title}_{suffix}.{extension}'
#         output_path = os.path.join(output_directory, new_file_name)
#
#     return output_path


def extract_artist(file_path):
    dot = '.'
    file_name = file_path.rsplit(dot, 1)[0]

    artist = file_name
    while SPACED_HYPHEN in artist:
        artist = artist.rsplit(SPACED_HYPHEN, 1)[0]

    # Remove `Best of`
    best_of_result = re.match(r'[bB]est [oO]f (.*)$', artist)
    if best_of_result:
        artist = best_of_result.group(1).strip()

    # Remove digits from the start
    while artist[0] in '0123456789':
        artist = artist[1:]
        if not artist:
            return None

    if artist_is_part_of_a_mix(artist):
        artist = file_name.rsplit(SPACED_HYPHEN, 1)[-1]
        artist = artist.split(' (', 1)[0]
        if artist_is_part_of_a_mix(artist):
            return None

    return artist


def artist_is_part_of_a_mix(artist):

    artist = artist.lower().strip()

    mix_prefixes = ['A Post', 'Post', 'hours', 'Mixtape']

    for prefix in mix_prefixes:
        if artist.startswith(prefix.lower()):
            return True

    mix_suffixes = [' Mix', 'post-rock']
    for suffix in mix_suffixes:
        if artist.endswith(suffix.lower()):
            return True

    return False


def clean_file_name(title):

    # Remove Track Title Prefixes ('1.' or '01.')
    if re.match(r'[0-9][0-9]?\..*', title):
        title = title.split('.', 1)[1].strip()

    # Remove characters that mess with ffmpeg cli commands
    remove_chars = '?"`#*<>|\'\\\.'
    for char in remove_chars:
        title = title.replace(char, '')
    title = title.strip(':- \n')
    title = title.replace(':', ' -')
    title = title.replace('/', ' ')

    # Limit of 159 chars for a file name. '.opus' is 5, so trim title to 154
    return title[:154]


def run(album_input_dir, verbose, commit, file_data):

    song_splitter = SongSplitter(
        album_done_dir=Paths.ORIGINAL_ALBUMS,
        song_output_dir=Paths.NEW_SONGS,
        album_error_dir=Paths.NEEDS_METADATA,
        verbose=verbose,
        commit=commit
    )
    song_splitter.split_songs_in_directory(album_input_dir, split_using_file=file_data)


if __name__ == '__main__':
    default_path = Paths.NEW_ALBUMS

    parser = argparse.ArgumentParser(description='Spilt Song Files Based on Metadata')
    parser.add_argument('directory', nargs='?', default=default_path, help='Target Directory')
    parser.add_argument('--commit', action='store_true', help='Commit Changes')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    parser.add_argument('--file-data', action='store_true', help='Use an external file for the track data')

    args = parser.parse_args()
    run(os.path.join(Paths.MUSIC, args.directory), args.verbose, args.commit, args.file_data)


"""
python split_songs.py
"""
