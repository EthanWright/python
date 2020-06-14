"""
Project Euler 
"""
import time


class PuzzleSolver(object):
    total_goal = 200

    coin_values = [1, 2, 5, 10, 20, 50, 100, 200]

    def run(self):
        result = self.do_recursive(0, 0)
        print(result)
        return result

    def do_recursive(self, amount, last_value):
        if amount == self.total_goal:
            return 1
        elif amount > self.total_goal:
            return -1

        # TODO Optimize
        total = 0
        for coin_value in self.coin_values:
            if coin_value < last_value:
                continue
            result = self.do_recursive(amount + coin_value, coin_value)
            if result < 0:
                return total
            else:
                total += result
        return total


if __name__ == "__main__":
    start_time = time.time()
    puzzle = PuzzleSolver()
    puzzle.run()
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
