"""
Test Project Euler 54
> python -m tests.test_project_euler_54
"""
import unittest

from project_euler_54 import PuzzleSolver, Hand, Scores


class TestPuzzleSolver(unittest.TestCase):

    def check_score(self, hand_string, expected_score, expected_score_rank):
        ps = PuzzleSolver()
        hand = ps.generate_hand(hand_string)

        self.assertEqual(hand.get_score(), expected_score)
        self.assertEqual(hand.score_rank, expected_score_rank)

    def test_check_for_royal_flush(self):
        hand_string = 'TS JS QS KS AS'
        score = Scores.ROYAL_FLUSH
        score_rank = 14
        self.check_score(hand_string, score, score_rank)

    def test_check_for_straight_flush(self):
        hand_string = '2D 3D 4D 5D 6D'
        score = Scores.STRAIGHT_FLUSH
        score_rank = 6
        self.check_score(hand_string, score, score_rank)

    def test_check_for_four_of_a_kind(self):
        hand_string = '7S 7D 7H 7C 9C'
        score = Scores.FOUR_OF_A_KIND
        score_rank = 7
        self.check_score(hand_string, score, score_rank)

    def test_check_for_full_house(self):
        hand_string = '7S 7D 7H 9S 9C'
        score = Scores.FULL_HOUSE
        score_rank = 9
        self.check_score(hand_string, score, score_rank)

    def test_check_for_flush(self):
        hand_string = '9D 3D 4D 5D 6D'
        score = Scores.FLUSH
        score_rank = 9
        self.check_score(hand_string, score, score_rank)

    def test_check_for_straight(self):
        hand_string = '2D 3D 4H 5D 6D'
        score = Scores.STRAIGHT
        score_rank = 6
        self.check_score(hand_string, score, score_rank)

    def test_check_for_three_of_a_kind(self):
        hand_string = '7S 7D 7H 8C 9C'
        score = Scores.THREE_OF_A_KIND
        score_rank = 7
        self.check_score(hand_string, score, score_rank)

    def test_check_for_two_pairs(self):
        hand_string = '7S 7D TH 9S 9C'
        score = Scores.TWO_PAIRS
        score_rank = 9
        self.check_score(hand_string, score, score_rank)

    def test_check_for_one_pair(self):
        hand_string = '7S 7D TH 9S 8C'
        score = Scores.ONE_PAIR
        score_rank = 7
        self.check_score(hand_string, score, score_rank)

    def test_get_high_card_value(self):
        hand_string = 'KS 7D TH 9S 8C'
        score = Scores.HIGH_CARD
        score_rank = 13
        self.check_score(hand_string, score, score_rank)


if __name__ == '__main__':
    unittest.main()