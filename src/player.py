"""
Defines Player object.
"""
class Player:
    def __init__(self, player_name, player_number: int, is_computer: bool):
        self.player_name = player_name
        self.player_number = player_number
        self.is_computer = is_computer

        self.pile_numbers_list = []

        self.total_score = 0
        self.hand_index = None
        self.has_gone_down = False
        self.longest_words = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                              9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
        self.color = None

    def __str__(self):
        return self.player_name
