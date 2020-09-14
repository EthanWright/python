"""
This contains a Wrapper around the youtube-dl python project
It reads video ids from a file, and then downloads them from
youtube using predetermined settings.
It only saves the audio, not the video.
It downloads the highest quality that it is able to.

Ethan Wright 6/15/20
"""

import os
import re
import time
import datetime
import youtube_dl

from video_ids_db import DB

position_file = os.path.join('input', 'position.txt')
TEN = 10


def retrieve_all_video_ids_from_file(file_name):
    file_path = os.path.join('input', file_name)
    video_id_list = []
    with open(file_path, 'r') as f:
        for video_id in f:
            if not video_id:
                continue
            video_id_list.append(video_id.strip())
    # exit("Confirm")
    call_youtube_dl(video_id_list)


def retrieve_one_video_id_from_file_tracked():
    position = int(get_position())
    print('Position: ' + str(position))
    video_id = get_next_line_from_file_tracked(position)
    set_position(position + 1)
    try:
        call_youtube_dl([video_id])
    except FileNotFoundError:
        set_position(position)  # Rollback


def get_next_line_from_file_tracked(position):
    with open(input_file, 'r') as f:
        count = 0
        for video_id in f:
            count += 1
            if count <= position:
                continue
            video_id = clean_video_id(video_id)
            if not video_id:
                position += 1
                set_position(position + 1)
                continue
            return video_id
    return None


def get_position():
    if not os.path.isfile(position_file):
        set_position(0)
    with open(position_file, 'rb') as read_file:
        position = read_file.readlines()[0]
    return position


def set_position(new_position):
    with open(position_file, 'wb') as write_file:
        write_file.write(bytes(str(new_position), 'utf-8'))


def call_youtube_dl(video_id_list):

    ydl_opts = {
        # 'verbose': True,  # For debugging
        # 'format': 'worstaudio/worst',  # For testing
        'format': 'bestaudio/best',  # Obviously
        # 'outtmpl': '%(title)s - %(artist)s.%(ext)s',  # Edited youtube-dl project to do this
        'keepvideo': False,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'nopostoverwrites': False},  # --extract-audio
            {'key': 'FFmpegMetadata'},  # --add-metadata
        ]
    }

    if not video_id_list:
        return
    if isinstance(video_id_list, str):
        video_id_list = [video_id_list]

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        db = DB()
        for video_id in video_id_list:

            video_id = clean_video_id(video_id)
            if not video_id:
                continue
            if not extract_video_id(video_id):
                print(f'Bad Video ID format {video_id}')
                continue  # ???

            # Check if it has been downloaded
            if db:
                if db.exists(video_id):
                    print(f'ERROR! {video_id} already exists!')
                    continue

            print('Downloading: ' + video_id)
            print('Time: ' + time.asctime())

            try:
                ydl.download([video_id])
            except youtube_dl.utils.DownloadError as e:
                print('ERROR!')
                print(e)
                continue

            # sleepy_time(40*60)
            sleepy_time(10*60)


def extract_video_id(video_id):
    video_id_regex = r'(https://www.youtube.com/watch\?v=)?([0-9a-zA-Z\-\_]{11})'
    return re.search(video_id_regex, video_id).group(2)


def clean_video_id(video_id):
    if ' ' in video_id:
        video_id = video_id.split(' ', 1)[0]
    return video_id.strip()


def sleepy_time(seconds_to_sleep=10):
    seconds_to_sleep = int(seconds_to_sleep)
    print(f'Sleeping! [{seconds_to_sleep} seconds]', end='', flush=True)
    sleep_string = '.'  # * 10
    remainder = seconds_to_sleep % TEN
    one_minute = TEN * 6
    ten_minutes = TEN * one_minute

    for x in range(0, seconds_to_sleep - remainder, TEN):
        if x % one_minute == 0:
            if x > 0 and x % ten_minutes == 0:
                print(' ' + str(x))
            else:
                print('')
        print(sleep_string, end='', flush=True)
        time.sleep(TEN)

    time.sleep(remainder)
    print('\n')


if __name__ == '__main__':
    # input_file = 'video_ids_to_listen_to.txt'
    # input_file = 'video_ids.txt'
    # input_file = 'video_ids_albums.txt'
    input_file = 'video_ids_songs.txt'

    retrieve_all_video_ids_from_file(input_file)
    # retrieve_one_video_id_from_file_tracked()

