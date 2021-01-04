import main as Quiddler
import unittest


class QuiddlerTest(unittest.TestCase):

    def test_len_player_hands(self):
        if Quiddler.Quiddler.__init__(self).rnd == 1:
            assert len(Quiddler.Quiddler.__init__(self).piles[Quiddler.PLAYER_1_HAND]) == 3


