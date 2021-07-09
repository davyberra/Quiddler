"""
Includes views for each instructions page.

InstructionsMenu - basic class that defines main instruction menu functionality,
subclassed by each InstructionMenu class.
"""
import arcade
import buttons

import arcade.gui
from arcade.gui import UIManager
from constants import WHITE, BACKGROUND_MUSIC, BACK, BACK_PRESSED


class InstructionsMenu(arcade.View):
    def __init__(self, game_view, background_filename):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.game_view = game_view
        self.background = arcade.Sprite(
            filename=background_filename,
            scale=self.scale
        )
        self.background.position = self.screen_width / 2, self.screen_height / 2

        self.ui_manager = UIManager()

        self.background_music = BACKGROUND_MUSIC

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        """ To be overriden. """
        pass

    def on_draw(self):
        arcade.start_render()

        self.background.draw()


class InstructionsMenu1(InstructionsMenu):

    def __init__(self, game_view):
        super().__init__(
            game_view=game_view,
            background_filename='images/instructions_1.png'
        )

    def setup(self):
        button = buttons.RightArrow(
            window=self.window,
            game_view=InstructionsMenu2(
                game_view=self.game_view
            ),
            screen_width=self.screen_width,
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)

        button = buttons.BackButton(
            game_view=self.game_view,
            window=self.window,
            screen_width=self.screen_width,
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)


class InstructionsMenu2(InstructionsMenu):

    def __init__(self, game_view):
        super().__init__(
            game_view=game_view,
            background_filename='images/instructions_2.png'
        )

    def setup(self):
        button = buttons.LeftArrow(
            window=self.window,
            game_view=InstructionsMenu1(
                game_view=self.game_view
            ),
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)

        button = buttons.RightArrow(
            window=self.window,
            game_view=InstructionsMenu3(
                game_view=self.game_view
            ),
            screen_width=self.screen_width,
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)

        button = buttons.BackButton(
            game_view=self.game_view,
            window=self.window,
            screen_width=self.screen_width,
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)


class InstructionsMenu3(InstructionsMenu):

    def __init__(self, game_view):
        super().__init__(
            game_view=game_view,
            background_filename='images/instructions_3.png'
        )

    def setup(self):
        button = buttons.LeftArrow(
            window=self.window,
            game_view=InstructionsMenu2(
                game_view=self.game_view
            ),
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)

        button = buttons.RightArrow(
            window=self.window,
            game_view=InstructionsMenu4(
                game_view=self.game_view
            ),
            screen_width=self.screen_width,
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)

        button = buttons.BackButton(
            game_view=self.game_view,
            window=self.window,
            screen_width=self.screen_width,
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)


class InstructionsMenu4(InstructionsMenu):

    def __init__(self, game_view):
        super().__init__(
            game_view=game_view,
            background_filename='images/instructions_4.png'
        )

    def setup(self):
        button = buttons.LeftArrow(
            window=self.window,
            game_view=InstructionsMenu3(
                game_view=self.game_view
            ),
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)

        button = buttons.BackButton(
            game_view=self.game_view,
            window=self.window,
            screen_width=self.screen_width,
            scale=self.scale
        )
        self.ui_manager.add_ui_element(button)
