"""
View for editing player names from Game Menu.
"""
import arcade
import game_menu
import shelve

from arcade.gui import UIManager
from arcade.gui.elements.inputbox import UIInputBox
from constants import GAME_MENU_BASE_BACKGROUND, BACK, BACK_PRESSED


class EditPlayerNames(arcade.View):

    def __init__(self, player_1, player_2, game_view):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.game_view = game_view
        self.player_1 = player_1
        self.player_2 = player_2

        self.button_list = arcade.SpriteList()
        self.back = arcade.Sprite(BACK, scale=self.scale)
        self.back.position = self.screen_width / 2, 100 * self.scale
        self.button_list.append(self.back)

        self.ui_manager = UIManager()
        self.player_1_name_box = UIInputBox(
            center_x=self.screen_width / 2,
            center_y=self.screen_height / 2 + 100 * self.scale,
            width=round(400 * self.scale),
            height=round(100 * self.scale),
            text=f'{self.player_1}',
        )
        self.player_1_name_box.cursor_index = len(self.player_1_name_box.text)
        self.ui_manager.add_ui_element(self.player_1_name_box)
        self.player_2_name_box = UIInputBox(
            center_x=self.screen_width / 2,
            center_y=self.screen_height / 2 - 100 * self.scale,
            width=round(400 * self.scale),
            height=round(100 * self.scale),
            text=f'{self.player_2}',

        )
        self.player_2_name_box.cursor_index = len(self.player_2_name_box.text)
        self.ui_manager.add_ui_element(self.player_2_name_box)

        self.background = arcade.Sprite(filename=GAME_MENU_BASE_BACKGROUND,
                                        scale=self.screen_width / 1920)
        self.background.position = self.screen_width / 2, self.screen_height / 2

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        self.button_list.draw()

        arcade.draw_text(
            'Player 1:',
            self.screen_width / 2,
            self.screen_height / 2 + 200 * self.scale,
            color=arcade.color.WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            'Player 2:',
            self.screen_width / 2,
            self.screen_height / 2,
            color=arcade.color.WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center"
        )

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.buttons_pressed = arcade.get_sprites_at_point((x, y), self.button_list)

        if self.back in self.buttons_pressed:
            self.back.texture = arcade.load_texture(BACK_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        button = arcade.get_sprites_at_point((x, y), self.button_list)

        if self.back in self.buttons_pressed and button:
            file = shelve.open('players', protocol=2)
            file['player_1'] = self.player_1_name_box.text
            file['player_2'] = self.player_2_name_box.text
            file.close()
            self.game_view.player = self.player_1_name_box.text
            self.game_view.computer = self.player_2_name_box.text
            self.window.show_view(self.game_view)

        self.back.texture = arcade.load_texture(BACK)

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.F9:
            file = shelve.open('players', protocol=2)
            file['player_1'] = self.player_1_name_box.text
            file['player_2'] = self.player_2_name_box.text
            file.close()
            self.game_view.player = self.player_1_name_box.text
            self.game_view.computer = self.player_2_name_box.text
            self.window.show_view(self.game_view)
