import unittest
import os
import arcade

from two_player import get_player_names, Quiddler
from constants import *


class GetClickedPileTest(unittest.TestCase):
    """ Tests get_clicked_pile method. """

    def setUp(self):
        self.window = arcade.Window(fullscreen=True, title="Quiddler")
        self.quiddler = Quiddler(
            rnd_number=16,
            player_1="Player 1",
            player_2="Player 2"
        )
        self.quiddler.setup()

    def test_get_clicked_pile_returns_correct_pile(self):
        pile = [self.quiddler.pile_mat_list[FACE_DOWN_PILE]]
        cards = self.quiddler.get_clicked_pile(
            pile,
            x=self.quiddler.face_down_position_x,
            y=self.quiddler.face_down_position_y
        )
        returned_cards = []
        for card in self.quiddler.piles[FACE_DOWN_PILE]:
            returned_cards.append(card)
        self.assertEqual(cards, returned_cards)


class GetCompletedWordsTest(unittest.TestCase):
    """ Tests get_completed_words. """

    def setUp(self):
        self.window = arcade.Window(fullscreen=True, title="Quiddler")
        self.quiddler = Quiddler(
            rnd_number=16,
            player_1="Player 1",
            player_2="Player 2"
        )
        self.quiddler.setup()



class GetButtonsPressedTest(unittest.TestCase):
    def setUp(self):
        self.window = arcade.Window(fullscreen=True, title="Quiddler")
        self.quiddler = Quiddler(
            rnd_number=16,
            player_1="Player 1",
            player_2="Player 2"
        )
        self.quiddler.setup()

    def test_get_buttons_pressed(self):
        buttons = arcade.get_sprites_at_point(
            (
                self.quiddler.next_turn_button.center_x,
                self.quiddler.next_turn_button.center_y
            ),
            self.quiddler.button_list
        )
        self.quiddler.get_buttons_pressed(buttons)
        self.assertIn(self.quiddler.next_turn_button, self.quiddler.buttons_pressed)

    def test_get_buttons_pressed_correct_texture(self):
        buttons = arcade.get_sprites_at_point(
            (
                self.quiddler.next_turn_button.center_x,
                self.quiddler.next_turn_button.center_y
            ),
            self.quiddler.button_list
        )
        self.quiddler.get_buttons_pressed(buttons)
        self.assertEqual(self.quiddler.next_turn_button.texture, arcade.load_texture(NEXT_TURN_PRESSED))

    def tearDown(self):
        arcade.close_window()

class FileMethodsTest(unittest.TestCase):
    """ Tests main methods dealing with reading/writing of game files. """

    def test_player_names_correct_on_instantiation(self):
        player_1, player_2 = get_player_names(filename='platers')
        self.assertEqual(player_1, 'Player 1')
        self.assertEqual(player_2, 'Player 2')

    def tearDown(self):
        if os.path.exists('platers.bak'):
            os.remove('platers.bak')
        if os.path.exists('platers.dat'):
            os.remove('platers.dat')
        if os.path.exists('platers.dir'):
            os.remove('platers.dir')
