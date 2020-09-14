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
from common import list_music_files, clean_file_name
from paths import Paths


class SongSplitter(object):

    def __init__(self, split_song_dir=None, error_dir=None, done_dir=None, verbose=0, commit=False):
        self.split_song_dir = split_song_dir
        self.error_dir = error_dir
        self.done_dir = done_dir
        self.verbose = verbose
        self.commit = commit

    def split_songs_in_directory(self, directory):
        for file_name in list_music_files(directory):
            # print(file_name)
            self.call_split_file(directory, file_name)

    def call_split_file(self, directory, file_name):
        full_path = os.path.join(directory, file_name)
        metadata, stdout = get_metadata(full_path, verbose=-1)
        split_data = parse_metadata_for_chapters(metadata)
        if len(split_data) == 0:
            return move_to_subdir(full_path, file_name, self.error_dir, commit=self.commit, print_error_msg=True)
        purl = extract_field_from_stdout(stdout, 'purl')
        split_file(full_path, file_name, split_data, purl, output_directory=self.split_song_dir, verbose=self.verbose, commit=self.commit)
        move_to_subdir(full_path, file_name, self.done_dir, commit=self.commit)


def extract_field_from_stdout(stdout, stdout_field):
    for line in stdout.split('\n'):
        line_clean = line.strip()
        if stdout_field in line_clean:
            return line_clean.rsplit(' ', 1)[1]


def parse_chapter_data(data):
    return {
        'start_timestamp': (int(data[0].strip()) + 1) / 1000,
        'end_timestamp': (int(data[1].strip()) - 1) / 1000,
        'title': data[2].strip(),
    }


def parse_metadata_for_chapters(metadata):
    return_data = []
    for chapter in metadata.split('[CHAPTER]'):
        regex = 'START=([0-9]+)\nEND=([0-9]+)\ntitle=(.+)\n'
        result = re.search(regex, chapter)
        if result and len(result.groups()) == 3:
            chapter_data = parse_chapter_data(result.groups())
            return_data.append(chapter_data)

    return return_data


def extract_artist(file_path):
    dot = '.'
    hyphen_split = ' - '

    file_name = file_path.rsplit(dot, 1)[0]

    artist = file_name
    while hyphen_split in artist:
        artist = artist.rsplit(hyphen_split, 1)[0]

    # Remove `Best of`
    best_of_result = re.match(r'[bB]est [oO]f (.*)$', artist)
    if best_of_result:
        artist = best_of_result.group(1).strip()

    if artist_is_part_of_a_mix(artist):
        artist = file_name.rsplit(hyphen_split, 1)[-1]
        artist = artist.split(' (', 1)[0]
        if artist_is_part_of_a_mix(artist):
            return None

    return artist


def artist_is_part_of_a_mix(artist):
    artist = artist.lower()
    mix_prefixes = ['A Post', 'Post', '2019', '5 hours', 'Mixtape']
    for prefix in mix_prefixes:
        if artist.startswith(prefix.lower()):
            return True

    mix_suffixes = [' Mix', 'post-rock']
    for suffix in mix_suffixes:
        if artist.endswith(suffix.lower()):
            return True

    return False


def move_to_subdir(source_file_path, file_name, output_directory, commit=False, print_error_msg=False):
    if print_error_msg:
        print(f'Can not split file. Marking as error: {source_file_path}')
    target_file_path = os.path.join(output_directory, file_name)
    if commit:
        os.rename(source_file_path, target_file_path)


def split_file(source_file_path, source_file_name, split_data, purl, output_directory=None, verbose=0, commit=False):

    if not output_directory:
        output_directory = os.path.split(source_file_path)[0]
    if not os.path.exists(output_directory):
        raise Exception(f'Output directory does not exist: {output_directory}')

    extension = source_file_name.rsplit('.', 1)[1]
    artist = extract_artist(source_file_name)

    print(f'Splitting File: {source_file_name}')

    for data in split_data:
        start_timestamp = data.get('start_timestamp')
        end_timestamp = data.get('end_timestamp')
        title = clean_file_name(data.get('title'))

        if 'livestream' in source_file_name.lower():
            title += ' (Live)'

        if artist:
            title = f'{artist} - {title}'

        new_file_name = f'{title}.{extension}'

        output_path = os.path.join(output_directory, new_file_name)

        suffix = 1
        while os.path.isfile(output_path):
            suffix += 1
            print('File already exists, appending _' + str(suffix))
            new_file_name = f'{title}_{suffix}.{extension}'
            output_path = os.path.join(output_directory, new_file_name)

        # command_2 = f'ffmpeg -ss {start_timestamp} -to {end_timestamp} -i "{source_file_path}" -acodec copy -metadata purl={purl} "{output_path}"'
        # command = f'ffmpeg -i "{source_file_path}" -acodec copy -metadata purl={purl} -ss {start_timestamp} -to {end_timestamp} "{output_path}"'

        command = [
            'ffmpeg',
            '-i', source_file_path,
            '-acodec', 'copy',
            '-metadata', 'purl=' + purl,
            '-ss', str(start_timestamp),
            '-to', str(end_timestamp),
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
        # ]
        print(f'Creating File: {new_file_name}')
        call_ffmpeg(command, verbose=-1, commit=commit)

    if not commit:
        print(f'~~~ NOT Committing Changes ~~~\n')
    else:
        print('--- Done!\n')


def run(directory, verbose, commit):
    song_output_dir = Paths.POST_ROCK_NEW_SONGS_DIR  # 'individual_songs'
    error_output_dir = Paths.POST_ROCK_NEEDS_METADATA_DIR  # 'needs_metadata'
    done_output_dir = Paths.POST_ROCK_ORIGINAL_ALBUMS_DIR  # 'split_albums'
    song_splitter = SongSplitter(split_song_dir=song_output_dir, error_dir=error_output_dir, done_dir=done_output_dir, verbose=verbose, commit=commit)
    song_splitter.split_songs_in_directory(directory)


if __name__ == '__main__':
    default_path = Paths.POST_ROCK_NEW_ALBUMS_DIR

    parser = argparse.ArgumentParser(description='Spilt Song Files Based on Metadata')
    parser.add_argument('directory', nargs='?', default=default_path, help='Target Directory')
    parser.add_argument('--commit', action='store_true', help='Commit Changes')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')

    args = parser.parse_args()
    run(os.path.join(Paths.MUSIC_DIR, args.directory), args.verbose, args.commit)


"""
python split_songs.py
"""