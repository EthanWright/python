"""
Compare lists of youtube links
Ethan Wright 6/15/20
"""

import os
import re

REGEX_YOUTUBE_ID = r'(https://www.youtube.com/watch\?v=)?([0-9a-zA-Z\-\_]{11})'

""" TODO Is this just extra?

def read_video_ids_from_file(file_path):
    video_id_mapping = dict()

    # Read in every song from the list
    for line in open(file_path, 'r').readlines():
        line = line.strip()
        search_result = re.search(REGEX_YOUTUBE_ID, line)
        if search_result:
            video_id_mapping[search_result.group(2)] = line

    return video_id_mapping


def read_video_ids_from_file(file_path):
    video_ids = list()

    # Read in every song from the list
    for line in open(file_path, 'r').readlines():
        line = line.strip()
        search_result = re.search(REGEX_YOUTUBE_ID, line)
        if search_result:
            video_ids.append(search_result.group(2))

    return video_ids
"""


def read_video_ids_from_file(file_path, use_mapping_dict=False):

    if use_mapping_dict:
        video_id_mapping = dict()
        video_ids = None
    else:
        video_ids = list()
        video_id_mapping = None

    # Read in every song from the list
    for line in open(file_path, 'r').readlines():
        line = line.strip()
        search_result = re.search(REGEX_YOUTUBE_ID, line)
        if search_result:
            video_id = search_result.group(2)
            if use_mapping_dict:
                video_id_mapping[video_id] = line
            else:
                video_ids.append(video_id)
            # print(video_id)

    if use_mapping_dict:
        return video_id_mapping
    return video_ids


def compare_video_id_lists():
    # Generate mapping dictionary from list of all links
    file_links_all = 'input/all_youtube_links.txt'
    links_all = read_video_ids_from_file(file_links_all, use_mapping_dict=True)
    link_ids_all = set(links_all.keys())

    file_links_done = 'input/links_done.txt'
    links_done = read_video_ids_from_file(file_links_done)
    link_ids_done = set(links_done)

    files_list = [
        #'input/links_done.txt',
        'input/links_done_melee.txt',
        'input/links_done_aoe.txt',
        'input/links_done_documentaries.txt',
        'input/links_lost.txt',
    ]
    # Loop through files
    for file_path_rel in files_list:
        more_link_ids_done = read_video_ids_from_file(file_path_rel)
        more_link_ids_done_set = set(more_link_ids_done)
        link_ids_done = link_ids_done.union(more_link_ids_done_set)

    # Compare lists
    missing = link_ids_all - link_ids_done
    for item in missing:
        # print(item)
        print(links_all.get(item))

    # DEBUG
    # print(link_ids_all)
    # print(link_ids_done)
    # import pdb;pdb.set_trace()


if __name__ == '__main__':
    compare_video_id_lists()
