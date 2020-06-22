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
from pprint import pprint

from common import (
    list_music_file_names, move_file, remove_file_extension, rename_file_safe, list_music_files, has_file_extension
)
from fix_names import FixFileNames, acceptable_phrases
from paths import MUSIC_DIR, MUSIC_SCRIPT_DIR

POSSIBLE_RATINGS = ['', '-', '+', '++', '--']
ffn = FixFileNames()


def run():
    file_sorting_path = os.path.join(MUSIC_DIR, r'post_rock\to_sort')
    song_file_name = r'input\post_rock_songs_all_sorted.txt'
    song_file_path = os.path.join(file_sorting_path, song_file_name)

    song_file_dict = gather_file_names_from_path(file_sorting_path)
    song_rating_dict = read_song_file(song_file_path)

    song_file_list = MultiLevelList(song_file_dict, "Computer")
    song_rating_list = MultiLevelList(song_rating_dict, "Master List")

    diff = CompareMultiLevelLists(song_file_list, song_rating_list)
    diff.print_results()

    # new_master_list_file_name = r'output\new_master_list.txt'
    # diff.print_new_master_list(write_list_to_file=new_master_list_file_name)

    file_mover = ExecuteMove(file_sorting_path)
    file_mover.move_dupes(song_file_list.duplicate_items, commit=False)
    # file_mover.apply_diff(diff.reconciled_1, diff.reconciled_2, commit=False)


def gather_file_names_from_path(files_to_sort_path):
    return_dict = {}
    for rating in POSSIBLE_RATINGS:
        path = '\\'.join([char for char in rating])
        return_dict[rating] = list_music_files(os.path.join(files_to_sort_path, path))
    return return_dict


def read_song_file(song_file_path):
    song_rating_dict = {rating: [] for rating in POSSIBLE_RATINGS}

    # Read in every song from the Master List
    for song_title in open(song_file_path, 'r').readlines():
        regex = r'(^\+\+?|^--?)[^(-+)]'
        match = re.search(regex, song_title)
        rating = ''
        if match:
            rating = match.group(1)
        # Remove rating string and whitespace, and add to rating dictionary
        song_title = song_title[len(rating):].strip()
        song_rating_dict[rating].append(song_title)

    return song_rating_dict


class SongData(object):

    def __init__(self, name, rating):
        self.rating = rating
        self.raw_text = name
        self.id = self.simplify_file_name_fuzzier(name)

    @staticmethod
    def simplify_file_name_fuzzier(name):
        return ffn.get_new_name(remove_file_extension(name)).lower()

    @staticmethod
    def are_they_really_the_same(name_1, name_2):
        extra_data_1 = ''
        extra_data_2 = ''
        if ' (' in name_1:
            name_1, extra_data_1 = name_1.split(' (', 1)
        if ' (' in name_2:
            name_2, extra_data_2 = name_2.split(' (', 1)

        # if extra_data_1 and extra_data_2:
        #     if extra_data_1.startswith(extra_data_2) or extra_data_2.startswith(extra_data_1):
        #         return True  # Same

        if name_1 != name_2:
            return False  # Different

        if not extra_data_1 and not extra_data_2:
            return name_1 == name_2

        for phrase in acceptable_phrases + ['3', '4', '5']:
            if (phrase.lower() in extra_data_1) ^ (phrase.lower() in extra_data_2):
                return False  # Different

        # for phrase in ['6581', 'falls', 'ii', 'iii']:
        #     if name_1.endswith(phrase) ^ name_2.endswith(phrase):
        #         return False  # Different

        # return name_1 == name_2
        return True

        # for extra_data in [extra_data_1, extra_data_2]:
        #     if extra_data:
        #         for phrase in acceptable_phrases:
        #             if phrase.lower() in extra_data:
        #                 return False  # Different

        # if name_1 == name_2:
        #     return True  # Same

        # for phrase in ['6581', 'falls'] + ['ii', 'iii']:
        #     if name_1.endswith(phrase) ^ name_2.endswith(phrase):
        #         return False

    def __eq__(self, song_data):
        return self.are_they_really_the_same(self.id, song_data.id)
        # name_1 = self.id
        # name_2 = song_data.id
        # if name_1.startswith(name_2) or name_2.startswith(name_1):
        #     if self.are_they_really_the_same(self.id, song_data.id):
        #         return True
        # return False

    def __gt__(self, song_data):
        return self.id > song_data.id

    def __repr__(self):
        return self.rating + self.raw_text


class ListIterator(object):

    def __init__(self, starting_list):
        self.unique = []
        self.sorted_list = sorted(starting_list)
        self.total_items = len(self.sorted_list)
        self.list_pointer = 0
        self.current_item = ''
        self._set_current_item()

    def start_iteration(self):
        self.list_pointer = 0
        self._set_current_item()
        return self.current_item

    def get_next(self, unique=False):
        if unique:
            self.unique.append(self.current_item)
        self.advance_position()
        return self.current_item

    def advance_position(self):
        self.list_pointer += 1
        self._set_current_item()

    def _set_current_item(self):
        if self.list_pointer < self.total_items:
            self.current_item = self.sorted_list[self.list_pointer]
        else:
            self.current_item = None

    def __iter__(self):
        for item in self.sorted_list:
            yield item


class PrintList(object):

    @staticmethod
    def print_list(song_list, list_desc, print_full_list=False, write_list_to_file=None):
        list_length = str(len(song_list))
        print('--- ' + list_desc + ':\nCount: ' + list_length)
        if print_full_list:
            new_list_string = ''
            for item in song_list:
                new_list_string += item.rating + remove_file_extension(item.raw_text) + '\n'
                # new_list_string += item.id + '\n'  # Verbose

            if write_list_to_file:
                print('Outputting sorted list for "' + list_desc + '" to file: "' + write_list_to_file + '"')
                with open(write_list_to_file, 'w') as write_file:
                    write_file.write(new_list_string)
            else:
                print('--- Printing sorted list for "' + list_desc + '":')
                print(new_list_string)
            print('Total Output: ' + list_length + '\n--- END of "' + list_desc + '"')
        print('')


class MultiLevelList(object):
    printer = PrintList()

    def __init__(self, song_dict, name):
        self.name = name
        self.all_items = self._initialize_multi_level_list_from_dict(song_dict)
        self.duplicate_items = self.get_dupes()

    def get_sub_level(self, rating):
        return self.all_items.get(rating, [])

    @staticmethod
    def _initialize_multi_level_list_from_dict(song_dict):
        all_songs = {rating: [] for rating in POSSIBLE_RATINGS}
        for rating in POSSIBLE_RATINGS:
            songs = []
            for song_title in song_dict.get(rating, []):
                songs.append(SongData(song_title, rating))
            all_songs[rating] = ListIterator(songs)
        return all_songs

    def get_dupes(self):
        all_items = self.flatten_dict_to_sorted_tuples(self.all_items)  # , ['++', '--'])
        return self.extract_dupes(all_items)

    def print_results(self):
        all_items = self.flatten_dict_to_sorted_tuples(self.all_items)  # , ['++', '--'])
        self.printer.print_list(all_items, f'All Songs On {self.name}', print_full_list=False)
        self.printer.print_list(self.duplicate_items, f'Duplicates on {self.name}', print_full_list=True)

    @staticmethod
    def flatten_dict_to_sorted_tuples(song_dict):
        return sorted([item for rating, song_list in song_dict.items() for item in song_list])

    # @staticmethod
    # def flatten_dict_to_sorted_tuples(song_dict, ignore_keys):
    #     return sorted(
    #         [item for rating, song_list in song_dict.items() if rating not in ignore_keys for item in song_list],
    #     )

    @staticmethod
    def extract_dupes(item_list):
        dupes = []
        last_item = None
        for item in item_list:
            if last_item:
                if item == last_item:
                    dupes.append(item)
                    dupes.append(last_item)
            last_item = item
        return dupes


class CompareMultiLevelLists(object):
    printer = PrintList()

    def __init__(self, list_1, list_2):
        self.list_1 = list_1
        self.list_2 = list_2

        self.unique_to_list_1 = []
        self.unique_to_list_2 = []

        self.reconciled_1 = []
        self.reconciled_2 = []
        self.only_list_1 = []
        self.only_list_2 = []

        self.compute_diffs_for_all_levels()
        self.reconcile_unique_entries()

    def compute_diffs_for_all_levels(self):
        for rating in POSSIBLE_RATINGS:
            song_list_1 = self.list_1.get_sub_level(rating)
            song_list_2 = self.list_2.get_sub_level(rating)
            self.compute_list_diff(song_list_1, song_list_2)

            self.unique_to_list_1.extend(song_list_1.unique)
            self.unique_to_list_2.extend(song_list_2.unique)

    @staticmethod
    def compute_list_diff(list_1, list_2):
        item_1 = list_1.start_iteration()
        item_2 = list_2.start_iteration()

        while item_1 and item_2:
            if item_1 < item_2:
                item_1 = list_1.get_next(unique=True)
            elif item_1 > item_2:
                item_2 = list_2.get_next(unique=True)
            else:
                item_1 = list_1.get_next()
                item_2 = list_2.get_next()

        while item_2:
            item_2 = list_2.get_next(unique=True)
        while item_1:
            item_1 = list_1.get_next(unique=True)

    def print_results(self):
        self.list_1.print_results()
        self.printer.print_list(self.only_list_1, f'Only on {self.list_1.name}', print_full_list=False)
        self.list_2.print_results()
        self.printer.print_list(self.only_list_2, f'Only on {self.list_2.name}', print_full_list=False)
        self.printer.print_list(self.reconciled_1, f'Needs to move', print_full_list=True)
        # self.printer.print_list(self.reconciled_2, f'Needs to be moved to', print_full_list=True)

    def print_new_master_list(self, write_list_to_file=None):
        songs_on_list = self.list_2.flatten_dict_to_sorted_tuples(self.list_2.all_items)#, ['++', '--'])
        master_list = sorted(songs_on_list + self.only_list_1)
        self.printer.print_list(master_list, 'New Master List', print_full_list=True, write_list_to_file=write_list_to_file)

    def reconcile_unique_entries(self):
        # Invert one of the songs dictionary as `{song_name: data}` for easier lookup
        list_2_inverted = {list_item.id: list_item for list_item in self.unique_to_list_2}

        # Attempt to find unresolved names from list_1 in unresolved names from list_2
        for item in self.unique_to_list_1:
            print(f'Looking for: {item.raw_text}')

            if item.id not in list_2_inverted:
                self.only_list_1.append(item)
                continue

            lookup = list_2_inverted.get(item.id)
            self.reconciled_1.append(item)
            self.reconciled_2.append(lookup)
            print(f'Found "{item.raw_text}" in "{item.rating}"\nShould be at "{lookup.rating}"')

        fuck = [item.id for item in self.reconciled_2]
        self.only_list_2 = [item for item in self.unique_to_list_2 if item.id not in fuck]


class ExecuteMove(object):

    def __init__(self, base_directory):
        self.base_directory = base_directory

    def move_dupes(self, dupes_list, commit=False):
        for dupe_song in dupes_list:
            file_name = dupe_song.raw_text
            location = '\\'.join([char for char in dupe_song.rating])

            old_full_path = os.path.join(self.base_directory, location, file_name)
            new_full_path = os.path.join(self.base_directory, location, 'dupes', file_name)
            # print(f'Moving "{old_full_path}" to "{new_full_path}"')
            move_file(old_full_path, new_full_path, commit=commit)

    def apply_diff(self, move_from, move_to, commit=False):
        # import pdb;pdb.set_trace()
        move_to_inverted = {list_item.id: list_item for list_item in move_to}
        for data_from in move_from:
            data_to = move_to_inverted.get(data_from.id)
            file_name = data_from.raw_text
            location_from = '\\'.join([char for char in data_from.rating])
            location_to = '\\'.join([char for char in data_to.rating])

            old_full_path = os.path.join(self.base_directory, location_from, file_name)
            new_full_path = os.path.join(self.base_directory, location_to, file_name)
            # print(f'Moving "{old_full_path}" to "{new_full_path}"')
            move_file(old_full_path, new_full_path, commit=commit)


class Something(object):
    # TODO ???
    def check_something(self, not_on_computer, not_on_list):
        import pdb;pdb.set_trace()
        # Print songs that are missing from the computer, and extra on the list
        compare_lists = self.compute_list_merge(not_on_computer, not_on_list)
        pprint(compare_lists.all_items)

    @staticmethod
    def compute_list_merge(list_1, list_2):
        # Fresh Start
        list_1.re_init()
        list_2.re_init()

        merged_list = []
        while list_1.still_going() or list_2.still_going():

            # Merge lists sorted
            if list_1.current_item <= list_2.current_item:
                merged_list.append('1: ' + item_1)
                list_1.get_next()
            if list_1.current_item >= list_2.current_item:
                merged_list.append('2: ' + item_2)
                list_2.get_next()

        return merged_list


#########################################################################################################


if __name__ == '__main__':
    run()
