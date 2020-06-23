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
This script will update the actual song file location on my HD to reflect
the master list, and update the master list for new or deleted files on the HD.
All songs will be moved to the correct HD folder corresponding to their
ratings on the list.

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

Print sorted list back out, along with other statistics regarding the names
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
fix_file_names = FixFileNames()


def run():
    file_sorting_path = os.path.join(MUSIC_DIR, r'post_rock\to_sort')
    song_file_name = r'input\post_rock_songs_all_sorted.txt'
    song_file_path = os.path.join(file_sorting_path, song_file_name)

    computer_file_list = gather_file_names_from_path(file_sorting_path)
    text_file_list = read_song_file(song_file_path)

    computer_song_data = SongDataList(computer_file_list, "Computer")
    text_song_data = SongDataList(text_file_list, "Master List")

    diff = CompareSongDataLists(computer_song_data, text_song_data)
    diff.print_results()

    file_mover = ExecuteMove(file_sorting_path)

    # Move ++ and -- rated songs
    # file_mover.move_completed(text_song_data.all_items, commit=False)

    file_mover.move_dupes(computer_song_data.duplicate_items, commit=False)

    # new_master_list_file_name = r'output\new_master_list.txt'
    # print_new_master_list(
    #     text_song_data.all_items,
    #     computer_song_data.get_unique(),
    #     write_list_to_file=new_master_list_file_name
    # )


def gather_file_names_from_path(files_to_sort_path):
    return [SongData(item) for item in list_music_files(files_to_sort_path)]


def read_song_file(song_file_path):
    song_data = []
    # Read in every song from the Master List
    for song_title in open(song_file_path, 'r').readlines():
        regex = r'(^\+\+?|^--?)[^(-+)]'
        match = re.search(regex, song_title)
        rating = ''
        if match:
            rating = match.group(1)
        # Remove rating string and whitespace, and add to rating dictionary
        song_title = song_title[len(rating):].strip()
        song_data.append(SongData(song_title, rating))

    return song_data


def print_new_master_list(songs_on_list, only_on_computer, write_list_to_file=None):
    remaining_songs = [song for song in songs_on_list if song.rating not in ['--', '++']]
    master_list = sorted(remaining_songs + only_on_computer)
    self.printer.print_list(master_list, 'New Master List', print_full_list=True, write_list_to_file=write_list_to_file)


class SongData(object):

    def __init__(self, name, rating=''):
        self.rating = rating
        self.raw_text = name
        self.id = self.simplify_file_name_fuzzier(name)

    @staticmethod
    def simplify_file_name_fuzzier(name):
        return fix_file_names.get_new_name(remove_file_extension(name)).lower()

    @staticmethod
    def are_they_really_the_same(name_1, name_2):

        def split_name_safe(name):
            if ' (' in name:
                return name.split(' (', 1)
            return name, None

        name_1, extra_data_1 = split_name_safe(name_1)
        name_2, extra_data_2 = split_name_safe(name_2)

        known_false_positives = ['falls', 'os 6581', 'ii', 'iii']
        for phrase in known_false_positives:
            if (name_1.endswith(phrase)) ^ (name_2.endswith(phrase)):
                return False  # Different

        min_len = min(len(name_1), len(name_2))
        same_song_root = name_1[:min_len] == name_2[:min_len]

        if not same_song_root:
            return False  # Different

        if not extra_data_1 and not extra_data_2:
            if len(name_1) - len(name_2) < 10:
                return same_song_root

        for phrase in acceptable_phrases + ['3', '4', '5']:
            check_phrase_1 = check_phrase_2 = False
            if extra_data_1:
                check_phrase_1 = phrase.lower() in extra_data_1
            if extra_data_2:
                check_phrase_2 = phrase.lower() in extra_data_2
            if check_phrase_1 ^ check_phrase_2:
                return False  # Different

        return name_1 == name_2

    def __eq__(self, song_data):
        return self.are_they_really_the_same(self.id, song_data.id)

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

    def __len__(self):
        return self.total_items


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


class SongDataList(object):
    printer = PrintList()

    def __init__(self, song_list, name):
        self.name = name
        self.all_items = ListIterator(song_list)
        self.duplicate_items = self.extract_dupes()

    def get_unique(self):
        return self.all_items.unique

    def print_results(self):
        self.printer.print_list(self.all_items, f'All Songs On {self.name}', print_full_list=False)
        self.printer.print_list(self.duplicate_items, f'Duplicates on {self.name}', print_full_list=True)

    def extract_dupes(self):
        dupes = []
        last_item = None
        for item in self.all_items:
            if last_item:
                if item == last_item:
                    dupes.append(item)
                    dupes.append(last_item)
            last_item = item
        return dupes


class CompareSongDataLists(object):
    printer = PrintList()

    def __init__(self, list_1, list_2):
        self.list_1 = list_1
        self.list_2 = list_2

    def compute_list_diff(self):
        list_1 = self.list_1
        list_2 = self.list_2

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
        self.printer.print_list(self.list_1.get_unique(), f'Only on {self.list_1.name}', print_full_list=False)
        self.list_2.print_results()
        self.printer.print_list(self.list_2.get_unique(), f'Only on {self.list_2.name}', print_full_list=False)


class ExecuteMove(object):

    def __init__(self, base_directory):
        self.base_directory = base_directory

    def move_dupes(self, dupes_list, commit=False):
        dupes_path = os.path.join(self.base_directory, 'dupes')
        for dupe_song in dupes_list:
            file_name = dupe_song.raw_text

            old_full_path = os.path.join(self.base_directory, file_name)
            new_full_path = os.path.join(dupes_path, file_name)
            # print(f'Moving "{old_full_path}" to "{new_full_path}"')
            move_file(old_full_path, new_full_path, commit=commit)

    def move_completed(self, completed, commit=False):

        destination_bad = os.path.join(self.base_directory, 'deleted')
        destination_good = os.path.join(self.base_directory, 'liked')
        # import pdb;pdb.set_trace()

        for data in completed:
            file_name = data.raw_text
            old_full_path = os.path.join(self.base_directory, file_name)
            if data.rating == '--':
                new_full_path = os.path.join(destination_bad, file_name)
            elif data.rating == '++':
                new_full_path = os.path.join(destination_good, file_name)
            else:
                continue
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
