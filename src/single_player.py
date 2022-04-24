import arcade
import random
import logging
import shelve

import quiddler
import game_menu
import game_end
import pause_menu
import splash_screen
import player
import card_class
import computer_turn
from constants import *


class QuiddlerSolo(quiddler.MainGame):

    def __init__(self, rnd_number: int, players: list):
        super().__init__(rnd_number=rnd_number, players=players)

    def setup(self):
        super().setup()

