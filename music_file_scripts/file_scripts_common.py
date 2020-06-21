"""
Common file script functions
"""
import os


def list_files(directory):
    return [
        file_name for file_name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file_name))
    ]


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


#####################################################################################

class TraverseDirectory(object):

    def handle_dir(self, dir_name, directory, full_path):
        raise NotImplemendedError()

    def handle_file(self, file_name, directory, full_path):
        raise NotImplemendedError()

    def iterate_files_recursively(self, directory):
        for file_name in os.listdir(directory):
            full_path = os.path.join(directory, file_name)

            if os.path.isfile(full_path):
                self.handle_file(file_name, directory, full_path)

            elif os.path.isdir(full_path):
                if self.handle_dir(file_name, directory, full_path):
                    self.iterate_files_recursively(full_path)

    def iterate_files_recursively_lazy(self, directory):
        found_dirs = []
        for file_name in os.listdir(directory):
            full_path = os.path.join(directory, file_name)

            if os.path.isfile(full_path):
                self.handle_file(file_name, directory, full_path)

            elif os.path.isdir(full_path):
                found_dirs.append(file_name)

        for dir_name in found_dirs:
            full_path = os.path.join(directory, dir_name)
            if self.handle_dir(dir_name, directory, full_path):
                self.iterate_files_recursively_lazy(full_path)
