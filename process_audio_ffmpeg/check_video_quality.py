"""
Search for video bitrates or resolutions over a certain threshold

Ethan Wright - 6/11/20
"""

import argparse
import os

from call_ffmpeg import call_ffprobe
from file_scripts_common import list_files
from paths import Paths


def get_file_bitrate(file_path, verbose=0):

    command = [
        'ffprobe',
        '-v', 'error',
        # The bitrate of the whole file
        '-show_entries', 'format=bit_rate',
        '-of', 'csv=p=0',
        file_path
    ]
    result = call_ffprobe(command, verbose=verbose)
    return int(result[0].strip().replace('N/A', '0'))


def get_bitrate_and_resolution(file_path, verbose=0):

    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        # The bitrate and resolution of the video stream
        '-show_entries', 'stream=width,height,bit_rate',
        '-of', 'csv=p=0',
        file_path
    ]

    result = call_ffprobe(command, verbose=verbose)
    width, height, bitrate = result[0].strip().replace('N/A', '0').split(',')
    return int(width), int(height), int(bitrate)


#def validate_stats(value, value_threshold):
    #if value > value_threshold:
        #return False
    #return True


def print_validate_stats_failure(file_name, field_name, value, value_threshold):
    print(f'FAILURE! - {file_name}')
    print(f'{field_name} {value} exceeds the threshold of: {value_threshold}')


def check_file_properties(directory, file_name, verbose=0):

    #print(f'Checking: {file_name}')
    file_path = os.path.join(directory, file_name)
    file_bitrate = get_file_bitrate(file_path, verbose=verbose)
    width, height, bitrate = get_bitrate_and_resolution(file_path, verbose=verbose)

    print(f'Width: {width} Height: {height} Bitrate: {bitrate} File Bitrate: {file_bitrate}')
    
    height_threshold = 1080
    width_threshold = 1920
    bitrate_threshold = 5100000
    file_bitrate_threshold = 5200000
    
    validate_fields = [
        ('Video Width', width, width_threshold),
        ('Video Height', height, height_threshold),
        ('Video Bitrate', bitrate, bitrate_threshold),
        ('File Bitrate', file_bitrate, file_bitrate_threshold),
    ]
    
    valid = True
    for field_name, field_value, value_threshold in validate_fields:
        if field_value > value_threshold:
            print_validate_stats_failure(file_name, field_name, field_value, value_threshold)
            valid = False

    return valid


def search_all_file_bitrates(directory, verbose=0):
    video_list = []

    for file_name in list_files(directory):
        result = check_file_properties(directory, file_name, verbose=verbose)
        if not result:
            video_list.append(file_name)

    with open('videos_redo.txt', 'w') as write_file:
        write_file.write('\n'.join(video_list))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search for video bitrates over a certain threshold')
    parser.add_argument('directory', help='Target Directory')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    args = parser.parse_args()

    search_all_file_bitrates(args.directory, args.verbose)
