import arcade
import random
import logging
import shelve

import game_menu
import game_end
import pause_menu
import splash_screen
import player
import card_class
import computer_turn
from constants import *


class QuiddlerSolo(arcade.View):
    """
    Main application class.
    """

    def __init__(self, rnd_number, player_1):
        super().__init__()

        # Initialize screen size and scale to be applied to screen elements
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)

        # Apply positions based on scale
        self.face_down_position_x, self.face_down_position_y = \
            (self.screen_width / 2) - 70 * self.scale, self.screen_height - self.screen_height / 4
        self.discard_position_x, self.discard_position_y = \
            (self.screen_width / 2) + 70 * self.scale, self.screen_height - self.screen_height / 4
        self.completed_card_position_x, self.completed_card_position_y = \
            150 * self.scale, self.screen_height - 250 * self.scale
        self.player_score_box = {
            'center_x': (self.screen_width / 2) - 450 * self.scale,
            'center_y': self.screen_height - 125 * self.scale,
            'width': 400 * self.scale,
            'height': 200 * self.scale
        }
        self.computer_score_box = {
            'center_x': (self.screen_width / 2) + 450 * self.scale,
            'center_y': self.screen_height - 125 * self.scale,
            'width': 400 * self.scale,
            'height': 200 * self.scale
        }

        # Initialize players
        self.player_list = []
        self.player = player.Player(player_name=player_1)
        self.player.hand_index = S_PLAYER_HAND
        self.player.pile_numbers_list = [0, 1, 2, 3, 5]
        self.player.color = WHITE_TRANSPARENT
        self.player_list.append(self.player)
        self.computer = player.Player(player_name="Computer")
        self.computer.hand_index = S_COMPUTER_HAND
        self.computer.pile_numbers_list = [0, 1, 2, 4, 5]
        self.computer.color = WHITE_TRANSPARENT
        self.player_list.append(self.computer)

        self.computer_turn = computer_turn.ComputerTurn()

        # Initialize round variables
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
        self.player_turn = None
        self.card_dict = None
        self.pile_mat_list = None
        self.has_drawn = False
        self.has_discarded = False
        self.completed_words_text_list = []
        self.completed_words_card_list = []
        self.card_input_original_position = None
        self.drawn_card_original_pile = None
        self.held_cards_original_pile = None
        self.moves = None
        self.last_move = None
        self.score_change_list = None
        self.current_player = None

        # Initialize buttons
        self.next_turn_button = None
        self.go_down_button = None
        self.save_word_button = None
        self.recall_button = None
        self.undo_button = None
        self.menu_button = None

        # Text string representing letters in the go_down pile.
        self.go_down_text = None

        # Timers for flashing buttons
        self.go_down_flash_timer = None
        self.save_word_flash_timer = None
        self.next_turn_flash_timer = None
        self.go_down_flash_timer_change = None
        self.save_word_flash_timer_change = None
        self.next_turn_flash_timer_change = None

        # Initialize background and sound
        self.background = None
        self.sound_list = []
        self.card_move_sound = CARD_MOVE_SOUND
        self.sound_list.append(self.card_move_sound)
        self.save_word_sound = SAVE_WORD_SOUND
        self.sound_list.append(self.save_word_sound)
        self.go_down_sound = GO_DOWN_SOUND
        self.sound_list.append(self.go_down_sound)
        self.wrong_word_sound = WRONG_WORD_SOUND
        self.sound_list.append(self.wrong_word_sound)

        self.background_music = BACKGROUND_MUSIC
        self.sound_player = None

        # Start playing background music
        self.sound_player = self.background_music.play(volume=.50, loop=True)

    def setup(self):
        """
        Initializes values for piles, hands.
        Called after initialization and after every round.
        """

        # Holds letters currently in the center pile
        self.go_down_text = ''

        # Holds words saved in the completed words pile, so that the original
        # word groupings are maintained for determining the longest word
        self.completed_words_text_list = []

        # Used to track number of moves taken when trying to use Undo feature
        self.moves = 0
        self.last_move = 0

        # List of scores that are animated above each player
        # whenever their score changes
        self.score_change_list = []

        # Initialize timer values
        self.go_down_flash_timer = 0
        self.save_word_flash_timer = 0
        self.next_turn_flash_timer = 0
        self.go_down_flash_timer_change = -1
        self.save_word_flash_timer_change = -1
        self.next_turn_flash_timer_change = -1

        # List of cards we're dragging with the mouse
        self.held_cards = []
        # List of buttons currently pressed
        self.buttons_pressed = []
        # Original location of cards we are dragging
        self.held_cards_original_position = []
        # Create a list of lists, each holds a pile of cards
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Create SpriteLists for each pile of cards
        self.card_list = arcade.SpriteList()
        self.small_card_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.piles[FACE_DOWN_PILE] = arcade.SpriteList()
        self.piles[DISCARD_PILE] = arcade.SpriteList()
        self.piles[GO_DOWN_PILE] = arcade.SpriteList()
        self.piles[S_PLAYER_HAND] = arcade.SpriteList()
        self.piles[S_COMPUTER_HAND] = arcade.SpriteList()
        self.piles[COMPLETED_CARDS] = arcade.SpriteList()

        # Create buttons -----------------------------------------------------------------------------------------------
        self.next_turn_button = arcade.Sprite(NEXT_TURN_PRESSED, self.scale)
        self.next_turn_button.center_x = self.screen_width - 150 * self.scale
        self.next_turn_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.next_turn_button)

        self.go_down_button = arcade.Sprite(GO_DOWN, self.scale)
        self.go_down_button.center_x = self.screen_width / 2 + 150 * self.scale
        self.go_down_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.go_down_button)

        self.save_word_button = arcade.Sprite(SAVE_WORD, self.scale)
        self.save_word_button.center_x = self.screen_width / 2 - 130 * self.scale
        self.save_word_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.save_word_button)

        self.recall_button = arcade.Sprite(RECALL, self.scale)
        self.recall_button.center_x = 400 * self.scale
        self.recall_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.recall_button)

        self.undo_button = arcade.Sprite(UNDO, self.scale)
        self.undo_button.center_x = 150 * self.scale
        self.undo_button.center_y = BUTTON_Y * self.scale
        self.button_list.append(self.undo_button)

        self.menu_button = arcade.Sprite(MENU, self.scale)
        self.menu_button.center_x = 150 * self.scale
        self.menu_button.center_y = self.screen_height - 50 * self.scale
        self.button_list.append(self.menu_button)

        # Create a card dictionary with Card keys assigned to letter values
        self.card_dict = {}

        # Create sprite list with all the mats
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the face down and discard piles
        pile = arcade.SpriteSolidColor(
            round(MAT_WIDTH * self.scale),
            round(MAT_HEIGHT * self.scale),
            (255, 255, 255, 40)
        )
        pile.position = self.face_down_position_x, self.face_down_position_y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(
            round(MAT_WIDTH * self.scale),
            round(MAT_HEIGHT * self.scale),
            (255, 255, 255, 40)
        )
        pile.position = self.discard_position_x, self.discard_position_y
        self.pile_mat_list.append(pile)

        # Create mat for going down
        pile = arcade.SpriteSolidColor(
            self.screen_width,
            round(MAT_HEIGHT * self.scale),
            (255, 255, 0, 1)
        )
        pile.position = self.screen_width / 2, GO_DOWN_MAT_Y * self.scale
        self.pile_mat_list.append(pile)

        # Create mat for the player hands
        for _ in range(2):
            pile = arcade.SpriteSolidColor(
                round(self.rnd_hand_count * MAT_WIDTH * self.scale),
                round(MAT_HEIGHT * self.scale),
                (255, 255, 255, 10)
            )
            pile.position = self.screen_width / 2, PLAYER_HAND_Y * self.scale
            self.pile_mat_list.append(pile)

        # Create mat for completed cards
        pile = arcade.SpriteSolidColor(
            round(MAT_WIDTH * self.scale),
            round(MAT_HEIGHT * self.scale),
            (255, 255, 255, 40)
        )
        pile.position = self.completed_card_position_x, self.completed_card_position_y
        self.pile_mat_list.append(pile)

        # Create every card, both regular and small versions
        # Small cards are used to display a player's completed words
        # after they go down
        for value in CARD_LIST:
            card = card_class.Card(value, self.scale)
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
        for _ in range(self.rnd_hand_count):
            card = self.piles[FACE_DOWN_PILE].pop()
            self.piles[S_PLAYER_HAND].append(card)

        for _ in range(self.rnd_hand_count):
            card = self.piles[FACE_DOWN_PILE].pop()
            self.piles[S_COMPUTER_HAND].append(card)

        # Position card in each hand
        for i in range(len(self.piles[S_PLAYER_HAND])):
            card = self.piles[S_PLAYER_HAND][i]
            card.center_x = self.straight_line(i, S_PLAYER_HAND)
            card.center_y = PLAYER_HAND_Y * self.scale

        for i in range(len(self.piles[S_COMPUTER_HAND])):
            card = self.piles[S_COMPUTER_HAND][i]
            card.center_x = self.straight_line(i, S_COMPUTER_HAND)
            card.center_y = PLAYER_HAND_Y * self.scale

        # Pop top card into discard pile
        discard = self.piles[FACE_DOWN_PILE].pop()
        self.piles[DISCARD_PILE].append(discard)

        # Initiate player turn, depending on rnd
        if self.rnd % 2 == 1:
            self.current_player = self.player
            self.player_turn = True
        else:
            self.current_player = self.computer
            self.player_turn = False

        # Initialize round-state variables
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

        self.background = arcade.Sprite(
            filename="images/quiddler_background_large(2).png",
            scale=self.screen_width / BACKGROUND_IMAGE_WIDTH
        )
        self.background.position = self.screen_width / 2, self.screen_height / 2

        if self.current_player == self.computer:
            self.take_computer_turn()

    def add_bonus_to_score(self, cur_player: player.Player):
        """ Adds longest word bonus to player's round score. """
        bonus = 10
        cur_player.total_score += bonus
        for score_list in self.score_change_list:
            if cur_player in score_list:
                score_list[1] += bonus
            else:
                self.score_change_list.append([cur_player, bonus, 0])
                break

    def continue_game(self):
        """
        Load last saved game from file.
        """
        try:
            file = shelve.open('quiddler_saved_game', protocol=2)
            self.player.player_name = file['player_1_name']
            self.player.total_score = file['player_1_score']
            self.player.longest_words = file['player_1_longest_words']
            self.player.has_gone_down = file['player_1_has_gone_down']

            self.computer.player_name = file['player_2_name']
            self.computer.total_score = file['player_2_score']
            self.computer.longest_words = file['player_2_longest_words']
            self.computer.has_gone_down = file['player_1_has_gone_down']
            self.player_turn = file['player_1_turn']
            if self.player_turn:
                self.current_player = self.player
            else:
                self.current_player = self.computer
            self.rnd = file['round']
            self.rnd_max = file['total_rounds']
            self.rnd_hand_count = file['total_cards']
            self.has_drawn = file['has_drawn']
            self.has_discarded = file['has_discarded']
            saved_piles = file['piles']
            self.piles = [[] for _ in range(PILE_COUNT)]
            self.piles[FACE_DOWN_PILE] = arcade.SpriteList()
            self.piles[DISCARD_PILE] = arcade.SpriteList()
            self.piles[GO_DOWN_PILE] = arcade.SpriteList()
            self.piles[S_PLAYER_HAND] = arcade.SpriteList()
            self.piles[S_COMPUTER_HAND] = arcade.SpriteList()
            self.piles[COMPLETED_CARDS] = arcade.SpriteList()
            self.card_list = arcade.SpriteList()
            self.card_dict = {}
            for index, pile in enumerate(saved_piles):
                for letter in pile:
                    print(f'saved_piles_letter: {index}{letter}')
                    card = card_class.Card(letter, scale=self.scale)
                    self.card_list.append(card)
                    self.card_dict[card] = letter
                    self.piles[index].append(card)
            for i in range(2):
                pile = arcade.SpriteSolidColor(round(self.rnd_hand_count * MAT_WIDTH * self.scale),
                                               round(MAT_HEIGHT * self.scale),
                                               (255, 255, 255, 10))
                pile.position = self.screen_width / 2, PLAYER_HAND_Y * self.scale
                self.pile_mat_list[i + 3] = pile
            file.close()
            self.get_all_card_positions()
        except:
            pass

    def get_all_card_positions(self):
        """
        Called when loading a game. Sets all cards to their correct position on the board.
        """
        for card in self.piles[FACE_DOWN_PILE]:
            card.center_x, card.center_y = self.face_down_position_x, self.face_down_position_y
            card.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        for card in self.piles[DISCARD_PILE]:
            card.center_x, card.center_y = self.discard_position_x, self.discard_position_y
        for card in self.piles[COMPLETED_CARDS]:
            card.center_x, card.center_y = self.completed_card_position_x, self.completed_card_position_y
        self.get_go_down_pile_position()
        self.get_hand_position()

    def get_buttons_pressed(self, buttons):
        """ Gets buttons pressed, and updates button UI accordingly. """
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
        elif self.menu_button in self.buttons_pressed:
            self.menu_button.texture = arcade.load_texture(MENU_PRESSED)

    def get_clicked_pile(self, pile, x, y):
        """
        Sets 'cards' variable to only the cards in the selected pile.
        pile: List[Sprite]
        """
        cards = []
        for value in pile:
            logging.debug(f'Pile #: {self.pile_mat_list.index(value)}')
        if len(pile) > 1:
            pile.remove(pile[-1])
        if self.pile_mat_list.index(pile[0]) == FACE_DOWN_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.piles[FACE_DOWN_PILE])
        elif self.pile_mat_list.index(pile[0]) == DISCARD_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.piles[DISCARD_PILE])
        elif self.pile_mat_list.index(pile[0]) == S_PLAYER_HAND or pile == S_COMPUTER_HAND:
            cards = arcade.get_sprites_at_point((x, y), self.piles[self.current_player.hand_index])
        elif self.pile_mat_list.index(pile[0]) == GO_DOWN_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.piles[GO_DOWN_PILE])
        elif self.pile_mat_list.index(pile[0]) == COMPLETED_CARDS:
            pass
        return cards

    def get_completed_words(self):
        """
        Returns words saved into the completed words pile during a player's turn.
        """

        # Recalls cards if a player went down using their entire hand plus the discard.
        if len(self.piles[COMPLETED_CARDS]) > self.rnd_hand_count:
            self.recall_sequence()

        # Does nothing if completed cards pile and player hand are empty.
        elif len(self.piles[COMPLETED_CARDS]) == 0 and len(self.piles[self.current_player.hand_index]) == 0 and self.current_player == self.player:
            pass
        else:

            # Calculate total score of cards in completed cards pile
            word_length_list = []
            current_score = 0
            small_go_down_list = []
            for word in self.completed_words_text_list:
                word_length_list.append(len(word))
                for letter in word:
                    current_score += CARD_SCORE[letter]

            # Display each word under the player using small card images
            for index, word in enumerate(self.completed_words_card_list):
                small_go_down_list.append([])
                for completed_card in word:
                    small_card = card_class.Card(completed_card.value, scale=.75 * self.scale)
                    self.small_card_list.append(small_card)
                    small_go_down_list[index].append(small_card)
                    small_card.position = self.get_small_go_down_card_position(
                        index,
                        small_go_down_list[index].index(small_card),
                        self.current_player
                    )

            self.completed_words_card_list = []

            # Subtracts card values of unused cards from total score
            if len(self.piles[self.current_player.hand_index]) != 0:
                for card in self.piles[self.current_player.hand_index]:
                    current_score -= CARD_SCORE[card.value]
            # logging.warning(current_score)
            self.current_player.total_score += current_score
            self.score_change_list.append([self.current_player, current_score, 0])

            # Get current player's longest word for the round
            if len(word_length_list) > 0:
                word_length_list.sort()
                self.current_player.longest_words[self.rnd] = word_length_list[-1]
            else:
                self.current_player.longest_words[self.rnd] = 0

            # Empty completed cards pile after score and words have been tabulated
            for _ in range(len(self.piles[COMPLETED_CARDS])):
                self.piles[COMPLETED_CARDS].pop()

    def get_go_down_pile_position(self):
        """
        Positions the cards in the center pile.
        """
        for i in range(len(self.piles[GO_DOWN_PILE])):
            card = self.piles[GO_DOWN_PILE][i]
            card.center_x = self.go_down_straight_line(i)
            card.center_y = GO_DOWN_MAT_Y * self.scale

    def get_hand_position(self):
        """
        Positions the cards in the player's hand.
        """
        for i in range(len(self.piles[S_PLAYER_HAND])):
            card = self.piles[S_PLAYER_HAND][i]
            card.center_x = self.straight_line(i, S_PLAYER_HAND)
            card.center_y = PLAYER_HAND_Y * self.scale

        for i in range(len(self.piles[S_COMPUTER_HAND])):
            card = self.piles[S_COMPUTER_HAND][i]
            card.center_x = self.straight_line(i, S_COMPUTER_HAND)
            card.center_y = PLAYER_HAND_Y * self.scale

    def get_high_scores(self):
        """
        Update high scores with current high score at the end of the game.
        """
        file = shelve.open('quiddler_high_scores', protocol=2)
        try:
            temp_score_list = file['scores']
        except KeyError:
            temp_score_list = []
        if self.player.total_score > self.computer.total_score:
            temp_score_list.append([self.player.player_name, self.player.total_score])
        elif self.computer.total_score > self.player.total_score:
            temp_score_list.append([self.computer.player_name, self.computer.total_score])
        if len(temp_score_list) > 10:
            temp_score_list.pop()
        file['scores'] = temp_score_list
        file.close()

    def get_pile_for_card(self, card):
        """
        Returns pile index of card.
        """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def get_small_go_down_card_position(self, index1, index2, current_player):
        """
        Positioning for completed cards display after a player has gone down.
        """
        x, y = 0, 0
        if current_player == self.player:
            x = (350 * self.scale) + (35 * self.scale * index2)
            y = (self.screen_height - 300 * self.scale) - (100 * self.scale * index1)
        elif current_player == self.computer:
            x = (self.screen_width - (500 * self.scale) + (35 * self.scale * index2))
            y = (self.screen_height - 300 * self.scale) - (100 * self.scale * index1)
        return x, y

    def get_top_card(self, cards):
        """
        Selects only the topmost card in the UI, and ensures
        player isn't grabbing any cards from the other player's hand.
        """
        self.held_cards = cards
        for card in self.held_cards:
            if card in self.piles[COMPLETED_CARDS]:
                self.held_cards = []

        # Ensure player isn't grabbing cards from other player's hand
        if len(self.held_cards) > 0:
            if self.current_player == self.player:
                for i in range(len(self.held_cards)):
                    if i < len(self.held_cards):
                        for card in self.piles[S_COMPUTER_HAND]:
                            if id(self.held_cards[i]) == id(card):
                                self.held_cards.remove(self.held_cards[i])

            for _ in range(len(self.held_cards) - 1):
                self.held_cards.remove(self.held_cards[0])

            pile = self.get_pile_for_card(self.held_cards[0])
            self.held_cards_original_pile: int = pile

            self.piles[pile].remove(self.held_cards[0])

    def go_down_straight_line(self, i):
        """
        Same as straight_line, used for center pile.
        """
        return 120 * self.scale * i - \
               (((len(self.piles[GO_DOWN_PILE]) - 1) * 120 * self.scale) / 2) + self.screen_width / 2

    def handle_discard(self):
        """ Called when the player discards. """
        for card in self.held_cards:
            self.move_card_to_new_pile(card, DISCARD_PILE, self.held_cards_original_pile)
        self.has_discarded = True
        self.last_move = self.moves
        self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)

    def handle_go_down_button_click(self):
        """ Called when Go Down button is clicked and released. """
        self.go_down_button.texture = arcade.load_texture(GO_DOWN)
        if len(self.piles[GO_DOWN_PILE]) == 0 and len(self.piles[self.current_player.hand_index]) == 0:
            self.current_player.has_gone_down = True

            self.get_completed_words()
            arcade.play_sound(self.go_down_sound, volume=0.3)

        else:
            arcade.play_sound(self.wrong_word_sound, volume=0.2)
            logging.warning("You can't go down yet.")

    def handle_menu_button_click(self):
        """ Called when menu button is clicked and released. """
        self.menu_button.texture = arcade.load_texture(MENU)
        game_view = pause_menu.PauseMenu(
            game_view=self,
            sound_list=self.sound_list,
            sound_player=self.sound_player
        )
        self.window.show_view(game_view)

    def handle_next_turn_button_click(self):
        """ Called when Next Turn button is clicked and released. """
        rnd_end = False
        if self.has_discarded:
            self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)

            if self.player_turn and self.computer.has_gone_down \
                    or not self.player_turn and self.player.has_gone_down:

                # Round end is called only if both players have gone down
                self.current_player.has_gone_down = True
                if len(self.piles[COMPLETED_CARDS]) != 0 \
                        or len(self.piles[self.current_player.hand_index]) != 0:
                    self.get_completed_words()
                rnd_end = True
                self.round_end_sequence()

            if len(self.piles[COMPLETED_CARDS]) != 0:
                for _ in range(len(self.piles[COMPLETED_CARDS])):
                    self.move_card_to_new_pile(
                        self.piles[COMPLETED_CARDS][0],
                        self.current_player.hand_index,
                        COMPLETED_CARDS
                    )
            if len(self.piles[GO_DOWN_PILE]) != 0:
                for _ in range(len(self.piles[GO_DOWN_PILE])):
                    self.move_card_to_new_pile(
                        self.piles[GO_DOWN_PILE][0],
                        self.current_player.hand_index,
                        GO_DOWN_PILE
                    )

            if not rnd_end:
                self.player_turn = not self.player_turn
                if not self.player_turn:
                    self.current_player = self.computer
                else:
                    self.current_player = self.player
                for pile in self.piles:
                    for card in pile:
                        card.texture = arcade.load_texture(FACE_DOWN_IMAGE)
                game_view = splash_screen.SplashScreen(
                    self,
                    current_player=self.current_player,
                    player_1=self.player,
                    player_2=self.computer,
                    rnd_end=False,
                    rnd_number=None,
                    score_change_list=self.score_change_list,
                    player_1_score_box=self.player_score_box,
                    player_2_score_box=self.computer_score_box,
                    piles=self.piles
                )
                self.window.show_view(game_view)

            self.has_drawn = False
            self.has_discarded = False
            self.buttons_pressed = []
            self.completed_words_text_list = []
            self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)

            # if not self.player_turn:
            #     self.take_computer_turn()

        else:
            pass

    def handle_undo_button_click(self):
        """ Called when Undo button is clicked and released. """
        if self.moves == self.last_move + 1:
            if self.has_drawn and not self.has_discarded:
                undo_card = self.piles[self.current_player.hand_index][-1]
                self.move_card_to_new_pile(undo_card, self.drawn_card_original_pile,
                                           self.held_cards_original_pile)
                if self.drawn_card_original_pile == FACE_DOWN_PILE:
                    undo_card.texture = arcade.load_texture(FACE_DOWN_IMAGE)
                self.has_drawn = False
                arcade.play_sound(self.wrong_word_sound, volume=0.2)

            elif self.has_discarded:
                undo_card = self.piles[DISCARD_PILE][-1]
                self.move_card_to_new_pile(undo_card, self.current_player.hand_index, DISCARD_PILE)
                self.has_discarded = False
                self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)
                arcade.play_sound(self.wrong_word_sound, volume=0.2)
        self.undo_button.texture = arcade.load_texture(UNDO)

    def move_card_to_new_pile(self, card, pile_index, held_cards_original_pile):
        """
        Handles movement of a card from one pile to another,
        ensuring the sprite is never in two piles at once.
        """
        try:
            self.remove_card_from_pile(id(card))
        except:
            pass
        self.piles[pile_index].append(card)

        if held_cards_original_pile != pile_index:
            if pile_index == S_PLAYER_HAND or pile_index == S_COMPUTER_HAND \
                    or pile_index == DISCARD_PILE or pile_index == GO_DOWN_PILE:
                arcade.play_sound(self.card_move_sound, volume=0.5)

    def on_draw(self):
        """
        Called when this view should draw.
        Overrides arcade.View.on_draw().
        """
        arcade.start_render()
        self.background.draw()

        # Draw player score boxes
        arcade.draw_rectangle_filled(
            center_x=self.player_score_box['center_x'],
            center_y=self.player_score_box['center_y'],
            width=self.player_score_box['width'],
            height=self.player_score_box['height'],
            color=self.player.color
        )
        arcade.draw_rectangle_filled(
            center_x=self.computer_score_box['center_x'],
            center_y=self.computer_score_box['center_y'],
            width=self.computer_score_box['width'],
            height=self.computer_score_box['height'],
            color=self.computer.color
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
            f'{self.player}',
            self.player_score_box['center_x'],
            self.player_score_box['center_y'] + 50 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            f'{self.player.total_score}',
            self.player_score_box['center_x'],
            self.player_score_box['center_y'] - 50 * self.scale,
            WHITE,
            font_size=round(24 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            f'{self.computer}',
            self.computer_score_box['center_x'],
            self.computer_score_box['center_y'] + 50 * self.scale,
            WHITE,
            font_size=round(40 * self.scale),
            anchor_x="center",
            anchor_y="center",
        )
        arcade.draw_text(
            f'{self.computer.total_score}',
            self.computer_score_box['center_x'],
            self.computer_score_box['center_y'] - 50 * self.scale,
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
        if self.player_turn:
            if self.computer.has_gone_down:
                arcade.draw_text(
                    "Final Turn!",
                    self.screen_width - 150 * self.scale,
                    100 * self.scale,
                    arcade.color.GOLD,
                    font_size=round(24 * self.scale),
                    anchor_x="center"
                )

        elif not self.player_turn:
            if self.player.has_gone_down:
                arcade.draw_text(
                    "Final Turn!",
                    self.screen_width - 150 * self.scale,
                    100 * self.scale,
                    arcade.color.GOLD,
                    font_size=round(24 * self.scale),
                    anchor_x="center"
                )

        # Draw score-change animations
        for score_list in self.score_change_list:
            x, y, color, prefix = 0, 0, None, None
            if score_list[0] == self.player:
                x, y = self.player_score_box['center_x'], self.player_score_box['center_y']
            elif score_list[0] == self.computer:
                x, y = self.computer_score_box['center_x'], self.computer_score_box['center_y']

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

    def on_key_press(self, key, modifiers):
        """
        Handles key presses that aren't letters.
        Events are triggered on key press, not key release.
        """
        if key == arcade.key.ENTER:

            if len(self.piles[COMPLETED_CARDS]) == self.rnd_hand_count and self.has_discarded:
                self.handle_go_down_button_click()
            elif self.has_discarded:
                self.handle_next_turn_button_click()
            else:
                self.save_word_sequence()

        elif key == arcade.key.ESCAPE:
            self.recall_sequence()

        elif key == arcade.key.BACKSPACE:
            if len(self.piles[GO_DOWN_PILE]) > 0:
                self.move_card_to_new_pile(
                    self.piles[GO_DOWN_PILE][-1],
                    self.current_player.hand_index,
                    GO_DOWN_PILE
                )

        elif key == arcade.key.F10:
            game_view = pause_menu.PauseMenu(self, sound_list=self.sound_list, sound_player=self.sound_player)
            self.window.show_view(game_view)

        elif key == arcade.key.DELETE:
            for card in self.card_list:
                card.texture = arcade.load_texture(FACE_DOWN_IMAGE)

        elif key == arcade.key.LSHIFT:
            if not self.has_drawn:
                card = self.piles[DISCARD_PILE][-1]
                self.move_card_to_new_pile(
                    card,
                    self.current_player.hand_index,
                    self.held_cards_original_pile
                )
                card.texture = arcade.load_texture(card.image_file_name)
                self.has_drawn = True
                self.drawn_card_original_pile = DISCARD_PILE
                self.last_move = self.moves
                self.moves += 1

        elif key == arcade.key.SPACE:
            if not self.has_drawn:
                card = self.piles[FACE_DOWN_PILE][-1]
                self.move_card_to_new_pile(
                    card,
                    self.current_player.hand_index,
                    self.held_cards_original_pile
                )
                card.texture = arcade.load_texture(card.image_file_name)
                self.has_drawn = True
                self.drawn_card_original_pile = FACE_DOWN_PILE
                self.last_move = self.moves
                self.moves += 1
            elif not self.has_discarded:
                if len(self.piles[PLAYER_1_HAND]) == 1:
                    card = self.piles[PLAYER_1_HAND][0]
                    self.move_card_to_new_pile(card, DISCARD_PILE, self.held_cards_original_pile)
                    self.has_discarded = True
                    self.last_move = self.moves
                    self.moves += 1
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)

    def on_key_release(self, _key: int, _modifiers: int):
        if _key == arcade.key.ENTER:
            if not self.player_turn:
                self.handle_next_turn_button_click()
                return

    def on_mouse_motion(self, x, y, dx: float, dy: float):
        """
        Logic for tracking card movement with mouse movement.
        Utilizes delta x and delta y to compute new card position.
        """
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Collects sprites at point of mouse press.
        Does not track which button is pressed.
        """
        pile = arcade.get_sprites_at_point((x, y), self.pile_mat_list)
        buttons = arcade.get_sprites_at_point((x, y), self.button_list)
        cards = []

        if pile:
            cards = self.get_clicked_pile(pile, x, y)

        # Get only top card of pile
        if len(cards) > 0:
            self.get_top_card(cards)

        # Get buttons pressed
        if len(buttons) > 0:
            self.get_buttons_pressed(buttons)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """
        Handles events on mouse release. Button/card events are triggered here instead of
        on_mouse_press().
        """

        if not self.player_turn:
            self.handle_next_turn_button_click()
            return

        # Check if any cards are held or buttons are pressed
        if len(self.held_cards) == 0 and len(self.buttons_pressed) == 0:
            return

        # Handle buttons -----------------------------------------------------------------------------------------------

        if len(self.buttons_pressed) > 0:

            # Ensure mouse is still over the same button that was pressed when mouse is released.
            buttons = arcade.get_sprites_at_point((x, y), self.button_list)
            if self.buttons_pressed == buttons:

                # Call methods for each button.
                if self.menu_button in self.buttons_pressed:
                    self.handle_menu_button_click()

                elif self.undo_button in self.buttons_pressed:
                    self.handle_undo_button_click()
                elif self.next_turn_button in self.buttons_pressed:
                    self.handle_next_turn_button_click()

                elif self.go_down_button in self.buttons_pressed:
                    self.handle_go_down_button_click()

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

        # Handle cards -------------------------------------------------------------------------------------------------

        if len(self.held_cards) > 0 and len(self.buttons_pressed) == 0:
            reset_position = True

            if button == arcade.MOUSE_BUTTON_LEFT:
                pile_index = self.held_cards_original_pile

                if pile_index == self.current_player.hand_index:
                    for card in self.held_cards:
                        self.move_card_to_new_pile(
                            card,
                            GO_DOWN_PILE,
                            self.held_cards_original_pile
                        )
                        reset_position = False

                elif pile_index == GO_DOWN_PILE:
                    for card in self.held_cards:
                        self.move_card_to_new_pile(
                            card,
                            self.current_player.hand_index,
                            self.held_cards_original_pile
                        )
                        reset_position = False

                if pile_index == FACE_DOWN_PILE or pile_index == DISCARD_PILE:
                    if not self.has_drawn:
                        for card in self.held_cards:
                            self.move_card_to_new_pile(
                                card,
                                self.current_player.hand_index,
                                self.held_cards_original_pile
                            )
                            card.texture = arcade.load_texture(card.image_file_name)
                        self.has_drawn = True
                        self.drawn_card_original_pile = pile_index
                        self.last_move = self.moves
                        reset_position = False
                else:
                    pass

            elif button == arcade.MOUSE_BUTTON_RIGHT:
                pile_index = self.held_cards_original_pile

                if pile_index != self.current_player.hand_index:
                    pass

                elif pile_index == self.current_player.hand_index:
                    if not self.has_drawn or self.has_discarded:
                        pass

                    elif self.has_drawn:
                        self.handle_discard()
                        reset_position = False

            else:
                pass

            # Keeps track of moves for Undo button purposes.
            self.moves += 1

            # Resets card position if an illegal move was made.
            if reset_position:
                for card in self.held_cards:
                    self.move_card_to_new_pile(
                        card,
                        self.held_cards_original_pile,
                        self.held_cards_original_pile
                    )

        # Resets cards held and buttons pressed after all logic is accounted for.
        self.held_cards = []
        self.buttons_pressed = []

    def on_text(self, text):
        """
        Handles key presses that are letters.
        Used for typing letters into the center pile when creating words.
        """
        for i in self.card_dict:

            # Get best matching card Sprite for keyboard input
            if text.lower() in self.card_dict[i]:
                card_input: card_class.Card = i

                if card_input in self.piles[self.current_player.hand_index]:
                    self.move_card_to_new_pile(
                        card_input,
                        GO_DOWN_PILE,
                        self.current_player.hand_index
                    )
                    self.go_down_text += text
                    # print(self.go_down_text)
                    break

    def on_update(self, delta_time):
        """
        Update card positions every 1/60 second based on the card's pile.
        """

        # Update card positions
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
        if self.player_turn:
            self.player.color = GOLD_TRANSPARENT
            self.computer.color = WHITE_TRANSPARENT
        elif not self.player_turn:
            self.player.color = WHITE_TRANSPARENT
            self.computer.color = GOLD_TRANSPARENT

    def recall_sequence(self):
        """
        Called when cards are to be recalled to the player's hand
        from the completed cards pile when Recall button is pressed.
        """

        # Check that completed cards pile isn't empty
        if len(self.piles[COMPLETED_CARDS]) != 0:
            for _ in range(len(self.piles[COMPLETED_CARDS])):
                self.move_card_to_new_pile(
                    self.piles[COMPLETED_CARDS][0],
                    self.current_player.hand_index,
                    COMPLETED_CARDS
                )
            arcade.play_sound(self.wrong_word_sound, volume=0.2)
            self.completed_words_text_list = []
            self.completed_words_card_list = []

    def remove_card_from_pile(self, card_id):
        """
        Removes card from its pile.
        """
        for pile in self.piles:
            for card in pile:
                if id(card) == card_id:
                    pile.remove(card)
                    break

    def round_end_sequence(self):
        """
        Called at the end of the round.
        Calculates scores, bonuses, and resets state variables for the next round
        before calling setup().
        """

        # Determine which player gets bonus for longest word
        if self.player.longest_words[self.rnd] > self.computer.longest_words[self.rnd]:
            self.add_bonus_to_score(cur_player=self.player)
        elif self.player.longest_words[self.rnd] < self.computer.longest_words[self.rnd]:
            self.add_bonus_to_score(cur_player=self.computer)

        # Determines whether the hand count should increase or decrease
        # depending on whether the game is in the first half or last half
        if self.rnd < 8:
            self.rnd_hand_count += 1
        elif self.rnd > 8:
            self.rnd_hand_count -= 1

        # Increase round number
        self.rnd += 1
        # Reset buttons_pressed
        self.buttons_pressed = []

        # If game is over, call game_end sequence
        if self.rnd > self.rnd_max:
            self.get_high_scores()
            self.background_music.stop(self.sound_player)
            game_view = game_end.GameEnd(player_1_name=self.player.player_name,
                                         player_1_score=self.player.total_score,
                                         player_2_name=self.computer.player_name,
                                         player_2_score=self.computer.total_score,)
            self.window.show_view(game_view)

        # Else, reset the board for the next round, with the dealer rotating to the next player
        else:
            if self.rnd % 2 == 1:
                self.current_player = self.player
                self.player_turn = True
            else:
                self.current_player = self.computer
                self.player_turn = False
            game_view = splash_screen.SplashScreen(
                self,
                self.current_player,
                player_1=self.player,
                player_2=self.computer,
                rnd_end=True,
                rnd_number=self.rnd,
                score_change_list=self.score_change_list,
                player_1_score_box=self.player_score_box,
                player_2_score_box=self.computer_score_box,
                piles=self.piles
            )
            self.window.show_view(game_view)

            self.setup()

    def save_game(self):
        """
        Save variable states to a file for future loading.
        """
        file = shelve.open('quiddler_saved_game', protocol=2)
        file['player_1_name'] = self.player.player_name
        file['player_1_score'] = self.player.total_score
        file['player_1_longest_words'] = self.player.longest_words
        file['player_1_has_gone_down'] = self.player.has_gone_down
        file['player_2_name'] = self.computer.player_name
        file['player_2_score'] = self.computer.total_score
        file['player_2_longest_words'] = self.computer.longest_words
        file['player_2_has_gone_down'] = self.computer.has_gone_down
        file['player_1_turn'] = self.player_turn
        file['round'] = self.rnd
        file['total_rounds'] = self.rnd_max
        file['total_cards'] = self.rnd_hand_count
        file['has_drawn'] = self.has_drawn
        file['has_discarded'] = self.has_discarded
        new_piles = [[] for _ in range(PILE_COUNT)]
        for index, pile in enumerate(self.piles):
            for card in pile:
                new_piles[index].append(card.value)
        print(new_piles)
        file['piles'] = new_piles
        file.close()

    def save_word_sequence(self):
        """
        Called when a player attempts to save a word from the center pile
        to the completed cards pile.
        """

        # Check that the word is at least two letters long
        if len(self.go_down_text) > 1:

            # If word is valid, move it to completed cards pile
            # and empty out the center pile
            if self.go_down_text in WORD_LIST:
                self.completed_words_card_list.append([])
                for _ in range(len(self.piles[GO_DOWN_PILE])):
                    card = self.piles[GO_DOWN_PILE][0]
                    self.move_card_to_new_pile(
                        card,
                        COMPLETED_CARDS,
                        GO_DOWN_PILE
                    )
                    self.completed_words_card_list[-1].append(card)

                self.completed_words_text_list.append(self.go_down_text)
                arcade.play_sound(self.save_word_sound)

                # logging.warning(self.completed_words_text_list)

            # Else, return cards to player hand
            else:
                arcade.play_sound(self.wrong_word_sound, volume=0.2)
                for _ in range(len(self.piles[GO_DOWN_PILE])):
                    card = self.piles[GO_DOWN_PILE][0]
                    self.move_card_to_new_pile(
                        card,
                        self.current_player.hand_index,
                        GO_DOWN_PILE
                    )

                self.go_down_text = ''

            self.go_down_text = ''

        # Return cards to player hand if the word is too short
        else:
            arcade.play_sound(self.wrong_word_sound, volume=0.2)
            for card in self.piles[GO_DOWN_PILE]:
                self.move_card_to_new_pile(
                    card,
                    self.current_player.hand_index,
                    GO_DOWN_PILE
                )
            self.go_down_text = ''

    def straight_line(self, i, current_player_hand):
        """
        Math for spacing the cards out evenly.
        """
        return 110 * self.scale * i - \
               ((((len(self.piles[current_player_hand])) - 1) * 110 * self.scale) / 2) + self.screen_width / 2

    def take_computer_turn(self):
        if not self.player.has_gone_down:
            self.piles[FACE_DOWN_PILE], self.piles[DISCARD_PILE], self.piles[S_COMPUTER_HAND], result = \
                self.computer_turn.take_turn(self.piles[FACE_DOWN_PILE], self.piles[DISCARD_PILE],
                                             self.piles[S_COMPUTER_HAND], False)
        else:
            self.piles[FACE_DOWN_PILE], self.piles[DISCARD_PILE], self.piles[S_COMPUTER_HAND], result = \
                self.computer_turn.take_turn(self.piles[FACE_DOWN_PILE], self.piles[DISCARD_PILE],
                                             self.piles[S_COMPUTER_HAND], True)
        self.has_drawn = True
        self.has_discarded = True
        if result:
            self.completed_words_card_list = result
            for card in self.piles[S_COMPUTER_HAND]:
                self.move_card_to_new_pile(card, COMPLETED_CARDS, self.piles[S_COMPUTER_HAND])
            for word in result:
                w = ""
                for card in word:
                    w += card.value
                self.completed_words_text_list.append(w)
            self.get_completed_words()
            self.computer.has_gone_down = True






def get_player_names(filename):
    file = shelve.open(filename=filename, protocol=2)
    try:
        player_1 = file['player_1']
        player_2 = file['player_2']
    except KeyError:
        player_1 = 'Player 1'
        player_2 = 'Player 2'
        file['player_1'] = player_1
        file['player_2'] = player_2
    file.close()
    return player_1, player_2

