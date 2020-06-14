"""
Project Euler 76
Sums are always written with integers in lowest to highest order
"""
import copy
import time


class PuzzleSolverOld(object):
    """
    Works!
    Slow!
    Count how many ways to sum to number recursive without ones
    """
    def __init__(self, maximum=50):
        self.maximum = maximum

    def run(self):
        summation_count = 1

        for x in xrange(1, self.maximum + 1):
            # Prefix each previous permutation with a `1 + `
            new_numbers = summation_count

            if x > 2:
                new_numbers += 1  # Add: [1, x - 1]

            summation_count = new_numbers + self.sum_to_number_no_ones_recursive(x, 0, first_time=True)

            print('{} can be written {} ways'.format(x, summation_count))

    def sum_to_number_no_ones_recursive(self, target_sum, last_num, first_time=False):
        #print('Target: {} Ongoing Sum: {} {} {}'.format(target_sum, ongoing_sum, last_num, depth))
        if 1 >= target_sum:
            return 0

        if not last_num:
            last_num = 2

        if target_sum < last_num:
            return 0

        result_count = 0
        if last_num and not first_time:
            result_count += 1

        for num in xrange(last_num, target_sum):
            result_count += self.sum_to_number_no_ones_recursive(target_sum - num, num)

        return result_count


class PuzzleSolverOld2(object):
    """
    Works!
    SUPER Slow!
    Count how many ways to sum to number recursive by length including ones
    """
    def __init__(self, maximum=10):
        self.maximum = maximum

    def run(self):
        for x in xrange(1, self.maximum + 1):
            summation_count = self.sum_to_number_recursive(x)
            print('{} can be written {} ways'.format(x, summation_count))

    def sum_to_number_recursive(self, target_sum):
        total = 0
        for desired_length in xrange(2, target_sum + 1):
            res = self.sum_to_number_recursive_by_length(target_sum, 0, desired_length, first_time=True)
            # print('Length: {} Sum: {} Ways: {}'.format(desired_length, target_sum, res))
            total += res

        return total

    def sum_to_number_recursive_by_length(self, target_sum, last_num, desired_length, first_time=False):
        # print('Target: {} Ongoing Sum: {} {} {}'.format(target_sum, ongoing_sum, last_num, depth))
        if desired_length > target_sum:
            return 0

        if not last_num:
            last_num = 1

        if target_sum < last_num:
            return 0

        if desired_length == 1:
            return 1

        result_count = 0
        for num in xrange(last_num, target_sum):
            result_count += self.sum_to_number_recursive_by_length(target_sum - num, num, desired_length - 1)

        return result_count


class PuzzleSolverPrintAll(object):
    """
    Works!
    Slow!
    Print all ways to sum to a number using positive integers
    """
    def __init__(self, maximum=35):
        self.maximum = maximum

    def run(self):
        numbers = [[]]
        old_numbers_without_ones = []
        for x in xrange(1, self.maximum + 1):
            new_numbers = []

            for number_list in numbers:
                number_list.insert(0, 1)
                new_numbers.append(number_list)
            if x > 2:
                new_numbers.append([1, x - 1])

            split_values = []
            # split_count = {}
            for item in old_numbers_without_ones:  # TODO What about ones? Like [1, 10] ?
                item[-1] += 1
                for y in xrange(2, x / 2 + 1):
                    if item[-1] % y == 0 and item[-1] / y > item[-2]:
                        # if item[-1] not in split_count:
                        #     split_count[item[-1]] = 0
                        # split_count[item[-1]] += 1
                        split_values.append(item[:-1] + [item[-1] / y] * y)

            factors = []
            for y in xrange(2, x / 2 + 1):
                if x % y == 0:
                    z = x / y
                    factors.append([y] * z)

            # organized_split_values = self.get_organized_split_values(split_values)
            numbers_without_ones = copy.deepcopy(factors) + copy.deepcopy(old_numbers_without_ones) + copy.deepcopy(split_values)

            # --- PRINTING --- #
            # print('Num: {} Split Count: {} Total: {}'.format(x, split_count, sum(split_count[temp] for temp in split_count)))
            # print('{}: {}'.format(x, len(split_values)))
            # xx print('{}: {} {}'.format(x, len(split_values), split_values))
            # print('--- {} ---'.format(x))
            # print(sum(len(organized_split_values[item]) for item in organized_split_values))
            # for item in sorted(organized_split_values):
            #    print('{} [{}]: {}'.format(item, len(organized_split_values[item]), organized_split_values[item]))
            # print('{}: {} {} {} {}'.format(x, len(old_numbers_without_ones), len(factors), len(split_values), split_values))
            # print('{} Total with ones'.format(len(new_numbers)))
            # print('{}'.format(new_numbers))
            # print('{} Total without ones'.format(len(numbers_without_ones)))
            # print('{}'.format(numbers_without_ones))
            # for item in sorted(numbers_without_ones, key=lambda lamb: lamb[-1]):
            #     print('{}'.format(item))
            # print('{} Total without ones from last time with 1 added to the last element'.format(len(old_numbers_without_ones)))
            # print('{}'.format(old_numbers_without_ones))
            # print('{} Total via factors'.format(len(factors)))
            # print('{}'.format(factors))
            # print('{} Total via splitting the last digit'.format(len(split_values)))
            # print('{}'.format(split_values))

            numbers = copy.deepcopy(new_numbers) + copy.deepcopy(numbers_without_ones) or []
            old_numbers_without_ones = copy.deepcopy(numbers_without_ones)

            # print('{} can be written {} ways: {}\n'.format(x, len(numbers), numbers))
            print('{} can be written {} ways'.format(x, len(numbers)))

    def get_organized_split_values(self, split_values):
        """For debugging"""
        organized_split_values = {}
        for item in split_values:
            last_digit = item[-1]
            split_value_sum = 0
            # print('List: {} Last Digit: {}'.format(item, last_digit))

            for digit in reversed(item):
                if digit == last_digit:
                    split_value_sum += digit
            if split_value_sum not in organized_split_values:
                organized_split_values[split_value_sum] = []
            # print('Adding {} {}'.format(split_value_sum, item))
            organized_split_values[split_value_sum].append(item)
        return organized_split_values


class PuzzleSolver(object):
    """
    Works!
    Fast!
    Tries to calculate all ways to sum to a number using 2+ positive integers
    """

    def __init__(self, maximum=100):
        self.maximum = maximum
        self.cache_dict = {}

    def run(self):
        all_numbers = 1
        numbers_without_ones_previous = 0

        for x in xrange(1, self.maximum + 1):
            numbers_prefixed_with_one = all_numbers  # Prefix each previous permutation with a `1 + `

            if x > 2:
                numbers_prefixed_with_one += 1  # Add: [1, x - 1]

            split_count = self.get_split_count(x)

            factors = 0
            for y in xrange(2, x / 2 + 1):
                if x % y == 0:
                    factors += 1

            # Increment the last digit of the previous round of numbers_without_ones_previous
            # Add up all the sequences we constructed that have no ones
            numbers_without_ones = numbers_without_ones_previous + factors + split_count
            all_numbers = numbers_prefixed_with_one + numbers_without_ones
            numbers_without_ones_previous = numbers_without_ones

            print('{} can be written {} ways'.format(x, all_numbers))

    def get_split_count(self, total_sum):
        prefix_arrangements = 0  # Return value
        value_to_split = total_sum - 2

        while value_to_split >= 4:  # [2, 2]
            prefix = total_sum - value_to_split

            if prefix < 2:
                value_to_split -= 1
                continue

            for divisor in xrange(2, (value_to_split / 2) + 1):
                if value_to_split % divisor == 0:
                    repeated_value = value_to_split / divisor
                    result = self.get_permutation_count_for_prefix(prefix, repeated_value)
                    # print('Adding Prefix Arrangements: {} Prefix {} Split Value: {} * {}'.format(result, prefix, repeated_value, divisor))
                    prefix_arrangements += result

            value_to_split -= 1

        return prefix_arrangements

    def get_permutation_count_for_prefix(self, prefix, repeated_value):
        # print('Checking Prefix: {} Repeated value {}'.format(prefix, repeated_value))
        if prefix < 2:
            return 1

        if prefix in self.cache_dict:  # Check Cache
            if repeated_value in self.cache_dict[prefix]:
                return self.cache_dict[prefix][repeated_value]

        prefix_arrangements = 0
        start = 2 + prefix % 2

        for max_value in [value for value in xrange(start, prefix - 1)] + [prefix]:
            if repeated_value > max_value:
                prefix_arrangements += self.get_permutation_count_for_prefix(prefix - max_value, max_value + 1)

        if prefix not in self.cache_dict:  # Cache
            self.cache_dict[prefix] = {}
        self.cache_dict[prefix][repeated_value] = prefix_arrangements
        return prefix_arrangements


########################################################################################################################################################################################################


if __name__ == "__main__":
    start_time = time.time()
    maximum = 100

    # puzzle = PuzzleSolverPrintAll(maximum=maximum)
    # puzzle.run()
    # print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
    # start_time = time.time()
    #
    # puzzle = PuzzleSolverOld(maximum=maximum)
    # puzzle.run()
    # print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
    # start_time = time.time()
    #
    # puzzle = PuzzleSolverOld2(maximum=maximum)
    # puzzle.run()
    # print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
    # start_time = time.time()

    puzzle = PuzzleSolver(maximum=maximum)
    puzzle.run()
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
