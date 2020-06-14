"""
Project Euler Prime Factorization Module
"""


class PrimeFactorization(object):
    TWO = 2

    def __init__(self, debug=0):
        self.DEBUG = debug
        self.factors = {}

    def _log_factor(self, factor):
        print('Adding Factor {}'.format(factor))

    def prime_factorization(self, number):
        if self.DEBUG > 0:
            print('Factorizing {}'.format(number))
        factors = {}

        while number % self.TWO == 0 and number > 0:
            if self.DEBUG > 1:
                self._log_factor(self.TWO)
            if self.TWO not in factors:
                factors[self.TWO] = 0
            factors[self.TWO] += 1
            number = number / self.TWO

        factor = 3
        while factor <= (number / (factor - 1)):
            if number % factor == 0:
                if factor not in factors:
                    factors[factor] = 0
                factors[factor] += 1
                if self.DEBUG > 1:
                    self._log_factor(factor)
                number = number / factor
            else:
                factor += 2

        if number > 1:
            if self.DEBUG > 1:
                self._log_factor(factor)
            if number not in factors:
                factors[number] = 0
            factors[number] += 1

        return factors
