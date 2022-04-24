"""
Includes classes for buttons.

NavButton - a user-defined class for navigation functions that overrides arcade.gui.UIImageButton.
"""

import arcade

import arcade.gui
from arcade.gui import UIManager
from constants import BACKGROUND_MUSIC, BACK, BACK_PRESSED

class NextTurnButton(arcade.gui.UIImageButton):
    def __init__(self, center_x, center_y, hover_texture, normal_texture, press_texture):
        super().__init__(
            center_x=center_x,
            center_y=center_y,
            hover_texture=hover_texture,
            normal_texture=normal_texture,
            press_texture=press_texture
        )
class NavButton(arcade.gui.UIImageButton):
    def __init__(self, center_x, center_y, hover_texture, normal_texture, press_texture, game_view, window):
        super().__init__(
            center_x=center_x,
            center_y=center_y,
            hover_texture=hover_texture,
            normal_texture=normal_texture,
            press_texture=press_texture
        )
        self.window = window
        self.game_view = game_view

    def on_click(self):
        self.window.show_view(self.game_view)


class RightArrow(NavButton):
    def __init__(self, game_view, window, screen_width, scale):
        super().__init__(
            center_x=screen_width - (150 * scale),
            center_y=100 * scale,
            normal_texture=arcade.load_texture('images/right_arrow.png'),
            hover_texture=arcade.load_texture('images/right_arrow_hover.png'),
            press_texture=arcade.load_texture('images/right_arrow_pressed.png'),
            game_view=game_view,
            window=window
        )


class LeftArrow(NavButton):
    def __init__(self, game_view, window, scale):
        super().__init__(
            center_x=150 * scale,
            center_y=100 * scale,
            normal_texture=arcade.load_texture('images/left_arrow.png'),
            hover_texture=arcade.load_texture('images/left_arrow_hover.png'),
            press_texture=arcade.load_texture('images/left_arrow_pressed.png'),
            game_view=game_view,
            window=window
        )


class BackButton(NavButton):
    def __init__(self, game_view, window, screen_width, scale):
        super().__init__(
            center_x=screen_width / 2,
            center_y=70 * scale,
            normal_texture=arcade.load_texture(BACK),
            hover_texture=arcade.load_texture(BACK),
            press_texture=arcade.load_texture(BACK_PRESSED),
            game_view=game_view,
            window=window
        )