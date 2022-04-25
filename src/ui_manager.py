import arcade

from src import score_box
from constants import BACKGROUND_IMAGE_WIDTH


class UIManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        # Apply positions based on scale
        self.face_down_position = ((self.screen_width / 2) - 70 * self.scale, self.screen_height - self.screen_height / 4)
        self.discard_position= ((self.screen_width / 2) + 70 * self.scale, self.screen_height - self.screen_height / 4)
        self.completed_card_position = (150 * self.scale, self.screen_height - 250 * self.scale)

        self.background = arcade.Sprite(
            filename="images/quiddler_background_large(2).png",
            scale=self.screen_width / BACKGROUND_IMAGE_WIDTH
        )
        self.background.position = self.screen_width / 2, self.screen_height / 2

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