import arcade
import random
import logging
import time

from word_list import get_word_list


WORD_LIST = get_word_list()
BACKGROUND_IMAGE_WIDTH, BACKGROUND_IMAGE_HEIGHT = 2560, 1920
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
CARD_SCORE = {'a': 2, 'b': 8, 'c': 8, 'd': 5, 'e': 2, 'f': 6, 'g': 6, 'h': 7, 'i': 2, 'j': 13, 'k': 8, 'l': 3, 'm': 5,
              'n': 5, 'o': 2, 'p': 6, 'q': 15, 'r': 5, 's': 3, 't': 3, 'u': 4, 'v': 11, 'w': 10, 'x': 12, 'y': 4,
              'z': 14, 'er': 7, 'cl': 10, 'in': 7, 'th': 9, 'qu': 9}

FACE_DOWN_IMAGE = "test_images/card_back.png"
GO_DOWN = "test_images/go_down.png"
GO_DOWN_PRESSED = "test_images/go_down_pressed.png"
GO_DOWN_FLASH = "test_images/go_down_flash.png"
NEXT_TURN = "test_images/next_turn.png"
NEXT_TURN_PRESSED = "test_images/next_turn_pressed.png"
NEXT_TURN_FLASH = "test_images/next_turn_flash.png"
SAVE_WORD = "test_images/save_word.png"
SAVE_WORD_PRESSED = "test_images/save_word_pressed.png"
SAVE_WORD_FLASH = "test_images/save_word_flash.png"
RECALL = "test_images/recall.png"
RECALL_PRESSED = "test_images/recall_pressed.png"
UNDO = "test_images/undo.png"
UNDO_PRESSED = "test_images/undo_pressed.png"
EXIT = "images/exit_button.png"
EXIT_PRESSED = "images/exit_button_pressed.png"

CARD_MOVE_SOUND = arcade.load_sound("sounds/card_move.ogg")
SAVE_WORD_SOUND = arcade.load_sound("sounds/save_word.ogg")
GO_DOWN_SOUND = arcade.load_sound("sounds/go_down.ogg")
WRONG_WORD_SOUND = arcade.load_sound("sounds/wrong_word.ogg")
BACKGROUND_MUSIC = arcade.load_sound("sounds/quiddler_theme_2.ogg")
MAIN_MENU_MUSIC = arcade.load_sound("sounds/quiddler_theme_1.ogg")

SCALE = 1

PLAYER_HAND_Y = 225
GO_DOWN_MAT_Y = 450
BUTTON_Y = 50

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

WHITE = arcade.color.WHITE
WHITE_TRANSPARENT = (255, 255, 255, 40)
GOLD_TRANSPARENT = (206, 201, 53, 100)

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

        self.image_file_name = f"test_cards/{self.value}.png"

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

    def __init__(self, rnd_number):
        super().__init__()
        # Initialize Players and add them to a list of all players
        self.screen_width, self.screen_height = self.window.get_size()
        # self.screen_width, self.screen_height = round(self.screen_width * .6), round(self.screen_height * .6)
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)

        self.face_down_position_x, self.face_down_position_y = (self.screen_width / 2) - 70 * self.scale, self.screen_height - self.screen_height / 4
        self.discard_position_x, self.discard_position_y = (self.screen_width / 2) + 70 * self.scale, self.screen_height - self.screen_height / 4
        self.completed_card_position_x, self.completed_card_position_y = 150 * self.scale, self.screen_height - 250 * self.scale
        self.player_1_score_box = {
            'center_x': (self.screen_width / 2) - 450 * self.scale,
            'center_y': self.screen_height - 125 * self.scale,
            'width': 400 * self.scale,
            'height': 200 * self.scale
        }
        self.player_2_score_box = {
            'center_x': (self.screen_width / 2) + 450 * self.scale,
            'center_y': self.screen_height - 125 * self.scale,
            'width': 400 * self.scale,
            'height': 200 * self.scale
        }

        self.player_list = []
        self.player_1 = Player('Player 1')
        self.player_1.hand_index = PLAYER_1_HAND
        self.player_1.pile_numbers_list = [0, 1, 2, 3, 5]
        self.player_1.color = WHITE_TRANSPARENT
        self.player_list.append(self.player_1)
        self.player_2 = Player('Player 2')
        self.player_2.hand_index = PLAYER_2_HAND
        self.player_2.pile_numbers_list = [0, 1, 2, 4, 5]
        self.player_2.color = WHITE_TRANSPARENT
        self.player_list.append(self.player_2)

        self.rnd = 1
        self.rnd_hand_count = 3
        self.rnd_max = rnd_number
        self.card_list = None
        self.small_card_list = None
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
        self.undo_button = None

        self.card_dict = None
        self.pile_mat_list = None

        # List of Player Scores
        self.player_scores = None
        # Text string representing letters in the go_down pile.
        self.go_down_text = None

        self.has_drawn = False
        self.has_discarded = False
        self.completed_words_text_list = []
        self.completed_words_card_list = []
        self.card_input_original_position = None
        self.drawn_card_original_pile = None
        self.moves = None
        self.last_move = None
        self.score_change_list= None

        self.go_down_flash_timer = None
        self.save_word_flash_timer = None
        self.next_turn_flash_timer = None
        self.go_down_flash_timer_change = None
        self.save_word_flash_timer_change = None
        self.next_turn_flash_timer_change = None


        self.background = None

        BACKGROUND_MUSIC.play(volume=.25)

    def setup(self):
        """
        Initializes values for piles, hands.
        :return:
        """

        self.go_down_text = ''
        self.completed_words_text_list = []
        self.moves = 0
        self.last_move = 0
        self.score_change_list = []
        self.go_down_flash_timer = 0
        self.save_word_flash_timer = 0
        self.next_turn_flash_timer = 0
        self.go_down_flash_timer_change = -1
        self.save_word_flash_timer_change = -1
        self.next_turn_flash_timer_change = -1


        # List of cards we're dragging with the mouse ------------------------------------------------------------------
        self.held_cards = []
        # List of buttons currently pressed
        self.buttons_pressed = []
        # Original location of cards we are dragging
        self.held_cards_original_position = []
        # Create a list of lists, each holds a pile of cards
        self.piles = [[] for _ in range(PILE_COUNT)]

        self.card_list = arcade.SpriteList()
        self.small_card_list = arcade.SpriteList()
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
        self.next_turn_button = arcade.Sprite(NEXT_TURN_PRESSED, self.scale)
        self.next_turn_button.center_x = self.screen_width - 150 * self.scale
        self.next_turn_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.next_turn_button)

        self.go_down_button = arcade.Sprite(GO_DOWN, self.scale)
        self.go_down_button.center_x = self.screen_width - 400 * self.scale
        self.go_down_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.go_down_button)

        self.save_word_button = arcade.Sprite(SAVE_WORD, self.scale)
        self.save_word_button.center_x = 150 * self.scale
        self.save_word_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.save_word_button)

        self.recall_button = arcade.Sprite(RECALL, self.scale)
        self.recall_button.center_x = 400 * self.scale
        self.recall_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.recall_button)

        self.undo_button = arcade.Sprite(UNDO, self.scale)
        self.undo_button.center_x = 150 * self.scale
        self.undo_button.center_y = self.screen_height - 50 * self.scale
        self.button_list.append(self.undo_button)

        # Create a card dictionary with Card keys assigned to letter values
        self.card_dict = {}

        # Create sprite list with all the mats
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the face down and discard piles
        pile = arcade.SpriteSolidColor(round(MAT_WIDTH * self.scale), round(MAT_HEIGHT * self.scale), (255, 255, 255, 40))
        pile.position = self.face_down_position_x, self.face_down_position_y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(round(MAT_WIDTH * self.scale), round(MAT_HEIGHT * self.scale), (255, 255, 255, 40))
        pile.position = self.discard_position_x, self.discard_position_y
        self.pile_mat_list.append(pile)

        # Create mat for going down
        pile = arcade.SpriteSolidColor(self.screen_width, round(MAT_HEIGHT * self.scale), (255, 255, 0, 1))
        pile.position = self.screen_width / 2, GO_DOWN_MAT_Y * self.scale
        self.pile_mat_list.append(pile)

        # Create mat for the player hands
        for i in range(2):
            pile = arcade.SpriteSolidColor(round(self.rnd_hand_count * MAT_WIDTH * self.scale),
                                           round(MAT_HEIGHT * self.scale),
                                           (255, 255, 255, 10))
            pile.position = self.screen_width / 2, PLAYER_HAND_Y * self.scale
            self.pile_mat_list.append(pile)

        # Create mat for completed cards
        pile = arcade.SpriteSolidColor(round(MAT_WIDTH * self.scale),
                                       round(MAT_HEIGHT * self.scale),
                                       (255, 255, 255, 40))
        pile.position = self.completed_card_position_x, self.completed_card_position_y
        self.pile_mat_list.append(pile)

        # Create every card, both regular and small versions
        for value in CARD_LIST:
            card = Card(value, self.scale)
            card.position = self.face_down_position_x, self.face_down_position_y
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

        for i in range(self.rnd_hand_count):
            card = self.piles[FACE_DOWN_PILE].pop()
            self.piles[PLAYER_1_HAND].append(card)

        for i in range(self.rnd_hand_count):
            card = self.piles[FACE_DOWN_PILE].pop()
            self.piles[PLAYER_2_HAND].append(card)

        # Position card in each hand
        for i in range(len(self.piles[PLAYER_1_HAND])):
            card = self.piles[PLAYER_1_HAND][i]
            card.center_x = self.straightline(i, PLAYER_1_HAND)
            card.center_y = PLAYER_HAND_Y * self.scale

        for i in range(len(self.piles[PLAYER_2_HAND])):
            card = self.piles[PLAYER_2_HAND][i]
            card.center_x = self.straightline(i, PLAYER_2_HAND)
            card.center_y = PLAYER_HAND_Y * self.scale

        # Pop top card into discard pile
        discard = self.piles[FACE_DOWN_PILE].pop()

        discard.center_x = self.discard_position_x
        discard.center_y = self.discard_position_y

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

        # Flip all cards (except draw pile) face_up
        for pile in self.piles[1:]:
            for card in pile:
                card.texture = arcade.load_texture(card.image_file_name)

        self.background = arcade.Sprite(filename="images/quiddler_background_large(2).png",
                                        scale=self.screen_width / BACKGROUND_IMAGE_WIDTH)
        self.background.position = self.screen_width / 2, self.screen_height / 2


    def get_hand_position(self):
        for i in range(len(self.piles[PLAYER_1_HAND])):
            card = self.piles[PLAYER_1_HAND][i]
            card.center_x = self.straightline(i, PLAYER_1_HAND)
            card.center_y = PLAYER_HAND_Y * self.scale

        for i in range(len(self.piles[PLAYER_2_HAND])):
            card = self.piles[PLAYER_2_HAND][i]
            card.center_x = self.straightline(i, PLAYER_2_HAND)
            card.center_y = PLAYER_HAND_Y * self.scale

    def get_go_down_pile_position(self):
        for i in range(len(self.piles[GO_DOWN_PILE])):
            card = self.piles[GO_DOWN_PILE][i]
            card.center_x = self.go_down_straightline(i)
            card.center_y = GO_DOWN_MAT_Y * self.scale

    def straightline(self, i, current_player_hand):
        return 110 * self.scale * i - ((((len(self.piles[current_player_hand])) - 1) * 110 * self.scale) / 2) + self.screen_width / 2

    def go_down_straightline(self, i):
        return 120 * self.scale * i - (((len(self.piles[GO_DOWN_PILE]) - 1) * 120 * self.scale) / 2) + self.screen_width / 2

    def pull_to_top(self, card, card_pile):
        # Loop and pull all the other cards down towards the zero end
        for i in range(len(card_pile) - 1):
            card_pile[i] = card_pile[i + 1]
        # Put this card at the right-side/top of list
        card_pile[len(card_pile) - 1] = card

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        # Draw player score boxes

        arcade.draw_rectangle_filled(
            center_x=self.player_1_score_box['center_x'],
            center_y=self.player_1_score_box['center_y'],
            width=self.player_1_score_box['width'],
            height=self.player_1_score_box['height'],
            color=self.player_1.color
        )
        arcade.draw_rectangle_filled(
            center_x=self.player_2_score_box['center_x'],
            center_y=self.player_2_score_box['center_y'],
            width=self.player_2_score_box['width'],
            height=self.player_2_score_box['height'],
            color=self.player_2.color
        )

        # Draw cards/buttons

        self.button_list.draw()

        self.pile_mat_list.draw()

        for pile in self.current_player.pile_numbers_list:
            self.piles[pile].draw()

        for card in self.held_cards:
            card.draw()

        self.small_card_list.draw()

        # Draw Player Scores
        
        arcade.draw_text(
            f'{self.player_1}',
            self.player_1_score_box['center_x'],
            self.player_1_score_box['center_y'] + 50 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            f'{self.player_1.total_score}',
            self.player_1_score_box['center_x'],
            self.player_1_score_box['center_y'] - 50 * self.scale,
            WHITE,
            font_size=round(24 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            f'{self.player_2}',
            self.player_2_score_box['center_x'],
            self.player_2_score_box['center_y'] + 50 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            f'{self.player_2.total_score}',
            self.player_2_score_box['center_x'],
            self.player_2_score_box['center_y'] - 50 * self.scale,
            WHITE,
            font_size=round(24 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )

        # Draw Round number

        arcade.draw_text(
            f"Round: {self.rnd}",
            self.screen_width - 125 * self.scale,
            self.screen_height - 50 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )

        # Draw hand_count number

        arcade.draw_text(
            f"Cards: {self.rnd_hand_count}",
            self.screen_width - 120 * self.scale,
            self.screen_height - 150 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center"
        )

        # Draw 'final turn' when other player has gone down
        if self.player_1_turn:
            if self.player_2.has_gone_down:
                arcade.draw_text(
                    "Final Turn!",
                    self.screen_width - 150 * self.scale,
                    100 * self.scale,
                    arcade.color.GOLD,
                    font_size=round(24 * self.scale),
                    anchor_x="center"
                )

        elif not self.player_1_turn:
            if self.player_1.has_gone_down:
                arcade.draw_text(
                    "Final Turn!",
                    self.screen_width - 150 * self.scale,
                    100 * self.scale,
                    arcade.color.GOLD,
                    font_size=round(24 * self.scale),
                    anchor_x="center"
                )

        for score_list in self.score_change_list:
            x, y, color, prefix = 0, 0, None, None
            if score_list[0] == self.player_1:
                x, y = self.player_1_score_box['center_x'], self.player_1_score_box['center_y']
            elif score_list[0] == self.player_2:
                x, y = self.player_2_score_box['center_x'], self.player_2_score_box['center_y']

            if score_list[1] >= 0:
                color = arcade.color.GREEN
                prefix = '+'
            elif score_list[1] < 0:
                color = arcade.color.RED
                prefix = ''

            arcade.draw_text(
                f'{prefix}{score_list[1]}',
                x, y,
                color,
                font_size=round(24 * self.scale),
                anchor_x="center",
                anchor_y="center"
            )



    def on_update(self, delta_time: float):
        """
        Update card positions every 1/60 second based on the card's pile.
        :param delta_time:
        :return:
        """
        # Loop audio
        if BACKGROUND_MUSIC.is_complete():
            BACKGROUND_MUSIC.play(volume=.25)

        # Update card positions

        # for pile in self.piles[1:]:
        #     for card in pile:
        #         card.texture = arcade.load_texture(card.image_file_name)
        for card in self.piles[FACE_DOWN_PILE]:
            card.center_x, card.center_y = self.face_down_position_x, self.face_down_position_y
        for card in self.piles[DISCARD_PILE]:
            card.center_x, card.center_y = self.discard_position_x, self.discard_position_y
        for card in self.piles[COMPLETED_CARDS]:
            card.center_x, card.center_y = self.completed_card_position_x, self.completed_card_position_y
        self.get_go_down_pile_position()
        self.get_hand_position()

        # Handle text in go_down pile
        text = ''
        for card in self.piles[GO_DOWN_PILE]:
            text += self.card_dict[card]
        self.go_down_text = text

        # Timer for score-change animation

        for score_list in self.score_change_list:
            if score_list[2] > 200:
                self.score_change_list.remove(score_list)
            else:
                score_list[2] += 1

        # Handle which buttons should be flashing based on turn state

        if len(self.piles[GO_DOWN_PILE]) < 2:
            self.save_word_flash_timer = 0
            self.save_word_flash_timer_change = -1
            self.save_word_button.texture = arcade.load_texture(SAVE_WORD)

        if len(self.piles[COMPLETED_CARDS]) == self.rnd_hand_count and self.has_discarded:
            if self.go_down_button not in self.buttons_pressed:
                if self.go_down_flash_timer >= 30:
                    self.go_down_button.texture = arcade.load_texture(GO_DOWN)
                    self.go_down_flash_timer_change = -self.go_down_flash_timer_change
                elif self.go_down_flash_timer <= 0:
                    self.go_down_button.texture = arcade.load_texture(GO_DOWN_FLASH)
                    self.go_down_flash_timer_change = -self.go_down_flash_timer_change
                self.go_down_flash_timer += self.go_down_flash_timer_change

        elif len(self.piles[GO_DOWN_PILE]) > 1:
            if self.save_word_button not in self.buttons_pressed:
                if self.save_word_flash_timer >= 30:
                    self.save_word_button.texture = arcade.load_texture(SAVE_WORD)
                    self.save_word_flash_timer_change = -self.save_word_flash_timer_change
                elif self.save_word_flash_timer <= 0:
                    self.save_word_button.texture = arcade.load_texture(SAVE_WORD_FLASH)
                    self.save_word_flash_timer_change = -self.save_word_flash_timer_change
                self.save_word_flash_timer += self.save_word_flash_timer_change

        elif self.current_player.has_gone_down:
            if self.next_turn_button not in self.buttons_pressed:
                if self.next_turn_flash_timer >= 30:
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)
                    self.next_turn_flash_timer_change = -self.next_turn_flash_timer_change
                elif self.next_turn_flash_timer <= 0:
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_FLASH)
                    self.next_turn_flash_timer_change = -self.next_turn_flash_timer_change
                self.next_turn_flash_timer += self.next_turn_flash_timer_change

        # Update player box color based on player turn
        if self.player_1_turn:
            self.player_1.color = GOLD_TRANSPARENT
            self.player_2.color = WHITE_TRANSPARENT
        elif not self.player_1_turn:
            self.player_1.color = WHITE_TRANSPARENT
            self.player_2.color = GOLD_TRANSPARENT





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
                self.pull_to_top(self.held_cards[0], self.card_list)

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
            elif self.next_turn_button in self.buttons_pressed:
                self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)
            elif self.undo_button in self.buttons_pressed:
                self.undo_button.texture = arcade.load_texture(UNDO_PRESSED)


    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if len(self.held_cards) == 0 and len(self.buttons_pressed) == 0:
            return



        if len(self.buttons_pressed) > 0:
            buttons = arcade.get_sprites_at_point((x, y), self.button_list)
            if self.buttons_pressed == buttons:
                if self.undo_button in self.buttons_pressed:
                    if self.moves == self.last_move + 1:
                        if self.has_drawn and not self.has_discarded:
                            undo_card = self.piles[self.current_player.hand_index][-1]
                            self.move_card_to_new_pile(undo_card, self.drawn_card_original_pile,
                                                       self.held_cards_original_pile)
                            if self.drawn_card_original_pile == FACE_DOWN_PILE:
                                undo_card.texture = arcade.load_texture(FACE_DOWN_IMAGE)
                            self.has_drawn = False
                            arcade.play_sound(WRONG_WORD_SOUND, volume=0.5)

                        elif self.has_discarded:
                            undo_card = self.piles[DISCARD_PILE][-1]
                            self.move_card_to_new_pile(undo_card, self.current_player.hand_index, DISCARD_PILE)
                            self.has_discarded = False
                            self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)
                            arcade.play_sound(WRONG_WORD_SOUND, volume=0.5)

                    self.undo_button.texture = arcade.load_texture(UNDO)
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
                                self.move_card_to_new_pile(self.piles[COMPLETED_CARDS][0], self.current_player.hand_index,
                                                           COMPLETED_CARDS)
                        if len(self.piles[GO_DOWN_PILE]) != 0:
                            for _ in range(len(self.piles[GO_DOWN_PILE])):
                                self.move_card_to_new_pile(self.piles[GO_DOWN_PILE][0], self.current_player.hand_index,
                                                           GO_DOWN_PILE)

                        if not rnd_end:
                            self.player_1_turn = not self.player_1_turn
                            if not self.player_1_turn:
                                self.current_player = self.player_2
                            else:
                                self.current_player = self.player_1
                            for pile in self.piles:
                                for card in pile:
                                    card.texture = arcade.load_texture(FACE_DOWN_IMAGE)
                            self.on_draw()
                            game_view = SplashScreen(self, current_player=self.current_player, player_1=self.player_1,
                                                     player_2=self.player_2, rnd_end=False,
                                                     rnd_number=None, score_change_list=self.score_change_list,
                                                     player_1_score_box=self.player_1_score_box,
                                                     player_2_score_box=self.player_2_score_box,
                                                     piles=self.piles)
                            self.window.show_view(game_view)

                        self.has_drawn = False
                        self.has_discarded = False
                        self.buttons_pressed = []
                        self.completed_words_text_list = []
                        self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)




                    else:
                        pass

                elif self.go_down_button in self.buttons_pressed:
                    self.go_down_button.texture = arcade.load_texture(GO_DOWN)
                    if len(self.piles[GO_DOWN_PILE]) == 0 and len(self.piles[self.current_player.hand_index]) == 0:
                        self.current_player.has_gone_down = True

                        self.get_completed_words()
                        # for _ in range(len(self.piles[COMPLETED_CARDS])):
                        #     self.piles[COMPLETED_CARDS].pop()

                    else:
                        arcade.play_sound(WRONG_WORD_SOUND, volume=0.5)
                        logging.warning("You can't go down yet.")



                elif self.save_word_button in self.buttons_pressed:
                    self.save_word_button.texture = arcade.load_texture(SAVE_WORD)
                    self.save_word_sequence()

                elif self.recall_button in self.buttons_pressed:
                    self.recall_button.texture = arcade.load_texture(RECALL)
                    self.recall_sequence()

            elif self.buttons_pressed[0] == self.save_word_button:
                self.save_word_button.texture = arcade.load_texture(SAVE_WORD)
            elif self.buttons_pressed[0] == self.recall_button:
                self.recall_button.texture = arcade.load_texture(RECALL)
            elif self.buttons_pressed[0] == self.go_down_button:
                self.go_down_button.texture = arcade.load_texture(GO_DOWN)
            elif self.buttons_pressed[0] == self.next_turn_button:
                if self.has_discarded:
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)
                else:
                    pass
            elif self.buttons_pressed[0] == self.undo_button:
                self.undo_button.texture = arcade.load_texture(UNDO)



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
                        self.move_card_to_new_pile(card, GO_DOWN_PILE, self.held_cards_original_pile)
                        reset_position = False

                elif pile_index == GO_DOWN_PILE:
                    for card in self.held_cards:
                        self.move_card_to_new_pile(card, self.current_player.hand_index, self.held_cards_original_pile)
                        reset_position = False

                if pile_index == FACE_DOWN_PILE or pile_index == DISCARD_PILE:
                    if not self.has_drawn:
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, self.current_player.hand_index, self.held_cards_original_pile)
                            card.texture = arcade.load_texture(card.image_file_name)
                        self.has_drawn = True
                        self.drawn_card_original_pile = pile_index
                        self.last_move = self.moves
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
                            self.move_card_to_new_pile(card, DISCARD_PILE, self.held_cards_original_pile)
                        self.has_discarded = True
                        self.last_move = self.moves
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
                                    self.move_card_to_new_pile(self.held_cards[0], pile_index,
                                                               self.held_cards_original_pile)
                                    self.has_discarded = True
                                    self.last_move = self.moves
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
                                self.move_card_to_new_pile(card, pile_index, self.held_cards_original_pile)
                                reset_position = False

                        elif pile_index == PLAYER_1_HAND:

                            for card in self.held_cards:
                                self.move_card_to_new_pile(card, self.current_player.hand_index,
                                                           self.held_cards_original_pile)
                            reset_position = False

                elif self.held_cards_original_pile == FACE_DOWN_PILE or self.held_cards_original_pile == DISCARD_PILE:
                    if arcade.check_for_collision(self.held_cards[0], pile):
                        pile_index = self.pile_mat_list.index(pile)

                        if pile_index != PLAYER_1_HAND:
                            reset_position = True

                        else:
                            for card in self.held_cards:
                                self.move_card_to_new_pile(card, self.current_player.hand_index,
                                                           self.held_cards_original_pile)

                            self.has_drawn = True
                            self.drawn_card_original_pile = pile_index
                            self.last_move = self.moves
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
                            self.move_card_to_new_pile(card, self.current_player.hand_index,
                                                       self.held_cards_original_pile)
                        reset_position = False

                    elif pile_index == GO_DOWN_PILE:

                        letter = self.held_cards[0].value
                        self.go_down_text += letter
                        logging.warning(self.go_down_text)

                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index, self.held_cards_original_pile)

                        reset_position = False

            else:
                pass

            self.moves += 1

            if reset_position:
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, self.held_cards_original_pile, self.held_cards_original_pile)
                    # logging.warning(self.get_pile_for_card(self.held_cards[0]))



        self.held_cards = []



        self.buttons_pressed = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def get_small_go_down_card_position(self, index1, index2, current_player):
        x, y = 0, 0
        if current_player == self.player_1:
            x = (350 * self.scale) + (35 * self.scale * index2)
            y = (self.screen_height - 300 * self.scale) - (100 * self.scale * index1)
        elif current_player == self.player_2:
            x = (self.screen_width - (500 * self.scale) + (35 * self.scale * index2))
            y = (self.screen_height - 300 * self.scale) - (100 * self.scale * index1)
        return x, y

    def get_completed_words(self):
        if len(self.piles[COMPLETED_CARDS]) > self.rnd_hand_count:
            logging.warning("You need to have a discard.")
            self.recall_sequence()
        elif len(self.piles[COMPLETED_CARDS]) == 0 and len(self.piles[self.current_player.hand_index]) == 0:
            pass
        else:
            word_length_list = []
            current_score = 0
            small_go_down_list = []
            for index, word in enumerate(self.completed_words_text_list):
                word_length_list.append(len(word))
                for letter in word:
                    current_score += CARD_SCORE[letter]

            for index, word in enumerate(self.completed_words_card_list):
                small_go_down_list.append([])
                for completed_card in word:
                    small_card = Card(completed_card.value, scale=.75)
                    self.small_card_list.append(small_card)
                    small_go_down_list[index].append(small_card)
                    small_card.position = self.get_small_go_down_card_position(index,
                                                                         small_go_down_list[index].index(small_card),
                                                                         self.current_player)
                    self.pull_to_top(small_card, self.small_card_list)

            self.completed_words_card_list = []

            if len(self.piles[self.current_player.hand_index]) != 0:
                for card in self.piles[self.current_player.hand_index]:
                    current_score -= CARD_SCORE[card.value]
            logging.warning(current_score)
            self.current_player.total_score += current_score
            self.score_change_list.append([self.current_player, current_score, 0])

            if len(word_length_list) > 0:
                word_length_list.sort()
                self.current_player.longest_words[self.rnd] = word_length_list[-1]
            else:
                self.current_player.longest_words[self.rnd] = 0



            for _ in range(len(self.piles[COMPLETED_CARDS])):
                self.piles[COMPLETED_CARDS].pop()
        arcade.play_sound(GO_DOWN_SOUND, volume=0.2)

    def round_end_sequence(self):

        if self.player_1.longest_words[self.rnd] > self.player_2.longest_words[self.rnd]:
            current_score = 10
            self.player_1.total_score += 10

            for score_list in self.score_change_list:
                if self.player_1 in score_list:
                    score_list[1] += current_score
                else:
                    self.score_change_list.append([self.player_1, current_score, 0])
                    break



        elif self.player_1.longest_words[self.rnd] < self.player_2.longest_words[self.rnd]:
            current_score = 10
            self.player_2.total_score += 10

            for score_list in self.score_change_list:
                if self.player_2 in score_list:
                    score_list[1] += current_score
                else:
                    self.score_change_list.append([self.player_2, current_score, 0])
                    break

        if self.rnd < 8:
            self.rnd_hand_count += 1
        elif self.rnd > 8:
            self.rnd_hand_count -= 1

        self.rnd += 1

        self.buttons_pressed = []
        if self.rnd > self.rnd_max:
            game_view = GameEnd(player_1_score=self.player_1.total_score, player_2_score=self.player_2.total_score)
            self.window.show_view(game_view)
        else:
            if self.rnd % 2 == 1:
                self.current_player = self.player_1
                self.player_1_turn = True
            else:
                self.current_player = self.player_2
                self.player_1_turn = False
            game_view = SplashScreen(self, self.current_player, player_1=self.player_1, player_2=self.player_2,
                                     rnd_end=True, rnd_number=self.rnd, score_change_list=self.score_change_list,
                                     player_1_score_box=self.player_1_score_box,
                                     player_2_score_box=self.player_2_score_box,
                                     piles=self.piles)
            self.window.show_view(game_view)

            self.setup()

    def save_word_sequence(self):
        if len(self.go_down_text) > 1:
            if self.go_down_text in WORD_LIST:
                self.completed_words_card_list.append([])
                for i in range(len(self.piles[GO_DOWN_PILE])):
                    card = self.piles[GO_DOWN_PILE][0]
                    self.move_card_to_new_pile(card, COMPLETED_CARDS, GO_DOWN_PILE)
                    self.completed_words_card_list[-1].append(card)

                self.completed_words_text_list.append(self.go_down_text)
                arcade.play_sound(SAVE_WORD_SOUND)

                logging.warning(self.completed_words_text_list)

            else:
                print("Sorry, that's not a word. Dumbass.")
                arcade.play_sound(WRONG_WORD_SOUND, volume=0.5)
                for i in range(len(self.piles[GO_DOWN_PILE])):
                    card = self.piles[GO_DOWN_PILE][0]
                    self.move_card_to_new_pile(card, self.current_player.hand_index, GO_DOWN_PILE)

                self.go_down_text = ''

            self.go_down_text = ''


        else:
            print("Sorry, your word needs to be at least 2 letters long. Dumbass.")
            arcade.play_sound(WRONG_WORD_SOUND, volume=0.5)
            for card in self.piles[GO_DOWN_PILE]:
                self.move_card_to_new_pile(card, self.current_player.hand_index, GO_DOWN_PILE)
            self.go_down_text = ''

    def recall_sequence(self):
        if len(self.piles[COMPLETED_CARDS]) != 0:
            for _ in range(len(self.piles[COMPLETED_CARDS])):
                self.move_card_to_new_pile(self.piles[COMPLETED_CARDS][0], self.current_player.hand_index,
                                           COMPLETED_CARDS)

            arcade.play_sound(WRONG_WORD_SOUND, volume=0.5)
            self.completed_words_text_list = []
            self.completed_words_card_list = []


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

    def move_card_to_new_pile(self, card, pile_index, held_cards_original_pile):
        try:
            self.remove_card_from_pile(id(card))
        except:
            pass
        self.piles[pile_index].append(card)

        if held_cards_original_pile != pile_index:
            if pile_index == PLAYER_1_HAND or pile_index == PLAYER_2_HAND or pile_index == DISCARD_PILE or pile_index == GO_DOWN_PILE:
                arcade.play_sound(CARD_MOVE_SOUND)
        # logging.warning(self.get_pile_for_card(card))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.save_word_sequence()
        elif key == arcade.key.ESCAPE:
            self.recall_sequence()
        elif key == arcade.key.BACKSPACE:
            if len(self.piles[GO_DOWN_PILE]) > 0:
                self.move_card_to_new_pile(self.piles[GO_DOWN_PILE][-1], self.current_player.hand_index,
                                           GO_DOWN_PILE)

        elif key == arcade.key.F10:
            game_view = QuitScreen(self)
            self.window.show_view(game_view)

        elif key == arcade.key.DELETE:
            for card in self.card_list:
                card.texture = arcade.load_texture(FACE_DOWN_IMAGE)

    def on_text(self, text):


        for i in self.card_dict:

            if text.lower() in self.card_dict[i]:
                card_input: Card = i

                if card_input in self.piles[self.current_player.hand_index]:
                    self.move_card_to_new_pile(card_input, GO_DOWN_PILE, self.current_player.hand_index)
                    self.go_down_text += text
                    print(self.go_down_text)
                    break


class SplashScreen(arcade.View):

    def __init__(self, game_view, current_player, player_1, player_2, rnd_end, rnd_number, score_change_list, player_1_score_box, player_2_score_box, piles):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self. screen_height / 1080)
        self.game_view = game_view
        self.current_player = current_player
        self.rnd_end = rnd_end
        self.rnd_number = rnd_number
        self.score_change_list = score_change_list
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1_score_box = player_1_score_box
        self.player_2_score_box = player_2_score_box
        self.piles = piles

    def on_show(self):
        arcade.draw_rectangle_filled(
            self.screen_width / 2,
            self.screen_height / 2,
            400 * self.scale,
            300 * self.scale,
            (94, 123, 128, 300)
        )
        if self.rnd_end:
            arcade.draw_text(
                f'Round {self.rnd_number}',
                self.screen_width / 2,
                self.screen_height / 2 + 100 * self.scale,
                WHITE,
                font_size=round(40 * self.scale),
                anchor_x="center",
                anchor_y="center",
            )

            arcade.draw_text(
                f"{self.current_player}'s Turn.",
                self.screen_width / 2,
                self.screen_height / 2 - 100 * self.scale,
                WHITE,
                font_size=round(40 * self.scale),
                anchor_x="center",
                anchor_y="center",
            )
        else:
            arcade.draw_text(
                f"{self.current_player}'s Turn.",
                self.screen_width / 2,
                self.screen_height / 2,
                WHITE,
                font_size=round(40 * self.scale),
                anchor_x="center",
                anchor_y="center",
            )

        for score_list in self.score_change_list:
            x, y, color, prefix = 0, 0, None, None
            if score_list[0] == self.player_1:
                x, y = self.player_1_score_box['center_x'], self.player_1_score_box['center_y']
            elif score_list[0] == self.player_2:
                x, y = self.player_2_score_box['center_x'], self.player_2_score_box['center_y']

            if score_list[1] >= 0:
                color = arcade.color.GREEN
                prefix = '+'
            elif score_list[1] < 0:
                color = arcade.color.RED
                prefix = ''

            arcade.draw_text(
                f'{prefix}{score_list[1]}',
                x, y,
                color,
                font_size=round(24 * self.scale),
                anchor_x="center",
                anchor_y="center",
            )

        for pile in self.piles:
            for card in pile:
                card.texture = arcade.load_texture(FACE_DOWN_IMAGE)



    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for pile in self.piles[1:]:
            for card in pile:
                card.texture = arcade.load_texture(card.image_file_name)
        self.window.show_view(self.game_view)


class GameEnd(arcade.View):

    def __init__(self, player_1_score, player_2_score):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
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
                             self.screen_width / 2, self.screen_height - 100 * self.scale, WHITE, font_size=round(24 * self.scale), align="center",
                             anchor_x="center")
        elif self.draw:
            arcade.draw_text(f'Congratulations, Player 1 and Player 2 - you tied!\nA rematch must be had to determine who is the best Quiddler player!',
                self.screen_width / 2, self.screen_height - 100 * self.scale, WHITE, font_size=round(24 * self.scale), align="center",
                             anchor_x="center")
        arcade.draw_text(f'SCORES\n\nPlayer 1: {self.player_1_score}       Player 2: {self.player_2_score}',
                             self.screen_width / 2, self.screen_height - 400 * self.scale, WHITE, font_size=round(24 * self.scale), align="center",
                         anchor_x="center")
        arcade.draw_text("Would you like to play again?\nPress 'y' for yes, 'n' for no.",
                         self.screen_width / 2, self.screen_height - 700 * self.scale, WHITE, font_size=round(24 * self.scale), align="center",
                         anchor_x="center")

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.Y:
            game_view = GameMenu()
            self.window.show_view(game_view)
        elif key == arcade.key.N:
            arcade.close_window()



class GameMenu(arcade.View):

    def __init__(self):
        super().__init__()
        self.window.set_fullscreen(True)
        self.screen_width, self.screen_height = self.window.get_size()
        # self.screen_width, self.screen_height = self.screen_width * .8, self.screen_height * .8
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)

        self.background = arcade.Sprite(filename="images/quiddler_main_menu_background(2).png",
                                        scale=self.screen_width / BACKGROUND_IMAGE_WIDTH)
        self.background.position = self.screen_width / 2, self.screen_height / 2

        self.button_list = arcade.SpriteList()

        self.half_game_button = arcade.Sprite("images/half_game_button.png", scale=self.scale)
        self.half_game_button.position = self.screen_width / 2, self.screen_height / 2 - 100 * self.scale
        self.button_list.append(self.half_game_button)
        self.full_game_button = arcade.Sprite("images/full_game_button.png", scale=self.scale)
        self.full_game_button.position = self.screen_width / 2, self.screen_height / 2 - 200 * self.scale
        self.button_list.append(self.full_game_button)
        self.instructions_button = arcade.Sprite("images/instructions_button.png", scale=self.scale)
        self.instructions_button.position = self.screen_width / 2, self.screen_height / 2 - 300 * self.scale
        self.button_list.append(self.instructions_button)
        self.exit_button = arcade.Sprite(EXIT, scale=self.scale)
        self.exit_button.position = self.screen_width / 2, self.screen_height / 2 - 400 * self.scale
        self.button_list.append(self.exit_button)

        self.buttons_pressed = []

    def on_show(self):
        """ This is run once when we switch to this view """
        self.background.draw()
        self.button_list.draw()

        MAIN_MENU_MUSIC.play(volume=.25)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.background.draw()
        self.button_list.draw()

    def on_update(self, delta_time: float):
        if MAIN_MENU_MUSIC.is_complete():
            MAIN_MENU_MUSIC.play(volume=.25)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1 or symbol == arcade.key.NUM_1:
            game_view = Quiddler(rnd_number=8)
            game_view.setup()
            MAIN_MENU_MUSIC.stop()
            self.window.show_view(game_view)
        elif symbol == arcade.key.KEY_2 or symbol == arcade.key.NUM_2:
            game_view = Quiddler(rnd_number=16)
            game_view.setup()
            MAIN_MENU_MUSIC.stop()
            self.window.show_view(game_view)
        elif symbol == arcade.key.F10:
            arcade.close_window()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.buttons_pressed = arcade.get_sprites_at_point((x, y,), self.button_list)

            if self.half_game_button in self.buttons_pressed:
                self.half_game_button.texture = arcade.load_texture("images/half_game_button_pressed.png")
            elif self.full_game_button in self.buttons_pressed:
                self.full_game_button.texture = arcade.load_texture("images/full_game_button_pressed.png")
            elif self.instructions_button in self.buttons_pressed:
                self.instructions_button.texture = arcade.load_texture("images/instructions_button_pressed.png")
            elif self.exit_button in self.buttons_pressed:
                self.exit_button.texture = arcade.load_texture(EXIT_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):

        button = arcade.get_sprites_at_point((x, y), self.button_list)

        if button:
            if self.half_game_button in self.buttons_pressed:
                if self.half_game_button == button[0]:

                    game_view = Quiddler(rnd_number=8)
                    game_view.setup()
                    MAIN_MENU_MUSIC.stop()
                    self.window.show_view(game_view)

            elif self.full_game_button in self.buttons_pressed:
                if self.full_game_button == button[0]:
                    game_view = Quiddler(rnd_number=16)
                    game_view.setup()
                    MAIN_MENU_MUSIC.stop()
                    self.window.show_view(game_view)

            elif self.instructions_button in self.buttons_pressed:
                if self.instructions_button == button[0]:
                    pass

            elif self.exit_button in self.buttons_pressed:
                if self.exit_button == button[0]:
                    arcade.close_window()



        self.half_game_button.texture = arcade.load_texture("images/half_game_button.png")
        self.full_game_button.texture = arcade.load_texture("images/full_game_button.png")
        self.instructions_button.texture = arcade.load_texture("images/instructions_button.png")
        self.exit_button.texture = arcade.load_texture(EXIT)
        self.buttons_pressed = []


class QuitScreen(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)

    def on_show(self):
        arcade.draw_rectangle_filled(
            self.screen_width / 2,
            self.screen_height / 2,
            800 * self.scale,
            300 * self.scale,
            (94, 123, 128, 300)
        )

        arcade.draw_text(
            'Are you sure you want to quit?',
            start_x=self.screen_width / 2,
            start_y=self.screen_height / 2 + 50 * self.scale,
            color=WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )

        arcade.draw_text(
            "Press 'y' for yes, 'n' for no.",
            start_x=self.screen_width / 2,
            start_y=self.screen_height / 2 - 50 * self.scale,
            color=WHITE,
            font_size=round(32 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.Y:
            arcade.close_window()
        elif key == arcade.key.N:
            game_view = self.game_view
            self.window.show_view(game_view)


def main():
    window = arcade.Window(fullscreen=True, title="Quiddler")
    window.center_window()
    start_view = GameMenu()
    window.show_view(start_view)

    arcade.run()





if __name__ == "__main__":
    main()
