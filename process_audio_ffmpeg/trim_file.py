"""
Use ffmpeg CLI commands to trim audio and video files

Ethan Wright 6/28/20
"""
import argparse
import os

from call_ffmpeg import call_ffmpeg
from paths import VIDEO_DIR, MUSIC_DIR


def run(file_path, start_timestamp, end_timestamp, verbose=False, commit=False):
    start = convert_timestamp_to_float(start_timestamp)
    end = convert_timestamp_to_float(end_timestamp)
    command_version = 1
    trim_video_file(file_path, start, end, command_version=command_version, verbose=verbose, commit=commit)

    # Both
    # trim_video_file(file_path, start, end, command_version=1, suffix='1', verbose=verbose, commit=commit)
    # trim_video_file(file_path, start, end, command_version=2, suffix='2', verbose=verbose, commit=commit)


def convert_timestamp_to_float(timestamp):
    if ':' not in timestamp:
        return str(timestamp)

    minutes, seconds = timestamp.split(':')
    return str((float(minutes) * 60.0) + float(seconds)).rstrip('0').rstrip('.')


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
    command = f'ffmpeg -ss {start} -to {end} -i "{source_file_path}" -c copy "{output_path}"'  # Trim input
    if command_version == 2:
        command = f'ffmpeg -i "{source_file_path}" -c copy -ss {start} -to {end} "{output_path}"'  # Trim output

    return call_ffmpeg(command, verbose=verbose, commit=commit)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fix Song Names')
    parser.add_argument('file', help='Target Directory')
    parser.add_argument('start', help='Start Timestamp')
    parser.add_argument('end', help='End Timestamp')
    parser.add_argument('--commit', action='store_true', help='Commit')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose')
    args = parser.parse_args()

    target_path = os.path.join(VIDEO_DIR, args.file)
    # target_path = os.path.join(MUSIC_DIR, args.file)
    # target_path = os.path.join(MUSIC_DIR, r'post_rock\to_sort', args.file)
    run(target_path, args.start, args.end, verbose=args.verbose, commit=args.commit)

r"""
python trim_file.py "FILE" xx:xx xx:xx
python trim_file.py "" 


"""
