import arcade
from constants import WHITE, FACE_DOWN_IMAGE


class SplashScreen(arcade.View):

    def __init__(self, game_view, current_player, player_1, player_2, rnd_end, rnd_number, score_change_list, player_1_score_box, player_2_score_box, piles):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self. screen_height / 1080)
        self.game_view = game_view
        self.current_player = current_player
        self.rnd_end = rnd_end
        self.rnd_number = rnd_number
        self.score_change_list = score_change_list
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_score_box = player_1_score_box
        self.player_2_score_box = player_2_score_box
        self.piles = piles

    def on_show(self):
        arcade.draw_rectangle_filled(
            self.screen_width / 2,
            self.screen_height / 2,
            400 * self.scale,
            300 * self.scale,
            (94, 123, 128, 300)
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

        for score_list in self.score_change_list:
            x, y, color, prefix = 0, 0, None, None
            if score_list[0] == self.player_1:
                x, y = self.player_1_score_box['center_x'], self.player_1_score_box['center_y']
            elif score_list[0] == self.player_2:
                x, y = self.player_2_score_box['center_x'], self.player_2_score_box['center_y']

            if score_list[1] >= 0:
                color = arcade.color.GREEN
                prefix = '+'
            elif score_list[1] < 0:
                color = arcade.color.RED
                prefix = ''

            arcade.draw_text(
                f'{prefix}{score_list[1]}',
                x, y,
                color,
                font_size=round(24 * self.scale),
                anchor_x="center",
                anchor_y="center",
            )

        for pile in self.piles:
            for card in pile:
                card.texture = arcade.load_texture(FACE_DOWN_IMAGE)



    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for pile in self.piles[1:]:
            for card in pile:
                card.texture = arcade.load_texture(card.image_file_name)
        self.window.show_view(self.game_view)
