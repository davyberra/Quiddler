"""
Includes classes for buttons.

NavButton - a user-defined class for navigation functions that overrides arcade.gui.UITextureButton.
"""

import arcade

import arcade.gui
from src.utils.constants import BACK, BACK_PRESSED, BUTTON_Y, NEXT_TURN, NEXT_TURN_PRESSED, NEXT_TURN_FLASH, GO_DOWN, \
    GO_DOWN_PRESSED, GO_DOWN_FLASH, SAVE_WORD, SAVE_WORD_PRESSED, SAVE_WORD_FLASH, UNDO, UNDO_PRESSED, RECALL, \
    RECALL_PRESSED, MENU, MENU_PRESSED


class GameButton(arcade.gui.UITextureButton):
    def __init__(self, x, y, texture, texture_pressed, scale, texture_flash=None):
        super().__init__(
            x=x,
            y=y,
            texture=texture,
            texture_pressed=texture_pressed,
            scale=scale
        )
        self.flash_texture = texture_flash

    def update_flash_texture(self):
        if self.texture == self.flash_texture:
            self.texture = self.texture
        else:
            self.texture = self.flash_texture


class NextTurnButton(GameButton):
    def __init__(self, screen_width, screen_height, scale):
        super().__init__(
            x=screen_width - 150 * scale,
            y=BUTTON_Y * scale,
            texture=NEXT_TURN,
            texture_pressed=NEXT_TURN_PRESSED,
            texture_flash=NEXT_TURN_FLASH,
            scale=scale
        )

    def set_unavailable(self):
        self.texture = self.texture_pressed

    def set_available(self):
        self.texture = self.texture


class GoDownButton(GameButton):
    def __init__(self, screen_width, screen_height, scale):
        super().__init__(
            x=screen_width / 2 + 150 * scale,
            y=BUTTON_Y * self.scale,
            texture=GO_DOWN,
            texture_pressed=GO_DOWN_PRESSED,
            texture_flash=GO_DOWN_FLASH,
            scale=scale
        )


class SaveWordButton(GameButton):
    def __init__(self, screen_width, screen_height, scale):
        super().__init__(
            x=screen_width / 2 - 130 * scale,
            y=BUTTON_Y * scale,
            texture=SAVE_WORD,
            texture_pressed=SAVE_WORD_PRESSED,
            texture_flash=SAVE_WORD_FLASH,
            scale=scale
        )


class UndoButton(GameButton):
    def __init__(self, screen_width, screen_height, scale):
        super().__init__(
            x=150 * scale,
            y=BUTTON_Y * scale,
            texture=UNDO,
            texture_pressed=UNDO_PRESSED,
            scale=scale
        )


class RecallButton(GameButton):
    def __init__(self, screen_width, screen_height, scale):
        super().__init__(
            x=400 * scale,
            y=BUTTON_Y * scale,
            texture=RECALL,
            texture_pressed=RECALL_PRESSED,
            scale=scale
        )


class MenuButton(GameButton):
    def __init__(self, screen_width, screen_height, scale):
        super().__init__(
            x=150 * scale,
            y=screen_height - 50 * scale,
            texture=MENU,
            texture_pressed=MENU_PRESSED,
            scale=scale
        )


class NavButton(arcade.gui.UITextureButton):
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

    def on_click(self, event):
        self.window.show_view(self.game_view)


class RightArrow(NavButton):
    def __init__(self, game_view, window, screen_width, scale):
        super().__init__(
            center_x=screen_width - (150 * scale),
            center_y=100 * scale,
            normal_texture=arcade.load_texture('../images/right_arrow.png'),
            hover_texture=arcade.load_texture('../images/right_arrow_hover.png'),
            press_texture=arcade.load_texture('../images/right_arrow_pressed.png'),
            game_view=game_view,
            window=window
        )


class LeftArrow(NavButton):
    def __init__(self, game_view, window, scale):
        super().__init__(
            center_x=150 * scale,
            center_y=100 * scale,
            normal_texture=arcade.load_texture('../images/left_arrow.png'),
            hover_texture=arcade.load_texture('../images/left_arrow_hover.png'),
            press_texture=arcade.load_texture('../images/left_arrow_pressed.png'),
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