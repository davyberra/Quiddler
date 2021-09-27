"""
Class for Card Sprite.
"""
import arcade


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

        self.image_file_name = f"images/{self.value}.png"

        super().__init__(self.image_file_name, scale, )
        self.texture = arcade.load_texture(self.image_file_name)