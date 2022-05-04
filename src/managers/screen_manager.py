from typing import List

import arcade

from src.managers.manager import Manager
from src.utils import score_box, mats
from src.utils.constants import BACKGROUND_IMAGE_WIDTH, OTHER_PILES, FACE_DOWN_PILE, DISCARD_PILE, COMPLETED_CARDS, \
    GO_DOWN_PILE, PLAYER_PILE_MAT, GO_DOWN_MAT_Y, PLAYER_HAND_Y, WHITE


class ScreenManager(Manager):
    def __init__(self, game_view, screen_width, screen_height):
        self.game_view = game_view
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        # Apply positions based on scale
        self.face_down_position = ((self.screen_width / 2) - 70 * self.scale, self.screen_height - self.screen_height / 4)
        self.discard_position= ((self.screen_width / 2) + 70 * self.scale, self.screen_height - self.screen_height / 4)
        self.completed_card_position = (150 * self.scale, self.screen_height - 250 * self.scale)
        self.go_down_position = self.screen_width / 2, GO_DOWN_MAT_Y * self.scale
        self.player_hand_position = self.screen_width / 2, PLAYER_HAND_Y * self.scale

        self.background = arcade.Sprite(
            filename="../images/quiddler_background_large(2).png",
            scale=self.screen_width / BACKGROUND_IMAGE_WIDTH
        )
        self.background.position = self.screen_width / 2, self.screen_height / 2
        self.pile_mat_list = None

    def setup(self):
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList(is_static=True)
        self.create_mats()

    def draw(self):
        self.background.draw()
        self.pile_mat_list.draw()

        # Draw Round number
        arcade.draw_text(
            f"Round: {self.game_view.game_state_manager.rnd}",
            self.screen_width - 125 * self.scale,
            self.screen_height - 50 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )

        # Draw hand_count number
        arcade.draw_text(
            f"Cards: {self.game_view.game_state_manager.rnd_hand_count}",
            self.screen_width - 120 * self.scale,
            self.screen_height - 150 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center"
        )

        # Draw 'final turn' when other player has gone down
        if self.game_view.player_manager.is_players_final_turn():
            self.draw_final_turn_text()

    def update(self):
        pass

    def round_start_sequence(self):
        pass

    def round_end_sequence(self):
        pass

    def turn_start_sequence(self):
        pass

    def turn_end_sequence(self):
        pass

    def create_score_boxes(self, players):
        score_box_dict = {}
        score_box_dict[players[0]] = score_box.ScoreBox(
            center_x=(self.screen_width / 2) - 450 * self.scale,
            screen_height=self.screen_height,
            player=players[0],
            scale=self.scale
        )
        score_box_dict[players[1]] = score_box.ScoreBox(
            center_x=(self.screen_width / 2) + 450 * self.scale,
            screen_height=self.screen_height,
            player=players[1],
            scale=self.scale
        )
        return score_box_dict

    def draw_final_turn_text(self):
        arcade.draw_text(
            "Final Turn!",
            self.screen_width - 150 * self.scale,
            100 * self.scale,
            arcade.color.GOLD,
            font_size=round(24 * self.scale),
            anchor_x="center"
        )

    def create_mats(self):
        # Create the mats for the face down and discard piles
        for i in range(len(OTHER_PILES) + 1):
            self.pile_mat_list.append(arcade.Sprite())
        self.pile_mat_list[FACE_DOWN_PILE] = mats.standard_pile_mat(self.scale, self.face_down_position)
        self.pile_mat_list[DISCARD_PILE] = mats.standard_pile_mat(self.scale, self.discard_position)
        self.pile_mat_list[COMPLETED_CARDS] = mats.standard_pile_mat(self.scale, self.completed_card_position)
        self.pile_mat_list[GO_DOWN_PILE] = mats.go_down_pile_mat(self.scale, self.screen_width, self.go_down_position)
        self.pile_mat_list[PLAYER_PILE_MAT] = mats.player_hand_mat(self.scale, self.screen_width, self.player_hand_position)

    def get_small_go_down_card_position(self, index1, index2, current_player):
        """
        Positioning for completed cards display after a player has gone down.
        """
        x, y = 0, 0
        if current_player.player_number == 1:
            x = (350 * self.scale) + (35 * self.scale * index2)
            y = (self.screen_height - 300 * self.scale) - (100 * self.scale * index1)
        elif current_player.player_number == 2:
            x = (self.screen_width - (500 * self.scale) + (35 * self.scale * index2))
            y = (self.screen_height - 300 * self.scale) - (100 * self.scale * index1)
        return x, y

