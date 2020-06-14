"""
Project Euler Long Division Module
"""


class LongDivision(object):

    DECIMAL = '.'
    TERMINAL = ''

    def __init__(self, max_divisions=100, debug=0):
        self.max_divisions = max_divisions
        self.DEBUG = debug

    def divide(self, numerator, denominator):
        if self.DEBUG > 0:
            print('Calculating {} / {}'.format(numerator, denominator))
        # return self._do_long_division_recursive(numerator, denominator, 0)
        return self._do_long_division_iterative(numerator, denominator)

    def _do_long_division_recursive(self, numerator, denominator, call_count):
        if call_count > self.max_divisions:  # That's enough
            return self.TERMINAL

        if numerator == 0:  # Evenly Divided
            return self.TERMINAL

        remainder = numerator % denominator
        divisor = numerator / denominator
        if self.DEBUG > 1:
            print('Numerator: {} Denominator: {}'.format(numerator, denominator, call_count))
            print("Divisor: {} Remainder: {}".format(divisor, remainder))
        insert = self.DECIMAL if call_count == 0 and remainder > 0 else ''
        return str(divisor) + insert + self._do_long_division_recursive(remainder * 10, denominator, call_count + 1)

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
