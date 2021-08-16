from constants import *


def straight_line(i, current_player_hand, piles, scale):
    """
    Math for spacing the cards out evenly.
    """
    return 110 * scale * i - \
           ((((len(piles[current_player_hand])) - 1) * 110 * scale) / 2) + self.screen_width / 2


def get_hand_position(piles, num_players, scale):
    """
    Positions the cards in the player's hand.
    """
    for player in range(3, num_players + 3):
        for i in range(len(piles[player])):
            card = piles[player][i]
            card.center_x = straight_line(i, player)
            card.center_y = PLAYER_HAND_Y * scale