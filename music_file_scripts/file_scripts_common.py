"""
Common file script functions

Ethan Wright 6/08/20
"""
import os


def list_files(directory):
    return sorted([
        file_name for file_name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file_name))
    ])


def move_file(source_file_path, target_file_path, verbose=True, commit=False):
    if not os.path.isfile(source_file_path):
        raise Exception(f'File does not exist: {source_file_path}')
    if os.path.isfile(target_file_path):
        raise Exception(f'File already exists: {target_file_path}')

    if verbose:
        print(f'{source_file_path} Shall move')
        print(f'{target_file_path} is the destination')
    if not commit:
        return
    os.rename(source_file_path, target_file_path)


def rename_file_safe(directory, file_name, new_file_name, verbose=True,  commit=False):
    count = 1
    while os.path.isfile(os.path.join(directory, new_file_name)):
        count += 1
        print(f'File already exists, appending _{count}')
        song_title, extension = new_file_name.rsplit('.', 1)
        new_file_name = f'{song_title}_{count}.{extension}'

    source_file_path = os.path.join(directory, file_name)
    target_file_path = os.path.join(directory, new_file_name)
    move_file(source_file_path, target_file_path, verbose=verbose, commit=commit)


def split_file_name_simple(file_name):
    if '.' not in file_name:
        return file_name, None
    return file_name.rsplit('.', 1)


def split_file_name(file_name):
    name, extension = split_file_name_simple(file_name)

    if is_extension_valid(extension):
        return name, extension

    return file_name, None


def remove_file_extension(file_name):
    return split_file_name(file_name)[0]
