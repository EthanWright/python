import re

from file_scripts_common import clean_file_name


def extract_field_from_metadata(metadata, field):
    search_string = field + '='
    for line in metadata.split('\n'):
        line_clean = line.strip()
        if line_clean.startswith(search_string):
            return line_clean.replace(search_string, '').strip()
    return None


def extract_field_from_stdout(stdout, stdout_field):
    for line in stdout.split('\n'):
        line_clean = line.strip()
        if stdout_field in line_clean:
            return line_clean.rsplit(' ', 1)[1]


def get_track_data_from_metadata(metadata):
    return parse_track_data(metadata.split('[CHAPTER]'), parse_ffmetadata_chapter)


def get_track_data_from_file(input_path):
    return parse_track_data(open(input_path, 'r').readlines(), parse_track_data_string)


def parse_track_data(track_data_list, parsing_function):
    return_data = []
    for chapter in track_data_list:
        parsed_track_data = parsing_function(chapter)
        if parsed_track_data:
            return_data.append(parsed_track_data)

    return return_data


def parse_track_data_string(data_string):
    timestamps = extract_timestamps(data_string)

    if len(timestamps) == 0:
        print('No timestamp in: ' + data_string)
        return None

    start_milliseconds = convert_timestamp_to_float_milliseconds(timestamps[0])
    title = data_string.replace(timestamps[0], '')

    end_milliseconds = None
    if len(timestamps) == 2:
        end_milliseconds = convert_timestamp_to_float_milliseconds(timestamps[1])
        title = title.replace(timestamps[1], '')

    title = clean_file_name(title)  # TODO Too strict?
    # print(f'{start_seconds} - {end_seconds} | {title}')

    # TODO Make a class for chapter_data?
    return {
        'start_timestamp': start_milliseconds,
        'end_timestamp': end_milliseconds,
        'title': title,
    }


def parse_ffmetadata_chapter(chapter):
    regex = 'START=([0-9]+)\nEND=([0-9]+)\ntitle=(.+)\n'
    result = re.search(regex, chapter)
    if result and len(result.groups()) == 3:
        # TODO Make a class for chapter_data?
        start_milliseconds = int(result.groups()[0].strip())
        end_milliseconds = int(result.groups()[1].strip())
        return {
            'start_timestamp': start_milliseconds,
            'end_timestamp': end_milliseconds,
            'title': result.groups()[2].strip(),
        }


def extract_timestamps(data_string):
    # regex = r'([0-9]{1,3}:[0-9][0-9]\.?[0-9]*)'
    regex = r'[^0-9:]?([0-9:]*:[0-9][0-9]?\.?[0-9]*)[^(0-9:)]?'
    return re.findall(regex, data_string)


def format_time_value(time_value):

    time_value = float(time_value / 1000.0)

    timestamp_minutes = int(time_value / 60.0)
    timestamp_seconds = time_value % 60.0
    timestamp_seconds_int = int(timestamp_seconds)
    timestamp_seconds_str = str(timestamp_seconds_int)

    if timestamp_seconds_int < 10:
        timestamp_seconds_str = '0' + timestamp_seconds_str

    # Add some precision
    timestamp_seconds_decimal = timestamp_seconds - float(timestamp_seconds_int)
    timestamp_seconds_decimal = round(timestamp_seconds_decimal, 3)
    if timestamp_seconds_decimal:
        timestamp_seconds_str = timestamp_seconds_str + '.' + str(timestamp_seconds_decimal)[2:]

    return f'{timestamp_minutes}:{timestamp_seconds_str}'


def convert_timestamp_to_float_milliseconds(timestamp):
    # TODO round ? int ?
    return convert_timestamp_to_float_seconds(timestamp) * 1000.0


def convert_timestamp_to_float_seconds(timestamp):
    # return convert_timestamp_to_float_seconds_1(timestamp)
    return convert_timestamp_to_float_seconds_2(timestamp)


def convert_timestamp_to_float_seconds_1(timestamp):
    total_seconds = 0.0
    seconds = timestamp

    if ':' in timestamp:
        minutes, seconds = timestamp.rsplit(':', 1)
        if ':' in minutes:
            hours, minutes = minutes.rsplit(':', 1)
            total_seconds += float(hours) * 60.0 * 60.0
        total_seconds += float(minutes) * 60.0

    total_seconds += float(seconds)

    return total_seconds


def convert_timestamp_to_float_seconds_2(timestamp):
    total_seconds = 0.0
    count = 0.0
    for item in reversed(timestamp.split(':')):
        total_seconds += float(item) * pow(60.0, float(count))
        count += 1.0
    return total_seconds


def convert_float_to_str_safe(float_time):
    str_time = str(float_time)
    if str_time.startswith('.'):
        str_time = '0' + str_time

    return str_time


def convert_str_timestamp_to_str_seconds(timestamp):
    return convert_float_to_str_safe(convert_timestamp_to_float_seconds(timestamp))
