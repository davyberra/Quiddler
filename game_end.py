import arcade
import game_menu
from constants import WHITE


class GameEnd(arcade.View):

    def __init__(self, player_1_score, player_2_score):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
        self.winner = None
        self.draw = False

        if self.player_1_score > self.player_2_score:
            self.winner = 'Player 1'
        elif self.player_2_score > self.player_1_score:
            self.winner = 'Player 2'
        elif self.player_1_score == self.player_2_score:
            self.draw = True

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        arcade.start_render()
        if self.winner:
            arcade.draw_text(f'Congratulations, {self.winner}!\nYou won by {abs(self.player_2_score - self.player_1_score)}.',
                             self.screen_width / 2, self.screen_height - 100 * self.scale, WHITE, font_size=round(24 * self.scale), align="center",
                             anchor_x="center")
        elif self.draw:
            arcade.draw_text(f'Congratulations, Player 1 and Player 2 - you tied!\nA rematch must be had to determine who is the best Quiddler player!',
                self.screen_width / 2, self.screen_height - 100 * self.scale, WHITE, font_size=round(24 * self.scale), align="center",
                             anchor_x="center")
        arcade.draw_text(f'SCORES\n\nPlayer 1: {self.player_1_score}       Player 2: {self.player_2_score}',
                             self.screen_width / 2, self.screen_height - 400 * self.scale, WHITE, font_size=round(24 * self.scale), align="center",
                         anchor_x="center")
        arcade.draw_text("Would you like to play again?\nPress 'y' for yes, 'n' for no.",
                         self.screen_width / 2, self.screen_height - 700 * self.scale, WHITE, font_size=round(24 * self.scale), align="center",
                         anchor_x="center")

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.Y:
            game_view = game_menu.GameMenu()
            self.window.show_view(game_view)
        elif key == arcade.key.N:
            arcade.close_window()