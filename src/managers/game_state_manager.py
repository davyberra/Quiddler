from src.managers.manager import Manager
from src.utils.constants import DISCARD_PILE, COMPLETED_CARDS


class GameStateManager(Manager):
    def __init__(self, game_view, rnd_number: int):
        self.game_view = game_view
        self.rnd = 1
        self.rnd_hand_count = 3
        self.rnd_max = rnd_number
        # List of cards we're dragging with the mouse
        self.held_cards = None
        self.has_drawn = False
        self.has_discarded = False
        self.drawn_card_original_pile = None
        self.held_cards_original_pile = None
        # Used to track number of moves taken when trying to use Undo feature
        self.moves = None
        self.last_move = None

    def setup(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def round_start_sequence(self):
        self.turn_start_sequence()

    def round_end_sequence(self):
        self.determine_round_hand_count()
        # Increase round number
        self.rnd += 1

    def turn_start_sequence(self):
        self.moves = 0
        self.last_move = 0
        self.held_cards = []
        self.has_drawn = False
        self.has_discarded = False

    def turn_end_sequence(self):
        pass

    def determine_round_hand_count(self):
        # Determines whether the hand count should increase or decrease
        # depending on whether the game is in the first half or last half
        if self.rnd < 8:
            self.rnd_hand_count += 1
        elif self.rnd > 8:
            self.rnd_hand_count -= 1

    def handle_discard(self):
        """ Called when the player discards. """
        for card in self.game_view.game_state_manager.held_cards:
            self.game_view.card_manager.move_card_to_new_pile(card, DISCARD_PILE, self.held_cards_original_pile)
        self.has_discarded = True
        self.last_move = self.moves

    def on_card_draw(self, pile_index):
        self.has_drawn = True
        self.drawn_card_original_pile = pile_index
        self.last_move = self.moves
        self.moves += 1

    def get_top_card(self, cards):
        """
        Selects only the topmost card in the UI, and ensures
        player isn't grabbing any cards from the other player's hand.
        """
        for card in cards:
            if card in self.game_view.card_manager.piles[COMPLETED_CARDS]:
                cards = []

        # Ensure player isn't grabbing cards from other player's hand
        if len(cards) > 0:
            for i in range(len(cards)):
                if i < len(cards):
                    for p in self.game_view.player_manager.player_list:
                        if p != self.game_view.player_manager.current_player:
                            for card in self.game_view.card_manager.piles[p.hand_index]:
                                if id(cards[i]) == id(card):
                                    cards.remove(cards[i])

            for _ in range(len(cards) - 1):
                cards.remove(cards[0])

            self.held_cards = cards
            pile = self.game_view.card_manager.get_pile_for_card(self.held_cards[0])
            self.held_cards_original_pile = pile

            self.game_view.card_managerpiles[pile].remove(self.held_cards[0])
