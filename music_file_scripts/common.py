"""
Common music script functions
"""
import os

from file_scripts_common import (
    TraverseDirectory, list_files, move_file, rename_file_safe
)

invalid_music_extensions = ['txt', 'jpg', 'png', 'py', 'ini']
music_extensions = ['mp3', 'ogg', 'm4a', 'opus']


def list_music_files(directory):
    return [
        file_name for file_name in list_files(directory)
        if split_into_file_name_and_extension(file_name)[1] not in invalid_music_extensions
    ]


def list_music_file_names(directory):
    return [split_into_file_name_and_extension(file_name)[0] for file_name in list_music_files(directory)]


def split_into_file_name_and_extension(file_name):
    if '.' not in file_name:
        return file_name, None
    name, extension = file_name.rsplit('.', 1)
    if len(extension) <= 5:
        if extension in invalid_music_extensions + music_extensions:
            return name, extension
    return file_name, None


def remove_file_extension(file_name):
    return split_file_name_from_extension(file_name)[0]
