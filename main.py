import arcade
import random
import pyglet
import logging

from word_list import get_word_list
from nltk.corpus import words
from pyglet.window import key

WORD_LIST = get_word_list()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
MAT_WIDTH = 120
MAT_HEIGHT = 180
CARD_LIST = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd', 'd', 'd', 'e', 'e', 'e', 'e',
             'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e',
             'f', 'f', 'g', 'g', 'g', 'g', 'h', 'h', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'j', 'j', 'k', 'k', 'l',
             'l', 'l', 'l', 'm', 'm', 'n', 'n', 'n', 'n', 'n', 'n',
             'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'p', 'p', 'q', 'q', 'r', 'r', 'r', 'r', 'r', 'r', 's', 's', 's',
             's', 't', 't', 't', 't', 't', 't', 'u', 'u', 'u', 'u', 'u', 'u',
             'v', 'v', 'w', 'w', 'x', 'x', 'y', 'y', 'y', 'y', 'z', 'z', 'er', 'er', 'cl', 'cl', 'in', 'in', 'th', 'th',
             'qu', 'qu']
CARD_SCORE = {'a': 2, 'b': 8, 'c': 8, 'd': 4, 'e': 2, 'f': 6, 'g': 6, 'h': 7, 'i': 2, 'j': 13, 'k': 8, 'l': 3, 'm': 5,
              'n': 5, 'o': 2, 'p': 6, 'q': 15, 'r': 5, 's': 3, 't': 3, 'u': 4, 'v': 11, 'w': 10, 'x': 12, 'y': 4,
              'z': 14, 'er': 7, 'cl': 10, 'in': 7, 'th': 9, 'qu': 9}

FACE_DOWN_IMAGE = "images/card_back.png"
GO_DOWN = "images/go_down.png"
GO_DOWN_PRESSED = "images/go_down_pressed.png"
NEXT_TURN = "images/next_turn.png"
NEXT_TURN_PRESSED = "images/next_turn_pressed.png"
SAVE_WORD = "images/save_word.png"
SAVE_WORD_PRESSED = "images/save_word_pressed.png"
RECALL = "images/recall.png"
RECALL_PRESSED = "images/recall_pressed.png"

FACE_DOWN_POSITION_X, FACE_DOWN_POSITION_Y = (SCREEN_WIDTH / 2) - 70, SCREEN_HEIGHT - SCREEN_HEIGHT / 4
DISCARD_POSITION_X, DISCARD_POSITION_Y = (SCREEN_WIDTH / 2) + 70, SCREEN_HEIGHT - SCREEN_HEIGHT / 4
COMPLETED_CARD_POSITION_X, COMPLETED_CARD_POSITION_Y = 150, SCREEN_HEIGHT - 150
PLAYER_HAND_Y = 150
GO_DOWN_MAT_Y = 450

PILE_COUNT = 6
FACE_DOWN_PILE = 0
DISCARD_PILE = 1
GO_DOWN_PILE = 2
PLAYER_1_HAND = 3
PLAYER_2_HAND = 4
COMPLETED_CARDS = 5

PLAYER_1 = 0
PLAYER_2 = 1
NUMBER_OF_PLAYERS = 2

logging.basicConfig(level=logging.WARNING)

class Card(arcade.Sprite):
    """
    Class for each card sprite.
    """

    def __init__(self, value, scale=1):
        """
        Assigns the letter value to the card, and creates the appropriate image.
        :param value: Letter(s) on card
        :param scale: Scaled size of card
        """
        self.value = value

        self.image_file_name = f"images/{self.value}.png"

        super().__init__(self.image_file_name, scale, )
        self.texture = arcade.load_texture(self.image_file_name)


class Player:
    def __init__(self, player_name):
        self.player_name = player_name

        self.pile_numbers_list = []
        self.card_list = arcade.SpriteList()
        self.total_score = 0
        self.rnd_score = None
        self.turn_order = None
        self.hand_index = None
        self.has_gone_down = False
        self.longest_words = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
        self.color = None

    def __str__(self):
        return self.player_name


class Quiddler(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        # Initialize Players and add them to a list of all players
        self.player_list = []
        self.player_1 = Player('Player 1')
        self.player_1.hand_index = PLAYER_1_HAND
        self.player_1.pile_numbers_list = [0, 1, 2, 3, 5]
        self.player_1.color = arcade.color.ALLOY_ORANGE
        self.player_list.append(self.player_1)
        self.player_2 = Player('Player 2')
        self.player_2.hand_index = PLAYER_2_HAND
        self.player_2.pile_numbers_list = [0, 1, 2, 4, 5]
        self.player_2.color = arcade.color.AIR_FORCE_BLUE
        self.player_list.append(self.player_2)

        self.rnd = 1
        self.card_list = None
        self.mat_list = None
        self.button_list = None
        self.buttons_pressed = None
        self.held_cards = None
        self.held_cards_original_position = None
        self.piles = None
        self.player_1_turn = None

        self.current_player = None
        self.next_turn_button = None
        self.go_down_button = None
        self.save_word_button = None
        self.recall_button = None

        self.card_dict = None
        self.pile_mat_list = None

        # List of Player Scores
        self.player_scores = None
        # Text string representing letters in the go_down pile.
        self.go_down_text = None

        self.has_drawn = False
        self.has_discarded = False
        self.completed_words_list = []
        self.card_input_original_position = None


        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """
        Initializes values for piles, hands.
        :return:
        """

        self.go_down_text = ''
        self.completed_words_list = []


        # List of cards we're dragging with the mouse ------------------------------------------------------------------
        self.held_cards = []
        # List of buttons currently pressed
        self.buttons_pressed = []
        # Original location of cards we are dragging
        self.held_cards_original_position = []
        # Create a list of lists, each holds a pile of cards
        self.piles = [[] for _ in range(PILE_COUNT)]

        self.card_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.piles[FACE_DOWN_PILE] = arcade.SpriteList()
        self.piles[DISCARD_PILE] = arcade.SpriteList()
        self.piles[GO_DOWN_PILE] = arcade.SpriteList()
        self.piles[PLAYER_1_HAND] = arcade.SpriteList()
        self.piles[PLAYER_2_HAND] = arcade.SpriteList()
        self.piles[COMPLETED_CARDS] = arcade.SpriteList()
        self.player_1.card_list = arcade.SpriteList()
        self.player_2.card_list = arcade.SpriteList()

        # Create buttons -----------------------------------------------------------------------------------------------
        self.next_turn_button = arcade.Sprite(NEXT_TURN_PRESSED)
        self.next_turn_button.center_x = 1160
        self.next_turn_button.center_y = 25
        self.button_list.append(self.next_turn_button)

        self.go_down_button = arcade.Sprite(GO_DOWN)
        self.go_down_button.center_x = 1010
        self.go_down_button.center_y = 25
        self.button_list.append(self.go_down_button)

        self.save_word_button = arcade.Sprite(SAVE_WORD)
        self.save_word_button.center_x = 100
        self.save_word_button.center_y = 25
        self.button_list.append(self.save_word_button)

        self.recall_button = arcade.Sprite(RECALL)
        self.recall_button.center_x = 250
        self.recall_button.center_y = 25
        self.button_list.append(self.recall_button)

        # Create a card dictionary with Card keys assigned to letter values
        self.card_dict = {}

        # Create sprite list with all the mats
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the face down and discard piles
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = FACE_DOWN_POSITION_X, FACE_DOWN_POSITION_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = DISCARD_POSITION_X, DISCARD_POSITION_Y
        self.pile_mat_list.append(pile)

        # Create mat for going down
        pile = arcade.SpriteSolidColor(SCREEN_WIDTH, MAT_HEIGHT, arcade.color.GLAUCOUS)
        pile.position = SCREEN_WIDTH / 2, GO_DOWN_MAT_Y
        self.pile_mat_list.append(pile)

        # Create mat for the player hands
        for i in range(2):
            pile = arcade.SpriteSolidColor((self.rnd + 2) * MAT_WIDTH, MAT_HEIGHT, arcade.color.AMAZON)
            pile.position = SCREEN_WIDTH / 2, PLAYER_HAND_Y
            self.pile_mat_list.append(pile)

        # Create mat for completed cards
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = COMPLETED_CARD_POSITION_X, COMPLETED_CARD_POSITION_Y
        self.pile_mat_list.append(pile)

        # Create every card
        for value in CARD_LIST:
            card = Card(value)
            card.position = FACE_DOWN_POSITION_X, FACE_DOWN_POSITION_Y
            self.card_list.append(card)
            card.texture = arcade.load_texture(FACE_DOWN_IMAGE)
            self.card_dict[card] = value

        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list[pos1], self.card_list[pos2] = self.card_list[pos2], self.card_list[pos1]

        # Put all the cards in the face down pile
        for card in self.card_list:
            self.piles[FACE_DOWN_PILE].append(card)

        # Create Both Player Hands

        for i in range((self.rnd + 2)):
            card = self.piles[FACE_DOWN_PILE].pop()
            self.piles[PLAYER_1_HAND].append(card)

        for i in range((self.rnd + 2)):
            card = self.piles[FACE_DOWN_PILE].pop()
            self.piles[PLAYER_2_HAND].append(card)

        # Position card in each hand
        for i in range(len(self.piles[PLAYER_1_HAND])):
            card = self.piles[PLAYER_1_HAND][i]
            card.center_x = self.straightline(i, PLAYER_1_HAND)
            card.center_y = PLAYER_HAND_Y

        for i in range(len(self.piles[PLAYER_2_HAND])):
            card = self.piles[PLAYER_2_HAND][i]
            card.center_x = self.straightline(i, PLAYER_2_HAND)
            card.center_y = PLAYER_HAND_Y

        # Pop top card into discard pile
        discard = self.piles[FACE_DOWN_PILE].pop()

        discard.center_x = DISCARD_POSITION_X
        discard.center_y = DISCARD_POSITION_Y

        self.piles[DISCARD_PILE].append(discard)

        # Create a list in each Player with all of the cards displayed,
        # to help with rendering order
        for player in self.player_list:
            for index in player.pile_numbers_list:
                for card in self.piles[index]:
                    player.card_list.append(card)

        # Initiate player turn, depending on rnd
        if self.rnd % 2 == 1:
            self.current_player = self.player_1
            self.player_1_turn = True
        else:
            self.current_player = self.player_2
            self.player_1_turn = False

        self.has_drawn = False
        self.has_discarded = False

        # Reset player rnd_scores, has_gone_down
        for player in self.player_list:
            player.rnd_score = 0
            player.has_gone_down = False

    def on_show(self):

        arcade.set_background_color(arcade.color.AMAZON)

    def get_hand_position(self):
        for i in range(len(self.piles[PLAYER_1_HAND])):
            card = self.piles[PLAYER_1_HAND][i]
            card.center_x = self.straightline(i, PLAYER_1_HAND)
            card.center_y = PLAYER_HAND_Y

        for i in range(len(self.piles[PLAYER_2_HAND])):
            card = self.piles[PLAYER_2_HAND][i]
            card.center_x = self.straightline(i, PLAYER_2_HAND)
            card.center_y = PLAYER_HAND_Y

    def get_go_down_pile_position(self):
        for i in range(len(self.piles[GO_DOWN_PILE])):
            card = self.piles[GO_DOWN_PILE][i]
            card.center_x = self.go_down_straightline(i)
            card.center_y = GO_DOWN_MAT_Y

    def straightline(self, i, current_player_hand):
        return 110 * i - ((((len(self.piles[current_player_hand])) - 1) * 110) / 2) + 640

    def go_down_straightline(self, i):
        return 120 * i - (((self.rnd + 1) * 120) / 2) + 640

    def pull_to_top(self, card):
        card_pile = self.card_list
        # Loop and pull all the other cards down towards the zero end
        for i in range(len(card_pile) - 1):
            card_pile[i] = card_pile[i + 1]
        # Put this card at the right-side/top of list
        card_pile[len(card_pile) - 1] = card

    def erase(self, player_hand):
        for card in player_hand:
            card.texture = arcade.make_transparent_color(arcade.csscolor.DARK_OLIVE_GREEN, 100000)

    def on_draw(self):
        arcade.start_render()

        self.button_list.draw()

        self.pile_mat_list.draw()

        for pile in self.current_player.pile_numbers_list:
            self.piles[pile].draw()

        for card in self.held_cards:
            card.draw()

        # Draw Player Scores

        arcade.draw_text(str(self.player_1.total_score), SCREEN_WIDTH / 2 - 50, 900, arcade.color.WHITE, font_size=24,
                         anchor_x="center")
        arcade.draw_text(str(self.player_2.total_score), SCREEN_WIDTH / 2 + 50, 900, arcade.color.WHITE, font_size=24,
                         anchor_x="center")
        arcade.draw_text(str(self.current_player), 1000, 900, self.current_player.color, font_size=40, anchor_x="center")
        arcade.draw_text(f"Round: {self.rnd}", 1200, 900, arcade.color.WHITE, font_size=24, anchor_x="center")

        # Draw 'final turn' when other player has gone down
        if self.player_1_turn:
            if self.player_2.has_gone_down:
                arcade.draw_text("Final Turn", 1200, 800, arcade.color.ALIZARIN_CRIMSON, font_size=40,
                                 anchor_x="center")

        elif not self.player_1_turn:
            if self.player_1.has_gone_down:
                arcade.draw_text("Final Turn", 1100, 600, arcade.color.ALIZARIN_CRIMSON, font_size=40,
                                 anchor_x="center")



    def on_update(self, delta_time: float):
        """
        Update card positions every 1/60 second based on the card's pile.
        :param delta_time:
        :return:
        """
        for pile in self.piles[1:]:
            for card in pile:
                card.texture = arcade.load_texture(card.image_file_name)
        for card in self.piles[FACE_DOWN_PILE]:
            card.center_x, card.center_y = FACE_DOWN_POSITION_X, FACE_DOWN_POSITION_Y
        for card in self.piles[DISCARD_PILE]:
            card.center_x, card.center_y = DISCARD_POSITION_X, DISCARD_POSITION_Y
        for card in self.piles[COMPLETED_CARDS]:
            card.center_x, card.center_y = COMPLETED_CARD_POSITION_X, COMPLETED_CARD_POSITION_Y
        self.get_go_down_pile_position()
        self.get_hand_position()

        # Handle text in go_down pile
        text = ''
        for card in self.piles[GO_DOWN_PILE]:
            text += self.card_dict[card]
        self.go_down_text = text








    def on_mouse_press(self, x, y, button, key_modifiers):

        pile = arcade.get_sprites_at_point((x, y), self.pile_mat_list)
        if pile:
            for value in pile:
                logging.debug(f'Pile #: {self.pile_mat_list.index(value)}')
            if len(pile) > 1:
                pile.remove(pile[-1])
            if self.pile_mat_list.index(pile[0]) == FACE_DOWN_PILE:
                cards = arcade.get_sprites_at_point((x, y), self.piles[FACE_DOWN_PILE])
            elif self.pile_mat_list.index(pile[0]) == DISCARD_PILE:
                cards = arcade.get_sprites_at_point((x, y), self.piles[DISCARD_PILE])
            elif self.pile_mat_list.index(pile[0]) == PLAYER_1_HAND or pile == PLAYER_2_HAND:
                cards = arcade.get_sprites_at_point((x, y), self.piles[self.current_player.hand_index])
            elif self.pile_mat_list.index(pile[0]) == GO_DOWN_PILE:
                cards = arcade.get_sprites_at_point((x, y), self.piles[GO_DOWN_PILE])
            elif self.pile_mat_list.index(pile[0]) == COMPLETED_CARDS:
                pass

        # cards = arcade.get_sprites_at_point((x, y), self.card_list)
            logging.debug('-' * 100)
            for i, card in enumerate(cards):
                logging.warning(f'#{i} card in held_cards: {card.value}')
            logging.warning(f'cards variable: {cards}')
        else:
            cards = []
        buttons = arcade.get_sprites_at_point((x, y), self.button_list)



        if len(cards) > 0:
            self.held_cards = cards
            for card in self.held_cards:
                if card in self.piles[COMPLETED_CARDS]:
                    self.held_cards = []

            if len(self.held_cards) > 0:
                logging.warning(f'Length of held_cards: {len(self.held_cards)}')
                logging.warning(f'Length of Player hand: {len(self.piles[self.current_player.hand_index])}')
                if self.current_player == self.player_1:
                    for i in range(len(self.held_cards)):
                        if i < len(self.held_cards):
                            for card in self.piles[PLAYER_2_HAND]:
                                if id(self.held_cards[i]) == id(card):

                                    self.held_cards.remove(self.held_cards[i])
                if self.current_player == self.player_2:
                    for i in range(len(self.held_cards)):
                        if i < len(self.held_cards):
                            for card in self.piles[PLAYER_1_HAND]:
                                if id(self.held_cards[i]) == id(card):
                                    self.held_cards.remove(self.held_cards[i])

                for _ in range(len(self.held_cards) - 1):
                    self.held_cards.remove(self.held_cards[0])

                pile = self.get_pile_for_card(self.held_cards[0])
                self.held_cards_original_pile: int = pile

                self.piles[pile].remove(self.held_cards[0])
                self.pull_to_top(self.held_cards[0])

                logging.warning(f'Length of held_cards at the end of mouse_press sequence: {len(self.held_cards)}')
                logging.debug('-' * 50)

        if len(buttons) > 0:
            self.buttons_pressed = buttons

            if self.go_down_button in self.buttons_pressed:
                self.go_down_button.texture = arcade.load_texture(GO_DOWN_PRESSED)
            elif self.save_word_button in self.buttons_pressed:
                self.save_word_button.texture = arcade.load_texture(SAVE_WORD_PRESSED)
            elif self.recall_button in self.buttons_pressed:
                self.recall_button.texture = arcade.load_texture(RECALL_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if len(self.held_cards) == 0 and len(self.buttons_pressed) == 0:
            return



        if len(self.buttons_pressed) > 0:

            if self.next_turn_button in self.buttons_pressed:
                rnd_end = False

                if self.has_discarded:
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)


                    if self.player_1_turn:
                        if self.player_2.has_gone_down:
                            self.current_player.has_gone_down = True

                            if len(self.piles[COMPLETED_CARDS]) != 0 or len(self.piles[self.current_player.hand_index]) != 0:
                                self.get_completed_words()
                            rnd_end = True
                            self.round_end_sequence()



                    elif not self.player_1_turn:
                        if self.player_1.has_gone_down:
                            self.current_player.has_gone_down = True

                            if len(self.piles[COMPLETED_CARDS]) != 0 or len(self.piles[self.current_player.hand_index]) != 0:
                                self.get_completed_words()
                            rnd_end = True
                            self.round_end_sequence()

                    if len(self.piles[COMPLETED_CARDS]) != 0:
                        for _ in range(len(self.piles[COMPLETED_CARDS])):
                            self.move_card_to_new_pile(self.piles[COMPLETED_CARDS][0], self.current_player.hand_index)
                    if len(self.piles[GO_DOWN_PILE]) != 0:
                        for _ in range(len(self.piles[GO_DOWN_PILE])):
                            self.move_card_to_new_pile(self.piles[GO_DOWN_PILE][0], self.current_player.hand_index)

                    if not rnd_end:
                        self.player_1_turn = not self.player_1_turn
                        if not self.player_1_turn:
                            self.current_player = self.player_2
                        else:
                            self.current_player = self.player_1
                    self.has_drawn = False
                    self.has_discarded = False
                    self.buttons_pressed = []
                    self.completed_words_list = []
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)


                else:
                    pass

            elif self.go_down_button in self.buttons_pressed:
                self.go_down_button.texture = arcade.load_texture(GO_DOWN)
                if len(self.piles[GO_DOWN_PILE]) == 0 and len(self.piles[self.current_player.hand_index]) == 0:
                    self.current_player.has_gone_down = True

                    self.get_completed_words()
                    for _ in range(len(self.piles[COMPLETED_CARDS])):
                        self.piles[COMPLETED_CARDS].pop()

                else:
                    logging.warning("You can't go down yet.")



            elif self.save_word_button in self.buttons_pressed:
                self.save_word_button.texture = arcade.load_texture(SAVE_WORD)
                self.save_word_sequence()

            elif self.recall_button in self.buttons_pressed:
                self.recall_sequence()


        if len(self.held_cards) > 0 and len(self.buttons_pressed) == 0:

            pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
            reset_position = True

            if modifiers and arcade.key.MOD_CTRL and button == arcade.MOUSE_BUTTON_LEFT:
                pile_index = self.held_cards_original_pile

                if pile_index == self.current_player.hand_index:
                    letter = self.held_cards[0].value
                    self.go_down_text += letter
                    logging.warning(self.go_down_text)
                    for card in self.held_cards:
                        self.move_card_to_new_pile(card, GO_DOWN_PILE)
                        reset_position = False

                elif pile_index == GO_DOWN_PILE:
                    for card in self.held_cards:
                        self.move_card_to_new_pile(card, self.current_player.hand_index)
                        reset_position = False

                if pile_index == FACE_DOWN_PILE or pile_index == DISCARD_PILE:
                    if not self.has_drawn:
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, self.current_player.hand_index)
                        self.has_drawn = True
                        reset_position = False
                else:
                    pass



            elif modifiers and arcade.key.MOD_CTRL and button == arcade.MOUSE_BUTTON_RIGHT:
                pile_index = self.held_cards_original_pile

                if pile_index != self.current_player.hand_index:
                    pass

                elif pile_index == self.current_player.hand_index:
                    if not self.has_drawn or self.has_discarded:
                        pass

                    elif self.has_drawn:
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, DISCARD_PILE)
                        self.has_discarded = True
                        self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)

                        reset_position = False

            elif not modifiers and button == arcade.MOUSE_BUTTON_LEFT:
                if self.has_drawn:
                    if arcade.check_for_collision(self.held_cards[0], pile):
                        pile_index = self.pile_mat_list.index(pile)

                        if pile_index == FACE_DOWN_PILE:
                            pass
                        elif pile_index == DISCARD_PILE:
                            if not self.has_discarded:
                                if self.held_cards_original_pile == self.current_player.hand_index:
                                    self.move_card_to_new_pile(self.held_cards[0], pile_index)
                                    self.has_discarded = True
                                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)
                                    reset_position = False

                            current_discard_pile = []
                            for card in self.piles[DISCARD_PILE]:
                                current_discard_pile.append(card.value)
                            logging.warning(current_discard_pile)

                        elif pile_index == GO_DOWN_PILE:
                            # letter = self.held_cards[0].value
                            # self.text += letter
                            # print(self.text)

                            for card in self.held_cards:
                                self.move_card_to_new_pile(card, pile_index)
                                reset_position = False

                elif self.held_cards_original_pile == FACE_DOWN_PILE or self.held_cards_original_pile == DISCARD_PILE:
                    if arcade.check_for_collision(self.held_cards[0], pile):
                        pile_index = self.pile_mat_list.index(pile)

                        if pile_index != PLAYER_1_HAND:
                            reset_position = True

                        else:
                            for card in self.held_cards:
                                self.move_card_to_new_pile(card, self.current_player.hand_index)

                            self.has_drawn = True

                            reset_position = False

                elif arcade.check_for_collision(self.held_cards[0], pile) and not self.has_drawn:

                    pile_index = self.pile_mat_list.index(pile)

                    if pile_index == self.held_cards_original_pile:
                        reset_position = True

                    elif pile_index == FACE_DOWN_PILE:
                        reset_position = True

                    elif pile_index == DISCARD_PILE:
                        reset_position = True


                    elif pile_index == PLAYER_1_HAND:

                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, self.current_player.hand_index)
                        reset_position = False

                    elif pile_index == GO_DOWN_PILE:

                        letter = self.held_cards[0].value
                        self.go_down_text += letter
                        logging.warning(self.go_down_text)

                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)

                        reset_position = False
            else:
                pass

            if reset_position:
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, self.held_cards_original_pile)
                    # logging.warning(self.get_pile_for_card(self.held_cards[0]))



        self.held_cards = []



        self.buttons_pressed = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def get_completed_words(self):
        if len(self.piles[COMPLETED_CARDS]) > self.rnd + 2:
            logging.warning("You need to have a discard.")
            self.recall_sequence()
        elif len(self.piles[COMPLETED_CARDS]) == 0 and len(self.piles[self.current_player.hand_index]) == 0:
            pass
        else:
            word_length_list = []
            current_score = 0
            for word in self.completed_words_list:
                word_length_list.append(len(word))
                for letter in word:
                    current_score += CARD_SCORE[letter]

            if len(self.piles[self.current_player.hand_index]) != 0:
                for card in self.piles[self.current_player.hand_index]:
                    current_score -= CARD_SCORE[card.value]
            logging.warning(current_score)
            self.current_player.total_score += current_score

            if len(word_length_list) > 0:
                word_length_list.sort()
                self.current_player.longest_words[self.rnd] = word_length_list[-1]

    def round_end_sequence(self):

        if self.player_1.longest_words[self.rnd] > self.player_2.longest_words[self.rnd]:
            self.player_1.total_score += 10
        elif self.player_1.longest_words[self.rnd] < self.player_2.longest_words[self.rnd]:
            self.player_2.total_score += 10

        self.rnd += 1
        self.buttons_pressed = []
        if self.rnd > 8:
            game_view = GameEnd(player_1_score=self.player_1.total_score, player_2_score=self.player_2.total_score)
            self.window.show_view(game_view)
        self.setup()

    def save_word_sequence(self):
        if len(self.go_down_text) > 1:
            if self.go_down_text in WORD_LIST:
                for i in range(len(self.piles[GO_DOWN_PILE])):
                    card = self.piles[GO_DOWN_PILE][0]
                    self.move_card_to_new_pile(card, COMPLETED_CARDS)

                self.completed_words_list.append(self.go_down_text)

                logging.warning(self.completed_words_list)

            else:
                print("Sorry, that's not a word. Dumbass.")

                for i in range(len(self.piles[GO_DOWN_PILE])):
                    card = self.piles[GO_DOWN_PILE][0]
                    self.move_card_to_new_pile(card, self.current_player.hand_index)

                self.go_down_text = ''

            self.go_down_text = ''


        else:
            print("Sorry, your word needs to be at least 2 letters long. Dumbass.")
            for card in self.piles[GO_DOWN_PILE]:
                self.move_card_to_new_pile(card, self.current_player.hand_index)
            self.go_down_text = ''

    def recall_sequence(self):
        if len(self.piles[COMPLETED_CARDS]) != 0:
            for _ in range(len(self.piles[COMPLETED_CARDS])):
                self.move_card_to_new_pile(self.piles[COMPLETED_CARDS][0], self.current_player.hand_index)

            self.completed_words_list = []


    def get_pile_for_card(self, card):

        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def remove_card_from_pile(self, card_id):
        for pile in self.piles:
            for card in pile:
                if id(card) == card_id:
                    pile.remove(card)
                    break

    def move_card_to_new_pile(self, card, pile_index):
        try:
            self.remove_card_from_pile(id(card))
        except:
            pass
        self.piles[pile_index].append(card)
        # logging.warning(self.get_pile_for_card(card))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.save_word_sequence()
        elif key == arcade.key.ESCAPE:
            self.recall_sequence()
        elif key == arcade.key.BACKSPACE:
            if len(self.piles[GO_DOWN_PILE]) > 0:
                self.move_card_to_new_pile(self.piles[GO_DOWN_PILE][-1], self.current_player.hand_index)

    def on_text(self, text):


        for i in self.card_dict:

            if text in self.card_dict[i]:
                card_input: Card = i

                if card_input in self.piles[self.current_player.hand_index]:
                    self.card_input_original_position = [card_input.position]
                    self.piles[GO_DOWN_PILE].append(card_input)
                    self.get_go_down_pile_position()
                    self.piles[self.current_player.hand_index].remove(card_input)
                    self.go_down_text += text
                    print(self.go_down_text)
                    break




    # def round_end(self):
    #     self.rnd += 1
    #     self.setup()

class GameEnd(arcade.View):

    def __init__(self, player_1_score, player_2_score):
        super().__init__()
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
        self.winner = None
        self.draw = False

        if self.player_1_score > self.player_2_score:
            self.winner = 'Player 1'
        elif self.player_2_score > self.player_1_score:
            self.winner = 'Player 2'
        elif self.player_1_score == self.player_2_score:
            self.draw = True

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        arcade.start_render()
        if self.winner:
            arcade.draw_text(f'Congratulations, {self.winner}!\nYou won by {abs(self.player_2_score - self.player_1_score)}.',
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, arcade.color.WHITE, font_size=24, align="center",
                             anchor_x="center")
        elif self.draw:
            arcade.draw_text(f'Congratulations, Player 1 and Player 2 - you tied!\nA rematch must be had to determine who is the best Quiddler player!',
                SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, arcade.color.WHITE, font_size=24, align="center",
                             anchor_x="center")
        arcade.draw_text(f'SCORES\n\nPlayer 1: {self.player_1_score}       Player 2: {self.player_2_score}',
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT - 400, arcade.color.WHITE, font_size=24, align="center",
                         anchor_x="center")
        arcade.draw_text("Would you like to play again?\nPress 'y' for yes, 'n' for no.",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT - 700, arcade.color.WHITE, font_size=24, align="center",
                         anchor_x="center")

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.Y:
            game_view = Quiddler()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.N:
            exit()



class GameMenu(arcade.View):

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("QUIDDLER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=100, anchor_x="center")
        arcade.draw_text("Click anywhere to start", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, arcade.color.WHITE, font_size=40, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Quiddler()
        game_view.setup()
        self.window.show_view(game_view)


class GoDownMenu(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.FOREST_GREEN)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("This is the go-down menu", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, arcade.color.WHITE,
                         font_size=40, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.window.show_view(self.game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Quiddler")
    window.center_window()
    start_view = GameMenu()
    window.show_view(start_view)

    arcade.run()





if __name__ == "__main__":
    main()
