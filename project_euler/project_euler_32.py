"""
Project Euler 32
"""
import time


class PuzzleSolver(object):

    def __init__(self):
        self.results = []

    def run(self):
        total = self.run_recursive([])

        print(total)
        print('Total {}'.format(total))
        print('Result = {}'.format(self.results))
        print('Sum = {}'.format(sum(self.results)))  # Sum all values

        unique_results = set(self.results)
        print('Unique Results: {}'.format(unique_results))  # Unique values
        print('Unique Sum = {}'.format(sum(unique_results)))  # Sum unique values
        return total

    def run_recursive(self, number_list):
        # print('In run_recursive. List: {}'.format(number_list))

        if len(number_list) == 4:
            return self.find_multiplicans(number_list)

        total = 0
        for x in xrange(1, 10):
            if x not in number_list:
                total += self.run_recursive(number_list + [x])
        return total

    def find_multiplicans(self, number_list):
        number = number_list[0] * 1 + number_list[1] * 10 + number_list[2] * 100 + number_list[3] * 1000
        # number = number_list[0] * 1000 + number_list[1] * 100 + number_list[2] * 10 + number_list[3] * 1
        return self.find_multiplicans_recursive(number, [], number_list)

    def find_multiplicans_recursive(self, target, number_list, off_limits):
        # print('In find_multiplicans_recursive. Target: {} List: {}'.format(target, number_list))

        if len(number_list) == 5:
            return self.calculate_result(target, number_list)

        total = 0
        for x in xrange(1, 10):
            if x not in number_list and x not in off_limits:
                total += self.find_multiplicans_recursive(target, number_list + [x], off_limits)
        return total

    def calculate_result(self, target, number_list):
        total = 0
        # print('In calculate_result. Target: {} List: {}'.format(target, number_list))
        multiplican_1 = number_list[0] * 1 + number_list[1] * 10
        multiplican_2 = number_list[2] * 1 + number_list[3] * 10 + number_list[4] * 100
        if multiplican_1 * multiplican_2 == target:
            print('Success! {} * {} = {}'.format(multiplican_1, multiplican_2, target))
            self.results.append(target)
            total += 1
        multiplican_1 = number_list[0] * 1
        multiplican_2 = number_list[1] * 1 + number_list[2] * 10 + number_list[3] * 100 + number_list[4] * 1000
        if multiplican_1 * multiplican_2 == target:
            print('Success! {} * {} = {}'.format(multiplican_1, multiplican_2, target))
            self.results.append(target)
            total += 1
        return total


if __name__ == "__main__":
    start_time = time.time()
    puzzle = PuzzleSolver()
    puzzle.run()
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
