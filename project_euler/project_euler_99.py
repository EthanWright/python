"""
Project Euler 99
"""
import copy
import math
import time
from project_euler_helpers import PrimeFactorization


class BaseObject(object):
    DEBUG = 0
    pf = PrimeFactorization(debug=DEBUG)

    def __init__(self, debug=0):
        if debug:
            self.DEBUG = debug


class Power(BaseObject):
    def __init__(self, base, exponent, debug=0):
        super(Power, self).__init__(debug)
        self.base = base
        self.exponent = exponent

    def get_value(self):
        return pow(self.base, self.exponent)

    def __repr__(self):
        return '{}^{}'.format(self.base, self.exponent)


class FactorList(BaseObject):

    def __init__(self, number, debug=0):
        super(FactorList, self).__init__(debug)

        self.number = number
        self.factorization = self.get_full_factorization()

    def get_values(self):
        return ' * '.join(['({})'.format(factor.get_value()) for factor in self.factorization])

    def __repr__(self):
        return '(' + ' * '.join(['({})'.format(factor) for factor in self.factorization]) + ')'

    def get_full_factorization(self):
        factors = []
        prime_factors = self.pf.prime_factorization(self.number)
        for item in prime_factors:
            factor = Power(item, prime_factors[item])
            factors.append(factor)
        return factors


class LargePower(Power):

    def __init__(self, base, exponent, debug=0):
        super(LargePower, self).__init__(base, exponent, debug)
        self.exponent_factorization = FactorList(self.exponent)

    def get_full_factorization(self):
        # TODO How to integrate this with the FactorList?
        factors = []
        prime_factors = self.pf.prime_factorization(self.base)
        for item in prime_factors:
            factor = Power(item, prime_factors[item] * self.exponent)
            factors.append(factor)
        return factors

    def __repr__(self):
        return '{} ^ {}'.format(self.base, self.exponent_factorization)


class PuzzleSolverOld(BaseObject):

    def run(self):
        file_name = 'data/project_euler_99_data.txt'
        count = 0
        powers = []

        with open(file_name) as exponent_file:
            line = exponent_file.readline().rstrip()
            while line:
                #line = '30,30'
                split_line = line.split(',')
                power = LargePower(int(split_line[0]), int(split_line[1]))
                powers.append(power)
                count += 1
                if count == 4:
                    break
                line = exponent_file.readline().rstrip()

        self.adjust_powers(powers[2], powers[3])
        self.compare_powers(powers[2], powers[3])

    def adjust_powers(self, power_1, power_2):
        print('Comparison of {} ^ {} and {} ^ {}'.format(power_1.base, power_1.exponent, power_2.base, power_2.exponent))
        print('Comparison of {} and {}'.format(power_1, power_2))

        print(power_1)
        factorization_1 = power_1.get_full_factorization()
        self.print_factorization(factorization_1)
        self.adjust_factorization(factorization_1)

        print(power_2)
        factorization_2 = power_2.get_full_factorization()
        self.print_factorization(factorization_2)
        self.adjust_factorization(factorization_2)

        print('Factor List of {} and {}'.format(factorization_1, factorization_2))

        #
        # TODO Compare !
        #

    def compare_factorizations(self, factorization_1, factorization_2):
        pass

    def adjust_factorization(self, factorization):
        for power in factorization:

            exponent = power.exponent
            exponent_factors = self.pf.prime_factorization(exponent)
            new_exponent_factors = copy.deepcopy(exponent_factors)

            factor = min(exponent_factors)
            count = exponent_factors[factor]
            new_base = pow(power.base, factor)
            new_count = count - 1

            if factor in new_exponent_factors:
                del new_exponent_factors[factor]
            if new_count > 0:
                new_exponent_factors[factor] = new_count

            self.print_exponent_factors(new_base, new_exponent_factors)
        print('')
        return

    def print_factorization(self, factorization):
        for power in factorization:
            exponent_factors = self.pf.prime_factorization(power.exponent)
            self.print_exponent_factors(power.base, exponent_factors)
        print('')

    def print_exponent_factors(self, base, exponent_factors):
        print('({}) ^ ('.format(base) +
              ' * '.join(['({}^{})'.format(factor, exponent_factors[factor]) for factor in exponent_factors]) +
              ') * ')

################################################################################################################################################


class PuzzleSolver(object):
    def run(self):
        file_name = 'data/project_euler_99_data.txt'
        line_number = 1
        results = {}

        with open(file_name) as exponent_file:
            line = exponent_file.readline().rstrip()
            while line:
                split_line = line.split(',')  # base,exponent
                # log (M ^ n) = n * log M (For same base log)
                results[line_number] = float(split_line[1]) * math.log(float(split_line[0]))
                line = exponent_file.readline().rstrip()
                line_number += 1

        print('From smallest to greatest:')
        print(sorted(results, key=lambda x: results[x]))


if __name__ == "__main__":
    start_time = time.time()
    puzzle = PuzzleSolver()
    puzzle.run()
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))

"""
>>> pow(6, 30)
>>> pow(6, 2*3*5)
>>> pow(6, 3*5) * pow(6, 3*5)
>>> pow(6, 2*5) * pow(6, 2*5) * pow(6, 2*5)
>>> pow(pow(6, 2*5), 3)
>>> pow(pow(pow(6, 2), 5), 3)
>>> pow(pow(6, 2 * 5), 3)
>>> pow(pow(pow(6, 5), 2), 3)
>>> pow(pow(6, 5), 2 * 3)
221073919720733357899776L

>>> pow(30, 30)
>>> pow(2, 30) * pow(3, 30) * pow(5, 30)
>>> pow(4, 15) * pow(9, 15) * pow(25, 15)
>>> pow(8, 10) * pow(27, 10) * pow(125, 10)
>>> pow(32, 6) * pow(243, 6) * pow(625*5, 6)
205891132094649000000000000000000000000000000L
"""
"""
632382 ^ 518061 <> 519432 ^ 525806

Method 1
632382 ^ 518061 <> 519432 ^ 525806
632382 <> 519432 ^ (525806.0 / 518061.0)
632382 > 632376.5012136808

Method 2
(632382 ^ 518061) / (519432 ^ 518061) <> 519432 ^ 7745
(632382 / 519432) ^ 518061 <> 519432 ^ 7745
(632382.0 / 519432.0) ^ (518061.0 / 7745.0) <> 519432
519734.2064410891 > 519432

Method 3
632382 ^ 518061 > 519432 ^ 525806
(632382 ^ 518061) / (519432 ^ 518061) <> 519432 ^ 7745
(632382 ^ 514188) / (519432 ^ 514188) <> (519432 ^ 7745) * (519432 ^ 3873) / (632382 ^ 3873)
(632382 / 519432) ^ 514188 <> (519432 ^ 7745) * (519432 / 632382) ^ 3873
(x/y) ^ z <> y ^ 7745 * (y/x) ^ 3873
---
(632382 ^ 518061) / (519432 ^ 518061) <> 519432 ^ 7745
(632382 ^ 259030.5) / (519432 ^ 259030.5) <> (519432 ^ 7745) * (519432 ^ 259030.5) / (632382 ^ 259030.5)
(632382 / 519432) ^ 259030.5 <> (519432 ^ 7745) * (519432 / 632382) ^ 259030.5
(x/y) ^ z <> (m ^ n) * (y/x) ^ z

---
Method 4 (The Good One)
log b (M ^ n) = n * log b M

632382 ^ 518061 <> 519432 ^ 525806
518061 * log(632382) <> 525806 * log(519432)
6919869.733217769 > 6919865.228473604
"""