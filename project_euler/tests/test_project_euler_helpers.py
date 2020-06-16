"""
Test Project Euler Long Division
> python -m tests.project_euler_helpers
"""
import unittest
import time

from project_euler_helpers import LongDivision, PrimeFactorization


class TestPrimeFactorization(unittest.TestCase):

    def test_prime_factorization(self):

        pf = PrimeFactorization(debug=1)
        result = pf.prime_factorization(2)
        self.assertEqual(result, {2: 1})
        result = pf.prime_factorization(137)
        self.assertEqual(result, {137: 1})
        result = pf.prime_factorization(64)
        self.assertEqual(result, {2: 6})
        result = pf.prime_factorization(120)
        self.assertEqual(result,  {2: 3, 3: 1, 5: 1})
        result = pf.prime_factorization(729)
        self.assertEqual(result,  {3: 6})
        result = pf.prime_factorization(248589)
        self.assertEqual(result,  {3: 6, 11: 1, 31: 1})
        result = pf.prime_factorization(6469693230)
        self.assertEqual(result,  {2: 1, 3: 1, 5: 1, 7: 1, 11: 1, 13: 1, 17: 1, 19: 1, 23: 1, 29: 1})
        result = pf.prime_factorization(95041567)
        self.assertEqual(result,  {31: 1, 37: 1, 41: 1, 43: 1, 47: 1})

    def _test_prime_factorization_speed(self):
        start_time = time.time()
        pf = PrimeFactorization(debug=0)
        for number in xrange(10000):
            pf.prime_factorization(number)
        print("---Execution took {} Seconds Total ---".format(time.time() - start_time))


class TestLongDivision(unittest.TestCase):

    def test_long_division(self):
        ld = LongDivision(debug=1)

        result = ld.divide(1, 2)
        self.assertEqual(result, '0.5')
        result = ld.divide(1, 3)
        self.assertEqual(result, '0.' + '3' * 100)
        result = ld.divide(1, 18)
        self.assertEqual(result, '0.0' + '5' * 99)
        result = ld.divide(1, 20)
        self.assertEqual(result, '0.05')
        result = ld.divide(1, 101)
        self.assertEqual(result, '0.' + '0099' * 25)
        result = ld.divide(30, 1)
        self.assertEqual(result, '30')
        result = ld.divide(301, 2)
        self.assertEqual(result, '150.5')
        result = ld.divide(87, 87)
        self.assertEqual(result, '1')


if __name__ == '__main__':
    unittest.main()