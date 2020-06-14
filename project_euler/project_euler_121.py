"""
Project Euler 121
"""

#
# class Choice(object):
#
#     def __init__(self, red_disc_count):
#         self.red_disc_count = red_disc_count
#         self.index = 0
#
#     def get_values(self):
#         return [-1] * self.red_disc_count + [1]
#


class PuzzleSolver(object):

    def __init__(self):
        self.turns = 15
        self.scores = {0: 1}

    def run(self):
        for red_disc_count in xrange(1, self.turns + 1):
            self.solve(red_disc_count)
            # print(self.scores)
            wins = sum([self.scores[score] for score in self.scores if score > 0])
            total = sum([self.scores[score] for score in self.scores])
            print("Win Chance is {} / {} for Turn {} with {} Red Disks and 1 Blue Disc".format(
                wins, total, red_disc_count, red_disc_count)
            )
            print("They should allocate ${} for the prize pool".format(total / wins))  # Truncated to nearest INT

    def solve(self, red_disc_count):
        new_scores = {}

        # Multiply the previous score possibilities by -1 for each Red Disc
        for score in self.scores:
            new_scores[score - 1] = self.scores[score] * red_disc_count

        # Account for the Blue Disc with a score of 1 added to all of the previous scores
        for score in self.scores:
            if score + 1 not in new_scores:
                new_scores[score + 1] = 0
            new_scores[score + 1] += self.scores[score]

        self.scores = new_scores

    # SLOW and stupid way
    # def run_old(self):
    #     for red_disc_count in xrange(1, self.turns + 1):
    #         choice = Choice(red_disc_count)
    #         self.choices.append(choice)
    #
    #     self.solve([x for x in xrange(self.turns)], 0)
    #     print("{} Turns | {}/{}".format(self.turns, self.success_count, self.attempt_count))
    #
    # def solve(self, pulls, depth):
    #     if depth >= self.turns:
    #         if sum(pulls) > 0:
    #             self.success_count += 1
    #         self.attempt_count += 1
    #         return
    #
    #     for value in self.choices[depth].get_values():
    #         pulls[depth] = value
    #         self.solve(pulls, depth + 1)


if __name__ == "__main__":
    puzzle = PuzzleSolver()
    puzzle.run()

"""
1 Turns | 1/2
2 Turns | 1/6
3 Turns | 7/24
4 Turns | 11/120
5 Turns | 101/720
6 Turns | 197/5040
7 Turns | 2311/40320
8 Turns | 5119/362880
9 Turns | 73639/3628800
"""