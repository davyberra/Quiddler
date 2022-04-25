class GameStateManager:
    def __init__(self, rnd_number: int):
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