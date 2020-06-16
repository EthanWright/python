"""
Test Project Euler 80
> python -m tests.test_project_euler_80
"""
import unittest

from project_euler_80 import PuzzleSolver, BigNumber


class TestPuzzleSolver(unittest.TestCase):

    def _test1(self):
        four = BigNumber(4, display_precision=5)
        three = BigNumber(3, display_precision=5)
        print(four)
        print(three)
        eight = four + four
        seven = four + three
        print(eight)
        print(seven)

        print(eight*seven)
        print(eight+seven)
        print(eight-seven)
        print(seven - eight)

    def test12(self):
        digits = 50
        num1 = BigNumber(0, display_precision=digits)
        num2 = BigNumber(0, display_precision=digits)
        num1.decimals = [3, 5, 1] + [0] * (digits + 10)
        num2.decimals = [1, 7, 9] + [0] * (digits + 10)

        print(num1)
        print(num2)
        print(num2 + num1)
        print(num1 + num2)
        print(num1 - num2)
        print(".351 - .179 = 0.172")
        print(num2 - num1)
        print(".179 - .351 = -0.172")

    def test2(self):
        # BigNumber(2).calculate_sqrt()
        # BigNumber(23).calculate_sqrt()
        # BigNumber(24).calculate_sqrt()
        BigNumber(25).calculate_sqrt()

    def _test3(self):
        target = BigNumber(100)
        for x in xrange(100):
            target.divide_by_two()
            print(target)

    def _test4(self):
        target = BigNumber(1)
        for x in xrange(100):
            target.divide_by_two()
            print(target)

    def _test5(self):
        target = BigNumber(0)
        target.decimals[2] = 2
        print(target)

        for x in xrange(20):
            target = target * target
            print(target)


if __name__ == '__main__':
    unittest.main()