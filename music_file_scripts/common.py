"""
Common music script functions
"""
import os

invalid_music_extensions = ['txt', 'jpg', 'png', 'py', 'ini']
music_extensions = ['mp3', 'ogg', 'm4a', 'opus']


def list_music_files(directory):
    return [
        file_name for file_name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file_name))
        and split_file_name(file_name)[1] in music_extensions
    ]


def list_music_file_names(directory):
    # TODO Test / Compare / Benchmark?
    return list_music_file_names_2(directory)
    # return list_music_file_names_1(directory)


def list_music_file_names_2(directory):
    return_list = []
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            name, extension = split_file_name(file_name)
            if extension in music_extensions:
                return_list.append(name)
    return return_list


def list_music_file_names_1(directory):
    return [remove_file_extension(file_name) for file_name in list_music_files(directory)]


def split_file_name_simple(file_name):
    if '.' not in file_name:
        return file_name, None
    return file_name.rsplit('.', 1)


def is_extension_valid(extension):
    if extension:
        if len(extension) <= 5:
            if extension not in invalid_music_extensions + music_extensions:
                return False
                # raise Exception('Unexpected file extension encountered: ' + extension)
            return True
    return False


def split_file_name(file_name):
    name, extension = split_file_name_simple(file_name)

    if is_extension_valid(extension):
        return name, extension

    return file_name, None


def remove_file_extension(file_name):
    return split_file_name(file_name)[0]
