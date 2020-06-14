"""
Project Euler 42
"""
import time


class PuzzleSolver(object):
    triangle_numbers_to_calc = 30
    triangle_numbers = [int(0.5 * x * (x + 1)) for x in xrange(triangle_numbers_to_calc)]
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letter_values = {}
    #letter_values = zip(letters, [x for x in xrange(1, len(letters) + 1)])

    def __init__(self):
        for x in xrange(len(self.letters)):
            self.letter_values[self.letters[x]] = x + 1

    def calc_triangle_numbers(self, n):
        return

    def calc_word_value(self, word):
        value = 0
        for letter in word:
            value += self.letter_values[letter]
        return value

    def run(self):
        total = 0
        file_name = 'data/project_euler_42_data.txt'

        with open(file_name) as words_file:
            line = words_file.readline().rstrip().replace('\"', '')
            while line:
                words = line.split(',')
                #print(words)
                for word in words:
                    value = self.calc_word_value(word)
                    if value in self.triangle_numbers:
                        total += 1
                    #print(value)
                line = words_file.readline().rstrip()

        # print(self.letter_values)
        print(total)


if __name__ == "__main__":
    start_time = time.time()
    puzzle = PuzzleSolver()
    puzzle.run()
    print("--- Execution took {} Seconds Total ---".format(time.time() - start_time))
