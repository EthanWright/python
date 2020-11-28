"""
Gather and Compare data between 2 files using ffmpeg CLI calls

Ethan Wright - 6/11/20
"""

import argparse
import copy
import os

from call_ffmpeg import get_metadata
from file_scripts_common import list_music_files, remove_file_extension
from paths import Paths, PathGen, PathConfig
from utils import extract_field_from_stdout, convert_timestamp_to_float_seconds


class MusicFileList(object):

    def __init__(self, directory, recursive=False):
        self.directory = directory
        self.recursive = recursive
        self.music_list_pointer = 0
        self.current_song = None

        self.helper = ComparisonHelper()

        self.sorted_list = self._get_sorted_list()
        self.total_items = len(self.sorted_list)
        self._set_current_song()

    def _get_sorted_list(self):
        return sorted(
            list_files_for_directory(self.directory, recursive=self.recursive, return_objects=True),
            key=lambda x: x.name_simplified
        )

    def _set_current_song(self):
        self.current_song = None
        if self.music_list_pointer < self.total_items:
            self.current_song = self.sorted_list[self.music_list_pointer]

    def increment_position(self, match=None):
        self.helper.check_bitratess(self.current_song, song_2=match)
        self.music_list_pointer += 1
        self._set_current_song()


class SongItem(object):
    def __init__(self, full_path):
        self.full_path = full_path
        self.file_name = os.path.split(full_path)[-1]
        self.name_simplified = self.simplify_string(self.file_name)

    @staticmethod
    def simplify_string(string_value):
        new_string = remove_file_extension(string_value.lower())
        new_string = new_string.split('(', 1)[0]
        new_string = new_string.replace('&', 'and').replace(' x ', ' and ')
        new_string = new_string.replace('.', '').replace('\'', '').replace(',', '').replace('-', '')
        return new_string


# Iterate through 2 lists simultaneously #


def compare_directory_contents(directory_1, directory_2, recursive=False):

    matches_count = 0

    music_file_list_1 = MusicFileList(directory_1, recursive=recursive)
    music_file_list_2 = MusicFileList(directory_2, recursive=recursive)

    while music_file_list_1.current_song and music_file_list_2.current_song:

        simple_string_1 = music_file_list_1.current_song.name_simplified
        simple_string_2 = music_file_list_2.current_song.name_simplified

        min_len = min(len(simple_string_1), len(simple_string_2))
        simple_string_1 = simple_string_1[:min_len]
        simple_string_2 = simple_string_2[:min_len]

        if simple_string_1 < simple_string_2:
            music_file_list_1.increment_position()

        elif simple_string_1 > simple_string_2:
            music_file_list_2.increment_position()

        elif simple_string_1 == simple_string_2:
            music_file_list_1.increment_position(match=music_file_list_2.current_song)
            music_file_list_2.increment_position(match=music_file_list_1.current_song)
            matches_count += 1
        # if matches_count > 5:  # Testing
        #     return

    while music_file_list_1.current_song:
        music_file_list_1.increment_position()

    while music_file_list_2.current_song:
        music_file_list_2.increment_position()

    print(f'Total Items in List 1: {music_file_list_1.total_items}')
    print(f'Total Items in List 2: {music_file_list_2.total_items}')
    print(f'Matches: {matches_count}')

    music_file_list_1.helper.write_files_to_playlist()
    music_file_list_2.helper.write_files_to_playlist()


# Comparison Functions #
# class Obj(object):
#     def __init__(self, **kwargs):
#         for item in kwargs:
#             self.__setattr__(item, kwargs.get(item))
class MinMax(object):
    def __init__(self, min=0, max=0):
        self.min = min
        self.max = max


class ComparisonHelper(object):

    bitrate_thresholds = {
        'mp3': MinMax(min=192, max=219),
        'm4a': MinMax(min=192, max=219),
        'opus': MinMax(min=120, max=192)
    }

    def __init__(self, folder_desc=None):
        self.high_bitrates = []
        self.low_bitrates = []
        self.bitrates_count = {}
        self.all_bitrates_1 = {}
        self.folder_desc = folder_desc

    def compare_lengths(self, song_1, song_2):
        length_1 = get_song_length(song_1.full_path)
        length_2 = get_song_length(song_2.full_path)
        length_1_int = convert_timestamp_to_float_seconds(length_1)
        length_2_int = convert_timestamp_to_float_seconds(length_2)
        if abs(length_1_int - length_2_int) > 3.0:
            print('Mismatched lengths')
            print(song_1.file_name + '\n' + length_1)
            print(song_2.file_name + '\n' + length_2)
            # import pdb;pdb.set_trace()

    def check_bitratess(self, song_1, song_2=None):
        if not song_1:
            return
        bitrate = get_song_bitrate(song_1.full_path)
        extension = song_1.file_name.rsplit('.', 1)[1]
        thresholds = self.bitrate_thresholds.get(extension.lower())
        if bitrate > thresholds.max:
            self.high_bitrates.append(song_1.full_path)
            if song_2:
                self.high_bitrates.append('# DUPLICATE FOUND')
                self.high_bitrates.append(song_2.full_path)

        if bitrate < thresholds.min:
            self.low_bitrates.append(song_1.full_path)
            if song_2:
                self.low_bitrates.append('# REPLACEMENT FOUND')
                self.low_bitrates.append(song_2.full_path)

        self.add_to_stats(bitrate, song_1.full_path, song_2=song_2)

    def add_to_stats(self, bitrate, song_name, song_2=None):
        if bitrate not in self.all_bitrates_1:
            self.all_bitrates_1[bitrate] = []
        self.all_bitrates_1[bitrate].append(song_name)

        if bitrate not in self.bitrates_count:
            self.bitrates_count[bitrate] = 0
        self.bitrates_count[bitrate] += 1
        if song_2:
            pass

    def write_files_to_playlist(self):
        output_file_path_low = os.path.join(Paths.MUSIC, f'low_bitrates_{self.folder_desc}.m3u')
        output_file_path_high = os.path.join(Paths.MUSIC, f'high_bitrates_{self.folder_desc}.m3u')
        all_files_path = os.path.join(Paths.MUSIC, f'all_files_{self.folder_desc}.m3u')

        for item in sorted(self.bitrates_count.keys()):
            print('~ ' + str(item) + ' ~')
            print(self.bitrates_count.get(item))

        with open(all_files_path, 'w') as write_file:
            for item in sorted(self.all_bitrates_1.keys()):
                write_file.write('# ~ ' + str(item) + ' ~\n')
                write_file.write('\n'.join(self.all_bitrates_1.get(item)) + '\n')

        with open(output_file_path_low, 'w') as write_file:
            write_file.write('\n'.join(self.low_bitrates))
        with open(output_file_path_high, 'w') as write_file:
            write_file.write('\n'.join(self.high_bitrates))


# Iterate through 1 list #


def list_files_for_directory(directory, recursive=False, return_objects=False):
    return_list = []
    for file_name in os.listdir(directory):
        full_path = os.path.join(directory, file_name)
        if os.path.isfile(full_path):
            if return_objects:
                return_list.append(SongItem(full_path))
            else:
                return_list.append(full_path)
        elif os.path.isdir(full_path):
            if recursive:
                return_list.extend(list_files_for_directory(
                    full_path, recursive=True, return_objects=return_objects
                ))
    return return_list


# Aggregate Data #


def aggregate_bitrates(directory, recursive=False):
    bitrates = {}
    for full_path in list_files_for_directory(directory, recursive=recursive):
        bitrate = check_bitrate(full_path)
        if bitrate not in bitrates:
            bitrates[bitrate] = 0
        bitrates[bitrate] += 1
    print(bitrates)


# Validate Data #


def check_bitrate(full_path):
    bitrate_obj = SongBitrate(full_path)

    # OPUS
    # bitrate_obj.check_high(190)
    # bitrate_obj.check_low(120)

    # MP3
    # bitrate_obj.check_high(219)
    bitrate_obj.check_low(192)

    return bitrate_obj.value


class SongBitrate(object):

    def __init__(self, full_path):
        self.full_path = full_path
        self.value = get_song_bitrate(full_path)

    def check_high(self, target):
        if self.value > target:
            self.print_outlier('HIGH')

    def check_low(self, target):
        if self.value < target:
            self.print_outlier('LOW')

    def print_outlier(self, relation):
        print(f'Song has a {relation} bitrate')
        print(self.full_path)
        print(self.value)
        print('---')


# Utils for extracting song data #


def get_song_length(song_path):
    return get_data_field(song_path, 'Duration:')


def get_song_bitrate(song_path):
    bitrate = get_data_field(song_path, 'bitrate:')
    return int(bitrate.split(' ', 1)[0])


def get_data_field(song_path, field):
    metadata, stdout = get_metadata(song_path)
    return extract_field_from_stdout(stdout, field)


def print_song_data(full_path, current_song):
    metadata, stdout = get_metadata(full_path)
    print('---\n' + current_song)
    print(extract_field_from_stdout(stdout, 'Duration:'))
    print(extract_field_from_stdout(stdout, 'bitrate:'))


# Print Thing Temp #
def print_bitrates():
    for x in range(32, 400):
        bar = bitrates.get(x, 0) * 'X'
        print(f'{x}{bar}')
    exit()


def compare_directory_bitrates(directory_1, directory_2, folder_desc):
    # helper = ComparisonHelper(folder_desc=folder_desc)
    compare_directory_contents(directory_1, directory_2, recursive=True)
    # helper.write_files_to_playlist(out_file_path_low, out_file_path_high)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compare Directories')
    parser.add_argument('--commit', action='store_true', help='Commit Changes')
    args = parser.parse_args()

    music_path = Paths.MUSIC

    most_music = os.path.join(music_path, 'most_music_original')
    most_music_redownloaded = os.path.join(music_path, 'most_music_redownloaded')
    liked = os.path.join(music_path, 'liked', 'liked_original')
    liked_redownloaded = os.path.join(music_path, 'liked', 'liked_redownloaded')

    # compare_directory_contents(path_1, path_2, recursive=True, commit=args.commit)
    # print_data_for_directory(most_music_redownloaded, recursive=True)
    # print_data_for_directory(liked_redownloaded, recursive=True)

    compare_directory_bitrates(liked, liked_redownloaded, 'old_liked')
    # compare_directory_bitrates(most_music, most_music_redownloaded, 'old_most_music')
