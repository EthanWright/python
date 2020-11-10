import copy
import os
import re

from paths import Paths


def parse_bookmark_entry(line_string):
    if '<DT><A ' in line_string:
        matches = re.search('<DT><A HREF="([^"]*)"([ ]?[^>]*)>(.*)</A>', line_string)
        return matches.groups()
    return None


def parse_bookmarks_file(file_path):
    current_folder = None
    urls = {}
    folder_queue = []
    bookmark_data = []

    for line in open(file_path, 'r').readlines():
        matches = parse_bookmark_entry(line)
        if matches is not None:
            urls[current_folder].append((matches[0], matches[2]))

        # Push old folder when entering new folder, and pop when leaving

        # Check for end of folder
        matches = re.search(r'</DL>', line)
        if matches is not None:
            if current_folder:
                bookmark_data.append({
                    'folder_name': current_folder,
                    'parent_folders': copy.deepcopy(folder_queue),
                    'data': urls.get(current_folder)
                })
                # print("Exited ", current_folder)
                if len(folder_queue):
                    current_folder = folder_queue.pop()
                else:
                    current_folder = None
                # print("Popped ", current_folder)

        # Check for beginning of folder
        matches = re.search('">(.*)<\/H3>', line)
        if matches is not None:
            if current_folder:
                folder_queue.append(current_folder)
                # print("Pushed ", current_folder)

            current_folder = matches.group(1)
            # print("Entered ", current_folder)
            urls[current_folder] = []

    return bookmark_data


def parse_bookmarks_into_new_file(bookmarks_file, output_file):

    include_sections = ['Todo', 'Music to Listen to']
    ignore_sections = ['Databases', 'System Design', 'Front End']

    def is_folder_list_in_section_list(folder_list, sections):
        for folder_item in folder_list:
            if folder_item in sections:
                return True
        return False

    all_bookmarks = parse_bookmarks_file(bookmarks_file)

    output = open(output_file, 'w')

    for data in all_bookmarks:
        folder = data.get('folder_name')
        parent_folders = data.get('parent_folders', [])
        values = data.get('data')

        all_folders = parent_folders + [folder]
        if not values:
            continue
        if is_folder_list_in_section_list(all_folders, ignore_sections):
            continue
        if not is_folder_list_in_section_list(all_folders, include_sections):
            continue

        # indent = len(parent_folders) * '&nbsp;'
        path = ' -> '.join(all_folders)
        output.write("<H3>" + path + " [" + str(len(values)) + "]</H3>\n")

        for value in values:
            output.write("<A HREF=\"" + value[0] + "\">" + value[1] + "</A><br>\n")

    output.close()


def parse_bookmarks_into_new_file_formatted(bookmarks_file, output_file):
    output = open(output_file, 'w')
    for line in open(bookmarks_file, 'r').readlines():

        if '<DT><A ' in line:
            matches = parse_bookmark_entry(line)
            if matches:
                line = line.replace(matches[1], '')

        if '<H3 ' in line:
            matches = re.search('<H3 ([^>]*)>.*</H3>', line)
            if matches:
                line = line.replace(matches.group(1), '')

        output.write(line)

    output.close()


def parse_bookmarks_into_new_file_formatted_2(bookmarks_file, output_file):
    output = open(output_file, 'w')
    for line in open(bookmarks_file, 'r').readlines():
        fields = ['ADD_DATE', 'LAST_MODIFIED', 'ICON_URI', 'ICON', 'LAST_CHARSET']
        for field in fields:
            if field in line:
                matches = re.search(f'({field}=".*")( |>)', line)
                if matches:
                    line = line.replace(matches.group(1), '')
        output.write(line)
    output.close()


if __name__ == '__main__':
    input_file = os.path.join(Paths.HOME_DIR, 'bookmarks.html')
    output_file_1 = os.path.join(Paths.HOME_DIR, 'bookmarks_todo.html')
    output_file_2 = os.path.join(Paths.HOME_DIR, 'bookmarks_all_simplified.html')

    parse_bookmarks_into_new_file(input_file, output_file_1)
    parse_bookmarks_into_new_file_formatted(input_file, output_file_2)
