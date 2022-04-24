import random

import card_class


def create_cards(card_values, position, scale):
    """
    Create every card, both regular and small versions
    Small cards are used to display a player's completed words
    after they go down
    """
    card_list = []
    card_dict = {}
    for value in card_values:
        card = card_class.Card(value, scale)
        card.set_position(*position)
        card_list.append(card)
        card.flip_down()
        card_dict[card] = value
    return card_list, card_dict


def shuffle_cards(cards):
    """Shuffle the cards"""
    for pos1 in range(len(cards)):
        pos2 = random.randrange(len(cards))
        cards[pos1], cards[pos2] = cards[pos2], cards[pos1]
    return cards
