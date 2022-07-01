"""
Use ffmpeg CLI commands to trim audio and video files

Ethan Wright 6/28/20
"""
import argparse
import os

from call_ffmpeg import call_ffmpeg
from paths import Paths
from utils import SPACED_HYPHEN, convert_timestamp_to_float_seconds, convert_float_to_str_safe


def trim_media_file(source_file_path, start, end, command_version=1, suffix='', verbose=False, commit=False):

    file_path, extension = source_file_path.rsplit('.', 1)
    output_path = file_path + SPACED_HYPHEN + 'clip' + str(suffix) + '.' + extension
    count = 1
    while os.path.isfile(output_path):
        count += 1
        suffix = '_' + str(count)
        output_path = file_path + SPACED_HYPHEN + 'clip' + suffix + '.' + extension
        print(f'File already exists, appending {suffix}')

    # Both commands have their charms. Trimming the input file seems to work better
    # for video, while trimming the output file is usually more accurate for audio
    # files. Consult the ffmpeg docs for more details about the trimming process.

    # Trim output
    if command_version in [1, '1']:
        command = [
            'ffmpeg',
            '-i', source_file_path,
            '-c', 'copy',
            '-ss', start,
            '-to', end,
            #'-avoid_negative_ts','make_zero',
            output_path
        ]
        # windows_command = ' '.join(command)

    elif command_version in [2, '2']:
        # Trim input
        command = [
            'ffmpeg',
            '-ss', start,
            '-to', end,
            '-i', source_file_path,
            '-c', 'copy',
            #'-avoid_negative_ts','make_zero',
            output_path
        ]
        # windows_command = ' '.join(command)
    else:
        raise Exception("Invalid command type specified")

    return call_ffmpeg(command, verbose=verbose, commit=commit)


def run(args):

    start = args.start
    end = args.end

    # TODO Check for no ':' and format appropriately
    # Or is this ok?
    # Try testing: .xx x.x -.x xx.x xxx.x
    # if ':' not in start:

    if start.startswith(':'):
        start = '0' + start
    if end.startswith(':'):
        end = '0' + end

    if args.video:
        target_dir = Paths.VIDEOS
    else:
        target_dir = os.path.join(Paths.PROCESSING, 'trim')

    target_path = os.path.join(target_dir, args.file)

    if args.both:
        # Both commands at the same time
        for command_v in [1, 2]:
            trim_media_file(
                target_path, start, end,
                command_version=command_v, suffix=str(command_v), verbose=args.verbose, commit=args.commit
            )
        return

    elif args.command:
        command = args.command
    elif args.video:
        command = 2
    else:
        command = 1

    trim_media_file(target_path, start, end, command_version=command, verbose=args.verbose, commit=args.commit)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Trim audio and video files')
    parser.add_argument('file', help='Target File')
    parser.add_argument('start', help='Start Timestamp')
    parser.add_argument('end', help='End Timestamp')
    parser.add_argument('--video', action='store_true', help='Trim a video file')
    parser.add_argument('--commit', action='store_true', help='Commit')
    parser.add_argument('--command', help='Command Type')
    parser.add_argument('--both', action='store_true', help='Both command types at the same time')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')

    run(parser.parse_args())


"""
# Show key frames
ffprobe -select_streams v:0 -skip_frame nokey -show_entries frame=pkt_pts_time FILE | grep -v FRAME > key_frames.txt

python trim_file.py "FILE" xx:xx xx:xx --commit
python trim_file.py "" --commit 

"""
