"""
Project Euler 54
"""
import time


class CardConstants(object):

    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4

    ABRV_TO_SUITS_MAP = {
        'S': SPADES,
        'H': HEARTS,
        'D': DIAMONDS,
        'C': CLUBS,
    }

    SUIT_TO_ABRV_MAP = {
        SPADES: 'Spades',
        HEARTS: 'Hearts',
        DIAMONDS: 'Diamonds',
        CLUBS: 'Clubs',
    }

    ABRV_TO_VALUES_MAP = {
        'A': 14,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
    }

    VALUES_TO_ABRV_MAP = {
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: 'Jack',
        12: 'Queen',
        13: 'King',
        14: 'Ace',
    }
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Scores(object):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    english = {
        HIGH_CARD: 'High Card',
        ONE_PAIR: 'One Pair',
        TWO_PAIRS: 'Two Pairs',
        THREE_OF_A_KIND: '3 Of A Kind',
        STRAIGHT: 'Straight',
        FLUSH: 'Flush',
        FULL_HOUSE: 'Full House',
        FOUR_OF_A_KIND: '4 Of A Kind',
        STRAIGHT_FLUSH: 'Straight Flush',
        ROYAL_FLUSH: 'Royal Flush'
    }


class Card(object):

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        value = CardConstants.VALUES_TO_ABRV_MAP[self.value]
        suit = CardConstants.SUIT_TO_ABRV_MAP[self.suit]
        return "{} of {}".format(value, suit)

    def __gt__(self, other):
        return self.value > other.value


class Hand(object):

    EXPECTED_CARDS = 5

    def __init__(self):
        self.card_count = 0
        self.cards = []
        self.score_rank = 0

    def __repr__(self):
        return ', '.join([card.__repr__() for card in sorted(self.cards)])

    def add_card(self, card):
        self.cards.append(card)
        self.card_count = len(self.cards)
        # TODO Validate Card?

    @property
    def values(self):
        return [card.value for card in self.cards] or [0]

    @property
    def card_values_sorted(self):
        return sorted(self.values)

    @property
    def suits(self):
        return [card.suit for card in self.cards] or [0]

    def get_score(self):
        score_ranking_list = [
            # (Hand score, Function to check for exact match of hand rank)
            (Scores.ROYAL_FLUSH, self.check_for_royal_flush),
            (Scores.STRAIGHT_FLUSH, self.check_for_straight_flush),
            (Scores.FOUR_OF_A_KIND, self.check_for_four_of_a_kind),
            (Scores.FULL_HOUSE, self.check_for_full_house),
            (Scores.FLUSH, self.check_for_flush),
            (Scores.STRAIGHT, self.check_for_straight),
            (Scores.THREE_OF_A_KIND, self.check_for_three_of_a_kind),
            (Scores.TWO_PAIRS, self.check_for_two_pairs),
            (Scores.ONE_PAIR, self.check_for_one_pair),
            (Scores.HIGH_CARD, self.get_high_card_value),
        ]

        for rank in score_ranking_list:
            result = rank[1].__call__()
            if result:
                self.score_rank = result
                return rank[0]

    def check_for_royal_flush(self):
        royal = set(self.values) == {
            CardConstants.TEN, CardConstants.JACK, CardConstants.QUEEN, CardConstants.KING, CardConstants.ACE
        }
        if royal:
            return self.check_for_flush()
        return False

    def check_for_straight_flush(self):
        straight = self.check_for_straight()
        flush = self.check_for_flush()
        if straight and flush:
            return self.get_high_card_value()
        return False

    def check_for_four_of_a_kind(self):
        return self.check_for_x_of_a_kind(4)

    def check_for_full_house(self):
        one_pair = self.check_for_one_pair()
        three_of_a_kind = self.check_for_three_of_a_kind()
        if one_pair and three_of_a_kind:
            # TODO Should it be from the Pair, or the Triplet, or either? Doesn't seem to matter...
            return self.get_high_card_value()

    def check_for_flush(self):
        suit_count = self.get_suit_count()
        for suit in suit_count:
            if suit_count[suit] == self.EXPECTED_CARDS:
                return self.get_high_card_value()

    def check_for_straight(self):
        if len(self.values) != self.EXPECTED_CARDS:
            return False

        last_value = None
        sorted_values = sorted(self.values)

        for value in sorted_values:
            if last_value:
                # TODO Is this right? Do Straights wrap around? Or just the Ace? Doesn't seem to matter...
                if value != last_value + 1:  # and value != last_value - 12:
                    return False
            last_value = value
        return self.get_high_card_value()

    def check_for_three_of_a_kind(self):
        return self.check_for_x_of_a_kind(3)

    def check_for_two_pairs(self):
        return self.check_for_x_of_a_kind(2, amount=2)

    def check_for_one_pair(self):
        return self.check_for_x_of_a_kind(2, amount=1)

    def get_high_card_value(self):
        return max(self.values)

### AUX FUNCTIONS ###

    def get_high_card(self):
        return max(self.cards)

    def get_suit_count(self):
        suit_count = {}
        for suit in self.suits:
            if suit not in suit_count:
                suit_count[suit] = 0
            suit_count[suit] += 1
        return suit_count

    def get_values_count(self):
        values_count = {}
        for value in self.values:
            if value not in values_count:
                values_count[value] = 0
            values_count[value] += 1
        return values_count

    def check_for_x_of_a_kind(self, target, amount=0):
        groups_found = 0
        rank = 0
        values_count = self.get_values_count()
        for value in values_count:
            if values_count[value] == target:
                if not amount:
                    return value
                groups_found += 1
                rank = max(value, rank)
        if amount:
            if groups_found == amount:
                return rank
        return False


class PuzzleSolver(object):
    def __init__(self):
        self.DEBUG = True
        self.player_1_wins = 0
        self.player_2_wins = 0
        self.draws = 0
        self.games_played = 0

    def run(self):
        file_name = 'data/project_euler_54_data.txt'

        with open(file_name) as poker_file:
            line = poker_file.readline().rstrip()
            while line:
                if self.DEBUG:
                    print("--- Hand {} ---".format(self.games_played + 1))
                hand_comparer = HandComparer(debug=self.DEBUG)
                result = hand_comparer.generate_and_compare_hands(line)
                self.score_result(result)
                self.games_played += 1
                line = poker_file.readline().rstrip()

        self.print_results()

    def score_result(self, result):
        if result > 0:
            self.player_1_wins += 1
        if result < 0:
            self.player_2_wins += 1
        if not result:
            self.draws += 1  # This should never happen

    def print_results(self):
        print("Player 1 won {} times out of {} games".format(self.player_1_wins, self.games_played))
        print("Player 2 won {} times out of {} games".format(self.player_2_wins, self.games_played))
        if self.draws:  # lol?
            print("There were {} Draws out of {} games".format(self.draws, self.games_played))


class HandComparer(object):

    def __init__(self, debug=False):
        self.DEBUG = debug

    def generate_and_compare_hands(self, hand_string):
        individual_cards = hand_string.split(' ')
        player_1_hand = self.generate_hand_from_string(individual_cards[:5])
        player_2_hand = self.generate_hand_from_string(individual_cards[5:])
        if self.DEBUG:
            print('Player 1: ({})\nPlayer 2: ({})'.format(player_1_hand, player_2_hand))

        result = self.compare_scores(player_1_hand.get_score(), player_2_hand.get_score(), card_values=False)
        if not result:
            result = self.compare_scores(player_1_hand.score_rank, player_2_hand.score_rank)
            if not result:
                result = self.compare_hands_in_order(player_1_hand.card_values_sorted, player_2_hand.card_values_sorted)
        return result

    def compare_scores(self, player_1_score, player_2_score, card_values=True):
        if self.DEBUG:
            self.print_score_comparison(player_1_score, player_2_score, card_values)
        return player_1_score - player_2_score

    def compare_hands_in_order(self, player_1_cards, player_2_cards):
        for rank in xrange(len(player_1_cards) - 1, 0, -1):  # Go Backwards, highest to lowest
            card_result = self.compare_scores(player_1_cards[rank], player_2_cards[rank])
            if card_result:
                return card_result
        return 0

    def print_score_comparison(self, player_1_score, player_2_score, card_values=True):
        result = player_1_score - player_2_score
        if not card_values:
            player_1_score = Scores.english[player_1_score]
            player_2_score = Scores.english[player_2_score]
        else:
            player_1_score = CardConstants.VALUES_TO_ABRV_MAP[player_1_score]
            player_2_score = CardConstants.VALUES_TO_ABRV_MAP[player_2_score]
        if result > 0:
            print("<{}> > <{}> - Player 1 Wins!".format(player_1_score, player_2_score))
        elif result < 0:
            print("<{}> < <{}> - Player 2 Wins!".format(player_1_score, player_2_score))
        elif result == 0:
            print("<{}> == <{}> - It's a Draw!".format(player_1_score, player_2_score))

    def string_to_card(self, card_string):
        # print(card_string)
        value_string = card_string[0]
        suit_string = card_string[1]
        value = CardConstants.ABRV_TO_VALUES_MAP.get(value_string, False)
        suit = CardConstants.ABRV_TO_SUITS_MAP.get(suit_string, False)
        if not value or not suit:
            return False
        card = Card(suit, value)
        return card

    def generate_hand_from_string(self, hand_string):
        # print(hand_string)
        if isinstance(hand_string, str):
            hand_string = hand_string.split(' ')
        hand = Hand()
        for card_string in hand_string:
            if card_string is not '':
                card = self.string_to_card(card_string.strip())
                if card:
                    hand.add_card(card)
        return hand


if __name__ == "__main__":
    start_time = time.time()
    puzzle = PuzzleSolver()
    puzzle.run()
    print("---Execution took {} Seconds Total ---".format(time.time() - start_time))
