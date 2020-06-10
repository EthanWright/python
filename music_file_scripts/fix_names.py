"""
Rename Songs according to my liking

Ethan Wright - 6/10/20
"""

import copy
import os
import re

from string_definitions import *
from functools import reduce


class FixFileNames(object):

    def __init__(self, commit=False):
        self.editor = StringEditor()
        self.commit = commit
        if not self.commit:
            print('NOT ', end='', flush=True)
        print("Commiting Changes")

    def fix_file_names(self, directory):
        for file_name in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file_name)):
                self.fix_file_name(directory, file_name)

        self.editor.stats.print_final_report()

    def fix_file_name(self, directory, file_name):
        song_title, extension = file_name.rsplit('.', 1)
        if extension not in invalid_extensions:
            new_song_title = self.get_new_name(song_title)
            self.editor.check_formatting(new_song_title)
            new_file_name = new_song_title + '.' + extension

            self.editor.rename_file(
                os.path.join(directory, file_name),
                os.path.join(directory, new_file_name),
                commit=self.commit  # DO YOU ACTUALLY WANT TO RENAME THE FILE?
            )

    def get_new_name(self, file_name):
        new_name = copy.deepcopy(file_name)

        # Remove specified substrings
        new_name = self.remove_specified_substrings(new_name)

        # Replace specified substrings
        new_name = self.replace_specified_substrings(new_name)

        # Find parts of the title that potentially should be removed
        new_name = self.handle_bad_strings(new_name)

        # Check for weird characters and attempt to replace or remove them
        new_name = self.replace_invalid_chars(new_name)

        # Clean up any potential lingering issues
        new_name = self.clean_whitespace_and_cruft(new_name)

        # If there is a remix artist, extract it, and prepend it to the file_name
        new_name = self.add_remix_artist(new_name)

        return new_name

    def remove_specified_substrings(self, name):
        return reduce(self.editor.remove_string, remove_strings, name)

    def replace_specified_substrings(self, name):
        return reduce(lambda x, y: self.editor.replace_string(x, *y), replace_strings, name)

    def handle_bad_strings(self, name):
        return reduce(self.editor.remove_string, self.editor.find_bad_string_patterns(name), name)

    def replace_invalid_chars(self, name):
        return reduce(self.editor.replace_invalid_char, self.editor.find_invalid_chars(name), name)

    def clean_whitespace_and_cruft(self, name):
        return self.editor.clean_whitespace_and_cruft(name)

    def add_remix_artist(self, name):
        return self.editor.add_remix_artist(name)


class StringEditor(object):

    def __init__(self):
        self.stats = Stats()

    def replace_string(self, name, find_val, replace_val):
        if find_val not in name:
            return name

        if not replace_val:
            return remove_string(name, find_val)

        self._log(f'\'{find_val}\' is going to replaced with \'{replace_val}\' in\n{name}')
        self.stats.replaced.append(find_val)
        return self._execute_replace(name, find_val, replace_val)

    def crop_string(self, name, start, end):
        removed_string, remaining_string = self._execute_crop(name, start, end)
        self._log(f'\'{name}\' is going to be cropped of \'{removed_string}\'')
        self.stats.removed.append(removed_string)
        return remaining_string

    def remove_string(self, name, bad_string):
        if bad_string not in name:
            return name
        self._log(f'\'{bad_string}\' Is going to be Removed in\n{name}')
        self.stats.removed.append(bad_string)
        return self._execute_replace(name, bad_string, '')

    def add_remix_artist(self, name):
        remix_artist = self.extract_remix_artist(name)
        if not remix_artist or self.already_has_remix_artist(name, remix_artist):
            return name

        self._log(f'Pre-pending Remix Artist: \'{remix_artist}\'')
        self.stats.remixed.append(remix_artist)
        return remix_artist + ' - ' + name

    def process_unhandled_char(self, name, invalid_char):
        print(f'unhandled Character found: {invalid_char} (' + str(ord(invalid_char)) + f') No replacement provided.\n{name}')
        self._log(f'unhandled Character found: {invalid_char} (' + str(ord(invalid_char)) + ') No replacement provided')
        self.stats.unhandled.append(invalid_char)

    def replace_invalid_char(self, name, invalid_char):

        replacement_char = self.get_invalid_char_replacement(invalid_char)

        if replacement_char == invalid_char:
            # Unhandled case
            self.process_unhandled_char(name, invalid_char)
            return name

        elif not replacement_char:
            return self.remove_string(name, invalid_char)

        else:
            return self.replace_string(name, invalid_char, replacement_char)

    def find_bad_string_patterns(self, name):
        bad_strings = []
        for regex in potential_problem_regexes:
            potentially_bad = re.findall(regex, name)
            for match in potentially_bad:
                if self.is_it_actually_bad(match):
                    bad_strings.append(match)

        return bad_strings

    def clean_whitespace_and_cruft(self, name):

        while '  ' in name:
            name = self.replace_string(name, '  ', ' ')

        # Remove cruft from the start and end
        for regex in ['^[-_ ]+', '[-_ ]+$']:
            cruft = re.search(regex, name)
            if cruft:
                name = self.crop_string(name, cruft.start(), cruft.end())

        return name

    def check_formatting(self, name):
        # Ensure formatting is correct
        if ' - ' not in name:
            return False

        # Is there repetitive information in the title?
        sections = name.lower().strip().split(' - ')
        length = len(sections)
        if length > 2:
            for x in range(length):
                for y in range(length):
                    if y != x and sections[x] in sections[y] and 'mix' not in sections[y].lower():
                        self.stats.improper_formatting.append(name)
                        return False
        return True

    def rename_file(self, current_name, new_name, commit=False):
        self._log(f'Original |{current_name}\nUpdated  |{new_name}\n')
        if commit:
            os.rename(current_name, new_name)

    ######################################################
    ### String Utils ###
    ######################################################

    @staticmethod
    def find_strings_to_replace(name):
        return [replace_data for replace_data in replace_strings if replace_data[0] in name]

    @staticmethod
    def find_strings_to_remove(name):
        return [string_ for string_ in remove_strings if string_ in name]

    @staticmethod
    def get_invalid_char_replacement(invalid_char):
        ascii_code = ord(invalid_char)
        if ascii_code in remove_char_codes:
            return None

        return replace_chars_mapping.get(ascii_code, invalid_char)

    @staticmethod
    def is_it_actually_bad(string_to_check):
        for good_regex in acceptable_regexes:
            if re.findall(good_regex, string_to_check):
                return False
        for phrase in acceptable_phrases:
            if phrase.lower() in string_to_check.lower():
                return False
        return True

    @staticmethod
    def find_invalid_chars(name):
        return [char for char in name if (ord(char) >= 128 or ord(char) < 32) or not char.isascii()]

    @staticmethod
    def extract_remix_artist(name):
        if 'remix' in name or 'Remix' in name:
            regex = '[\[\(]([^\]^\)]*)[ _-][rR]emix[\)\]]'
            # regex2 = '[\[\(]([^\]^\)]*)[ _-]([rR]e?)?[mM]ix[\)\]]'  # TODO Test
            remix_artist = re.findall(regex, name)
            if remix_artist:
                return remix_artist[0]
        return name

    @staticmethod
    def already_has_remix_artist(name, remix_artist):
        first_chunk = name.split(' - ', 1)[0].lower()
        if name.startswith(remix_artist.lower()) or first_chunk in remix_artist.lower():
            return True
        return False

    @staticmethod
    def _execute_replace(name, find_val, replace_val):
        return name.replace(find_val, replace_val)

    @staticmethod
    def _execute_crop(name, start, end):
        return name[start:end], name[0:start] + name[end:-1]

    @staticmethod
    def _log(message):
        return
        print(message)


######################################################
### Stats ###
######################################################

class Stats(object):

    def __init__(self):
        # Stats
        self.unhandled = []
        self.removed = []
        self.replaced = []
        self.remixed = []
        self.improper_formatting = []

    def print_final_report(self):

        stats_output = [
            {'title': 'REMOVED', 'data': self.removed},
            {'title': 'REPLACED', 'data': self.replaced},
            {'title': 'REMIX ARTIST ADDED', 'data': self.remixed},
        ]
        problems_output = [
            {'title': 'UNHANDLED', 'data': self.unhandled},
            {'title': 'IMPROPER FORMATTING', 'data': self.improper_formatting, 'simple': True},
        ]
        output_categories = [
            {'title': 'STATS', 'data': stats_output},
            {'title': 'PROBLEMS', 'data': problems_output},
        ]

        for item in output_categories:
            # title = item.get('title')
            # print(f'\n~~~~~~~ {title} ~~~~~~~')
            print('\n' + '~' * 7 + ' ' + item.get('title') + ' ' + '~' * 7)

            for data in item.get('data'):
                stats_name = data.get('title')
                stats_list = data.get('data')
                print(f'\n--- {stats_name}: ' + str(len(stats_list)))

                if data.get('simple'):
                    for name in stats_list:
                        print(f'{name}')

                else:
                    stats_dict = {}
                    for item in stats_list:
                        stats_dict[item] = stats_dict.get(item, 0) + 1
                    for item in reversed(sorted(stats_dict.items(), key=lambda x: x[1])):
                        print(f' \'{item[0]}\' : {item[1]}')


########################################################################################################

if __name__ == '__main__':

    music_directory = r'C:\Users\Mimorox\Documents\Music\post_rock\full_albums\liked\individual_songs'

    # commit = True  # DO YOU ACTUALLY WANT TO RENAME THE FILE?
    commit = False
    name_fixer = FixFileNames(commit)
    name_fixer.fix_file_names(music_directory)

########################################################################################################
