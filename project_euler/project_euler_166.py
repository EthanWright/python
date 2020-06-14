"""
Project Euler 166
"""
import time


class PuzzleSolver(object):

    def __init__(self, width):
        self.total = 0
        self.width = width

    def run(self):
        number_list = [0] * pow(self.width - 1, 2)  # (width - 1) ^ 2
        last_position = len(number_list) - 1
        position = last_position
        while position >= 0:
            if position == last_position:
                self.find_solution_for_starting_grid(number_list)

            number_list[position] += 1

            if number_list[position] >= 10:
                number_list[position] = 0
                position -= 1
            else:
                position = last_position

    def find_solution_for_starting_grid(self, number_list):
        if self.width == 3:
            return self.find_solution_for_starting_grid_3x3(number_list)
        elif self.width == 4:
            return self.find_solution_for_starting_grid_4x4(number_list)

    def find_solution_for_starting_grid_3x3(self, number_list):
        """
        XXX
        0X0
        000
        """
        total = number_list[0] + number_list[1] + number_list[2]
        some_val = total - number_list[3]
        empty_1 = some_val - number_list[0]
        empty_2 = some_val - number_list[1]
        empty_3 = some_val - number_list[2]
        if empty_1 < 0 or empty_2 < 0 or empty_3 < 0:
            return False
        if empty_1 > 9 or empty_2 > 9 or empty_3 > 9:
            return False

        empty_4 = total - (empty_3 + number_list[0])
        empty_5 = total - (empty_1 + number_list[2])

        if empty_4 < 0 or empty_5 < 0:
            return False
        if empty_4 > 9 or empty_5 > 9:
            return False

        if empty_4 + number_list[3] + empty_5 != total:
            return False

        solution = [
            number_list[0], number_list[1], number_list[2],
            empty_4, number_list[3], empty_5,
            empty_3, empty_2, empty_1
        ]
        print(solution)
        return True

    def find_solution_for_starting_grid_4x4(self, number_list):
        """
        Minimal set where the full grid can be deterministically completed from the known total
        XXXX
        0XX0
        X000
        0XX0
        """
        total = number_list[0] + number_list[1] + number_list[2] + number_list[3]
        empty_1 = total - (number_list[1] + number_list[4] + number_list[7])
        empty_2 = total - (number_list[2] + number_list[5] + number_list[8])
        empty_3 = total - (number_list[6] + empty_1 + empty_2)

        if empty_1 < 0 or empty_2 < 0 or empty_3 < 0:
            return False
        if empty_1 > 9 or empty_2 > 9 or empty_3 > 9:
            return False

        empty_4 = total - (number_list[3] + number_list[5] + empty_1)
        empty_5 = total - (number_list[0] + number_list[4] + empty_2)

        if empty_4 < 0 or empty_5 < 0:
            return False
        if empty_4 > 9 or empty_5 > 9:
            return False

        empty_6 = total - (empty_4 + number_list[6] + number_list[0])
        empty_7 = total - (empty_3 + empty_5 + number_list[3])

        if empty_6 < 0 or empty_7 < 0:
            return False
        if empty_6 > 9 or empty_7 > 9:
            return False

        if empty_6 + number_list[4] + number_list[5] + empty_7 != total:
            return False
        if empty_4 + number_list[7] + number_list[8] + empty_5 != total:
            return False

        solution = [
            number_list[0], number_list[1], number_list[2], number_list[3],
            empty_6, number_list[4], number_list[5], empty_7,
            number_list[6], empty_1, empty_2, empty_3,
            empty_4, number_list[7], number_list[8], empty_5
        ]

        # print(solution)
        for x in xrange(pow(self.width, 2)):
            if x % self.width == 0 and x > 1:
                print('')
            print(solution[x]),
        print('\n')
        return True


if __name__ == "__main__":
    start_time = time.time()
    # puzzle = PuzzleSolver(width=3)
    puzzle = PuzzleSolver(width=4)
    puzzle.run()
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
