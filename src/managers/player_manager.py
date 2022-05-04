from typing import List
from src.managers.manager import Manager
from src.utils.constants import OTHER_PILES, WHITE_TRANSPARENT, GOLD_TRANSPARENT

from src.utils import player


class PlayerManager(Manager):
    def __init__(self, game_view):
        self.game_view = game_view
        self.player_list: List[player.Player] = []
        self.current_player: player.Player = None

    def setup(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def create_players(self, players):
        for i, player_dict in enumerate(players):
            p: player.Player = player.Player(
                player_name=player_dict.get('player_name'),
                player_number=i+1,
                is_computer=player_dict.get('is_computer')
            )
            p.hand_index = i + len(OTHER_PILES)
            p.pile_numbers_list = []
            p.pile_numbers_list.extend(OTHER_PILES)
            p.pile_numbers_list.append(p.hand_index)
            print(f'player_hand_indexes: {p.pile_numbers_list}')
            p.color = WHITE_TRANSPARENT
            self.player_list.append(p)

        self.current_player = self.player_list[0]

    def round_start_sequence(self):
        for player in self.player_list:
            player.rnd_score = 0
            player.has_gone_down = False
        self.set_current_player(self.game_view.game_state_manager)
        self.turn_start_sequence()

    def set_current_player(self, game_state_manager):
        index = (game_state_manager.rnd - 1) % len(self.player_list)
        self.current_player = self.player_list[index]

    def round_end_sequence(self):
        self.current_player.has_gone_down = True

    def turn_start_sequence(self):
        self.update_player_colors()

    def turn_end_sequence(self):
        self.rotate_players()

    def set_round_start_player(self, game_state_manager):
        # Initiate player turn, depending on rnd
        cur_player_index = (game_state_manager.rnd - 1) % len(self.player_list)
        self.current_player = self.player_list[cur_player_index]

    def rotate_players(self):
        i = self.current_player.player_number + 1
        if i > len(self.player_list):
            i = 1
        self.current_player = self.player_list[i - 1]

    def is_round_final_turn(self) -> bool:
        for p in self.player_list:
            if p != self.current_player and not p.has_gone_down:
                return False
        return True

    def is_players_final_turn(self) -> bool:
        for p in self.player_list:
            if p != self.current_player and p.has_gone_down:
                return True
        return False

    def update_player_colors(self):
        """Update player box color based on player turn"""
        for p in self.player_list:
            if p == self.current_player:
                p.color = GOLD_TRANSPARENT
            else:
                p.color = WHITE_TRANSPARENT
