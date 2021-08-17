import unittest

from src.main import get_player_names


class MainMethodsTest(unittest.TestCase):
    """ Tests methods within main application class. """

    def setUp(self):
        # self.quiddler = Quiddler(
        #     rnd_number=16,
        #     player_1="Player 1",
        #     player_2="Player 2"
        # )
        pass

    def test_get_hand_position(self):
        pass


class FileMethodsTest(unittest.TestCase):
    """ Tests main methods dealing with reading/writing of game files. """

    def test_player_names_key_not_found(self):
        self.assertRaises(KeyError, get_player_names(filename='platers'))
