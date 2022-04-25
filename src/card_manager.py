import arcade

from src import card_class, player
from constants import FACE_DOWN_PILE, DISCARD_PILE, GO_DOWN_PILE, COMPLETED_CARDS, CARD_MOVE_SOUND


class CardManager:
    def __init__(self):
        self.card_list = None
        self.card_dict = None
        self.small_card_list = None
        self.piles = None

    def round_start_sequence(self):
        self.turn_start_sequence()

    def round_end_sequence(self):
        pass

    def turn_start_sequence(self):
        self.flip_all_cards_up()

    def turn_end_sequence(self):
        self.flip_all_cards_down()

    def flip_all_cards_up(self):
        for pile in self.piles[1:]:
            for card in pile:
                card.flip_up()

    def flip_all_cards_down(self):
        for pile in self.piles:
            for card in pile:
                card.flip_down()

    def return_cards(self, cur_player: player.Player):
        if len(self.piles[COMPLETED_CARDS]) != 0:
            for _ in range(len(self.piles[COMPLETED_CARDS])):
                self.move_card_to_new_pile(
                    self.piles[COMPLETED_CARDS][0],
                    cur_player.hand_index,
                    COMPLETED_CARDS
                )
        if len(self.piles[GO_DOWN_PILE]) != 0:
            for _ in range(len(self.piles[GO_DOWN_PILE])):
                self.move_card_to_new_pile(
                    self.piles[GO_DOWN_PILE][0],
                    cur_player.hand_index,
                    GO_DOWN_PILE
                )

    def move_card_to_new_pile(self, card: card_class.Card, destination_pile_index: int, original_pile_index: int):
        """
        Handles movement of a card from one pile to another,
        ensuring the sprite is never in two piles at once.
        """
        try:
            self.remove_card_from_pile(id(card))
        except:
            pass
        self.piles[destination_pile_index].append(card)

        if original_pile_index != destination_pile_index:
            if destination_pile_index != FACE_DOWN_PILE and destination_pile_index != COMPLETED_CARDS:
                arcade.play_sound(CARD_MOVE_SOUND, volume=0.5)

    def remove_card_from_pile(self, card_id):
        """
        Removes card from its pile.
        """
        for pile in self.piles:
            for card in pile:
                if id(card) == card_id:
                    pile.remove(card)
                    break
