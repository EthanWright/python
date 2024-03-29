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
import argparse
import copy
import os
import re
import time

from pprint import pprint

from common import list_music_file_names, list_music_files, remove_file_extension
from file_scripts_common import move_file, rename_file_safe
from fix_names import FixFileNames, song_version, SPACED_HYPHEN
from paths import Paths

fix_file_names = FixFileNames()


def run(actions):
    export_list = actions.export_list
    move_dupes = actions.move_dupes
    move_bad = actions.move_bad
    move_good = actions.move_good
    verbose = actions.verbose
    commit = actions.commit
    sub_directory = actions.sub_directory
    stats = actions.stats

    file_sorting_path = Paths.POST_ROCK
    if sub_directory:
        file_sorting_path = os.path.join(Paths.MUSIC, sub_directory)
    # txt_song_file_path = os.path.join(file_sorting_path, 'txt', 'master_list.txt')
    txt_song_file_path = os.path.join(Paths.TXT, 'master_list.txt')

    computer_file_list = gather_file_names_from_path(file_sorting_path)
    text_file_list = read_song_file(txt_song_file_path)

    computer_song_data = SongDataList(computer_file_list, "Computer")
    text_song_data = SongDataList(text_file_list, "Master List")
    song_differ = DiffSongLists(computer_song_data, text_song_data, commit=commit)
    # song_differ = DiffSongLists(
    #     (computer_file_list, "Computer"),
    #     (text_file_list, "Master List"),
    #     commit=commit
    # )

    if not export_list and not move_dupes and not move_bad and not move_good:
        song_differ.print_results()

    file_actions = FileActions(file_sorting_path, verbose=verbose, commit=commit)

    if stats:
        stats = song_differ.list_2.get_stats()
        pprint(stats)  # TODO Prettier

    if export_list:
        remove_song_ids = song_differ.list_2.get_bad_items()  # Don't include --
        remove_song_ids += song_differ.list_2.get_good_items()  # Don't include ++  TODO Double check I don't remove songs still in trim
        #for item_ in song_differ.list_2.get_good_ids():
        #    print(item_)
        all_songs = text_file_list + song_differ.unique_1
        # all_songs = sorted(all_songs)  # TODO Did this help?
        all_songs = sorted([song for song in all_songs if song not in remove_song_ids])

        file_actions.export_new_master_list_to_file(all_songs)

    # TODO Make file moving functions simpler and more generic

    if move_dupes:
        # Move duplicate files on computer
        dupes = song_differ.list_1.duplicate_items
        file_actions.move_songs(dupes, 'dupes', export_logs=False)

    if move_bad:
        # Get -- songs from the text file, then get file names from the file list
        bad_songs = song_differ.list_2.get_bad_items()

        # TODO This is the old method
        bad_song_file_names = [item for item in song_differ.list_1 if item in bad_songs]

        # TODO What about this instead?
        # bad_song_data = SongDataList(bad_songs, "Master List")
        # song_differ_2 = DiffSongLists(computer_song_data, bad_song_data, commit=commit)
        # bad_song_file_names = song_differ_2.intersection

        file_actions.move_songs(bad_song_file_names, 'delete')

    if move_good:
        # Get ++ songs from the text file, then get file names from the file list
        good_songs = song_differ.list_2.get_good_items()

        # TODO This is the old method
        good_song_file_names = [item for item in song_differ.list_1 if item in good_songs]

        # TODO What about this instead?
        # good_song_data = SongDataList(good_songs, "Master List")
        # song_differ_2 = DiffSongLists(computer_song_data, good_song_data, commit=commit)
        # good_song_file_names = song_differ_2.intersection

        file_actions.move_songs(good_song_file_names, 'good')


def gather_file_names_from_path(files_to_sort_path):
    return [SongData(item) for item in list_music_files(files_to_sort_path)]


def read_song_file(song_file_path):
    song_data = []
    # Read in every song from the Master List
    for song_title in open(song_file_path, 'r').readlines():
        rating = ''
        regex = r'(^\+\+?|^--?)[^(-+)]'
        match = re.search(regex, song_title)
        if match:
            rating = match.group(1)
        # Remove rating string and whitespace, and add to rating dictionary
        song_title = song_title[len(rating):].strip().replace('.', '')
        song_data.append(SongData(song_title, rating))

    return song_data


class DiffSongLists(object):
    def __init__(self, list_data_1, list_data_2, commit=False):
        self.commit = commit
        self.list_1 = list_data_1
        self.list_2 = list_data_2
        # self.list_1 = SongDataList(list_data_1[0], list_data_1[1])
        # self.list_2 = SongDataList(list_data_2[0], list_data_2[1])
        self.unique_1 = []
        self.unique_2 = []
        self.compute_list_diff()

    def advance_list_1(self):
        self.unique_1.append(self.list_1.current_item)
        return self.list_1.get_next()

    def advance_list_2(self):
        self.unique_2.append(self.list_2.current_item)
        return self.list_2.get_next()

    def compute_list_diff(self):
        item_1 = self.list_1.start_iteration()
        item_2 = self.list_2.start_iteration()

        while item_1 and item_2:
            if item_1 < item_2:
                item_1 = self.advance_list_1()
            elif item_1 > item_2:
                item_2 = self.advance_list_2()
            else:
                item_1 = self.list_1.get_next()
                item_2 = self.list_2.get_next()

        while item_2:
            item_2 = self.advance_list_2()
        while item_1:
            item_1 = self.advance_list_1()

    def print_results(self):
        list_outputter = ListOutputter()
        self.list_1.print_results()
        list_outputter.print_list(self.unique_1, f'Only on {self.list_1.name}', print_full_list=True)  # Computer Only
        self.list_2.print_results()

        # Master List No Rating Only
        # no_rating = [item for item in self.unique_2 if item.rating == '']
        # list_outputter.print_list(no_rating, f'Only on {self.list_2.name}', print_full_list=True)

        # Master List Only
        list_outputter.print_list(self.unique_2, f'Only on {self.list_2.name}', print_full_list=True)


class SongData(object):

    def __init__(self, name, rating=''):
        self.rating = rating
        self.raw_text = name
        self.id = self.simplify_file_name_fuzzier(name)

    @staticmethod
    def simplify_file_name_fuzzier(name):
        if '.' in name:
            name = remove_file_extension(name)

        name = fix_file_names.get_new_name(name).lower()

        # TODO Can song_info_prefix be used here?
        # TODO Is this a good spot to do this?
        phrase_trimmed = '(trimmed)'
        if phrase_trimmed in name:
            name = name.replace(phrase_trimmed, '')

        #phrase_feat = '(feat '
        #if phrase_feat in name:
        #    name, extra = name.split(phrase_feat, 1)
        #    unneeded, extra = extra.split(')', 1)
        #    name += extra

        return name.strip()

    @staticmethod
    def are_they_really_the_same(name_1, name_2):

        def split_name_safe(name):
            name = name.replace('  ', ' ').strip()
            if ' (' in name:
                return name.split(' (', 1)
            return name, None

        name_1, extra_data_1 = split_name_safe(name_1)
        name_2, extra_data_2 = split_name_safe(name_2)

        if abs(len(name_1) - len(name_2)) > 5:
            return False  # Different

        roman_numerals = [' i', ' ii', ' iii', ' iv', ' v', ' vi']
        for phrase in roman_numerals:
            if (name_1.endswith(phrase)) ^ (name_2.endswith(phrase)):
                return False  # Different

        # If they BOTH end with a digit, but it's a different digit, return False
        digits = [str(x) for x in range(10)]
        if name_1[-1] in digits and name_2[-1] in digits and name_1[-1] != name_2[-1]:
            return False  # Different

        min_len = min(len(name_1), len(name_2))
        same_song_root = name_1[:min_len] == name_2[:min_len]
        if not same_song_root:
            return False  # Different

        if not extra_data_1 and not extra_data_2:
            #known_false_positives = ['interlude']
            #for false_positive in known_false_positives:
            #    if false_positive in name_1 and false_positive in name_2:
            #        return False  # Different
            return same_song_root

        for phrase in song_version:
            check_phrase_1 = check_phrase_2 = False
            if extra_data_1:
                check_phrase_1 = phrase.lower() in extra_data_1
            if extra_data_2:
                check_phrase_2 = phrase.lower() in extra_data_2
            if check_phrase_1 ^ check_phrase_2:
                return False  # Different

        if extra_data_1 and not extra_data_2:
            return 'feat' in extra_data_1
        if extra_data_2 and not extra_data_1:
            return 'feat' in extra_data_2

        if extra_data_1 and extra_data_2:
            return extra_data_1 == extra_data_2
            # TODO Delete? What was this for?
            # if ')' in extra_data_1 and ')' in extra_data_2:
            #     phrase_1, more_1 = extra_data_1.split(')', 1)
            #     phrase_2, more_2 = extra_data_2.split(')', 1)
            #     if phrase_1 != phrase_2:
            #         return False
            #     return more_1 == more_2
            #     if more_1 != more_2:
            #         return False
            #     if more_1.startswith(SPACED_HYPHEN) and more_2.startswith(SPACED_HYPHEN):
            #         return more_1 == more_2
            #     return True

        return name_1 == name_2

    def __eq__(self, song_data):
        return self.are_they_really_the_same(self.id, song_data.id)

    def __gt__(self, song_data):
        if self == song_data:
            return False
        return self.id > song_data.id

    def __repr__(self):
        return self.rating + self.raw_text + ' (' + self.id + ')'
        # return self.rating + self.raw_text


class SongDataList(object):

    def __init__(self, starting_list, name):
        self.name = name
        self.sorted_list = sorted(starting_list)
        self.total_items = len(self.sorted_list)
        self._duplicate_items = None
        self.bad_ratings = None
        self.good_ratings = None
        self.list_pointer = 0
        self.current_item = ''
        self._set_current_item()

    def start_iteration(self):
        self.list_pointer = 0
        self._set_current_item()
        return self.current_item

    def get_next(self):
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

    def print_results(self):
        list_outputter = ListOutputter()
        list_outputter.print_list(self, f'All Songs On {self.name}', print_full_list=False)
        list_outputter.print_list(self.duplicate_items, f'Duplicates on {self.name}', print_full_list=True)

    def get_bad_items(self):
        if not self.bad_ratings:
            self.bad_ratings = [item for item in self if item.rating == '--']
        return self.bad_ratings

    def get_good_items(self):
        if not self.good_ratings:
            self.good_ratings = [item for item in self if item.rating == '++']
        return self.good_ratings

    def get_stats(self):
        # Count ratings
        rating_dict = {}
        for item in self:
            if item.rating not in rating_dict:
                rating_dict[item.rating] = 0
            rating_dict[item.rating] += 1

        # TODO Cache list counts per rating?
        # self.cached_stats = rating_dict
        return rating_dict

    @property
    def duplicate_items(self):
        if not self._duplicate_items:
            self._duplicate_items = self._extract_dupes()
        return self._duplicate_items

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


class ListOutputter(object):

    @staticmethod
    def print_list(song_list, list_desc, print_full_list=False):
        list_length = str(len(song_list))
        print('--- ' + list_desc + ':\nCount: ' + list_length)

        if print_full_list:
            new_list_string = '\n'.join(
                [item.rating + remove_file_extension(item.raw_text) for item in song_list]  # + item.id
            )

            print('--Printing sorted list for "' + list_desc + '":')
            if new_list_string:
                print(new_list_string)
            print('--Printed: "' + list_length + '" items for "' + list_desc + '"')
        print('')

    @staticmethod
    def export_list_to_file(song_list, file_path, commit=False):

        print('Outputting sorted Master List to file: "' + file_path + '"')
        list_length = str(len(song_list))
        print('Total Lines In List: ' + list_length + '\n')

        if os.path.isfile(file_path):
            raise Exception('File already exists: "' + file_path + '"')

        new_list_string = '\n'.join(
            [item.rating + remove_file_extension(item.raw_text) for item in song_list]
        ) + '\n'

        if commit:
            with open(file_path, 'w') as write_file:
                write_file.write(new_list_string)
        else:
            print('Not Actually writing to file. Supply the "--commit" flag to do so.')


class FileActions(object):

    def __init__(self, song_directory, verbose=0, commit=False):
        self.song_directory = song_directory
        self.verbose = verbose
        self.commit = commit

    def export_new_master_list_to_file(self, master_list):
        file_path = os.path.join(Paths.TXT, 'new_master_list.txt')
        list_outputter = ListOutputter()
        list_outputter.export_list_to_file(master_list, file_path, self.commit)

    def move_songs(self, song_data_list, destination_dir, export_logs=True):
        print('Moving ' + str(len(song_data_list)) + ' song files to: "' + destination_dir + '"')
        destination_path = os.path.join(Paths.PROCESSING, destination_dir)

        for song_data in song_data_list:
            file_name = song_data.raw_text
            if self.verbose >= 1:
                print(f'Moving "{file_name}" to {destination_dir}')

            old_full_path = os.path.join(self.song_directory, file_name)
            new_full_path = os.path.join(destination_path, file_name)
            if self.commit:
                move_file(old_full_path, new_full_path, verbose=self.verbose, commit=self.commit)

        if self.commit and export_logs:
            all_songs_string = '\n'.join([song_data.raw_text for song_data in song_data_list]) + '\n'

            # Write songs to cumulative list in a txt file
            file_name = f'all_files_{destination_dir}.txt'
            file_path = os.path.join(Paths.TXT, file_name)
            with open(file_path, 'a') as write_file:
                write_file.write(all_songs_string)

            # Write changes from this run to its own file
            this_run_file_name = time.strftime('%Y_%m_%d_%H_%M_%S') + '.txt'
            file_path = os.path.join(Paths.TXT, this_run_file_name)
            with open(file_path, 'w') as write_file:
                write_file.write(all_songs_string)


#########################################################################################################


if __name__ == '__main__':
    default_path = Paths.POST_ROCK
    parser = argparse.ArgumentParser(description='Compare Songs to Master List and sort according to the rules')
    parser.add_argument('sub_directory', nargs='?', default=default_path, help='Target Sub Directory')
    parser.add_argument('--commit', action='store_true', help='Commit File Changes')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    parser.add_argument('--export-list', action='store_true', help='Print New Master List')
    parser.add_argument('--move-dupes', action='store_true', help='Move duplicate files on the computer somewhere else')
    parser.add_argument('--move-bad', action='store_true', help='Move bad files on the computer somewhere else')
    parser.add_argument('--move-good', action='store_true', help='Move good files on the computer somewhere else')
    parser.add_argument('--stats', action='store_true', help='Print out statistics for the ratings in the text file')

    run(parser.parse_args())


"""
python sort_songs.py --stats
"""

""" Find dupe file names in directory
print(SongDataList(gather_file_names_from_path(args.directory), "Dir").duplicate_items)
"""
