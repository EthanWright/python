"""
Use ffmpeg CLI commands to convert audio files
Only converts to opus right now

Ethan Wright 6/10/20
"""
import os
import re

from call_ffmpeg import call_ffmpeg, get_metadata
from music_file_scripts_common import list_music_files
from paths import Paths
from utils import extract_field_from_metadata


def run(file_path, commit=False):
    if os.path.isdir(file_path):
        return
    metadata, stdout_data = get_metadata(file_path)
    title = extract_field_from_metadata(metadata, 'title')
    if not title:
        title = os.path.split(file_path)[1].rsplit('.', 1)[0]
    convert_file_to_opus(file_path, title, commit=commit)


def convert_file_to_opus(source_file_path, new_name, commit=False):

    source_directory, source_file_name = os.path.split(source_file_path)
    new_file_name = new_name + '.opus'
    output_path = os.path.join(source_directory, new_file_name)

    # TODO Configurable bitrate from CLI
    command = ['ffmpeg', '-i', source_file_path, '-c:a', 'libopus', '-b:a', '48000', output_path]
    # windows_command = ' '.join(command)
    print('Running command:\n', command)
    result, stdout = call_ffmpeg(command, commit=commit, verbose=5)

    return result


if __name__ == '__main__':

    # directory = Paths.TO_SORT
    directory = Paths.FULL_ALBUMS

    commit_result = True

    for file_name in list_music_files(directory):
        run(os.path.join(directory, file_name), commit=commit_result)
