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

import os
import re

from call_ffmpeg import call_ffmpeg, get_metadata
from paths import MUSIC_DIR


def run(source_file_path, song_dir=None, error_dir=None, done_dir=None):
    metadata, stdout = get_metadata(source_file_path)
    split_data = parse_metadata_for_chapters(metadata)
    if len(split_data) == 0:
        return mark_as_error(source_file_path, error_dir)
    purl = extract_field_from_stdout(stdout, 'purl')
    split_file(source_file_path, split_data, purl, output_subdir=song_dir)
    mark_as_done(source_file_path, output_subdir=done_dir)


def extract_field_from_stdout(stdout, stdout_field):
    for line in stdout.split('\n'):
        line_clean = line.strip()
        if stdout_field in line_clean:
            return line_clean.rsplit(' ', 1)[1]


def parse_metadata_for_chapters(metadata):
    return_data = []
    for chapter in metadata.split('[CHAPTER]'):
        regex = 'START=([0-9]+)\nEND=([0-9]+)\ntitle=(.+)\n'
        result = re.search(regex, chapter)
        if result:
            data = result.groups()

            if len(data) == 3:
                return_data.append({
                    'start_timestamp': (int(data[0].strip()) + 1) / 1000,
                    'end_timestamp': (int(data[1].strip()) - 1) / 1000,
                    'title': data[2].strip(),
                })

    return return_data


def clean_title(title):
    # Remove Track Title Prefixes ('1.' or '01.')
    if re.match(r'[0-9][0-9]?\..*', title):
        title = title.split('.', 1)[1].strip()

    # Remove characters that mess with ffmpeg cli commands
    bad_chars = '?"`#*<>:|.,\'\\'
    for char in bad_chars:
        title = title.replace(char, '')
    title = title.replace('/', ' ')

    # Limit of 159 chars for a file name. '.opus' is 5, so trim title to 154
    return title[:154]


def mark_as_done(source_file_path, output_subdir=None):
    move_to_subdir(source_file_path, output_subdir)


def mark_as_error(source_file_path, output_subdir=None):
    print(f'Can not split file. Marking as error: {source_file_path}')
    move_to_subdir(source_file_path, output_subdir)


def move_to_subdir(source_file_path, output_subdir):
    if output_subdir:
        source_dir, name = source_file_path.rsplit('\\', 1)
        target_file_path = os.path.join(source_dir, output_subdir, name)
        os.rename(source_file_path, target_file_path)


def split_file(source_file_path, split_data, purl, output_subdir=None):
    source_directory, source_file_name = source_file_path.rsplit('\\', 1)

    if output_subdir:
        output_directory = os.path.join(source_directory, output_subdir)
    else:
        output_directory = source_directory
    if not os.path.exists(output_directory):
        raise Exception(f'Output directory does not exist: {output_directory}')

    print(f'Splitting File: {source_file_name}')
    extension = source_file_name.rsplit('.', 1)[1]
    artist = source_file_name.split(' - ', 1)[0]

    # Remove `Best of`
    result = re.match(f'[bB]est of (.*)\.{extension}', artist)
    if result:
        artist = result.group(1).strip()

    for data in split_data:
        start_timestamp = data.get('start_timestamp')
        end_timestamp = data.get('end_timestamp')
        title = clean_title(data.get('title'))

        new_title = f'{artist} - {title}'
        new_file_name = f'{new_title}.{extension}'

        output_path = os.path.join(output_directory, new_file_name)

        suffix = 1
        while os.path.isfile(output_path):
            suffix += 1
            print('File already exists, appending _' + str(suffix))
            new_file_name = f'{new_title}_{suffix}.{extension}'
            output_path = os.path.join(output_directory, new_file_name)

        command = f'ffmpeg -i "{source_file_path}" -acodec copy -metadata purl={purl} -ss {start_timestamp} -to {end_timestamp} "{output_path}"'
        print(f'Creating File: {new_file_name}')
        # print(command)
        call_ffmpeg(command)
    print('--- Done!\n')


if __name__ == '__main__':

    song_output_dir = 'individual_songs'
    error_output_dir = 'no_metadata'
    done_output_dir = 'already_split'
    input_subdirectory = r'post_rock\full_albums\to_listen_to'
    # input_subdirectory = r'post_rock\full_albums\liked_plus'
    # input_subdirectory = r'post_rock\full_albums\liked'
    directory = os.path.join(MUSIC_DIR, input_subdirectory)

    files = os.listdir(directory)
    for file_name in files:
        # print(file_name)
        # continue
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            run(file_path, song_dir=song_output_dir, error_dir=error_output_dir, done_dir=done_output_dir)
