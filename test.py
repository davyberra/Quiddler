from main import Quiddler, Player, Card
import unittest


class QuiddlerTest(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player()
        self.player_2 = Player()
        Quiddler.setup(Quiddler)

    def test_player_card_list(self):

       self.assertEqual(Quiddler.pull_to_top(self.player_1.card_list[5], self.player_1),
                       Quiddler.pull_to_top(self.player_2.card_list[5], self.player_2)
                       )


if __name__ == '__main__':
    unittest.main()