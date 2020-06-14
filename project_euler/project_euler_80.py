"""
Project Euler 80
"""
import copy
import operator
import time


class PuzzleSolver(object):

    def __init__(self, max_value=100, debug=0):
        self.DEBUG = debug
        self.max_value = max_value

    def run(self):
        squares = [x * x for x in xrange(10)]
        total = 0
        for x in xrange(self.max_value):
            if x in squares:
                continue
            number = BigNumber(x, debug=self.DEBUG)
            square_root = number.calculate_sqrt()
            total += square_root.get_digital_sum(100)
            print('Ongoing Sum of decimal digits: {}'.format(total))
        print('Final Result: {}'.format(total))
        return total


class BigNumber(object):

    def __init__(self, number, display_precision=100, debug=0):
        self.integer = number
        self.sign = -1 if number < 0 else 1
        self.display_precision = display_precision
        self.precision = self.display_precision + 10
        self.decimals = [0] * self.precision
        self.length = len(self.decimals)
        self.DEBUG = debug

    def __index__(self):
        return self.decimals

    def __repr__(self):
        sign = ''
        if self.sign == -1 and self.integer == 0:
            sign = '-'
        elif self.integer > 0:
            sign = '+'
        decimals = self.get_decimals_rounded()
        return sign + str(self.integer) + '.' + ''.join(str(decimal) for decimal in decimals)

    def calculate_sqrt(self):
        print('Calculating sqrt {}'.format(self))

        start = ((self.integer - 1) / 2) + 1
        square_root = BigNumber(start)
        adjustment = copy.copy(square_root)
        loop_count = 0
        while adjustment.still_going():
            loop_count += 1
            adjustment.divide_by_two()
            attempted_square = square_root * square_root
            if self.DEBUG > 1:
                print('Square Root: {}'.format(square_root))
                print('Attempted Square: {}'.format(attempted_square))
                print('Adjustment: {}'.format(adjustment))

            if attempted_square < self:
                square_root += adjustment
            elif attempted_square > self:
                square_root -= adjustment
            else:
                break

        print('Result: {}'.format(square_root))
        print('Took: {} Loops'.format(loop_count))
        return square_root

    def add_to_integer(self, new_int):
        if not new_int:
            return
        old_integer = self.integer
        self.integer += new_int

        # Am I crossing the threshold but staying -1 < x < 1?
        if self.integer > 0:
            self.sign = 1
        elif self.integer < 0:
            self.sign = -1

        elif old_integer == 0 and new_int >= 1:
            self.sign = 1
        elif old_integer == 0 and new_int <= -1:
            self.sign = -1

        elif self.integer == 0 and new_int >= 1:
            self.sign = 1
        elif self.integer == 0 and new_int <= -1:
            self.sign = -1

    def get_decimals_rounded(self):
        decimals = self.decimals[:self.display_precision]
        return decimals
        # if self.decimals[self.display_precision] >= 5:
        #     index = len(decimals) - 1
        #     decimals[index] += 1
        #     while decimals[index] >= 10:
        #         if index == 0:
        #             self.integer += 1
        #             decimals[index] = decimals[index] % 10
        #             break
        #         decimals[index - 1] += decimals[index] / 10
        #         decimals[index] = decimals[index] % 10
        #         index -= 1
        # return decimals

    def get_decimal_sum(self, digit_count=-1):
        return sum([decimal for decimal in self.decimals[:digit_count]]) or 0

    def get_digital_sum(self, digit_count):
        integer_count = 0
        integer_sum = 0
        integer = self.integer
        while integer > 0:
            integer_sum += integer
            integer_count += 1
            integer /= 10
        return integer_sum + self.get_decimal_sum(digit_count - integer_count)

    def get_decimal(self, index):
        if index < self.precision:
            return self.decimals[index]
        return 0

    def set_decimal(self, index, new_value):
        if index < self.precision:
            self.decimals[index] = new_value

    def add_to_decimal(self, index, value_to_add):
        #print('Adding {} to Index {}'.format(new_value, index))
        offset = 0
        new_value = value_to_add
        while new_value != 0:
            current_index = index - offset
            if current_index < 0:
                self.add_to_integer(new_value)
                return
            else:
                new_value += self.get_decimal(current_index)
                if new_value < 0:
                    self.add_to_decimal(current_index - 1, -1)
                    new_value += 10

                if current_index < self.precision:
                    self.set_decimal(current_index, new_value % 10)

            new_value /= 10
            offset += 1

    def invert_decimals(self):
        index = 0
        for decimal in self.decimals:
            self.set_decimal(index, 9 - decimal)
            index += 1

    def divide_by_two(self):
        carry = 0

        if self.integer % 2 == 1:
            carry = 5
        self.integer = self.integer / 2

        index = 0
        for decimal in self.decimals:
            old_value = decimal
            new_value = decimal / 2
            self.set_decimal(index, new_value + carry)
            if old_value % 2 == 1:
                carry = 5
            else:
                carry = 0
            index += 1

    def execute_operation_add_or_sub(self, other, math_expression):
        #print('Executing {} {} {}'.format(self, math_expression.__name__, other))
        length = max(self.precision, other.precision)
        new_number = BigNumber(0, display_precision=self.display_precision)

        for index in xrange(length - 1, -1, -1):
            a = self.get_decimal(index)
            b = other.get_decimal(index)
            calculated_value = math_expression(a, b)
            #print('{} {} {} = {}'.format(a, math_expression.__name__, b, calculated_value))
            new_number.add_to_decimal(index, calculated_value)

        new_number.add_to_integer(math_expression(self.integer, other.integer))

        if new_number.sign != self.sign:
            new_number.invert_decimals()  # Fun

        return new_number

    def __add__(self, other):
        return self.execute_operation_add_or_sub(other, operator.add)

    def __sub__(self, other):
        return self.execute_operation_add_or_sub(other, operator.sub)

    def __mul__(self, other):
        return self.execute_operation_mul(other, operator.mul)

    def __div__(self, other):
        raise Exception("no")

    def execute_operation_mul(self, other, math_expression):
        #print('Executing {} on {} and {}'.format(math_expression.__name__, self, other))
        new_number = BigNumber(0, display_precision=self.display_precision)

        for index_1 in xrange(self.precision):
            for index_2 in xrange(other.precision):
                new_index = (index_1 + 1) + (index_2 + 1) - 1  # Huh
                a = self.get_decimal(index_1)
                b = other.get_decimal(index_2)
                result = math_expression(a, b)
                new_number.add_to_decimal(new_index, result)

        for index_1 in xrange(self.precision):
            a = self.get_decimal(index_1)
            b = other.integer
            result = math_expression(a, b)
            new_number.add_to_decimal(index_1, result)

        for index_2 in xrange(other.precision):
            a = other.get_decimal(index_2)
            b = self.integer
            result = math_expression(a, b)
            new_number.add_to_decimal(index_2, result)

        new_number.add_to_integer(math_expression(self.integer, other.integer))
        return new_number

    def __gt__(self, other):
        if self.sign == 1 and other.sign == -1:
            return True
        if self.sign == -1 and other.sign == 1:
            return False
        if (self.sign * self.integer) > (other.sign * other.integer):
            return True

        length = max(self.precision, other.precision)
        for index in xrange(length - 1, -1, -1):
            if (self.sign * self.get_decimal(index)) > (other.sign * other.get_decimal(index)):
                return True
            elif (self.sign * self.get_decimal(index)) < (other.sign * other.get_decimal(index)):
                return False

    def still_going(self):
        if self.integer == 0 and self.get_decimal_sum() == 0:
            return False
        return True


if __name__ == "__main__":
    start_time = time.time()
    puzzle = PuzzleSolver()
    puzzle.run()
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
