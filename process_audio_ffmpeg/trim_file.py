"""
Use ffmpeg CLI commands to trim audio and video files

Ethan Wright 6/28/20
"""
import argparse
import os

from call_ffmpeg import call_ffmpeg
from paths import Paths
from utils import convert_timestamp_to_float_seconds, convert_float_to_str_safe


def trim_media_file(source_file_path, start, end, command_version=1, suffix='', verbose=False, commit=False):

    file_path, extension = source_file_path.rsplit('.', 1)
    output_path = file_path + ' - clip' + str(suffix) + '.' + extension
    count = 1
    while os.path.isfile(output_path):
        count += 1
        output_path = file_path + ' - clip_' + str(count) + '.' + extension
        print(f'File already exists, appending _{count}')

    # Both commands have their charms. Trimming the input file seems to work better
    # for video, while trimming the output file is usually more accurate for audio
    # files. Consult the ffmpeg docs for more details about the trimming process.

    # Trim output
    command = [
        'ffmpeg',
        '-i', source_file_path,
        '-c', 'copy',
        '-ss', start,
        '-to', end,
        output_path
    ]
    # windows_command = ' '.join(command)

    if command_version in [2, '2']:
        # Trim input
        command = [
            'ffmpeg',
            '-ss', start,
            '-to', end,
            '-i', source_file_path,
            '-c', 'copy',
            output_path
        ]
        # windows_command = ' '.join(command)
    return call_ffmpeg(command, verbose=verbose, commit=commit)


def run(args):

    start = args.start
    end = args.end

    if start.startswith(':'):
        start = '0' + start
    if end.startswith(':'):
        end = '0' + end

    if args.video:
        target_dir = Paths.VIDEOS
        command = 2
    else:
        target_dir = os.path.join(Paths.PROCESSING, 'trim')
        command = 1

    if args.command:
        command = args.command

    target_path = os.path.join(target_dir, args.file)
    trim_media_file(target_path, start, end, command_version=command, verbose=args.verbose, commit=args.commit)

    # Both commands at the same time
    # for command_v in [1, 2]:
    #     trim_media_file(
    #         target_path, start, end,
    #         command_version=command_v, suffix=str(command_v), verbose=args.verbose, commit=args.commit
    #     )


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fix Song Names')
    parser.add_argument('file', help='Target File')
    parser.add_argument('start', help='Start Timestamp')
    parser.add_argument('end', help='End Timestamp')
    parser.add_argument('--video', action='store_true', help='Trim a video file')
    parser.add_argument('--commit', action='store_true', help='Commit')
    parser.add_argument('--command', help='Command Type')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')

    run(parser.parse_args())


"""
python trim_file.py "FILE" xx:xx xx:xx --commit
python trim_file.py "" --commit

"""

