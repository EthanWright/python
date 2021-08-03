"""
Gather and Compare data between 2 files using ffmpeg CLI calls

Ethan Wright - 6/11/20
"""

import argparse
import copy
import os

from call_ffmpeg import get_metadata
from music_file_scripts_common import list_music_files, remove_file_extension
from paths import Paths, PathGen, PathConfig
from utils import extract_field_from_stdout, convert_timestamp_to_float_seconds


class MusicFileList(object):

    def __init__(self, directory, folder_desc, recursive=False):
        self.directory = directory
        self.recursive = recursive
        self.music_list_pointer = 0
        self.current_song = None

        self.helper = ComparisonHelper(folder_desc=folder_desc)

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
        self.helper.check_bitrates(self.current_song, song_2=match)
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
        self.matching_bitrates = []
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

    def check_bitrates(self, song_1, song_2=None):
        if not song_1:
            return
        if not song_2:
            return
        bitrate = get_song_bitrate(song_1.full_path)
        extension = song_1.file_name.rsplit('.', 1)[1]
        thresholds = self.bitrate_thresholds.get(extension.lower())

        if bitrate > thresholds.max:
            self.high_bitrates.append(song_1.full_path)
            # if song_2:
            #     self.high_bitrates.append('# DUPLICATE FOUND')
            #     self.high_bitrates.append(song_2.full_path)

        if bitrate < thresholds.min:
            self.low_bitrates.append(song_1.full_path)
            # if song_2:
            #     self.low_bitrates.append('# REPLACEMENT FOUND')
            #     self.low_bitrates.append(song_2.full_path)
        if song_2:
            self.matching_bitrates.append((song_1.full_path, '#', bitrate))

        self.add_to_stats(bitrate, song_1.full_path)

    def add_to_stats(self, bitrate, song_name):
        if bitrate not in self.all_bitrates_1:
            self.all_bitrates_1[bitrate] = []
        self.all_bitrates_1[bitrate].append(song_name)

        if bitrate not in self.bitrates_count:
            self.bitrates_count[bitrate] = 0
        self.bitrates_count[bitrate] += 1

    def write_matching_bitrates_to_file(self):
        file_path = os.path.join(Paths.MUSIC, f'matching_bitrates_{self.folder_desc}.txt')
        with open(file_path, 'w') as write_file:
            for item in self.matching_bitrates:
                write_file.write(' '.join([str(sub_item) for sub_item in item]) + '\n')
        
        file_path_2 = os.path.join(Paths.MUSIC, f'matching_bitrates_{self.folder_desc}_playlist.m3u')
        with open(file_path_2, 'w') as write_file:
            for item in self.matching_bitrates:
                write_file.write(item[0] + '\n')

    def write_bitrate_stats_to_file(self):
        file_path = os.path.join(Paths.MUSIC, f'all_files_{self.folder_desc}.m3u')

        for item in sorted(self.bitrates_count.keys()):
            print('~ ' + str(item) + ' ~')
            print(self.bitrates_count.get(item))

        with open(file_path, 'w') as write_file:
            for item in sorted(self.all_bitrates_1.keys()):
                write_file.write('# ~ ' + str(item) + ' ~\n')
                write_file.write('\n'.join(self.all_bitrates_1.get(item)) + '\n')

    def write_outliers_to_playlist(self):
        output_file_path_low = os.path.join(Paths.MUSIC, f'low_bitrates_{self.folder_desc}.m3u')
        output_file_path_high = os.path.join(Paths.MUSIC, f'high_bitrates_{self.folder_desc}.m3u')

        with open(output_file_path_low, 'w') as write_file:
            write_file.write('\n'.join(self.low_bitrates))
        with open(output_file_path_high, 'w') as write_file:
            write_file.write('\n'.join(self.high_bitrates))


# Iterate through 2 lists simultaneously #


def compare_directory_contents(music_file_list_1, music_file_list_2):

    matches_count = 0
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
        # if matches_count > 0:  # TODO Testing
        #     break
    while music_file_list_1.current_song:
        music_file_list_1.increment_position()

    while music_file_list_2.current_song:
        music_file_list_2.increment_position()


def print_bitrate_data(music_file_list_1, music_file_list_2):

    print(f'Total Items in List 1: {music_file_list_1.total_items}')
    print(f'Total Items in List 2: {music_file_list_2.total_items}')
    # print(f'Matches: {matches_count}')

    music_file_list_1.helper.write_outliers_to_playlist()
    music_file_list_2.helper.write_outliers_to_playlist()

    music_file_list_1.helper.write_bitrate_stats_to_file()
    music_file_list_2.helper.write_bitrate_stats_to_file()

    music_file_list_1.helper.write_matching_bitrates_to_file()
    music_file_list_2.helper.write_matching_bitrates_to_file()


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


# Functions for checking only one directory at a time


def aggregate_bitrates(directory, recursive=False):
    bitrates = {}
    for full_path in list_files_for_directory(directory, recursive=recursive):
        bitrate = check_bitrate(full_path)
        if bitrate not in bitrates:
            bitrates[bitrate] = 0
        bitrates[bitrate] += 1
    print(bitrates)


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


def compare_directory_bitrates(directory_1, directory_2):
    folder_desc_1 = os.path.split(directory_1)[-1]
    folder_desc_2 = os.path.split(directory_2)[-1]
    music_file_list_1 = MusicFileList(directory_1, folder_desc_1, recursive=True)
    music_file_list_2 = MusicFileList(directory_2, folder_desc_2, recursive=True)

    compare_directory_contents(music_file_list_1, music_file_list_2)

    print_bitrate_data(music_file_list_1, music_file_list_2)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compare Directories')
    parser.add_argument('--commit', action='store_true', help='Commit Changes')
    args = parser.parse_args()

    music_path = Paths.MUSIC

    good = os.path.join(music_path, 'good', 'good_original')
    good_redownloaded = os.path.join(music_path, 'good', 'good_redownloaded')
    phone = os.path.join(music_path, 'phone', 'phone_original')
    phone_redownloaded = os.path.join(music_path, 'phone', 'phone_redownloaded')

    # compare_directory_contents(path_1, path_2, recursive=True)
    # print_data_for_directory(good_redownloaded, recursive=True)
    # print_data_for_directory(phone_redownloaded, recursive=True)

    # compare_directory_bitrates(phone, phone_redownloaded)
    compare_directory_bitrates(good, good_redownloaded)
