"""
View called after a game is finished.
"""
import arcade
import game_menu
from constants import WHITE, GAME_END_THEME, GAME_END_BACKGROUND, GAME_END_BACKGROUND_WIDTH, YES, YES_PRESSED,\
    NO, NO_PRESSED


class GameEnd(arcade.View):

    def __init__(self,player_1_name, player_1_score, player_2_name, player_2_score):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.player_1 = player_1_name
        self.player_1_score = player_1_score
        self.player_2 = player_2_name
        self.player_2_score = player_2_score
        self.winner = None
        self.draw = False

        if self.player_1_score > self.player_2_score:
            self.winner = 'Player 1'
        elif self.player_2_score > self.player_1_score:
            self.winner = 'Player 2'
        elif self.player_1_score == self.player_2_score:
            self.draw = True

        self.button_list = arcade.SpriteList()

        self.yes = arcade.Sprite(YES, scale=self.scale)
        self.yes.position = self.screen_width / 2 - 200 * self.scale, 100 * self.scale
        self.button_list.append(self.yes)
        self.no = arcade.Sprite(NO, scale=self.scale)
        self.no.position = self.screen_width / 2 + 200 * self.scale, 100 * self.scale
        self.button_list.append(self.no)

        self.buttons_pressed = []

        self.background = arcade.Sprite(filename=GAME_END_BACKGROUND,
                                        scale=self.screen_width / GAME_END_BACKGROUND_WIDTH)
        self.background.position = self.screen_width / 2, self.screen_height / 2
        self.background_music = GAME_END_THEME
        self.sound_player = None

    def on_show(self):

        self.sound_player = self.background_music.play(volume=0.25, loop=True)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        self.button_list.draw()

        arcade.draw_text(
            f'{self.player_1}',
            start_x=self.screen_width / 2 - 400 * self.scale,
            start_y=self.screen_height / 2 + 100 * self.scale,
            color=WHITE,
            font_size=60,
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            f'{self.player_2}',
            start_x=self.screen_width / 2 + 400 * self.scale,
            start_y=self.screen_height / 2 + 100 * self.scale,
            color=WHITE,
            font_size=60,
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            f'{self.player_1_score}',
            start_x=self.screen_width / 2 - 400 * self.scale,
            start_y=self.screen_height / 2,
            color=WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            f'{self.player_2_score}',
            start_x=self.screen_width / 2 + 400 * self.scale,
            start_y=self.screen_height / 2,
            color=WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.buttons_pressed = arcade.get_sprites_at_point((x, y), self.button_list)

        if self.yes in self.buttons_pressed:
            self.yes.texture = arcade.load_texture(YES_PRESSED)
        elif self.no in self.buttons_pressed:
            self.no.texture = arcade.load_texture(NO_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        button = arcade.get_sprites_at_point((x, y), self.button_list)

        if button:
            if self.yes in self.buttons_pressed and self.yes == button[0]:
                self.background_music.stop(self.sound_player)
                game_view = game_menu.GameMenu(player_1=self.player_1,
                                               player_2=self.player_2)
                self.window.show_view(game_view)
            elif self.no in self.buttons_pressed and self.no == button[0]:
                arcade.close_window()

        self.yes.texture = arcade.load_texture(YES)
        self.no.texture = arcade.load_texture(NO)

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.Y:
            self.background_music.stop()
            game_view = game_menu.GameMenu(player_1=self.player_1,
                                           player_2=self.player_2)
            self.window.show_view(game_view)
        elif key == arcade.key.N:
            arcade.close_window()