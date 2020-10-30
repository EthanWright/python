import re

SIXTY = 60.0


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

    title = remove_track_number_from_title(title)
    # Remove Track Title Prefixes ('1.' or '01.')
    if re.match(r'[0-9][0-9]?\..*', title):
        title = title.split('.', 1)[1]

    # print(f'{start_seconds} - {end_seconds} | {title}')

    # TODO Make a class for chapter_data?
    return {
        'start_timestamp': start_milliseconds,
        'end_timestamp': end_milliseconds,
        'title': title.strip(),
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


def format_into_timestamp(value):

    # seconds vs milliseconds ?
    time_value = int(value / 1000.0)

    minutes = int(time_value / SIXTY)
    seconds = time_value % SIXTY
    minutes_str = str(minutes)
    seconds_str = str(seconds)

    spacer = ':'
    if seconds < 10.0:
        spacer += '0'

    return f'{minutes_str}{spacer}{seconds_str}'


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
            total_seconds += float(hours) * SIXTY * SIXTY
        total_seconds += float(minutes) * SIXTY

    total_seconds += float(seconds)

    return total_seconds


def convert_timestamp_to_float_seconds_2(timestamp):
    total_seconds = 0.0
    count = 0.0
    for item in reversed(timestamp.split(':')):
        if item:
            total_seconds += float(item) * pow(SIXTY, float(count))
            count += 1.0
    return total_seconds


def convert_float_to_str_safe(float_time):
    str_time = str(float_time)
    if str_time.startswith('.'):
        str_time = '0' + str_time

    return str_time
