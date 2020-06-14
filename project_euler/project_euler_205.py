"""
Project Euler 205

Peter has nine four-sided (pyramidal) dice, each with faces numbered 1, 2, 3, 4.
Colin has six six-sided (cubic) dice, each with faces numbered 1, 2, 3, 4, 5, 6.
"""

class PuzzleSolver(object):

    def run(self):
        player_1 = DiceGroup(9, 4, 'Peter')
        player_1.print_totals()

        player_2 = DiceGroup(6, 6, 'Colin')
        player_2.print_totals()

        # What are the odds of Peter beating Colin?
        win_rate = self.compare_players(player_1, player_2)
        print(win_rate)

        # What are the odds of Colin beating Peter?
        #win_rate = self.compare_players(player_2, player_1)
        #print(win_rate)

        return win_rate

    def compare_players(self, player_1, player_2):
        totals = player_1.totals
        rolls_that_are_less_than_dict = player_2.get_rolls_that_are_less_than_dict()
        total_rolls = player_2.total_rolls
        wins_count = 0
        rolls_count = 0

        for total in totals:
            roll_attempts = totals[total]
            wins = rolls_that_are_less_than_dict.get(total, 0)
            print("{} was rolled {} times by {}".format(total, roll_attempts, player_1.name))
            print("{} had {} / {} rolls less than {}".format(player_2.name, rolls_that_are_less_than_dict[total], total_rolls, total))
            print("{} will win {} and lose {} out of {} total, {} times".format(player_1.name, wins, losses, total_rolls, roll_attempts))
            print("")
            wins_count += roll_attempts * wins
            rolls_count += roll_attempts * total_rolls

        win_rate = float(wins_count) / float(rolls_count)
        print("Win Rate: {} / {} = {}".format(wins_count, rolls_count, win_rate))

        return win_rate

class DiceGroup(object):

    def __init__(self, dice_count, side_count, name):
        self.totals = {}
        self.dice_count = dice_count
        self.side_count = side_count
        self.name = name
        self.construct_totals_aggregate([0 for x in range(self.dice_count)], 0)
        self.total_rolls = pow(self.side_count, self.dice_count)

    def print_totals(self):
        running_total = 0
        for total in self.totals:
            print("{} was rolled {} times".format(total, self.totals[total]))
            running_total += self.totals[total]
        print "{} total rolls".format(running_total)

    def add_total(self, total):
        if total in self.totals:
            self.totals[total] += 1
        else:
            self.totals[total] = 1

    def construct_totals_aggregate(self, rolled_numbers, position):

        if position == self.dice_count:
            self.add_total(sum(rolled_numbers))
            return

        for side in range(1, self.side_count + 1):
            rolled_numbers[position] = side
            self.construct_totals_aggregate(rolled_numbers, position + 1)

    def get_rolls_that_are_less_than_dict(self):
        running_total = 0
        rolls_that_are_less_than = {}

        for total in range(max(self.totals)):
            running_total += self.totals.get(total, 0)
            rolls_that_are_less_than[total + 1] = running_total
        # print(rolls_that_are_less_than)
        return rolls_that_are_less_than

if __name__ == "__main__":
    puzzle = PuzzleSolver()
    puzzle.run()
