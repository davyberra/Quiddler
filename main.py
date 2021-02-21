import arcade
import random
import pyglet
import logging

from nltk.corpus import words
from pyglet.window import key

WORD_LIST = words.words()
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

FACE_DOWN_IMAGE = "card_back.png"
GO_DOWN = "images/go_down.png"
GO_DOWN_PRESSED = "images/go_down_pressed.png"
NEXT_TURN = "images/next_turn.png"
NEXT_TURN_PRESSED = "images/next_turn_pressed.png"
SAVE_WORD = "images/save_word.png"
SAVE_WORD_PRESSED = "images/save_word_pressed.png"

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
    def __init__(self):
        self.pile_numbers_list = []
        self.card_list = arcade.SpriteList()
        self.score = None
        self.turn_order = None
        self.hand_index = None


class Quiddler(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        # Initialize Players and add them to a list of all players
        self.player_list = []
        self.player_1 = Player()
        self.player_1.hand_index = PLAYER_1_HAND
        self.player_1.pile_numbers_list = [0, 1, 2, 3]
        self.player_list.append(self.player_1)
        self.player_2 = Player()
        self.player_2.hand_index = PLAYER_2_HAND
        self.player_2.pile_numbers_list = [0, 1, 2, 4]
        self.player_list.append(self.player_2)

        self.rnd = 1
        self.card_list = None
        self.mat_list = None
        self.button_list = None
        self.buttons_pressed = None
        self.held_cards = None
        self.held_cards_original_position = None
        self.piles = None
        self.player_turn = None

        # self.current_player = None
        self.next_turn_button = None
        self.go_down_button = None
        self.save_word_button = None

        self.card_dict = None
        self.pile_mat_list = None

        # List of Player Scores
        self.player_scores = None
        # Text string representing letters in the go_down pile.
        self.text = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """
        Initializes values for piles, hands.
        :return:
        """

        self.text = ''


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
        pile = arcade.SpriteSolidColor(SCREEN_WIDTH, MAT_HEIGHT, arcade.color.ALIZARIN_CRIMSON)
        pile.position = SCREEN_WIDTH / 2, GO_DOWN_MAT_Y
        self.pile_mat_list.append(pile)

        # Create mat for the player hands
        for i in range(2):
            pile = arcade.SpriteSolidColor((self.rnd + 2) * MAT_WIDTH, MAT_HEIGHT, arcade.color.ALIZARIN_CRIMSON)
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

        # Initiate player turn
        self.current_player = self.player_1
        self.player_turn = True

        self.has_drawn = False
        self.has_discarded = False

        """ Test which cards are being drawn """
        # self.player_2.card_list = arcade.SpriteList()

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

    def pull_to_top(self, card, current_player):
        # Figure out which player's card list is being used
        card_pile = current_player.card_list
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

        # if self.current_player == self.player_1:
        #     self.player_1.card_list.draw()
        # elif self.current_player == self.player_2:
        #     self.player_2.card_list.draw()

        self.current_player.card_list.draw()

        # self.card_list.draw()

        # self.piles[FACE_DOWN_PILE].draw()
        #
        # self.piles[DISCARD_PILE].draw()
        #
        # self.piles[GO_DOWN_PILE].draw()
        #
        # self.piles[self.current_player.hand_index].draw()
        #
        # self.piles[COMPLETED_CARDS].draw()

    def on_update(self, delta_time: float):
        """
        Update card positions every 1/60 second based on the card's pile.
        :param delta_time:
        :return:
        """
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
        self.text = text

        self.current_player.card_list.update()





    def on_mouse_press(self, x, y, button, key_modifiers):

        cards = arcade.get_sprites_at_point((x, y), self.card_list)
        buttons = arcade.get_sprites_at_point((x, y), self.button_list)
        self.update(delta_time=.1)

        if self.has_discarded:
            pass

        elif len(cards) > 0:

            self.held_cards = cards

            for card in cards:
                if card in self.piles[COMPLETED_CARDS]:
                    self.held_cards = []

            if len(self.held_cards) > 0:
                if self.current_player == self.player_1:
                    for i in range(len(self.held_cards)):
                        if i < len(self.held_cards):
                            if self.held_cards[i] in self.piles[PLAYER_2_HAND]:
                                self.held_cards.remove(self.held_cards[i])
                if self.current_player == self.player_2:
                    for i in range(len(self.held_cards)):
                        if i < len(self.held_cards):
                            if self.held_cards[i] in self.piles[PLAYER_1_HAND]:
                                self.held_cards.remove(self.held_cards[i])

                pile = self.get_pile_for_card(cards[0])
                self.held_cards = [self.held_cards[-1]]

                self.held_cards_original_pile: int = pile
                self.piles[pile].remove(self.held_cards[0])
                self.pull_to_top(self.held_cards[0], self.current_player)

                # logging.warning(self.held_cards_original_pile)


        if len(buttons) > 0:
            self.buttons_pressed = buttons

            if self.go_down_button in self.buttons_pressed:
                self.go_down_button.texture = arcade.load_texture(GO_DOWN_PRESSED)
            elif self.save_word_button in self.buttons_pressed:
                self.save_word_button.texture = arcade.load_texture(SAVE_WORD_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if len(self.held_cards) == 0 and len(self.buttons_pressed) == 0:
            return

        if len(self.buttons_pressed) > 0:
            if self.next_turn_button in self.buttons_pressed:
                if self.has_discarded:
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)
                    self.player_turn = not self.player_turn
                    if not self.player_turn:
                        self.current_player = self.player_2
                    else:
                        self.current_player = self.player_1
                    self.has_drawn = False
                    self.has_discarded = False
                    self.buttons_pressed = []
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)
                else:
                    pass

            elif self.go_down_button in self.buttons_pressed:
                self.go_down_button.texture = arcade.load_texture(GO_DOWN)
                self.rnd += 1
                self.buttons_pressed = []
                self.setup()

            elif self.save_word_button in self.buttons_pressed:
                self.save_word_button.texture = arcade.load_texture(SAVE_WORD)
                if len(self.text) > 1:
                    if self.text in WORD_LIST:
                        for i in range(len(self.piles[GO_DOWN_PILE])):
                            card = self.piles[GO_DOWN_PILE][0]
                            self.move_card_to_new_pile(card, COMPLETED_CARDS)

                    else:
                        print("Sorry, that's not a word. Dumbass.")

                        for i in range(len(self.piles[GO_DOWN_PILE])):
                            card = self.piles[GO_DOWN_PILE][0]
                            self.move_card_to_new_pile(card, self.current_player.hand_index)

                        self.text = ''


                    self.text = ''
                    if len(self.piles[GO_DOWN_PILE]) != len(self.text):
                        print(len(self.piles[GO_DOWN_PILE]))
                        print(len(self.text))
                        print(len(self.piles[COMPLETED_CARDS]))


                else:
                    print("Sorry, your word needs to be at least 2 letters long. Dumbass.")
                    for card in self.piles[GO_DOWN_PILE]:
                        self.move_card_to_new_pile(card, self.current_player.hand_index)
                    self.text = ''

        if len(self.held_cards) > 0 and len(self.buttons_pressed) == 0:

            pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
            reset_position = True
            if self.has_drawn:
                if arcade.check_for_collision(self.held_cards[0], pile):
                    pile_index = self.pile_mat_list.index(pile)

                    if pile_index == FACE_DOWN_PILE:
                        pass
                    elif pile_index == DISCARD_PILE:

                        if self.held_cards_original_pile == self.current_player.hand_index:
                            self.move_card_to_new_pile(self.held_cards[0], pile_index)
                            self.has_discarded = True
                            self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)
                            reset_position = False

                    elif pile_index == GO_DOWN_PILE:
                        # letter = self.held_cards[0].value
                        # self.text += letter
                        # print(self.text)

                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)

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
                    self.move_card_to_new_pile(self.held_cards[0], self.held_cards_original_pile)

                elif pile_index == FACE_DOWN_PILE:
                    pass

                elif pile_index == DISCARD_PILE:
                    # for i, dropped_card in enumerate(self.held_cards):
                    #     dropped_card.position = pile.center_x, pile.center_y

                    for card in self.held_cards:
                        self.move_card_to_new_pile(card, pile_index)

                elif pile_index == PLAYER_1_HAND:

                    for card in self.held_cards:
                        self.move_card_to_new_pile(card, self.current_player.hand_index)


                elif pile_index == GO_DOWN_PILE:

                    letter = self.held_cards[0].value
                    self.text += letter
                    logging.warning(self.text)

                    for card in self.held_cards:
                        self.move_card_to_new_pile(card, pile_index)




                
                reset_position = False

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

    def get_pile_for_card(self, card):

        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def remove_card_from_pile(self, card):
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def move_card_to_new_pile(self, card, pile_index):
        try:
            self.remove_card_from_pile(card)
        except:
            pass
        self.piles[pile_index].append(card)
        # logging.warning(self.get_pile_for_card(card))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            if len(self.text) > 1:
                if self.text in WORD_LIST:
                    for i in range(len(self.piles[GO_DOWN_PILE])):
                        card = self.piles[GO_DOWN_PILE][0]
                        self.move_card_to_new_pile(card, COMPLETED_CARDS)
                        card.position = COMPLETED_CARD_POSITION_X, COMPLETED_CARD_POSITION_Y
                    score = 0
                    for letter in self.text:
                        score += CARD_SCORE[letter]

                    self.player_scores[self.current_player.hand_index - 3] += score
                    print(self.player_scores)
                    print(self.player_scores[self.current_player.hand_index - 3])
                    self.text = ''

                else:
                    print("Sorry, that's not a word. Dumbass.")

                    for i in range(len(self.piles[GO_DOWN_PILE])):
                        card = self.piles[GO_DOWN_PILE][0]
                        self.move_card_to_new_pile(card, self.current_player.hand_index)

                    self.text = ''
                    self.get_hand_position()

                self.text = ''
                if len(self.piles[GO_DOWN_PILE]) != len(self.text):
                    print(len(self.piles[GO_DOWN_PILE]))
                    print(len(self.text))
                    print(len(self.piles[COMPLETED_CARDS]))


            else:
                print("Sorry, your word needs to be at least 2 letters long. Dumbass.")
                for i in range(len(self.piles[GO_DOWN_PILE])):
                    card = self.piles[GO_DOWN_PILE][0]
                    self.move_card_to_new_pile(card, self.current_player.hand_index)

                self.text = ''
                self.get_hand_position()

    def on_text(self, text):


        for i in self.card_dict:

            if text in self.card_dict[i]:
                card_input: Card = i

                if card_input in self.piles[self.current_player.hand_index]:
                    self.card_input_original_position = [card_input.position]
                    self.piles[GO_DOWN_PILE].append(card_input)
                    self.get_go_down_pile_position()
                    self.piles[self.current_player.hand_index].remove(card_input)
                    self.text += text
                    print(self.text)
                    break




    def round_end(self):
        self.rnd += 1
        self.setup()






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
