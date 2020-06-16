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
TODO What order?
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
    list_music_file_names, move_file, remove_file_extension, rename_file_safe
)
from fix_names import FixFileNames
from paths import MUSIC_DIR, MUSIC_SCRIPT_DIR

POSSIBLE_RATINGS = ['', '-', '+', '++', '--']

"""
TODO
Rearrange classes
Add process_diff and print_new_master_list to the diff class?
Invert dictionaries to list of tuples (name, rating) for easier parsing during the diff?
"""


def run():
    # song_file_name = r'input\test_master_list.txt'
    files_to_sort_path = os.path.join(MUSIC_DIR, r'post_rock\to_sort')
    song_file_name = r'input\post_rock_songs_all.txt'
    song_file_path = os.path.join(files_to_sort_path, song_file_name)

    # Terms: missing and extra are from the perspective of the computer
    song_rating_dict = read_song_file(song_file_path)
    song_list_diff = compute_diff(files_to_sort_path, song_rating_dict)
    missing_entirely, super_extra = process_diff(files_to_sort_path, song_list_diff.missing, song_list_diff.extra, song_list_diff.mapping)
    print_new_master_list(song_list_diff.all_songs, missing_entirely, super_extra)


def read_song_file(song_file_path):
    song_rating_dict = {rating: [] for rating in POSSIBLE_RATINGS}

    # Read in every song from the main list
    for song_title in open(song_file_path, 'r').readlines():
        regex = '^(\+\+?|--?)[^(-+)]'  # TODO Test
        match = re.match(regex, song_title)
        rating = ''
        if match:
            rating = match.group(0)

        # Clean title, remove rating string, and add to rating dictionary
        song_title = song_title[len(rating):].strip()
        song_rating_dict[rating].append(song_title)

    return song_rating_dict


def compute_diff(files_to_sort_path, song_rating_dict):
    song_list_diff = DiffFilesAgainstList(files_to_sort_path, song_rating_dict)

    for rating in POSSIBLE_RATINGS:
        song_list_diff.compute_diff_for_category(rating)

    return song_list_diff


def compute_diff_for_lists(list_1, list_2, name_1=None, name_2=None):
    """Find differences between two lists"""
    only_list_2 = []
    only_list_1 = []

    song_title_list_1 = SongList(list_1, name=name_1)
    song_title_list_2 = SongList(list_2, name=name_2)

    while song_title_list_1.current_song and song_title_list_2.current_song:

        string_1 = song_title_list_1.current_song
        string_2 = song_title_list_2.current_song

        if string_1 < string_2:
            only_list_1.append(string_1)
            song_title_list_1.advance_position()

        elif string_1 > string_2:
            only_list_2.append(string_2)
            song_title_list_2.advance_position()

        elif string_1 == string_2:
            # both.append(song_title_list_1.current_song)
            song_title_list_1.advance_position()
            song_title_list_2.advance_position()

    while song_title_list_1.current_song:
        only_list_1.append(song_title_list_1.current_song)
        song_title_list_1.advance_position()

    while song_title_list_2.current_song:
        only_list_2.append(song_title_list_2.current_song)
        song_title_list_2.advance_position()

    return only_list_2, only_list_1


class SongList(object):

    def __init__(self, starting_list, name=None):
        self.name = name
        self.sorted_list = sorted(starting_list)
        self.total_items = len(self.sorted_list)
        self.list_pointer = 0
        self.current_song = None
        self._set_current_song()

    def advance_position(self):
        # Having a name makes it verbose
        if self.name:
            print(self.name + ': ' + self.current_song)
        self.list_pointer += 1
        self._set_current_song()

    def _set_current_song(self):
        if self.list_pointer < self.total_items:
            file_name = self.sorted_list[self.list_pointer]
            self.current_song = remove_file_extension(file_name)
        else:
            self.current_song = None


class DiffFilesAgainstList(object):
    ffn = FixFileNames()

    def __init__(self, files_to_sort_path, song_rating_dict):
        self.all_songs = {}
        self.mapping = {}
        self.missing = {}
        self.extra = {}
        self.files_to_sort_path = files_to_sort_path
        self.song_rating_dict = song_rating_dict

    def simplify_file_name_fuzzier(self, name):
        return self.ffn.get_new_name(remove_file_extension(name)).lower()[:35]

    def simplify_list(self, song_list):
        simplified = []
        for song_title in song_list:
            song_title_simplified = self.simplify_file_name_fuzzier(song_title)
            simplified.append(song_title_simplified)
            if song_title_simplified not in self.mapping:
                self.mapping[song_title_simplified] = song_title
        return simplified

    def compute_diff_for_category(self, rating):

        path = '\\'.join([char for char in rating])
        list_1 = list_music_file_names(os.path.join(self.files_to_sort_path, path))
        list_2 = self.song_rating_dict.get(rating)
        self.all_songs[rating] = list_2

        missing, extra = compute_diff_for_lists(
            self.simplify_list(list_1),
            self.simplify_list(list_2)
        )

        self.missing[rating] = missing
        self.extra[rating] = extra


def process_diff(base_directory, missing_dict, extra_dict, mapping):
    extra_songs = {}
    could_not_find = {}
    resolved = []

    # Invert the extra songs dictionary as `{song_name: location}` for faster lookup
    for rating_group in extra_dict:
        for extra_song_name in extra_dict.get(rating_group, []):
            extra_songs[extra_song_name] = rating_group

    # Look for each missing song in the extra_songs list
    for rating_group in missing_dict:
        for missing_song_name in missing_dict.get(rating_group, []):
            real_name = mapping.get(missing_song_name)
            print(f'Looking for: {real_name}')

            rating = extra_songs.get(missing_song_name)
            if not rating:
                if rating_group not in could_not_find:
                    could_not_find[rating_group] = []
                could_not_find[rating_group].append(real_name)
                continue

            location = '\\'.join([char for char in rating])
            old_location = '\\'.join([char for char in rating_group])

            new_full_path = os.path.join(base_directory, location, real_name)
            old_full_path = os.path.join(base_directory, old_location, real_name)

            print(f'Found `{real_name}` in {rating}')
            print(f'Used to be at {rating_group}')

            # rename_file_safe(old_full_path, new_full_path, commit=False)

            resolved.append(missing_song_name)

    exists_with_no_log = {}
    for rating_group in extra_dict:
        exists_with_no_log[rating_group] = [
            mapping.get(song, 'ERROR') for song in extra_dict.get(rating_group) if song not in resolved
        ]
    return could_not_find, exists_with_no_log


#########################################################################################################


def print_new_master_list(songs_on_list, missing_dict, extra_dict):
    from pprint import pprint

    def flatten_dict(song_dict, ignore_keys):
        return [key + name for key, value in song_dict.items() if key not in ignore_keys for name in value]

    def remove_rating_prefix(song_name):
        for thing in ['-', '+']:
            while song_name.startswith(thing):
                song_name = song_name[1:]
        return song_name

    def sort_and_print(song_dict, message=None):
        song_list_flat = sorted(song_dict, key=remove_rating_prefix)
        if message:
            pprint(message)
            pprint(song_list_flat)
        return song_list_flat

    # pprint('songs_on_list')
    # pprint(songs_on_list)
    # pprint('Could Not Find on Computer')
    # pprint(missing_dict)
    # pprint('On Computer but not on Master List')
    # pprint(extra_dict)

    songs_on_list_flat = sort_and_print(flatten_dict(songs_on_list, ['++', '--']), message=None)   # 'All Songs on Computer'

    extra_songs_flat = sort_and_print(flatten_dict(extra_dict, []), message=None)  # 'Extra Songs on Computer'

    # inverted = sort_and_print(flatten_dict(songs_on_list, ['+', '-', '']), message='Removed From List')

    missing_songs_flat = sort_and_print(flatten_dict(missing_dict, []), message='Missing From Computer')

    # count_songs_on_computer = len(songs_on_list_flat) - len(missing_songs_flat) + len(extra_songs_flat)

    # Sort list and print list back out with updated ratings
    master_list = sort_and_print(songs_on_list_flat + extra_songs_flat, message='master_list')

    # pprint(extra_songs_flat)
    # pprint(missing_songs_flat)
    # Print songs that are missing from the computer, and extra on the list
    compute_diff_for_lists(missing_songs_flat, extra_songs_flat, name_1='MISSING', name_2='EXTRA  ')
#########################################################################################################


if __name__ == '__main__':
    run()
