"""
Compare files between two directories and move the files if needed

Ethan Wright - 6/11/20
"""

import argparse
import copy
import os

from common import list_music_files, move_file, remove_file_extension
from fix_names import FixFileNames
from paths import Paths, PathGen


class MusicFileList(object):
    ffn = FixFileNames()

    def __init__(self, directory, good_folder, bad_folder, commit=False):
        self.directory = directory
        self.target_good = os.path.join(directory, good_folder)
        self.target_bad = os.path.join(directory, bad_folder)
        self.music_list_pointer = 0
        self.sorted_music_list = self._get_sorted_music_list()
        self.total_items = len(self.sorted_music_list)
        self.current_song = None
        self.current_song_simplified = None
        self.commit = commit

        self._set_current_song()

    def _get_sorted_music_list(self):
        # return sorted(list_music_files(self.directory), key=self.simplify_file_name_fuzzier)
        return sorted(list_music_files(self.directory), key=lambda x: x.lower())

    def move_current_song_match_found(self, result_string=None):
        # result_string = '   MATCHED'
        self._move_current_song(self.target_good, result_string=result_string, commit=False)

    def move_current_song_no_match(self, result_string=None):
        result_string = 'X NO MATCH'
        self._move_current_song(self.target_bad, result_string=result_string, commit=self.commit)

    def _move_current_song(self, target_directory, result_string=None, commit=False):
        file_name = self.current_song
        verbose = False
        if result_string:
            print(f'{result_string}: {file_name}')
            verbose = True
        source_path = os.path.join(self.directory, file_name)
        target_path = os.path.join(target_directory, file_name)
        if commit:
            move_file(source_path, target_path, verbose=verbose, commit=commit)
        self._increment_position()

    def _set_current_song(self):
        if self.music_list_pointer < self.total_items:
            result = self.sorted_music_list[self.music_list_pointer]
            self.current_song = result
            # self.current_song_simplified = self.simplify_file_name_fuzzier(result)
            self.current_song_simplified = result.lower()  # More Exact Match (Need to change sorting key too!)
        else:
            self.current_song = None
            self.current_song_simplified = None

    def _increment_position(self):
        self.music_list_pointer += 1
        self._set_current_song()

    def simplify_file_name_fuzzier(self, name):
        return self.ffn.get_new_name(remove_file_extension(name)).lower()


def sort_directory_contents(directory_1, directory_2, commit=False):
    matches_count = 0

    music_file_list_1 = MusicFileList(directory_1, 'replacement_found', 'extra', commit=commit)
    music_file_list_2 = MusicFileList(directory_2, 'liked_replacements', 'extra', commit=commit)

    while music_file_list_1.current_song and music_file_list_2.current_song:

        simple_string_1 = music_file_list_1.current_song_simplified
        simple_string_2 = music_file_list_2.current_song_simplified

        min_len = min(len(simple_string_1), len(simple_string_2))
        simple_string_1 = simple_string_1[:min_len]
        simple_string_2 = simple_string_2[:min_len]

        if simple_string_1 < simple_string_2:
            music_file_list_1.move_current_song_no_match()

        elif simple_string_1 > simple_string_2:
            music_file_list_2.move_current_song_no_match()

        elif simple_string_1 == simple_string_2:
            music_file_list_1.move_current_song_match_found()
            music_file_list_2.move_current_song_match_found()
            matches_count += 1

    while music_file_list_1.current_song:
        music_file_list_1.move_current_song_no_match()

    while music_file_list_2.current_song:
        music_file_list_2.move_current_song_no_match()

    print(f'Matches: {matches_count}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compare Directories')
    parser.add_argument('--commit', action='store_true', help='Commit Changes')
    args = parser.parse_args()

    # existing_music = Paths.POST_ROCK_ORIGINAL_ALBUMS
    existing_music = Paths.POST_ROCK

    # new_music = r'E:\- Backup -\Music\post_rock\original_albums'
    # new_music = r'E:\- Backup -\Music\post_rock\songs_to_sort'
    # new_music = r'F:\backup\Music\post_rock\original_albums'
    # new_music = r'F:\backup\Music\post_rock\songs_to_sort'
    # new_music = r'/media/mimorox/My Passport/backup/Music/to_sort_post_rock/'
    # new_music = r'/media/mimorox/My Passport/- Backup -/Music/to_sort_post_rock/'

    external_path = PathGen.gen_path_from_root(root_path='/media/mimorox/My Passport/- Backup -')
    new_music = external_path.POST_ROCK

    sort_directory_contents(existing_music, new_music, commit=args.commit)
