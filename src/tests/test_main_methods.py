import unittest

from src.main import Quiddler


class MainMethodsTest(unittest.TestCase):
    """ Tests methods within main application class. """

    def setUp(self):
        self.quiddler = Quiddler(
            rnd_number=16,
            player_1="Player 1",
            player_2="Player 2"
        )

    def test_get_hand_position(self):
        pass