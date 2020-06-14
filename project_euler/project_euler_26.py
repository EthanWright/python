"""
Project Euler 26

1/505 = 0.0019801980198019801980198019801980198019801980198019801980198019801980198019801980198019801980198019
"""
import time

from utils.project_euler_long_division import LongDivision


class PuzzleSolver(object):

    DECIMAL = '.'

    def __init__(self, debug=0, max_divisions=3000):
        self.DEBUG = debug
        self.max_divisions = max_divisions

    def run(self):
        max_length = 0
        max_length_number = 0
        for x in xrange(1, 1000):

            result = self._do_long_division_iterative(1, x)
            length = self.find_repeat_length(result)

            print('1/{} = {}'.format(x, result[:20]))
            print('There is a repeat length of: {}'.format(length))
            if length > max_length:
                max_length = length
                max_length_number = x

        print(max_length_number, max_length)
        return max_length

    def _do_long_division_iterative(self, numerator, denominator):
        result_string = ''
        loop_count = 0
        while numerator != 0:  # Evenly Divided
            if loop_count > self.max_divisions:
                break

            remainder = numerator % denominator
            divisor = numerator / denominator
            if self.DEBUG > 1:
                print('Numerator: {} Denominator: {}'.format(numerator, denominator, loop_count))
                print("Divisor: {} Remainder: {}".format(divisor, remainder))
            result_string += str(divisor)
            if loop_count == 0 and remainder > 0:
                result_string += self.DECIMAL
            numerator = remainder * 10
            loop_count += 1

        return result_string

    def find_repeat_length(self, number_string):
        number_string = number_string.replace('0.', '')
        max_length = len(number_string)
        tolerance = max_length / 25

        for position in xrange(max_length):
            for y in xrange(position + 1, max_length - tolerance):
                success = True
                for extra in xrange(0, max_length - y):
                    if number_string[position + extra] != number_string[y + extra]:
                        success = False
                        break
                if success:
                    return y - position  # Repeat length
        return 0


if __name__ == "__main__":
    start_time1 = time.time()
    puzzle = PuzzleSolver(debug=0)
    puzzle.run()
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time1))
