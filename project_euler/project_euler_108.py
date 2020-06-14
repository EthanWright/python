"""
Project Euler 108
What is the least value of n for which the number of distinct solutions exceeds one-thousand?
"""
import time
import copy

from utils.project_euler_helpers import PrimeFactorization

prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 61, 67, 71, 73, 79, 83, 97]


class PuzzleSolver(object):

    def __init__(self, max_value=10000, debug=0, factor_count=1000, max_factors=30):
        self.DEBUG = debug
        self.max_value = max_value
        self.factor_target = factor_count
        self.pf = PrimeFactorization(debug=0)
        self.factor_formula = FactorFormula(debug=debug, factor_count=factor_count)
        self.different_primes = 0
        self.use_numbers = True
        self.max_factors = max_factors

    def run_specific(self, number):
        if isinstance(number, int):
            number = [number]
        for number in number:
            self.run_number(number)

    def run_sequential(self, start=0):
        self.factor_formula.use_predetermined_values = False
        for number in xrange(1, self.max_value):
            self.run_number(number, start)

    def run_unique_factorization_exponents_list_only(self, count=2):
        self.use_numbers = False
        self.run_unique_factorization_exponents(count=count)

    def run_unique_factorization_exponents(self, count=2):
        self.different_primes = count
        self.run_unique_factorization_exponents_recursive([])

    def run_unique_factorization_exponents_recursive(self, factor_list):
        if len(factor_list) >= self.different_primes:
            return False
        last_value = 1
        if len(factor_list) > 0:
            if self.use_numbers:
                number = self.calculate_number_from_factor_list(factor_list)
                if number >= self.max_value:
                    return False
                self.run_number(number)
            else:
                self.run_factor_count_list(factor_list)
            last_value = factor_list[-1]

        for x in xrange(last_value, self.max_factors):
            new_factor_list = copy.copy(factor_list)
            new_factor_list.append(x)
            if x >= last_value:
                if not self.run_unique_factorization_exponents_recursive(new_factor_list):
                    return True

    def run_factor_count_list(self, factor_count_list):
        solution_count = self.factor_formula.formula(factor_count_list)
        if solution_count > self.factor_target:
            print('Answer: {} has {} solutions'.format(factor_count_list, solution_count))
        return solution_count

    def calculate_number_from_factor_list(self, factor_count_list):
        number = 1
        count = 0
        for factor_count in reversed(factor_count_list):
            prime = prime_list[count]
            number *= pow(prime, factor_count)
            count += 1
        return number

    def run_number(self, number, start=0):
        if self.DEBUG > 1:
            print('Count: {}'.format(self.factor_formula.count))
        # Force print Heartbeats
        if self.factor_formula.count % 500 == 0:
            print('Count: {}'.format(self.factor_formula.count))
        if self.factor_formula.count >= start:
            if number <= self.max_value:
                solution_count = self.factor_formula.run_number(number)
                # if self.DEBUG > 0:
                #     print('There are {} unique solutions of the form: 1/x + 1/y = 1/{}'.format(
                #         solution_count, number))
                if solution_count > self.factor_target:
                    print('Answer: {} has {} solutions'.format(number, solution_count))
                return solution_count
        else:
            self.factor_formula.count += 1
            return 1


class FactorFormula(object):

    def __init__(self, debug=0, factor_count=1000):
        self.DEBUG = debug
        self.pf = PrimeFactorization(debug=0)
        self.count = 0
        self.factor_count = factor_count

    def run_number(self, number):
        self.count += 1
        prime_factorization = self.pf.prime_factorization(number)
        factor_count_list = [prime_factorization[item] for item in prime_factorization]
        result = self.formula(factor_count_list)

        if self.DEBUG > 0:
            print('There are {} unique solutions for the factor list: {}. The smallest is: {}'.format(
                result, factor_count_list, number)
            )
        if result > self.factor_count:
            print(factor_count_list)

        return result

    def formula(self, factor_count_list):
        result = 1
        for value in factor_count_list:
            result += (((result * 2) - 1) * value)
        return result


def run_specific(number):
    puzzle = PuzzleSolver(max_value=1000000, debug=2)
    puzzle.run_specific(number)


def run_sequential(start=0, max_value=20000):
    puzzle = PuzzleSolver(max_value=max_value, debug=1)
    puzzle.run_sequential(start=start)


def run_unique_factorization_exponents(count=0, max_value=20000, debug=0, factor_count=1000, use_list=False, max_factors=30):
    puzzle = PuzzleSolver(max_value=max_value, debug=debug, factor_count=factor_count, max_factors=max_factors)
    if use_list:
        puzzle.run_unique_factorization_exponents_list_only(count=count)
    else:
        puzzle.run_unique_factorization_exponents(count=count)


if __name__ == "__main__":
    start_time = time.time()
    # run_unique_factorization_exponents(count=len(prime_list), debug=0, factor_count=4000000, use_list=True, max_factors=300)
    run_unique_factorization_exponents(count=len(prime_list), max_value=10000000000000000, debug=0, factor_count=4000000, max_factors=300)
    # run_specific([510510])
    # run_sequential(start=0, max_value=200000)
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
