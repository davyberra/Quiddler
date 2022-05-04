import logging

from src.managers.manager import Manager
from src.utils.buttons import *
from src.utils.constants import GO_DOWN_PILE, COMPLETED_CARDS

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class ButtonManager(Manager):
    def __init__(self, game_view, screen_manager):
        self.game_view = game_view
        self.screen_width = screen_manager.screen_width
        self.screen_height = screen_manager.screen_height
        self.scale = screen_manager.scale
        self.next_turn_button = None
        self.go_down_button = None
        self.save_word_button = None
        self.undo_button = None
        self.recall_button = None
        self.menu_button = None
        self.flash_timer = 0
        self.flashing_button = None
        self.button_list = []

    def setup(self):
        self.create_buttons()

    def draw(self):
        pass

    def round_start_sequence(self):
        pass

    def round_end_sequence(self):
        pass

    def turn_start_sequence(self):
        pass

    def turn_end_sequence(self):
        pass

    def update(self):
        self.update_flash_timer()

        if len(self.game_view.card_manager.piles[GO_DOWN_PILE]) < 2:
            if self.flashing_button == self.save_word_button:
                self.set_flashing_button(None)

        if len(self.game_view.card_manager.piles[COMPLETED_CARDS]) == self.game_view.game_state_manager.rnd_hand_count \
                and self.game_view.game_state_manager.has_discarded:
            self.set_flashing_button(self.go_down_button)

        elif len(self.game_view.card_manager.piles[GO_DOWN_PILE]) > 1:
            self.set_flashing_button(self.save_word_button)

        elif self.game_view.player_manager.current_player.has_gone_down:
            self.set_flashing_button(self.next_turn_button)

    def set_flashing_button(self, button: GameButton):
        self.flashing_button = button

    def update_flash_timer(self):
        self.flash_timer += 1
        if self.flash_timer > 30:
            self.flashing_button.update_flash_texture()
            self.flash_timer = 0

    def create_buttons(self):
        self.next_turn_button = NextTurnButton(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            scale=self.scale
        )
        self.next_turn_button.on_click = self.on_next_turn_click
        self.button_list.append(self.next_turn_button)
        self.go_down_button = GoDownButton(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            scale=self.scale
        )
        self.go_down_button.on_click = self.on_go_down_click
        self.button_list.append(self.go_down_button)
        self.save_word_button = SaveWordButton(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            scale=self.scale
        )
        self.save_word_button.on_click = self.on_save_word_click
        self.button_list.append(self.save_word_button)
        self.undo_button = UndoButton(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            scale=self.scale
        )
        self.undo_button.on_click = self.on_undo_click
        self.button_list.append(self.undo_button)
        self.recall_button = RecallButton(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            scale=self.scale
        )
        self.recall_button.on_click = self.on_recall_click
        self.button_list.append(self.recall_button)
        self.menu_button = MenuButton(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            scale=self.scale
        )
        self.menu_button.on_click = self.on_menu_click
        self.button_list.append(self.menu_button)

    def on_next_turn_click(self, event):
        self.game_view.handle_next_turn_button_click()

    def on_go_down_click(self, event):
        self.game_view.handle_go_down_button_click()

    def on_save_word_click(self, event):
        self.game_view.handle_save_word_button_click()

    def on_undo_click(self, event):
        self.game_view.handle_undo_button_click()
        self.next_turn_button.set_unavailable()

    def on_recall_click(self, event):
        self.game_view.handle_recall_button_click()

    def on_menu_click(self, event):
        self.game_view.handle_menu_button_click()
