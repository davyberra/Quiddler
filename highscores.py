import arcade
import shelve

from constants import HIGHSCORES_BACKGROUND, BACK, BACK_PRESSED

class HighScores(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.game_view = game_view

        self.button_list = arcade.SpriteList()
        self.back = arcade.Sprite(BACK, scale=self.scale)
        self.back.position = self.screen_width / 2, 100 * self.scale
        self.button_list.append(self.back)

        file = shelve.open(filename='quiddler_highscores', protocol=2)
        try:
            self.highscore_list = file['scores']
        except KeyError:
            self.highscore_list = [['AAA', 100]]
        self. highscore_list = sorted(self.highscore_list, key=lambda player: player[1], reverse=True)

        self.background = arcade.Sprite(filename=HIGHSCORES_BACKGROUND,
                                        scale=self.scale)
        self.background.position = self.screen_width / 2, self.screen_height / 2

    def on_draw(self):
        arcade.start_render()

        self.background.draw()
        self.button_list.draw()

        for i, score in enumerate(self.highscore_list):
            arcade.draw_text(
                f'{score[0]}: {score[1]}',
                start_x=self.screen_width / 2 + 10 * self.scale,
                start_y=(self.screen_height - 300 * self.scale) - i * 50 * self.scale,
                color=arcade.color.WHITE,
                font_size=40,
                anchor_x="right",
                anchor_y="center"
            )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.buttons_pressed = arcade.get_sprites_at_point((x, y), self.button_list)

        if self.back in self.buttons_pressed:
            self.back.texture = arcade.load_texture(BACK_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        button = arcade.get_sprites_at_point((x, y), self.button_list)

        if self.back in self.buttons_pressed and button:
            self.window.show_view(self.game_view)

        self.back.texture = arcade.load_texture(BACK)

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.F8:
            self.window.show_view(self.game_view)
