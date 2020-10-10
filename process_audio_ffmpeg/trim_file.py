"""
Use ffmpeg CLI commands to trim audio and video files

Ethan Wright 6/28/20
"""
import argparse
import os

from call_ffmpeg import call_ffmpeg
from paths import Paths
from utils import convert_timestamp_to_float


def trim_video_file(source_file_path, start, end, command_version=1, suffix='', verbose=False, commit=False):

    file_path, extension = source_file_path.rsplit('.', 1)
    output_path = file_path + ' - clip' + str(suffix) + '.' + extension
    count = 1
    while os.path.isfile(output_path):
        count += 1
        output_path = file_path + ' - clip_' + str(count) + '.' + extension
        print(f'File already exists, appending _{count}')

    # Both commands have their charms. Trimming the input file rather than the
    # output file seems to usually work better, but sometimes it's the opposite
    # Consult the ffmpeg docs for more details about the trimming process.
    # command = f'ffmpeg -ss {start} -to {end} -i "{source_file_path}" -c copy "{output_path}"'  # Trim input
    command = [
        'ffmpeg',
        '-ss', start,
        '-to', end,
        '-i', source_file_path,
        '-c', 'copy',
        output_path
    ]
    if command_version in [2, '2']:
        # command = f'ffmpeg -i "{source_file_path}" -c copy -ss {start} -to {end} "{output_path}"'  # Trim output
        command = [
            'ffmpeg',
            '-i', source_file_path,
            '-c', 'copy',
            '-ss', start,
            '-to', end,
            output_path
        ]

    return call_ffmpeg(command, verbose=verbose, commit=commit)


def convert_timestamp_to_str(timestamp):
    str_timestamp = str(convert_timestamp_to_seconds(timestamp))
    if str_timestamp.startswith('.'):
        str_timestamp = '0' + str_timestamp
    return str_timestamp


def run(args):
    # TODO Which?
    start = convert_timestamp_to_str(args.start)
    end = convert_timestamp_to_str(args.end)
    # start2 = convert_timestamp_to_seconds(args.start)
    # end2 = convert_timestamp_to_seconds(args.end)


    # target_dir = Paths.VIDEOS
    # target_dir = Paths.POST_ROCK_SONGS
    target_dir = os.path.join('trim', Paths.PROCESSING_DIR)
    target_path = os.path.join(target_dir, args.file)

    trim_video_file(target_path, start, end, command_version=args.command, verbose=args.verbose, commit=args.commit)

    # Both commands at the same time
    # for command_v in [1, 2]:
    #     trim_video_file(target_path, start, end, command_version=command_v, suffix=str(command_v), verbose=args.verbose, commit=args.commit)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fix Song Names')
    parser.add_argument('file', help='Target File')
    parser.add_argument('start', help='Start Timestamp')
    parser.add_argument('end', help='End Timestamp')
    parser.add_argument('--commit', action='store_true', help='Commit')
    parser.add_argument('--command', default=2, help='Command Type')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')

    run(parser.parse_args())


r"""
python trim_file.py "FILE" xx:xx xx:xx --commit
python trim_file.py "" --commit

"""

