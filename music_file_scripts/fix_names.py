"""
Rename Songs according to my liking

Ethan Wright - 6/10/20
"""
import argparse
import copy
import os
import re

from string_definitions import *
from functools import reduce

from common import list_music_files, rename_file_safe, invalid_music_extensions
from paths import MUSIC_DIR, POST_ROCK_DIR, POST_ROCK_NEW_ALBUMS_DIR


class RenameFilesInDir(object):

    def __init__(self, verbose=False, commit=False):
        self.editor = StringEditor(verbose=verbose, commit=commit)

    def fix_file_names(self, directory, recursive=False):
        self.editor.print_is_commit_true_or_false()
        if recursive:
            self._fix_file_names_recursive(directory)
        else:
            self._fix_file_names(directory)

        self.editor.stats.print_final_report()

    def _fix_file_names_recursive(self, directory):
        for path_name in os.listdir(directory):
            full_path = os.path.join(directory, path_name)
            if os.path.isdir(full_path):
                self._fix_file_names_recursive(full_path)
        self._fix_file_names(directory)

    def _fix_file_names(self, directory):
        for file_name in list_music_files(directory):
            self.fix_file_name(directory, file_name)

    def fix_file_name(self, directory, file_name):
        self.editor.log_message(f'Checking: "{file_name}"', level=2)
        song_title, extension = file_name.rsplit('.', 1)
        if extension not in invalid_music_extensions:
            new_song_title = self.get_new_name(song_title)
            self.extra_actions(new_song_title)
            if new_song_title != song_title:
                new_file_name = new_song_title + '.' + extension
                self.editor.rename_file(directory, file_name, new_file_name)

    def extra_actions(self, file_name):
        pass

    def get_new_name(self, file_name):
        raise NotImplementedError()


class CapitalizeArtist(RenameFilesInDir):

    def get_new_name(self, file_name):
        new_name = copy.deepcopy(file_name)
        caps_name = self.capitalize_artist(new_name)
        if caps_name != new_name:
            # new_name = join('renamed', caps_name)
            new_name = caps_name
        return new_name

    def capitalize_artist(self, name):
        new_words = []
        should_be_lower = [
            'the', 'of', 'if', 'is', 'in', 'an', 'a', 'to', 'too', 'or', 'and', 'by', 'at', 'for'
        ]

        artist, title = name.split(' - ', 1)
        if len(artist) <= 6 and artist[0] == artist[0].upper():
            return name

        all_caps = artist == artist.upper()

        words = artist.split(' ')
        if len(words) <= 2 and len(artist) <= 8 and all_caps:
            return name

        for word in words:
            first_letter = word[0]
            word_lower = word.lower()
            some = word[1:]
            if word == word.upper() and not all_caps:
                word_formatted = word
            elif word_lower in should_be_lower and len(new_words) > 0:
                word_formatted = word_lower
            elif (len(word) == 1 and word != 'i' and len(new_words) > 0) or not first_letter.isalpha() or (some != some.lower() and some != some.upper()) or (first_letter.islower() and word != word.lower()):
                word_formatted = word
            else:
                word_formatted = first_letter.upper() + word_lower[1:]

            new_words.append(word_formatted)

        new_artist = ' '.join(new_words)
        if artist != new_artist:
            return self.editor.replace_string(name, artist, new_artist)
        return name


class FixFileNames(RenameFilesInDir):

    def extra_actions(self, file_name):
        self.editor.check_formatting(file_name)

    def get_new_name(self, file_name):
        new_name = copy.deepcopy(file_name)

        # Remove specified substrings
        new_name = self.remove_specified_substrings(new_name)

        # Replace specified substrings
        new_name = self.replace_specified_substrings(new_name)

        # Find parts of the title in ()
        new_name = self.handle_parenthetical_values(new_name)

        # Find parts of the title that potentially should be removed
        new_name = self.handle_bad_strings(new_name)

        # Check for weird characters and attempt to replace or remove them
        new_name = self.replace_invalid_chars(new_name)

        # Clean up any potential lingering issues
        new_name = self.clean_whitespace_and_cruft(new_name)

        # If there is a remix artist, extract it, and prepend it to the file_name
        new_name = self.add_remix_artist(new_name)

        # # Check formatting, don't try to rename
        # self.editor.check_formatting(new_song_title)

        return new_name

    def remove_specified_substrings(self, name):
        return reduce(self.editor.remove_string, remove_strings, name)

    def replace_specified_substrings(self, name):
        return reduce(lambda x, y: self.editor.replace_string(x, *y), replace_strings, name)

    def handle_parenthetical_values(self, name):
        return reduce(self.editor.remove_string, self.editor.find_parenthetical_values(name), name)

    def handle_bad_strings(self, name):
        return reduce(self.editor.remove_string, self.editor.find_bad_string_patterns(name), name)

    def replace_invalid_chars(self, name):
        return reduce(self.editor.replace_invalid_char, self.editor.find_invalid_chars(name), name)

    def clean_whitespace_and_cruft(self, name):
        return self.editor.clean_whitespace_and_cruft(name)

    def add_remix_artist(self, name):
        return self.editor.add_remix_artist(name)


class StringEditor(object):

    def __init__(self, verbose=0, commit=False):
        self.stats = Stats()
        self.verbose = verbose
        self.commit = commit

    def replace_string(self, name, find_val, replace_val):
        if find_val not in name or find_val == replace_val:
            return name

        if not replace_val:
            return self.remove_string(name, find_val)

        for x in range(name.count(find_val)):
            self.log_message(f'\'{find_val}\' is going to replaced with \'{replace_val}\' in\n{name}')
            self.stats.replaced.append((find_val, replace_val))
            name = self._execute_replace(name, find_val, replace_val, 1)
        return name

    def remove_string(self, name, bad_string):
        if bad_string not in name:
            return name
        for x in range(name.count(bad_string)):
            self.log_message(f'\'{bad_string}\' Is going to be Removed in\n{name}')
            self.stats.removed.append(bad_string)
            name = self._execute_replace(name, bad_string, '', 1)
        return name

    def crop_string(self, name, start, end):
        removed_string, remaining_string = self._execute_crop(name, start, end)
        self.log_message(f'\'{name}\' is going to be cropped of \'{removed_string}\'')
        self.stats.removed.append(removed_string)
        return remaining_string

    def add_remix_artist(self, name):
        remix_artist = self.extract_remix_artist(name)
        if not remix_artist or self.already_has_remix_artist(name, remix_artist) or self.contains_genre(remix_artist.lower()):
            return name

        self.log_message(f'Pre-pending Remix Artist: \'{remix_artist}\'')
        self.stats.remixed.append(remix_artist)
        return remix_artist + ' - ' + name

    def process_unhandled_char(self, name, invalid_char):
        self.log_message(f'unhandled Character found: {invalid_char} (' + str(ord(invalid_char)) + f') No replacement provided\n{name}', level=0)
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

    def find_parenthetical_values(self, name):
        bad_strings = []
        parenthetical_values = re.findall(parenthetical_regex, name)
        for match in parenthetical_values:
            if self.should_parenthetical_value_be_removed(match):
                bad_strings.append(match)

        return bad_strings

    @staticmethod
    def should_parenthetical_value_be_removed(string_to_check):
        string_to_check = string_to_check.strip('()').lower()

        for phrase in acceptable_song_specific_parenthetical_phrases + song_version_descriptors:
            if phrase.lower() == string_to_check:
                return False

        for phrase in song_info_prefix + song_version_prefix:
            if string_to_check.lower().startswith(phrase.lower()):
                return False

        for phrase in song_info_suffix + song_version_suffix:
            if string_to_check.lower().endswith(phrase.lower()):
                return False
        return True

    @staticmethod
    def find_bad_string_patterns(name):
        bad_strings = []
        for regex in potential_problem_regexes:
            potentially_bad = re.findall(regex, name)
            for match in potentially_bad:
                # if self.is_it_actually_bad(match):
                bad_strings.append(match)

        return bad_strings

    def clean_whitespace_and_cruft(self, name):

        while '  ' in name:
            name = self.replace_string(name, '  ', ' ')

        cruft = [' ', '_', '-']
        start_position = 0
        while name[start_position] in cruft:
            start_position += 1
        if start_position:
            name = self.crop_string(name, 0, start_position)

        length_string = len(name)
        end_position = length_string
        while name[end_position - 1] in cruft:
            end_position -= 1

        if 0 < length_string - end_position < 5:
            if name[end_position - 1] != '+':
                name = self.crop_string(name, end_position, length_string)

        return name

    def check_formatting(self, name):
        if not self._check_formatting(name):
            self.stats.improper_formatting.append(name)

    def rename_file(self, directory, file_name, new_file_name):
        if file_name == new_file_name:
            return
        self.log_message(f'Original |{file_name}\nUpdated  |{new_file_name}\n', level=3)  # Spammy
        temp_file_name = new_file_name + '.temp'
        if self.commit:
            rename_file_safe(directory, file_name, temp_file_name, verbose=self.verbose,  commit=self.commit)
            rename_file_safe(directory, temp_file_name, new_file_name, verbose=self.verbose,  commit=self.commit)

    def print_is_commit_true_or_false(self):
        if not self.commit:
            print('~~~ NOT Commiting Changes! ~~~')
            print('Change the commit flag to persist changes')
        else:
            print("!!! Commiting Changes !!!")

    def log_message(self, message, level=1):
        if level <= self.verbose:
            print(message)

    ######################################################
    ### String Utils ###
    ######################################################

    @staticmethod
    def find_strings_to_replace(name):
        return [replace_data * name.count(replace_data) for replace_data in replace_strings if replace_data[0] in name]

    @staticmethod
    def find_strings_to_remove(name):
        return [string_ * name.count(string_) for string_ in remove_strings if string_ in name]

    @staticmethod
    def get_invalid_char_replacement(invalid_char):
        ascii_code = ord(invalid_char)
        if ascii_code in remove_char_codes:
            return None

        return replace_chars_mapping.get(ascii_code, invalid_char)

    @staticmethod
    def find_invalid_chars(name):
        return [char for char in name if (ord(char) >= 128 or ord(char) < 32) or not char.isascii()]

    @staticmethod
    def extract_remix_artist(name):
        if 'remix' in name or 'Remix' in name:
            regex = r'[\[\(]([^\]^\)]*)[ _-][rR]emix[\)\]]'
            # regex2 = r'[\[\(]([^\]^\)]*)[ _-]([rR]e?)?[mM]ix[\)\]]'  # TODO Test
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
    def contains_genre(remix_artist):
        genre_list = ['techno', 'rock']
        for genre in genre_list:
            if genre in remix_artist:
                return True
        return False

    @staticmethod
    def _check_formatting(name):
        # Ensure formatting is correct
        for required_string in required_strings:
            if required_string not in name:
                return False

        for regex in improper_format_regexes:
            if re.findall(regex, name):
                return False

        # Is there repetitive information in the title?
        sections = name.lower().strip().split(' - ')
        length = len(sections)
        if length > 2:
            for x in range(length):
                for y in range(length):
                    if y != x and sections[x] in sections[y] and 'mix' not in sections[y].lower():
                        return False
        return True

    @staticmethod
    def _execute_replace(name, find_val, replace_val, limit):
        return name.replace(find_val, replace_val, limit)

    @staticmethod
    def _execute_crop(name, start, end):
        return name[start:end], name[0:start] + name[end:]

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
                    for stats_item in stats_list:
                        stats_dict[stats_item] = stats_dict.get(stats_item, 0) + 1
                    for stats_item in reversed(sorted(stats_dict.items(), key=lambda x: x[1])):
                        res = stats_item[0]
                        if isinstance(res, tuple):
                            res = '\' <-> \''.join(res)
                        print(f' \'{res}\' : {stats_item[1]}')


########################################################################################################

if __name__ == '__main__':
    # default_path = POST_ROCK_FULL_ALBUMS_DIR
    default_path = POST_ROCK_NEW_ALBUMS_DIR

    parser = argparse.ArgumentParser(description='Fix Song Names')
    parser.add_argument('directory', nargs='?', default=default_path, help='Target Directory')
    parser.add_argument('--commit', action='store_true', help='Rename Files')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    parser.add_argument('--capitalize-artist', action='store_true', help='Capitalize Artist Names and that\'s it')
    # TODO
    # parser.add_argument('--albums', '-a', action='store_true', default=False, help='Renaming Albums')
    args = parser.parse_args()

    music_directory = args.directory
    if not music_directory.startswith('C:/'):
        music_directory = os.path.join(MUSIC_DIR, music_directory)

    rename_type = FixFileNames
    if args.capitalize_artist:
        rename_type = CapitalizeArtist
    name_fixer = rename_type(verbose=args.verbose, commit=args.commit)
    name_fixer.fix_file_names(music_directory)
    # name_fixer.fix_file_names(music_directory, recursive=True)

########################################################################################################

r"""
python fix_names.py

python fix_names.py post_rock\new_albums -v
python fix_names.py post_rock\new_songs -v

"""
