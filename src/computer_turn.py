import random
from typing import List

from constants import WORD_LIST
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

    def take_turn(
            self,
            face_down_pile: List[Card],
            discard_pile: List[Card],
            computer_hand: List[Card]
    ) -> list:
        """
        Main method for computer player's turn sequence.
        1. Draws from face-down pile
        2. Plays hand if valid
        3. Discards random card

        Returns new face-down pile, discard pile, computer hand, valid hand( ? List[Card] : None)
        """
        drawn_card = face_down_pile.pop()
        computer_hand.append(drawn_card)
        valid_hand = self.valid_playable_hand(computer_hand, [])
        discard = computer_hand
        if valid_hand:
            for word in valid_hand:
                for card in word:
                    discard.remove(card)
            discard = discard[0]
        else:
            discard = computer_hand[random.randrange(len(computer_hand))]
        discard_pile.append(discard)
        computer_hand.remove(discard)
        return [face_down_pile, discard_pile, computer_hand, valid_hand]

# c = ComputerTurn()
# letters = ['t','b','a','x','a','e','g','g','a','q','i']
# cards = []
# for letter in letters:
#     card = Card(letter)
#     cards.append(card)
#
# result = c.valid_playable_hand(cards, [])
# if result:
#     for word in result:
#         w = ""
#         for card in word:
#             w += card.value
#         print(w)
# else:
#     print("No playable hand found.")