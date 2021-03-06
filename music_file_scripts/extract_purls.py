"""
Traverse directories and extract the `purl` metadata value from the files

Ethan Wright - 6/11/20
"""
import os
import re

from common import list_music_files
from paths import Paths
from traverse_directory import TraverseDirectory

READ_SIZE_BYTES = 100
MAX_BYTES_TO_READ = 30000


class ReadFileBytes(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.bytes_read = 0
        self.file = open(self.file_path, 'rb')
        return self

    def __exit__(self, *kwargs):
        self.file.close()

    def read_bytes(self, amount):
        self.bytes_read += amount
        return self.file.read(amount).decode('utf-8', 'replace')


def extract_video_id(full_path):
    with ReadFileBytes(full_path) as music_file:
        search_string = ''
        while music_file.bytes_read < MAX_BYTES_TO_READ:
            search_string = search_string[-5:] + music_file.read_bytes(READ_SIZE_BYTES)
            if 'purl=' in search_string:
                search_string += music_file.read_bytes(50)
                regex = r'purl=https://www.youtube.com/watch\?v=(.{11})'
                search_result = re.search(regex, search_string)
                if search_result:
                    return search_result.group(1)

        return None


class TraverseDirectoryWriteToFile(TraverseDirectory):

    def __init__(self, write_file):
        self.write_file = write_file

    def handle_dir(self, dir_name, directory, full_path):
        message = '--- ' + dir_name + ' ---\n'
        print(message)
        return True

    def handle_file(self, file_name, directory, full_path):
        song_name, extension = file_name.rsplit('.')
        if extension in ['m4a', 'mp3', 'txt']:
            print(f'SKIPPING! {file_name} does not support PURL metadata')
            return

        video_id = extract_video_id(full_path)
        if video_id:
            self.write_file.write(video_id + '\n')
        else:
            print(f'{file_name} has no PURL metadata entry')


def extract_video_ids_to_file(output_path):

    subdirs = [
        # r'liked_redownloaded',
        # r'most_music_redownloaded',
        # Paths.POST_ROCK_FULL_ALBUMS_DIR,
        # os.path.join(Paths.POST_ROCK_FULL_ALBUMS_DIR, r''),
        Paths.POST_ROCK_TO_SORT_DIR,
        # os.path.join(Paths.POST_ROCK_TO_SORT_DIR, r''),
    ]

    with open(output_path, 'w') as write_file:
        traveler = TraverseDirectoryWriteToFile(write_file)
        for subdir in subdirs:
            directory = os.path.join(Paths.MUSIC_DIR, subdir)
            traveler.iterate_files_recursively(directory)


if __name__ == '__main__':
    # output_file = r'output\downloaded_video_ids_all.txt'
    # output_file = r'output\all_album_purls.txt'
    output_file = r'output\all_song_purls.txt'
    output_file_path = os.path.join(Paths.Paths.MUSIC_SCRIPT_DIR, output_file)

    extract_video_ids_to_file(output_file_path)
