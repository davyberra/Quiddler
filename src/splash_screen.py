"""
Splash Screen called between player turns.
"""

import arcade
import player

from constants import WHITE, FACE_DOWN_IMAGE
from src import quiddler


class SplashScreen(arcade.View):

    # Persists game state between views.
    def __init__(self,
                 game_view: quiddler.Quiddler,
                 current_player: player.Player,
                 player_1,
                 player_2,
                 rnd_end,
                 rnd_number,
                 piles
                 ):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self. screen_height / 1080)
        self.game_view = game_view
        self.current_player = current_player
        self.rnd_end = rnd_end
        self.rnd_number = rnd_number
        self.player_1 = player_1
        self.player_2 = player_2
        self.piles = piles

    def on_show(self):
        print(f"Called splash screen before {self.current_player} turn.")
        if self.current_player == self.player_1:
            arcade.draw_rectangle_filled(
                self.screen_width / 2,
                self.screen_height / 2,
                400 * self.scale,
                300 * self.scale,
                (56, 174, 207, 300)
            )
        else:
            arcade.draw_rectangle_filled(
                self.screen_width / 2,
                self.screen_height / 2,
                400 * self.scale,
                300 * self.scale,
                (196, 77, 79, 300)
            )

        if self.rnd_end:
            arcade.draw_text(
                f'Round {self.rnd_number}',
                self.screen_width / 2,
                self.screen_height / 2 + 100 * self.scale,
                WHITE,
                font_size=round(40 * self.scale),
                anchor_x="center",
                anchor_y="center",
            )

            arcade.draw_text(
                f"{self.current_player}'s Turn.",
                self.screen_width / 2,
                self.screen_height / 2 - 100 * self.scale,
                WHITE,
                font_size=round(40 * self.scale),
                anchor_x="center",
                anchor_y="center",
            )

        else:
            arcade.draw_text(
                f"{self.current_player}'s Turn.",
                self.screen_width / 2,
                self.screen_height / 2,
                WHITE,
                font_size=round(40 * self.scale),
                anchor_x="center",
                anchor_y="center",
            )

        for pile in self.piles:
            for card in pile:
                card.texture = arcade.load_texture(FACE_DOWN_IMAGE)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.change_turn()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            self.change_turn()

    def change_turn(self):
        if self.current_player.is_computer:
            self.game_view.take_computer_turn(self.current_player)
        self.game_view.turn_start_sequence()
        self.window.show_view(self.game_view)
