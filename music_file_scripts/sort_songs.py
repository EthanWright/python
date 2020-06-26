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
from fix_names import FixFileNames, song_version
from paths import MUSIC_DIR, MUSIC_SCRIPT_DIR

fix_file_names = FixFileNames()


def run():
    file_sorting_path = os.path.join(MUSIC_DIR, r'post_rock\to_sort')
    song_file_path = os.path.join(file_sorting_path, r'list\master_list.txt')

    commit = False
    song_differ = DiffSongLists(file_sorting_path, song_file_path, commit=commit)
    song_differ.print_results()
    # song_differ.print_new_master_list()
    # song_differ.print_songs_to_move()
    # song_differ.move_dupes()
    # song_differ.move_completed()


class DiffSongLists(object):
    def __init__(self, file_sorting_path, song_file_path, commit=False):
        self.file_sorting_path = file_sorting_path
        self.song_file_path = song_file_path
        self.commit = commit

        self.printer = PrintList()
        self.computer_song_data = None
        self.text_song_data = None
        self.diff = None
        self._read_in_lists()
        self._perform_diff()

    def _read_in_lists(self):

        computer_file_list = gather_file_names_from_path(self.file_sorting_path)
        text_file_list = read_song_file(self.song_file_path)

        self.computer_song_data = SongDataList(computer_file_list, "Computer")
        self.text_song_data = SongDataList(text_file_list, "Master List")

    def _perform_diff(self):
        self.diff = CompareSongDataLists(self.computer_song_data, self.text_song_data)

    def print_results(self):
        self.diff.print_results(self.printer)

    def move_dupes(self):
        file_mover = FileMover(self.file_sorting_path)
        file_mover.move_dupes(self.computer_song_data.duplicate_items, commit=self.commit)

    def move_completed(self):
        file_mover = FileMover(self.file_sorting_path)
        file_mover.move_completed(self.text_song_data, commit=self.commit)

    def print_new_master_list(self):
        file_path = None
        if self.commit:
            file_path = os.path.join(MUSIC_DIR, r'post_rock\to_sort\list\new_master_list.txt')
        list_parser = ParseResultsForPrinting(self.text_song_data, self.printer)  # TODO Duplicated
        list_parser.add_list_to_remaining(self.diff.unique_1)
        list_parser.print_new_master_list(write_list_to_file=file_path)

    def print_songs_to_move(self):
        # Print -- or ++ songs
        list_parser = ParseResultsForPrinting(self.text_song_data, self.printer)  # TODO Duplicated
        list_parser.print_good_songs()
        list_parser.print_bad_songs()


class ParseResultsForPrinting(object):

    def __init__(self, song_list, printer):
        self.printer = printer
        self.good = []
        self.bad = []
        self.remaining_songs = []
        self._parse(song_list)

    def print_bad_songs(self, print_full_list=False):
        self.printer.print_list(self.bad, 'Bad', print_full_list=print_full_list)

    def print_good_songs(self, print_full_list=False):
        self.printer.print_list(self.good, 'Good', print_full_list=print_full_list)

    def add_list_to_remaining(self, new_list):
        self.remaining_songs = self.remaining_songs + new_list

    def print_new_master_list(self, write_list_to_file=None):
        master_list = sorted(self.remaining_songs)
        self.printer.print_list(master_list, 'New Master List', print_full_list=True, write_list_to_file=write_list_to_file)

    def _parse(self, song_list):
        for song in song_list:
            if song.rating == '--':
                self.good.append(song)
            elif song.rating == '++':
                self.bad.append(song)
            # else:
            #     self.remaining_songs.append(song)
            # TODO
            self.remaining_songs.append(song)


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

        for phrase in song_version + ['3', '4', '5']:
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
        if self.are_they_really_the_same(self.id, song_data.id):
            return False
        return self.id > song_data.id

    def __repr__(self):
        return self.rating + self.raw_text


class SongDataList(object):

    def __init__(self, starting_list, name):
        self.name = name
        self.sorted_list = sorted(starting_list)
        self.total_items = len(self.sorted_list)
        self.duplicate_items = self._extract_dupes()
        # self.unique = []
        self.list_pointer = 0
        self.current_item = ''
        self._set_current_item()

    def start_iteration(self):
        self.list_pointer = 0
        self._set_current_item()
        return self.current_item

    def get_next(self):
        # if unique:
        #     self.unique.append(self.current_item)
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

    def print_results(self, printer):
        printer.print_list(self, f'All Songs On {self.name}', print_full_list=False)
        printer.print_list(self.duplicate_items, f'Duplicates on {self.name}', print_full_list=True)

    def _extract_dupes(self):
        dupes = []
        last_item = None
        for item in self:
            if last_item:
                if item == last_item:
                    dupes.append(item)
                    dupes.append(last_item)
            last_item = item
        return dupes

    def __iter__(self):
        for item in self.sorted_list:
            yield item

    def __len__(self):
        return self.total_items


class CompareSongDataLists(object):

    def __init__(self, list_1, list_2):
        self.list_1 = list_1
        self.list_2 = list_2
        self.unique_1 = []
        self.unique_2 = []
        self.compute_list_diff()

    def advance_list_1(self, item=None):
        if item:
            self.unique_1.append(item)
        return self.list_1.get_next()

    def advance_list_2(self, item=None):
        if item:
            self.unique_2.append(item)
        return self.list_2.get_next()

    def compute_list_diff(self):
        item_1 = self.list_1.start_iteration()
        item_2 = self.list_2.start_iteration()

        while item_1 and item_2:
            if item_1 < item_2:
                item_1 = self.advance_list_1(item_1)
            elif item_1 > item_2:
                item_2 = self.advance_list_2(item_2)
            else:
                item_1 = self.advance_list_1()
                item_2 = self.advance_list_2()

        while item_2:
            item_2 = self.advance_list_2(item_2)
        while item_1:
            item_1 = self.advance_list_1(item_1)

    def print_results(self, printer):
        self.list_1.print_results(printer)
        printer.print_list(self.unique_1, f'Only on {self.list_1.name}', print_full_list=False)
        self.list_2.print_results(printer)
        printer.print_list(self.unique_2, f'Only on {self.list_2.name}', print_full_list=False)


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


class FileMover(object):

    def __init__(self, base_directory, verbose=0):
        self.base_directory = base_directory
        self.verbose = verbose

    def move_dupes(self, dupes_list, commit=False):
        dupes_path = os.path.join(self.base_directory, r'issues\dupes')
        for dupe_song in dupes_list:
            file_name = dupe_song.raw_text

            old_full_path = os.path.join(self.base_directory, file_name)
            new_full_path = os.path.join(dupes_path, file_name)
            # print(f'Moving "{old_full_path}" to "{new_full_path}"')
            move_file(old_full_path, new_full_path, commit=commit)

    def move_completed(self, items, commit=False):

        destination_bad = os.path.join(self.base_directory, 'deleted')
        destination_good = os.path.join(self.base_directory, 'liked')
        # import pdb;pdb.set_trace()

        for data in items:
            file_name = data.raw_text
            if data.rating == '--':
                new_full_path = os.path.join(destination_bad, file_name)
            elif data.rating == '++':
                new_full_path = os.path.join(destination_good, file_name)
            else:
                continue
            old_full_path = os.path.join(self.base_directory, file_name)
            # print(f'Moving "{old_full_path}" to "{new_full_path}"')
            move_file(old_full_path, new_full_path, commit=commit)


#########################################################################################################


if __name__ == '__main__':
    run()
