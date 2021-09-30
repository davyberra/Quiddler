import random
import time
from typing import List

from constants import WORD_LIST, CARD_SCORE
from card_class import Card

class ComputerTurn:
    def two_letter_valid(self, c1: Card, c2: Card):
        l1, l2 = c1.value, c2.value
        if l1 + l2 in WORD_LIST:
            return [c1, c2]
        if l2 + l1 in WORD_LIST:
            return [c2, c1]
        return None

    def three_letter_valid(self, c1: Card, c2: Card, c3: Card):
        l1, l2, l3 = c1.value, c2.value, c3.value
        if l1 + l2 + l3 in WORD_LIST:
            return [c1, c2, c3]
        if l1 + l3 + l2 in WORD_LIST:
            return [c1, c3, c2]
        if l2 + l1 + l3 in WORD_LIST:
            return [c2, c1, c3]
        if l2 + l3 + l1 in WORD_LIST:
            return [c2, c3, c1]
        if l3 + l1 + l2 in WORD_LIST:
            return [c3, c1, c2]
        if l3 + l2 + l1 in WORD_LIST:
            return [c3, c2, c1]
        return None

    def valid_playable_hand(self, cards: List[Card], result: List[List[Card]]):
        """
        Determine if a hand of cards is eligible to go down.
        Return the words if true, and return None if false.
        :param cards: List[Card]
        :param result: List[List[Card]]
        """
        if len(cards) > 3 and len(cards) != 5:
            for i in range(len(cards)):
                for j in range(i + 1, len(cards)):
                    for k in range(j + 1, len(cards)):
                        word = self.three_letter_valid(cards[i], cards[j], cards[k])
                        if word:
                            new_cards = cards[:]
                            for card in word:
                                new_cards.remove(card)
                            if len(new_cards) == 1:
                                result.append(word)
                                return result
                            elif len(new_cards) > 2:
                                result.append(word)
                                return self.valid_playable_hand(new_cards, result)

        elif len(cards) > 2 and len(cards) != 4:
            for i in range(len(cards)):
                for j in range(i + 1, len(cards)):
                    word = self.two_letter_valid(cards[i], cards[j])
                    if word:
                        new_cards = cards[:]
                        for card in word:
                            new_cards.remove(card)
                        if len(new_cards) == 1:
                            result.append(word)
                            return result
                        elif len(new_cards) > 2:
                            result.append(word)
                            return self.valid_playable_hand(new_cards, result)

    def valid_last_hand (self, cards: List[Card], result: List[List[Card]]):
        """
        Allow the computer to go down with the valid words available on the final turn.
        Return the words if true, and return None if false.
        :param cards: List[Card]
        :param result: List[List[Card]]
        """
        if len(cards) > 3 and len(cards) != 5:
            for i in range(len(cards)):
                for j in range(i + 1, len(cards)):
                    for k in range(j + 1, len(cards)):
                        word = self.three_letter_valid(cards[i], cards[j], cards[k])
                        if word:
                            new_cards = cards[:]
                            for card in word:
                                new_cards.remove(card)
                            if len(new_cards) == 1:
                                result.append(word)
                                return result
                            elif len(new_cards) > 2:
                                result.append(word)
                                return self.valid_last_hand(new_cards, result)
                            elif len(new_cards) == 2:
                                result.append(word)
                                return result

        elif len(cards) > 2 and len(cards) != 4:
            for i in range(len(cards)):
                for j in range(i + 1, len(cards)):
                    word = self.two_letter_valid(cards[i], cards[j])
                    if word:
                        new_cards = cards[:]
                        for card in word:
                            new_cards.remove(card)
                        if len(new_cards) == 1:
                            result.append(word)
                            return result
                        elif len(new_cards) > 2:
                            result.append(word)
                            return self.valid_last_hand(new_cards, result)
                        elif len(new_cards) == 2:
                            result.append(word)
                            return result

        return result

    def valid_hand_random(self, cards: List[Card]):
        """
        Select cards at random with random ranges to find words.
        """
        print("Called random computer hand method.")
        start_time = time.time()
        end_time = start_time
        cur_result = []
        result = []
        cur_cards = cards[:]
        while end_time < start_time + 2:
            cur_word_list = []
            try:
                word_length = random.randrange(2, len(cur_cards) + 1)
            except ValueError:
                print(cur_cards, cur_result)
                return
            indices_left = [i for i in range(len(cur_cards))]
            while len(indices_left) > len(cur_cards) - word_length:
                rand_i = random.randrange(0, len(cards) + 1)
                if rand_i in indices_left:
                    cur_word_list.append(cur_cards[rand_i])
                    indices_left.remove(rand_i)
            cur_word = ""
            for val in cur_word_list:
                cur_word += val.value
            if cur_word in WORD_LIST:
                cur_result.append(cur_word_list)
                for card in cur_word_list:
                    cur_cards.remove(card)
                if len(cur_cards) == 1:
                    return cur_result
                elif len(cur_cards) == 2 or len(cur_cards) == 0:
                    print(f"got here with: {cur_word}")
                    cur_cards = cards[:]
                    result = cur_result[:]
                    cur_result = []
            end_time = time.time()

        return result

    def take_turn(self, face_down_pile: List[Card], discard_pile: List[Card], computer_hand: List[Card], final_turn: bool) -> list:
        """
        Main method for computer player's turn sequence.
        1. Draws from face-down pile
        2. Plays hand if valid
        3. Discards random card

        Returns new face-down pile, discard pile, computer hand, valid hand( ? List[Card] : None)
        """
        drawn_card = face_down_pile.pop()
        computer_hand.append(drawn_card)
        if final_turn:
            valid_hand = self.valid_last_hand(computer_hand, [])
        else:
            valid_hand = self.valid_hand_random(computer_hand)
            if valid_hand:
                card_count = 0
                for word in valid_hand:
                    for card in word:
                        card_count += 1
                if card_count != len(computer_hand) - 1:
                    print(f'valid hand: {card_count} computer hand: {len(computer_hand)}')
                    valid_hand = None
        discard = computer_hand
        if valid_hand:
            for word in valid_hand:
                for card in word:
                    discard.remove(card)

            if len(discard) > 1:
                max_score = [0, None]
                for i, card in enumerate(discard):
                    if CARD_SCORE[card.value] > max_score[0]:
                        max_score = [CARD_SCORE[card.value], i]
                discard = discard[max_score[1]]
            else:
                discard = discard[0]
        else:
            discard = computer_hand[random.randrange(len(computer_hand))]
        discard_pile.append(discard)
        computer_hand.remove(discard)
        return [face_down_pile, discard_pile, computer_hand, valid_hand]

# c = ComputerTurn()
# letters = ['t','b','a','x','a','e','g','g','a','q','i']
# letters2 = ['g','r','e','a','t']
# cards = []
# for letter in letters2:
#     card = Card(letter)
#     cards.append(card)
#
# result = c.valid_hand_random(cards)
# if result:
#     for word in result:
#         w = ""
#         for card in word:
#             w += card.value
#         print(w)
# else:
#     print("No playable hand found.")