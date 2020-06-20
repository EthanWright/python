"""
Move Songs on computer to mirror the master rating list that I maintain

Ethan Wright - 6/11/20
"""
"""
~~~ Manual Song Sorting ~~~
Manually maintain master list of song names that I like
Listen to albums and pick out the potential good ones.
Split albums into songs and add those to the song sorting process.

If I like the song, put a + in front of it's name.
If I do not like the song, put a - in front of it's name.
If it already has a rating, combine it with the new rating
- and - = --
+ and + = ++
+ and - = (Nothing)


~~~ Automated Song Moving ~~~
This script will update the actual song file location on my HD to
reflect the master list, and update the master list for new or deleted files
All songs will be moved to the correct folder according to their ratings:
-- Will be deleted
++ Will be confirmed

This script will output an updated and sorted master list.
Deleted songs will be removed, and confirmed songs will be in a separate list
New songs files found will be added to the master list with no rating

The music sorting directories on the HD are arranged to match the ratings
The `to_sort` folder has 2 subdirectories: + and -
    The + directory has files and a + subdirectory
    The - directory has files and a - subdirectory


~~~ Script Design ~~~
Read in every song from the master list of songs
Sort them into groups based off their prefix
prefixes = ['', '-', '--', '+', '++']

Iterate through each song folder on the HD
Compare the files there to what the master list has
Compile a diff: `missing` and `extra` songs for each folder

Loop through each possible rating section in the generated diff.
Loop through that ratings `missing` songs
Search for them in the `extra` songs lists in the other rating sections
Move the files so that they match the master list

Songs left in extra for no-prefix are newly added songs that
should be added to the master list with no rating
Other left over songs are errors

Print sorted list back out, with `++` and `--` in a separate list
"""

import copy
import os
import re

from common import (
    list_music_file_names, move_file, remove_file_extension, rename_file_safe, list_music_files, has_file_extension
)
from fix_names import FixFileNames
from paths import MUSIC_DIR, MUSIC_SCRIPT_DIR

POSSIBLE_RATINGS = ['', '-', '+', '++', '--']
END_OF_LIST = chr(128) * 8

"""
TODO
Separate mapping 1 and 2
Move dupes into folder
Split DiffMultiLevelLists into sub class of something?
If there is a duplicate in one list and both map to the same song in the other list, what happens?

"""


def run():
    files_to_sort_path = os.path.join(MUSIC_DIR, r'post_rock\to_sort')
    song_file_name = r'input\post_rock_songs_all_sorted.txt'
    song_file_path = os.path.join(files_to_sort_path, song_file_name)

    # Terms: `missing` and `extra` are from the perspective of the computer
    song_rating_dict = read_song_file(song_file_path)
    song_file_dict = gather_file_names_from_path(files_to_sort_path)

    diff_lists = DiffMultiLevelLists(song_file_dict, song_rating_dict)
    wrong_dir, missing, extra = diff_lists.compute_diff()
    # diff_lists.apply_diff(wrong_dir, files_to_sort_path)
    diff_lists.print_new_master_list(missing, extra)


def gather_file_names_from_path(files_to_sort_path):
    return_dict = {}
    for rating in POSSIBLE_RATINGS:
        path = '\\'.join([char for char in rating])
        return_dict[rating] = list_music_files(os.path.join(files_to_sort_path, path))
    return return_dict


def read_song_file(song_file_path):
    song_rating_dict = {rating: [] for rating in POSSIBLE_RATINGS}

    # Read in every song from the main list
    for song_title in open(song_file_path, 'r').readlines():
        regex = r'(^\+\+?|^--?)[^(-+)]'
        match = re.search(regex, song_title)
        rating = ''
        if match:
            rating = match.group(1)
        # Clean title, remove rating string, and add to rating dictionary
        song_title = song_title[len(rating):].strip()
        song_rating_dict[rating].append(song_title)

    return song_rating_dict


class CompareLists(object):

    def __init__(self, list_1, list_2):
        if not isinstance(list_1, SongList):
            list_1 = SongList(list_1)
        if not isinstance(list_2, SongList):
            list_2 = SongList(list_2)
        self.list_1 = list_1
        self.list_2 = list_2
        self.only_list_2 = []
        self.only_list_1 = []
        self.all_items = []
        self._compare_lists()

    def _compare_lists(self):

        while self.list_1.current_song != END_OF_LIST or self.list_2.current_song != END_OF_LIST:

            string_1 = self.list_1.current_song
            string_2 = self.list_2.current_song

            # Track unique elements
            if string_1 < string_2:
                self.only_list_1.append(string_1)
            elif string_1 > string_2:
                self.only_list_2.append(string_2)

            # Advance position by removing whichever item comes first alphabetically
            if string_1 <= string_2:
                self.all_items.append('M: ' + string_1)
                self.list_1.advance_position()
            if string_1 >= string_2:
                self.all_items.append('E: ' + string_2)
                self.list_2.advance_position()


class SongList(object):

    def __init__(self, starting_list):
        self.dupes = []
        self.sorted_list = sorted(starting_list)
        self.total_items = len(self.sorted_list)
        self.list_pointer = 0
        self.current_song = ''
        self._set_current_song()

    def advance_position(self):
        self.list_pointer += 1
        self._set_current_song()

    def _set_current_song(self):
        if self.list_pointer < self.total_items:
            file_name = remove_file_extension(self.sorted_list[self.list_pointer])
            if self.current_song:
                if file_name in self.current_song or self.current_song in file_name:
                    self.dupes.append(file_name)
            self.current_song = file_name
        else:
            self.current_song = END_OF_LIST


class DiffMultiLevelLists(object):
    ffn = FixFileNames()

    def __init__(self, song_file_dict, song_rating_dict):
        self.all_songs = {}
        self.missing = {}
        self.extra = {}
        self.mapping_1 = {}
        self.mapping_2 = {}
        self.dupes_dict_1 = {}
        self.dupes_dict_2 = {}
        self.song_file_dict = song_file_dict
        self.song_rating_dict = song_rating_dict

    def simplify_file_name_fuzzier(self, name):
        return self.ffn.get_new_name(remove_file_extension(name)).lower()

    def simplify_list(self, song_list, number):
        simplified = []
        for song_title in song_list:
            song_title_simplified = self.simplify_file_name_fuzzier(song_title)
            simplified.append(song_title_simplified)
            if number == 1:
                self.mapping_1[song_title_simplified] = song_title
            elif number == 2:
                self.mapping_2[song_title_simplified] = song_title
        return simplified

    def get_sub_dicts_as_lists(self, rating):
        # return (self.simplify_list(song_list.get(rating, [])) for song_list in [self.song_file_dict, self.song_rating_dict])
        list_1 = self.song_file_dict.get(rating, [])
        list_2 = self.song_rating_dict.get(rating, [])
        return self.simplify_list(list_1, 1), self.simplify_list(list_2, 2)

    def compute_diff_for_category(self, rating):

        simple_computer_list, simple_master_list = self.get_sub_dicts_as_lists(rating)
        self.all_songs[rating] = simple_master_list

        compare_lists = CompareLists(simple_computer_list, simple_master_list)

        self.missing[rating] = compare_lists.only_list_1
        self.extra[rating] = compare_lists.only_list_2

        # self.dupes_dict_1[rating] = [(item, rating) for item in compare_lists.list_1.dupes]
        # self.dupes_dict_2[rating] = [(item, rating) for item in compare_lists.list_2.dupes]
        self.dupes_dict_1[rating] = compare_lists.list_1.dupes
        self.dupes_dict_2[rating] = compare_lists.list_2.dupes

    def compute_diff(self):
        for rating in POSSIBLE_RATINGS:
            self.compute_diff_for_category(rating)

        return self.process_diff()

    def apply_diff(self, files_to_move, base_directory):
        for song_name, ratings in files_to_move.items():
            new_location = '\\'.join([char for char in ratings[0]])
            old_location = '\\'.join([char for char in ratings[1]])

            file_name = self.mapping.get(song_name)
            if '.' not in file_name[-5:]:
                file_name = self.mapping_2.get(song_name)
            print(f'Name: "{file_name}"')
            new_full_path = os.path.join(base_directory, new_location, file_name)
            old_full_path = os.path.join(base_directory, old_location, file_name)
            # rename_file_safe(old_full_path, new_full_path, commit=False)
            # print(f'Moving "{old_full_path}" to "{new_full_path}"')

    def process_diff(self):
        missing_missing = []
        located = {}

        # Invert the extra songs dictionary as `{song_name: location}` for faster lookup
        extra_songs = self.invert_dict(self.extra, [])

        # Look for each missing_song in the extra_songs list
        for rating in self.missing:
            for missing_song_name in self.missing.get(rating, []):
                real_name = self.mapping_1.get(missing_song_name)
                print(f'Looking for: {real_name}')

                if missing_song_name not in extra_songs:
                    missing_missing.append((missing_song_name, rating))
                    continue

                old_rating = extra_songs.get(missing_song_name)

                print(f'Found "{real_name}" in "{old_rating}"')
                print(f'Should be at "{rating}"')

                located[missing_song_name] = (old_rating, rating)

        extra_extra = [
            (song, rating) for rating in POSSIBLE_RATINGS for song in self.extra.get(rating) if song not in located
        ]
        # TODO Better return value?
        return located, missing_missing, extra_extra

    @staticmethod
    def invert_dict(song_dict, ignore_keys):
        return {name: key for key, value in song_dict.items() if key not in ignore_keys for name in value}

    @staticmethod
    def sort_tuples(song_dict, ignore_keys):
        return sorted(
            [(song_name, rating) for song_name, rating in song_dict if rating not in ignore_keys],
            key=lambda x: x[0]
        )

    @staticmethod
    def flatten_dict_to_sorted_tuples(song_dict, ignore_keys):
        return sorted(
            [(name, rating) for rating, song_list in song_dict.items() if rating not in ignore_keys for name in song_list],
            key=lambda x: x[0]
        )

    def get_mapping_with_extension(self, song_name):
        name = self.mapping_1.get(song_name, '')
        if not name or not has_file_extension(name):
            return self.mapping_2.get(song_name, name)

    def get_mapping_no_extension(self, song_name):
        name = self.mapping_1.get(song_name, '')
        if not name or has_file_extension(name):
            name = self.mapping_2.get(song_name, name)
            if has_file_extension(name):
                name = remove_file_extension(name)
        return name

    def unmap_tuples(self, song_tuples, include_prefixes=True, include_extension=False):
        def print_prefix(prefix):
            if include_prefixes:
                return prefix
            return ''
        if include_extension:
            get_mapping = self.get_mapping_with_extension
        else:
            get_mapping = self.get_mapping_no_extension

        return [print_prefix(prefix) + get_mapping(song) for song, prefix in song_tuples]

    def print_new_master_list(self, missing_dict, extra_dict):
        from pprint import pprint
        PRINT_INITIAL_VALUES = False

        if PRINT_INITIAL_VALUES:
            pprint('songs_on_list')
            pprint(self.all_songs)
            pprint('Could Not Find on Computer')
            pprint(missing_dict)
            pprint('On Computer but not on Master List')
            pprint(extra_dict)
            pprint('Duplicates on Computer')
            pprint(self.dupes_dict_1)
            pprint('Duplicates on Master List')
            pprint(self.dupes_dict_2)
            # import pdb;pdb.set_trace()

        songs_on_list_flat = self.flatten_dict_to_sorted_tuples(self.all_songs, ['++', '--'])
        extra_songs_flat = self.sort_tuples(extra_dict, [])
        # inverted = self.sort_and_unmap_tuples(self.flatten_dict(songs_on_list, ['+', '-', '']))
        missing_songs_flat = self.sort_tuples(missing_dict, [])
        dupes_dict_1_flat = self.flatten_dict_to_sorted_tuples(self.dupes_dict_1, [])
        dupes_dict_2_flat = self.flatten_dict_to_sorted_tuples(self.dupes_dict_2, [])
        count_songs_on_computer = len(missing_songs_flat) + (len(songs_on_list_flat) - len(extra_songs_flat))
        master_list = sorted(songs_on_list_flat + missing_songs_flat, key=lambda x: x[0])

        PRINT_COUNTS = True
        if PRINT_COUNTS:
            print('songs_on_list: ' + str(len(songs_on_list_flat)))
            print('count_songs_on_computer: ' + str(count_songs_on_computer))
            print('Could Not Find on Computer: ' + str(len(extra_songs_flat)))
            print('On Computer but not on Master List: ' + str(len(missing_songs_flat)))
            print('Duplicates on Computer: ' + str(len(dupes_dict_1_flat)))
            print('Duplicates on Master List: ' + str(len(dupes_dict_2_flat)))
            print('New Master List: ' + str(len(master_list)))

        # print('Extra Songs on Computer')
        # pprint(self.unmap_tuples(extra_songs_flat))
        # print('Missing From Computer')
        # pprint(self.unmap_tuples(missing_songs_flat))
        pprint('Duplicates on Computer')
        pprint(self.unmap_tuples(dupes_dict_1_flat, include_prefixes=False))
        pprint('Duplicates on Master List')
        pprint(self.unmap_tuples(dupes_dict_2_flat, include_prefixes=False))

        # print('New Master List')
        # pprint(self.unmap_tuples(master_list))

        # import pdb;pdb.set_trace()
        # Print songs that are missing from the computer, and extra on the list
        # compare_lists = CompareLists(
        #     [item[0] for item in missing_songs_flat],
        #     [item[0] for item in extra_songs_flat]
        # )
        # pprint(compare_lists.all_items)
#########################################################################################################


if __name__ == '__main__':
    run()
