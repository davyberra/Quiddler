from src.utils.constants import MAT_WIDTH, MAT_HEIGHT
import arcade


def standard_pile_mat(scale: float, position):
    sprite = arcade.SpriteSolidColor(
        round(MAT_WIDTH * scale),
        round(MAT_HEIGHT * scale),
        (255, 255, 255, 40)
    )
    sprite.position = position
    return sprite


def go_down_pile_mat(scale: float, screen_width: int, position):
    sprite = arcade.SpriteSolidColor(
        screen_width,
        round(MAT_HEIGHT * scale),
        (255, 255, 0, 1)
    )
    sprite.position = position
    return sprite


def player_hand_mat(scale: float, rnd_hand_count: int, position):
    sprite = arcade.SpriteSolidColor(
            round(rnd_hand_count * MAT_WIDTH * scale),
            round(MAT_HEIGHT * scale),
            (255, 255, 255, 10)
        )
    sprite.position = position
    return sprite

def create_mats(scale: float) -> arcade.SpriteList():
    # Create the mats for the face down and discard piles
    FACE_DOWN_PILE_MAT = arcade.SpriteSolidColor(
        round(MAT_WIDTH * scale),
        round(MAT_HEIGHT * scale),
        (255, 255, 255, 40)
    )
    pile.position = self.face_down_position
    self.pile_mat_list.append(pile)
    pile = arcade.SpriteSolidColor(
        round(MAT_WIDTH * scale),
        round(MAT_HEIGHT * scale),
        (255, 255, 255, 40)
    )
    pile.position = self.discard_position
    self.pile_mat_list.append(pile)
    # Create mat for going down
    pile = arcade.SpriteSolidColor(
        self.screen_width,
        round(MAT_HEIGHT * scale),
        (255, 255, 0, 1)
    )
    pile.position = self.screen_width / 2, GO_DOWN_MAT_Y * scale
    self.pile_mat_list.append(pile)
    # Create mat for the player hands
    for _ in range(2):
        pile = arcade.SpriteSolidColor(
            round(self.rnd_hand_count * MAT_WIDTH * scale),
            round(MAT_HEIGHT * scale),
            (255, 255, 255, 10)
        )
        pile.position = self.screen_width / 2, PLAYER_HAND_Y * scale
        self.pile_mat_list.append(pile)
    # Create mat for completed cards
    pile = arcade.SpriteSolidColor(
        round(MAT_WIDTH * scale),
        round(MAT_HEIGHT * scale),
        (255, 255, 255, 40)
    )
    pile.position = self.completed_card_position
    self.pile_mat_list.append(pile)