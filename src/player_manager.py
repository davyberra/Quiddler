from typing import List
from constants import OTHER_PILES, WHITE_TRANSPARENT

from src import player


class PlayerManager:
    def __init__(self):
        self.player_list: List[player.Player] = []
        self.current_player: player.Player = None

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

    def round_start_sequence(self, game_state_manager):
        for player in self.player_list:
            player.rnd_score = 0
            player.has_gone_down = False
        self.set_current_player(game_state_manager)

    def round_end_sequence(self):
        self.current_player.has_gone_down = True

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
