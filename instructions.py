import arcade

import arcade.gui
from arcade.gui import UIManager
from constants import WHITE, BACKGROUND_MUSIC, BACK, BACK_PRESSED


class BackButton(arcade.gui.UIImageButton):
    def __init__(self,center_x, center_y, hover, normal, pressed, game_view, window):
        super().__init__(
            center_x=center_x,
            center_y=center_y,
            hover_texture=hover,
            normal_texture=normal,
            press_texture=pressed
        )
        self.window = window
        self.game_view = game_view

    def on_click(self):
        self.window.show_view(self.game_view)


class InstructionsMenu1(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.game_view = game_view
        self.background = arcade.Sprite(
            filename="images/instructions_1.png",
            scale=self.scale
        )
        self.background.position = self.screen_width / 2, self.screen_height / 2

        self.ui_manager = UIManager()

        self.background_music = BACKGROUND_MUSIC

    def on_show_view(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        right_arrow = arcade.load_texture('images/right_arrow.png')
        hovered = arcade.load_texture('images/right_arrow_hover.png')
        pressed = arcade.load_texture('images/right_arrow_pressed.png')
        button = arcade.gui.UIImageButton(
            center_x=self.screen_width - (150 * self.scale),
            center_y=100 * self.scale,
            normal_texture=right_arrow,
            hover_texture=hovered,
            press_texture=pressed,
        )
        self.ui_manager.add_ui_element(button)

        back_normal = arcade.load_texture(BACK)
        pressed = arcade.load_texture(BACK_PRESSED)
        hovered = arcade.load_texture(BACK)
        button = BackButton(
            center_x=self.screen_width / 2,
            center_y=70 * self.scale,
            normal=back_normal,
            hover=hovered,
            pressed=pressed,
            window=self.window,
            game_view=self.game_view
        )
        self.ui_manager.add_ui_element(button)

    def on_draw(self):
        arcade.start_render()

        self.background.draw()

