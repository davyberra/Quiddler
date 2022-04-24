"""
Class for Card Sprite.
"""
import arcade
from constants import FACE_DOWN_IMAGE


class Card(arcade.Sprite):
    """
    Class for each card sprite.
    """

    def __init__(self, value: str, scale=1):
        """
        Assigns the letter value to the card, and creates the appropriate image.
        :param value: Letter(s) on card
        :param scale: Scaled size of card
        """
        self.value = value
        self.face_up_texture = f"images/{self.value}.png"
        self.face_down_texture  = FACE_DOWN_IMAGE
        super().__init__(self.face_up_texture, scale)
        self.texture = arcade.load_texture(self.face_up_texture)

    def flip_up(self):
        self.texture = arcade.load_texture(self.face_up_texture)

    def flip_down(self):
        self.texture = arcade.load_texture(self.face_down_texture)

