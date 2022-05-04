import arcade
from src.utils import player, score_change_object
from src.utils.constants import WHITE, GREEN, RED


class ScoreBox:
    def __init__(
            self,
            center_x: float,
            screen_height,
            player: player.Player,
            scale: float
    ):
        self.center_x = center_x
        self.center_y = screen_height - 125 * scale
        self.width = 400 * scale
        self.height = 200 * scale
        self.player = player
        self.scale = scale

    def draw(self):
        arcade.draw_rectangle_filled(
            center_x=self.center_x,
            center_y=self.center_y,
            width=self.width,
            height=self.height,
            color=self.player.color
        )
        arcade.draw_text(
            f'{self.player}',
            self.center_x,
            self.center_y + 50 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            f'{self.player.total_score}',
            self.center_x,
            self.center_y - 50 * self.scale,
            WHITE,
            font_size=round(24 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )

    def draw_score_change(self, score_change_object: score_change_object.ScoreChangeObject):
        color, prefix = None, None

        if score_change_object.score >= 0:
            color = GREEN
            prefix = '+'
        elif score_change_object.score < 0:
            color = RED
            prefix = ''

        arcade.draw_text(
            f'{prefix}{score_change_object.score}',
            self.center_x,
            self.center_y,
            color,
            font_size=round(24 * self.scale),
            anchor_x="center",
            anchor_y="center"
        )