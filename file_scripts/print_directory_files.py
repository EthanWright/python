import os

from traverse_directory import TraverseDirectory
from paths import Paths

ROOT_DIR_PLACEHOLDER = 'ROOT'


def run():
    # sub_dir = 'phone'
    # sub_dir = 'good'
    # sub_dir = 'to_sort'
    # sub_dir = 'to_sort_post_rock'

    # for sub_dir in ['phone', 'good', 'to_sort']:

    output_file_name = 'all_files_' + sub_dir + '.txt'
    file_path = os.path.join(Paths.MUSIC, sub_dir)
    output_file_path = os.path.join(file_path, output_file_name)

    directory_lister = TraverseDirectoryLister(print_dir_names=True)
    directory_lister.print_directory_to_file(file_path, output_file_path)


class TraverseDirectoryLister(TraverseDirectory):

    def __init__(self, print_sizes=False, print_flat_list=False, print_dir_names=True):
        self.dir_list = []
        self.file_dict = {}
        self.file_size_dict = {}

        self.print_sizes = print_sizes
        self.print_flat_list = print_flat_list
        self.root_path = ''
        self.print_dir_names = print_dir_names

    def print_directory_to_file(self, file_path, output_file_path):
        self.root_path = file_path
        self.iterate_files_recursively(file_path, lazy=True)
        self.write_lists_to_file(output_file_path)

    def get_short_str(self, str_to_shorten):
        return str_to_shorten.replace(self.root_path, '').strip('/')

    def handle_dir(self, file_name, directory, full_path):
        short_dir = self.get_short_str(full_path)
        self.dir_list.append(short_dir)

        if short_dir in self.file_dict:
            print(self.file_dict)
            raise Exception("oh no " + short_dir)

        self.file_dict[short_dir] = []
        return True

    def handle_file(self, file_name, directory, full_path):

        if self.print_flat_list:
            directory = ROOT_DIR_PLACEHOLDER

        short_dir = self.get_short_str(directory)
        short_full_path = self.get_short_str(full_path)

        self.file_dict[short_dir].append(short_full_path)

        if self.print_sizes:
            # TODO Untested
            self.file_size_dict[short_dir][file_name] = os.path.getsize(full_path)

        return True

    def get_sorted_list(self, dir_name):
        return sorted(
            self.file_dict.get(dir_name, []),
            key=lambda x: x.lower()
        )

    def get_sorted_list_size(self, dir_name):
        # TODO Untested
        return reversed(
            sorted(
                self.file_size_dict.get(dir_name, []),
                key=lambda x: x[1]
            )
        )

    def write_lists_to_file(self, output_file_path):

        write_string = ""
        for dir_name in self.dir_list:
            if self.print_dir_names and dir_name != ROOT_DIR_PLACEHOLDER:
                write_string += '--- ' + self.root_path + '/' + dir_name + '\n'

            if self.print_sizes:
                # TODO Untested
                for item in self.get_sorted_list_size(dir_name):
                    mb_size = int(item[1] / MEGA)
                    write_string += f'{item[0]}\n{mb_size:,} MB\n'
            else:
                for file_name in self.get_sorted_list(dir_name):
                    extension = file_name.rsplit('.', 1)[-1]
                    if extension.lower() not in ['jpg', 'txt', 'm3u']:
                        write_string += file_name + '\n'
            write_string += '\n'

        with open(output_file_path, 'w') as write_file:
            # write_file.write("Generated by " + os.path.realpath(__file__) + "\n")
            try:
                write_file.write(write_string)
            except UnicodeEncodeError as e:
                print(f'ERROR writing data! \n{e}')


if __name__ == '__main__':
    run()
