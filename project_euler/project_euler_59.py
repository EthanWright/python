"""
Project Euler 59
"""
import time
import copy
import sys


class Errors(object):
    def __init__(self):
        self.errors = {}

    def report(self, error_index):
        if error_index in self.errors:
            self.errors[error_index] += 1
        else:
            self.errors[error_index] = 1

    def __repr__(self):
        return_string = ""
        for index in self.errors:
            return_string += "Error {} Count: {}\n".format(index, self.errors[index])
        return return_string


class AsciiLetters(object):
    BANG = 33
    COMMA = 44
    PERIOD = 46
    QUESTION_MARK = 63
    A_UPPER = 65
    A_LOWER = 97
    I_UPPER = 73


class AsciiConstants(object):

    MIN_ASCII_VALUE = 32
    MAX_ASCII_VALUE = 126  # 127 is ASCII but `11111111`, so XOR is ineffective
    SPACE_ASCII_VALUE = 32
    MIN_LOWER_CASE_ASCII_VALUE = 97
    MAX_LOWER_CASE_ASCII_VALUE = 122
    MIN_UPPER_CASE_ASCII_VALUE = 65
    MAX_UPPER_CASE_ASCII_VALUE = 90
    MIN_NUMBER_ASCII_VALUE = 48
    MAX_NUMBER_ASCII_VALUE = 57
    I_ASCII_VALUE = AsciiLetters.I_UPPER
    A_ASCII_VALUES = [AsciiLetters.A_LOWER, AsciiLetters.A_UPPER]
    PUNCTUATION_ASCII_VALUES = [
        AsciiLetters.PERIOD, AsciiLetters.COMMA, AsciiLetters.QUESTION_MARK, AsciiLetters.BANG
    ]


class PuzzleSolver(object):

    def __init__(self, file_name, key_length, debug=False):
        self.start_time = time.time()
        self.time_heartbeat = self.start_time
        self.DEBUG = debug
        self.ascii_values = []
        self.key_length = key_length
        self.file_name = file_name
        self.possible_values = {x: [] for x in xrange(self.key_length)}
        self.potential_keys = []
        self.keys_checked = 0
        self.errors = Errors()

    def heartbeat(self, message=None, force=False):
        if not self.DEBUG and not force:
            return
        print("--- {} Seconds since last heartbeat, {} Total. Location: {} ---".format(
            time.time() - self.time_heartbeat,
            time.time() - self.start_time,
            message
        ))
        self.time_heartbeat = time.time()

    def run(self):
        self.heartbeat('Beginning')
        self.setup()
        self.heartbeat('After Setup')
        for xor_value in xrange(128):
            self.analyze_xor_value(xor_value)
        self.heartbeat('After XOR')
        self.validate_possible_values()
        self.heartbeat('After Validation, Final Heartbeat', force=True)

    def setup(self):
        with open(self.file_name) as xor_file:
            line = xor_file.readline().rstrip()
            while line:
                chars = line.split(',')
                for char in chars:
                    # print(char),
                    ascii_value = int(char)
                    self.ascii_values.append(ascii_value)
                line = xor_file.readline().rstrip()
        # print(self.ascii_values)

    def analyze_xor_value(self, xor_value):
        """Try XOR Value for each letter of the key"""
        count = 0
        valid_list = [True] * self.key_length

        for char in self.ascii_values:
            ascii_value = char ^ xor_value
            if ascii_value < AsciiConstants.MIN_ASCII_VALUE or ascii_value > AsciiConstants.MAX_ASCII_VALUE:
                valid_list[count % self.key_length] = False
                if True not in valid_list:
                    break
            count += 1

        index = 0
        for validity in valid_list:
            # print("Key index {} can be {}".format(index, xor_value))
            if validity:
                self.possible_values[index].append(xor_value)
            index += 1

    def increment(self, ref_dict, index):
        if index < 0:
            return False
        ref_dict[index] += 1
        if ref_dict[index] >= len(self.possible_values[index]):
            ref_dict[index] = 0
            return self.increment(ref_dict, index - 1)

        return True

    def validate_possible_values_iterative(self):

        ref_dict = {x: 0 for x in xrange(self.key_length)}
        new_list = [0 for x in range(self.key_length)]
        continue_validating = True

        while continue_validating:
            for index in self.possible_values:
                new_list[index] = self.possible_values[index][ref_dict[index]]

            if self.check_key(new_list):
                self.potential_keys.append(copy.deepcopy(new_list))
            continue_validating = self.increment(ref_dict, self.key_length - 1)

    def validate_possible_values(self):
        self.validate_possible_values_recursive([0 for x in range(self.key_length)], 0)
        #self.validate_possible_values_iterative()
        if self.DEBUG:
            keys_formatted = ', '.join(
                ["({})".format(
                    ', '.join(
                        [str(char) for char in key]
                    )
                ) for key in self.potential_keys]
            )

            print("{} Potential keys found: {}".format(len(self.potential_keys), keys_formatted))
            print("{} Total keys checked".format(self.keys_checked))
            print("{}".format(self.errors))

    def validate_possible_values_recursive(self, key, position):

        if position == self.key_length:
            if self.check_key(key):
                self.potential_keys.append(copy.deepcopy(key))
            return

        for value in self.possible_values[position]:
            key[position] = value
            self.validate_possible_values_recursive(key, position + 1)

    def check_key(self, key):
        self.keys_checked += 1
        ascii_values = []
        count = 0
        is_valid_string = True
        stats = EnglishMan(len(self.ascii_values), self.errors)

        for char in self.ascii_values:
            new_ascii_value = char ^ key[count % self.key_length]
            if not stats.process_ascii_value(new_ascii_value):
                # If the key validation failed, return.
                # Unless we want to analyze all the failures in DEBUG mode...
                if not self.DEBUG:
                    return False
                is_valid_string = False

            ascii_values.append(new_ascii_value)
            count += 1

        if is_valid_string:
            print("Key: {}".format(key))
            self.print_ascii_values(ascii_values)
            print("The sum of the ASCII values of this text is {}\n".format(sum(ascii_values)))
            return True

    def print_ascii_values(self, ascii_values):
        print(''.join([chr(ascii_value) for ascii_value in ascii_values]))


class EnglishMan(AsciiConstants):

    MIN_STRING_LENGTH_TO_VALIDATE = 20

    def __init__(self, total_length, errors):
        self.total_length = total_length
        self.errors = errors
        self.position = 0
        self.error_count = 0
        self.lower_case_count = 0
        self.upper_case_count = 0
        self.space_count = 0
        self.number_count = 0
        self.non_alpha_numeric_count = 0
        self.punctuation_count = 0
        self.last_value = 0
        self.i_or_a_count = 0
        self.space_i_or_a = False

    def process_ascii_value(self, ascii_value):
        self.position += 1

        if self.MIN_LOWER_CASE_ASCII_VALUE <= ascii_value <= self.MAX_LOWER_CASE_ASCII_VALUE:
            self.lower_case_count += 1

        elif self.MIN_UPPER_CASE_ASCII_VALUE <= ascii_value <= self.MAX_UPPER_CASE_ASCII_VALUE:
            self.upper_case_count += 1
            if ascii_value == self.I_ASCII_VALUE or ascii_value in self.A_ASCII_VALUES:
                if self.last_value == self.SPACE_ASCII_VALUE:
                    self.space_i_or_a = True

        elif ascii_value == self.SPACE_ASCII_VALUE:
            self.space_count += 1
            if self.space_i_or_a:
                self.i_or_a_count += 1

        elif self.MIN_NUMBER_ASCII_VALUE <= ascii_value <= self.MAX_NUMBER_ASCII_VALUE:
            self.number_count += 1

        else:
            self.non_alpha_numeric_count += 1
            if ascii_value in self.PUNCTUATION_ASCII_VALUES:
                self.punctuation_count += 1
            if not self.is_probably_english():
                return False

        if self.position % 10 == 0:
            if not self.is_probably_english():
                return False

        if self.space_i_or_a:
            if self.last_value != self.SPACE_ASCII_VALUE:
                self.space_i_or_a = False

        self.last_value = ascii_value
        return True

    def is_probably_english(self):
        """Check a few simple but arbitrary criteria that suggest that the given text is english"""
        if self.position <= self.MIN_STRING_LENGTH_TO_VALIDATE:
            return True

        error_count_before = self.error_count
        letter_count = self.lower_case_count + self.upper_case_count + self.space_count

        if self.non_alpha_numeric_count * 3 > letter_count:
            self.report_error(1)

        if self.punctuation_count * 12 > letter_count:
            self.report_error(2)

        if self.space_count * 20 < self.position:
            self.report_error(3)

        if self.number_count * 8 > letter_count:
            self.report_error(4)

        if letter_count * 1.5 <= self.position:
            self.report_error(5)

        if self.position > self.MIN_STRING_LENGTH_TO_VALIDATE * 10:
            if self.i_or_a_count == 0:
                self.report_error(6)

        return self.error_count == error_count_before

    def report_error(self, error_index):
        self.error_count += 1
        self.errors.report(error_index)


if __name__ == "__main__":
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] in ['True', '1', 'DEBUG']:
            print("Using DEBUG mode")
            debug = True
    key_length = 3
    file_name = 'data/project_euler_59_data.txt'
    puzzle = PuzzleSolver(file_name, key_length, debug=debug)
    puzzle.run()
