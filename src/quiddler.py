import logging
import shelve

from typing import List

import game_end
import pause_menu
import splash_screen
import player
import card_class
import card_utils
import computer_turn
from constants import *
from src import mats, player_manager, game_state_manager, card_manager, score_manager, score_change_object, \
    ui_manager

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class Quiddler(arcade.View):
    """
    Main application class.
    """

    def __init__(self, rnd_number: int, players: List[dict]):
        super().__init__()
        self.game_state_manager = game_state_manager.GameStateManager(rnd_number=rnd_number)
        self.card_manager = card_manager.CardManager()
        self.score_manager = score_manager.ScoreManager()

        # Initialize screen size and scale to be applied to screen elements
        screen_width, screen_height = self.window.get_size()
        self.ui_manager = ui_manager.UIManager(screen_width=screen_width, screen_height=screen_height)
        
        # Initialize players
        self.player_manager: player_manager.PlayerManager = player_manager.PlayerManager()
        self.player_manager.create_players(players=players)
        self.computer_turn = computer_turn.ComputerTurn()

        self.score_manager.score_dict = self.ui_manager.create_score_boxes(self.player_manager.player_list)

        # Initialize round variables
        self.button_list = None
        self.buttons_pressed = None
        self.pile_mat_list = None
        self.completed_words_text_list = []
        self.completed_words_card_list = []

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
        self.background = self.ui_manager.background
        self.sound_list = []
        self.sound_list.extend(SOUND_LIST)

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

        # Initialize timer values
        self.go_down_flash_timer = 0
        self.save_word_flash_timer = 0
        self.next_turn_flash_timer = 0
        self.go_down_flash_timer_change = -1
        self.save_word_flash_timer_change = -1
        self.next_turn_flash_timer_change = -1
        # List of buttons currently pressed
        self.buttons_pressed = []
        # Create a list of lists, each holds a pile of cards
        self.card_manager.piles = [[] for _ in range(PILE_COUNT)]

        self.create_sprite_lists()

        self.create_buttons()

        self.create_mats()

        # Create a card dictionary with Card keys assigned to letter values
        self.card_manager.card_dict = {}

        self.setup_cards()

        self.update_player_colors()

        # Reset player rnd_scores, has_gone_down
        self.player_manager.round_start_sequence(self.game_state_manager)

        # Flip all cards (except draw pile) face_up
        self.card_manager.round_start_sequence()

        self.game_state_manager.round_start_sequence()
                
        if self.player_manager.current_player.is_computer:
            self.take_computer_turn(self.player_manager.current_player)

    def setup_cards(self):
        self.card_manager.card_list, self.card_manager.card_dict = card_utils.create_cards(
            card_values=CARD_LIST,
            position=self.ui_manager.face_down_position,
            scale=self.ui_manager.scale
        )
        self.card_manager.card_list = card_utils.shuffle_cards(self.card_manager.card_list)
        # Put all the cards in the face down pile
        self.card_manager.piles[FACE_DOWN_PILE].extend(self.card_manager.card_list)
        # Create Both Player Hands
        for p in self.player_manager.player_list:
            self.deal_hand(p)
            self.get_hand_position(p)
        # Pop top card into discard pile
        self.card_manager.move_card_to_new_pile(self.card_manager.piles[FACE_DOWN_PILE][-1], DISCARD_PILE, FACE_DOWN_PILE)

    def deal_hand(self, cur_player: player):
        for _ in range(self.game_state_manager.rnd_hand_count):
            card = self.card_manager.piles[FACE_DOWN_PILE][-1]
            self.card_manager.move_card_to_new_pile(card, cur_player.hand_index, FACE_DOWN_PILE)

    def create_mats(self):
        # Create the mats for the face down and discard piles
        for i in range(len(OTHER_PILES) + 1):
            self.pile_mat_list.append(arcade.Sprite())
        self.pile_mat_list[FACE_DOWN_PILE] = mats.standard_pile_mat(self.ui_manager.scale)
        self.pile_mat_list[FACE_DOWN_PILE].position = self.ui_manager.face_down_position
        self.pile_mat_list[DISCARD_PILE] = mats.standard_pile_mat(self.ui_manager.scale)
        self.pile_mat_list[DISCARD_PILE].position = self.ui_manager.discard_position
        self.pile_mat_list[COMPLETED_CARDS] = mats.standard_pile_mat(self.ui_manager.scale)
        self.pile_mat_list[COMPLETED_CARDS].position = self.ui_manager.completed_card_position
        self.pile_mat_list[GO_DOWN_PILE] = mats.go_down_pile_mat(self.ui_manager.scale, self.ui_manager.screen_width)
        self.pile_mat_list[GO_DOWN_PILE].position = self.ui_manager.screen_width / 2, GO_DOWN_MAT_Y * self.ui_manager.scale
        self.pile_mat_list[PLAYER_PILE_MAT] = mats.player_hand_mat(self.ui_manager.scale, self.game_state_manager.rnd_hand_count)
        self.pile_mat_list[PLAYER_PILE_MAT].position = self.ui_manager.screen_width / 2, PLAYER_HAND_Y * self.ui_manager.scale

    def create_sprite_lists(self):
        # Create SpriteLists for each pile of cards
        self.card_manager.card_list = arcade.SpriteList()
        self.card_manager.small_card_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.card_manager.piles[FACE_DOWN_PILE] = arcade.SpriteList()
        self.card_manager.piles[DISCARD_PILE] = arcade.SpriteList()
        self.card_manager.piles[GO_DOWN_PILE] = arcade.SpriteList()
        for p in self.player_manager.player_list:
            self.card_manager.piles[p.hand_index] = arcade.SpriteList()
        self.card_manager.piles[COMPLETED_CARDS] = arcade.SpriteList()
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList(is_static=True)

    def create_buttons(self):
        # Create buttons -----------------------------------------------------------------------------------------------
        self.next_turn_button = arcade.Sprite(NEXT_TURN_PRESSED, self.ui_manager.scale)
        self.next_turn_button.center_x = self.ui_manager.screen_width - 150 * self.ui_manager.scale
        self.next_turn_button.center_y = BUTTON_Y * self.ui_manager.scale
        self.button_list.append(self.next_turn_button)
        self.go_down_button = arcade.Sprite(GO_DOWN, self.ui_manager.scale)
        self.go_down_button.center_x = self.ui_manager.screen_width / 2 + 150 * self.ui_manager.scale
        self.go_down_button.center_y = BUTTON_Y * self.ui_manager.scale
        self.button_list.append(self.go_down_button)
        self.save_word_button = arcade.Sprite(SAVE_WORD, self.ui_manager.scale)
        self.save_word_button.center_x = self.ui_manager.screen_width / 2 - 130 * self.ui_manager.scale
        self.save_word_button.center_y = BUTTON_Y * self.ui_manager.scale
        self.button_list.append(self.save_word_button)
        self.recall_button = arcade.Sprite(RECALL, self.ui_manager.scale)
        self.recall_button.center_x = 400 * self.ui_manager.scale
        self.recall_button.center_y = BUTTON_Y * self.ui_manager.scale
        self.button_list.append(self.recall_button)
        self.undo_button = arcade.Sprite(UNDO, self.ui_manager.scale)
        self.undo_button.center_x = 150 * self.ui_manager.scale
        self.undo_button.center_y = BUTTON_Y * self.ui_manager.scale
        self.button_list.append(self.undo_button)
        self.menu_button = arcade.Sprite(MENU, self.ui_manager.scale)
        self.menu_button.center_x = 150 * self.ui_manager.scale
        self.menu_button.center_y = self.ui_manager.screen_height - 50 * self.ui_manager.scale
        self.button_list.append(self.menu_button)

    def continue_game(self):
        """
        Load last saved game from file.
        """
        try:
            file = shelve.open('quiddler_saved_game', protocol=2)
            for i in range(1, len(self.player_manager.player_list) + 1):
                p: player.Player = self.player_manager.player_list[i]
                p.player_name = file[f'player_{i}_name']
                p.total_score = file[f'player_{i}_score']
                p.longest_words = file[f'player_{i}_longest_words']
                p.has_gone_down = file[f'player_{i}_has_gone_down']
            self.player_manager.current_player = self.player_manager.player_list[file['current_player']]
            self.game_state_manager.rnd = file['round']
            self.game_state_manager.rnd_max = file['total_rounds']
            self.game_state_manager.rnd_hand_count = file['total_cards']
            self.game_state_manager.has_drawn = file['has_drawn']
            self.game_state_manager.has_discarded = file['has_discarded']
            saved_piles = file['piles']
            self.card_manager.piles = [[] for _ in range(PILE_COUNT)]
            self.card_manager.piles[FACE_DOWN_PILE] = arcade.SpriteList()
            self.card_manager.piles[DISCARD_PILE] = arcade.SpriteList()
            self.card_manager.piles[GO_DOWN_PILE] = arcade.SpriteList()
            for p in self.player_manager.player_list:
                self.card_manager.piles[p.hand_index] = arcade.SpriteList()
            self.card_manager.piles[COMPLETED_CARDS] = arcade.SpriteList()
            self.card_manager.card_list = arcade.SpriteList()
            self.card_manager.card_dict = {}
            for index, pile in enumerate(saved_piles):
                for letter in pile:
                    print(f'saved_piles_letter: {index}{letter}')
                    card = card_class.Card(letter, scale=self.ui_manager.scale)
                    self.card_manager.card_list.append(card)
                    self.card_manager.card_dict[card] = letter
                    self.card_manager.piles[index].append(card)
            for i in range(2):
                pile = arcade.SpriteSolidColor(round(self.game_state_manager.rnd_hand_count * MAT_WIDTH * self.ui_manager.scale),
                                               round(MAT_HEIGHT * self.ui_manager.scale),
                                               (255, 255, 255, 10))
                pile.position = self.ui_manager.screen_width / 2, PLAYER_HAND_Y * self.ui_manager.scale
                self.pile_mat_list[i + 3] = pile
            file.close()
            self.get_all_card_positions()
        except:
            pass

    def get_all_card_positions(self):
        """
        Called when loading a game. Sets all cards to their correct position on the board.
        """
        for card in self.card_manager.piles[FACE_DOWN_PILE]:
            card.set_position(*self.ui_manager.face_down_position)
            card.flip_down()
        for card in self.card_manager.piles[DISCARD_PILE]:
            card.set_position(*self.ui_manager.discard_position)
        for card in self.card_manager.piles[COMPLETED_CARDS]:
            card.set_position(*self.ui_manager.completed_card_position)
        self.get_go_down_pile_position()
        for p in self.player_manager.player_list:
            self.get_hand_position(p)

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

    def get_clicked_pile(self, pile_mats: List[arcade.Sprite], x, y):
        """
        Sets 'cards' variable to only the cards in the selected pile.
        pile: List[Sprite]
        """
        cards = []
        for value in pile_mats:
            logging.debug(f'Pile #: {self.pile_mat_list.index(value)}')
        if len(pile_mats) > 1:
            pile_mats.remove(pile_mats[-1])
        if self.pile_mat_list.index(pile_mats[0]) == FACE_DOWN_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.card_manager.piles[FACE_DOWN_PILE])
        elif self.pile_mat_list.index(pile_mats[0]) == DISCARD_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.card_manager.piles[DISCARD_PILE])
        elif self.pile_mat_list.index(pile_mats[0]) == GO_DOWN_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.card_manager.piles[GO_DOWN_PILE])
        elif self.pile_mat_list.index(pile_mats[0]) == COMPLETED_CARDS:
            pass
        else:
            cards = arcade.get_sprites_at_point((x, y), self.card_manager.piles[self.player_manager.current_player.hand_index])
        return cards

    def get_completed_words(self, cur_player: player.Player):
        """
        Returns words saved into the completed words pile during a player's turn.
        """

        # Recalls cards if a player went down using their entire hand plus the discard.
        if len(self.card_manager.piles[COMPLETED_CARDS]) > self.game_state_manager.rnd_hand_count:
            self.recall_sequence()

        # Does nothing if completed cards pile and player hand are empty.
        elif len(self.card_manager.piles[COMPLETED_CARDS]) == 0 and len(self.card_manager.piles[cur_player.hand_index]) == 0:
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
                    small_card = card_class.Card(completed_card.value, scale=.75 * self.ui_manager.scale)
                    self.card_manager.small_card_list.append(small_card)
                    small_go_down_list[index].append(small_card)
                    small_card.position = self.get_small_go_down_card_position(
                        index,
                        small_go_down_list[index].index(small_card),
                        cur_player
                    )

            self.completed_words_card_list = []

            # Subtracts card values of unused cards from total score
            if len(self.card_manager.piles[cur_player.hand_index]) != 0:
                for card in self.card_manager.piles[cur_player.hand_index]:
                    current_score -= CARD_SCORE[card.value]
            # logging.warning(current_score)
            cur_player.total_score += current_score
            self.score_manager.score_change_list.append(
                score_change_object.ScoreChangeObject(
                    player=cur_player,
                    score=current_score,
                    timer=0
                )
            )

            # Get current player's longest word for the round
            if len(word_length_list) > 0:
                word_length_list.sort()
                cur_player.longest_words[self.game_state_manager.rnd] = word_length_list[-1]
            else:
                cur_player.longest_words[self.game_state_manager.rnd] = 0

            # Empty completed cards pile after score and words have been tabulated
            for _ in range(len(self.card_manager.piles[COMPLETED_CARDS])):
                self.card_manager.piles[COMPLETED_CARDS].pop()

    def get_go_down_pile_position(self):
        """
        Positions the cards in the center pile.
        """
        for i in range(len(self.card_manager.piles[GO_DOWN_PILE])):
            card = self.card_manager.piles[GO_DOWN_PILE][i]
            card.center_x = self.go_down_straight_line(i)
            card.center_y = GO_DOWN_MAT_Y * self.ui_manager.scale

    def get_hand_position(self, cur_player: player):
        """
        Positions the cards in the player's hand.
        """
        for i in range(len(self.card_manager.piles[cur_player.hand_index])):
            card = self.card_manager.piles[cur_player.hand_index][i]
            card.center_x = self.straight_line(i, cur_player.hand_index)
            card.center_y = PLAYER_HAND_Y * self.ui_manager.scale

    def get_high_scores(self):
        """
        Update high scores with current high score at the end of the game.
        """
        file = shelve.open('quiddler_high_scores', protocol=2)
        try:
            temp_score_list = file['scores']
        except KeyError:
            temp_score_list = []
        cur_high_score = ['', 0]
        for p in self.player_manager.player_list:
            if p.total_score > cur_high_score[1]:
                cur_high_score = [p.player_name, p.total_score]
        for i, score in enumerate(temp_score_list):
            if cur_high_score[1] >= score[1]:
                temp_score_list.insert(i, cur_high_score)
                break
        if len(temp_score_list) < 10:
            temp_score_list.append(cur_high_score)
        if len(temp_score_list) > 10:
            temp_score_list.pop()
        file['scores'] = temp_score_list
        file.close()

    def get_pile_for_card(self, card):
        """
        Returns pile index of card.
        """
        for index, pile in enumerate(self.card_manager.piles):
            if card in pile:
                return index

    def get_small_go_down_card_position(self, index1, index2, current_player: player.Player):
        """
        Positioning for completed cards display after a player has gone down.
        """
        x, y = 0, 0
        if current_player.player_number == 1:
            x = (350 * self.ui_manager.scale) + (35 * self.ui_manager.scale * index2)
            y = (self.ui_manager.screen_height - 300 * self.ui_manager.scale) - (100 * self.ui_manager.scale * index1)
        elif current_player.player_number == 2:
            x = (self.ui_manager.screen_width - (500 * self.ui_manager.scale) + (35 * self.ui_manager.scale * index2))
            y = (self.ui_manager.screen_height - 300 * self.ui_manager.scale) - (100 * self.ui_manager.scale * index1)
        return x, y

    def get_top_card(self, cards):
        """
        Selects only the topmost card in the UI, and ensures
        player isn't grabbing any cards from the other player's hand.
        """
        self.game_state_manager.held_cards = cards
        for card in self.game_state_manager.held_cards:
            if card in self.card_manager.piles[COMPLETED_CARDS]:
                self.game_state_manager.held_cards = []

        # Ensure player isn't grabbing cards from other player's hand
        if len(self.game_state_manager.held_cards) > 0:
            for i in range(len(self.game_state_manager.held_cards)):
                if i < len(self.game_state_manager.held_cards):
                    for p in self.player_manager.player_list:
                        if p != self.player_manager.current_player:
                            for card in self.card_manager.piles[p.hand_index]:
                                if id(self.game_state_manager.held_cards[i]) == id(card):
                                    self.game_state_manager.held_cards.remove(self.game_state_manager.held_cards[i])

            for _ in range(len(self.game_state_manager.held_cards) - 1):
                self.game_state_manager.held_cards.remove(self.game_state_manager.held_cards[0])

            pile = self.get_pile_for_card(self.game_state_manager.held_cards[0])
            self.game_state_manager.held_cards_original_pile: int = pile

            self.card_manager.piles[pile].remove(self.game_state_manager.held_cards[0])

    def go_down_straight_line(self, i):
        """
        Same as straight_line, used for center pile.
        """
        return 120 * self.ui_manager.scale * i - \
               (((len(self.card_manager.piles[GO_DOWN_PILE]) - 1) * 120 * self.ui_manager.scale) / 2) + self.ui_manager.screen_width / 2

    def handle_discard(self):
        """ Called when the player discards. """
        for card in self.game_state_manager.held_cards:
            self.card_manager.move_card_to_new_pile(card, DISCARD_PILE, self.game_state_manager.held_cards_original_pile)
        self.game_state_manager.has_discarded = True
        self.game_state_manager.last_move = self.game_state_manager.moves
        self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)

    def handle_go_down_button_click(self):
        """ Called when Go Down button is clicked and released. """
        self.go_down_button.texture = arcade.load_texture(GO_DOWN)
        if len(self.card_manager.piles[GO_DOWN_PILE]) == 0 and len(self.card_manager.piles[self.player_manager.current_player.hand_index]) == 0:
            self.player_manager.current_player.has_gone_down = True

            self.get_completed_words(self.player_manager.current_player)
            arcade.play_sound(GO_DOWN_SOUND, volume=0.3)

        else:
            arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)
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
        if self.game_state_manager.has_discarded:
            self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)

            if self.player_manager.is_round_final_turn():
                # Round end is called only if all players have gone down
                self.round_end_sequence()
                return
            
            self.card_manager.return_cards(cur_player=self.player_manager.current_player)
            self.turn_end_sequence()

        else:
            pass

    def turn_start_sequence(self):
        self.card_manager.turn_start_sequence()
        self.game_state_manager.turn_start_sequence()
        self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)

    def turn_end_sequence(self):
        self.player_manager.turn_end_sequence()
        self.card_manager.turn_end_sequence()
        self.buttons_pressed = []
        self.completed_words_text_list = []
        game_view = splash_screen.SplashScreen(
            self,
            current_player=self.player_manager.current_player,
            player_1=self.player_manager.player_list[0],
            player_2=self.player_manager.player_list[1],
            rnd_end=False,
            rnd_number=None,
            piles=self.card_manager.piles
        )
        self.window.show_view(game_view)

    def handle_undo_button_click(self):
        """ Called when Undo button is clicked and released. """
        if self.game_state_manager.moves == self.game_state_manager.last_move + 1:
            if self.game_state_manager.has_drawn and not self.game_state_manager.has_discarded:
                undo_card = self.card_manager.piles[self.player_manager.current_player.hand_index][-1]
                self.card_manager.move_card_to_new_pile(undo_card, self.game_state_manager.drawn_card_original_pile,
                                           self.game_state_manager.held_cards_original_pile)
                if self.game_state_manager.drawn_card_original_pile == FACE_DOWN_PILE:
                    undo_card.flip_down()
                self.game_state_manager.has_drawn = False
                arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)

            elif self.game_state_manager.has_discarded:
                undo_card = self.card_manager.piles[DISCARD_PILE][-1]
                self.card_manager.move_card_to_new_pile(undo_card, self.player_manager.current_player.hand_index, DISCARD_PILE)
                self.game_state_manager.has_discarded = False
                self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_PRESSED)
                arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)
        self.undo_button.texture = arcade.load_texture(UNDO)

    def on_draw(self):
        """
        Called when this view should draw.
        Overrides arcade.View.on_draw().
        """
        arcade.start_render()
        self.background.draw()

        # Draw cards/buttons
        self.button_list.draw()
        self.pile_mat_list.draw()
        for pile in self.player_manager.current_player.pile_numbers_list:
            self.card_manager.piles[pile].draw()
        for card in self.game_state_manager.held_cards:
            card.draw()
        self.card_manager.small_card_list.draw()

        # Draw Player Scores
        self.score_manager.draw_score_boxes()

        # Draw Round number
        arcade.draw_text(
            f"Round: {self.game_state_manager.rnd}",
            self.ui_manager.screen_width - 125 * self.ui_manager.scale,
            self.ui_manager.screen_height - 50 * self.ui_manager.scale,
            WHITE,
            font_size=round(40 * self.ui_manager.scale),
            anchor_x="center",
            anchor_y="center",
        )

        # Draw hand_count number
        arcade.draw_text(
            f"Cards: {self.game_state_manager.rnd_hand_count}",
            self.ui_manager.screen_width - 120 * self.ui_manager.scale,
            self.ui_manager.screen_height - 150 * self.ui_manager.scale,
            WHITE,
            font_size=round(40 * self.ui_manager.scale),
            anchor_x="center",
            anchor_y="center"
        )

        # Draw 'final turn' when other player has gone down
        if self.player_manager.is_players_final_turn():
            self.ui_manager.draw_final_turn_text()

    def on_key_press(self, key, modifiers):
        """
        Handles key presses that aren't letters.
        Events are triggered on key press, not key release.
        """
        if key == arcade.key.ENTER:

            if len(self.card_manager.piles[COMPLETED_CARDS]) == self.game_state_manager.rnd_hand_count and self.game_state_manager.has_discarded:
                self.handle_go_down_button_click()
            elif self.game_state_manager.has_discarded:
                self.handle_next_turn_button_click()
            else:
                self.save_word_sequence()

        elif key == arcade.key.ESCAPE:
            self.recall_sequence()

        elif key == arcade.key.BACKSPACE:
            if len(self.card_manager.piles[GO_DOWN_PILE]) > 0:
                self.card_manager.move_card_to_new_pile(
                    self.card_manager.piles[GO_DOWN_PILE][-1],
                    self.player_manager.current_player.hand_index,
                    GO_DOWN_PILE
                )

        elif key == arcade.key.F10:
            game_view = pause_menu.PauseMenu(self, sound_list=self.sound_list, sound_player=self.sound_player)
            self.window.show_view(game_view)

        elif key == arcade.key.DELETE:
            for card in self.card_manager.card_list:
                card.flip_down()

        elif key == arcade.key.LSHIFT:
            if not self.game_state_manager.has_drawn:
                self.draw_card(DISCARD_PILE)

        elif key == arcade.key.SPACE:
            if not self.game_state_manager.has_drawn:
                self.draw_card(FACE_DOWN_PILE)
                
            elif not self.game_state_manager.has_discarded:
                if len(self.card_manager.piles[PLAYER_1_HAND]) == 1:
                    card = self.card_manager.piles[PLAYER_1_HAND][0]
                    self.card_manager.move_card_to_new_pile(card, DISCARD_PILE, self.game_state_manager.held_cards_original_pile)
                    self.game_state_manager.has_discarded = True
                    self.game_state_manager.last_move = self.game_state_manager.moves
                    self.game_state_manager.moves += 1
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)

    def draw_card(self, pile_index: int):
        card = self.card_manager.piles[pile_index][-1]
        self.card_manager.move_card_to_new_pile(
            card,
            self.player_manager.current_player.hand_index,
            self.game_state_manager.held_cards_original_pile
        )
        card.flip_up()
        self.game_state_manager.has_drawn = True
        self.game_state_manager.drawn_card_original_pile = pile_index
        self.game_state_manager.last_move = self.game_state_manager.moves
        self.game_state_manager.moves += 1

    def on_key_release(self, _key: int, _modifiers: int):
        if _key == arcade.key.ENTER:
            if self.player_manager.current_player.is_computer:
                self.handle_next_turn_button_click()
                return

    def on_mouse_motion(self, x, y, dx: float, dy: float):
        """
        Logic for tracking card movement with mouse movement.
        Utilizes delta x and delta y to compute new card position.
        """
        for card in self.game_state_manager.held_cards:
            card.center_x += dx
            card.center_y += dy

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Collects sprites at point of mouse press.
        Does not track which button is pressed.
        """
        pile_mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)
        buttons = arcade.get_sprites_at_point((x, y), self.button_list)
        cards = []

        if pile_mats:
            cards = self.get_clicked_pile(pile_mats, x, y)

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

        if self.player_manager.current_player.is_computer:
            self.handle_next_turn_button_click()
            return

        # Check if any cards are held or buttons are pressed
        if len(self.game_state_manager.held_cards) == 0 and len(self.buttons_pressed) == 0:
            return

        self.handle_buttons_on_mouse_release(x, y)
        self.handle_cards_on_mouse_release(button)

        # Resets cards held and buttons pressed after all logic is accounted for.
        self.game_state_manager.held_cards = []
        self.buttons_pressed = []

    def handle_cards_on_mouse_release(self, button):
        if len(self.game_state_manager.held_cards) > 0 and len(self.buttons_pressed) == 0:
            reset_position = True

            if button == arcade.MOUSE_BUTTON_LEFT:
                pile_index = self.game_state_manager.held_cards_original_pile

                if pile_index == self.player_manager.current_player.hand_index:
                    for card in self.game_state_manager.held_cards:
                        self.card_manager.move_card_to_new_pile(
                            card,
                            GO_DOWN_PILE,
                            self.game_state_manager.held_cards_original_pile
                        )
                        reset_position = False

                elif pile_index == GO_DOWN_PILE:
                    for card in self.game_state_manager.held_cards:
                        self.card_manager.move_card_to_new_pile(
                            card,
                            self.player_manager.current_player.hand_index,
                            self.game_state_manager.held_cards_original_pile
                        )
                        reset_position = False

                if pile_index == FACE_DOWN_PILE or pile_index == DISCARD_PILE:
                    if not self.game_state_manager.has_drawn:
                        for card in self.game_state_manager.held_cards:
                            self.card_manager.move_card_to_new_pile(
                                card,
                                self.player_manager.current_player.hand_index,
                                self.game_state_manager.held_cards_original_pile
                            )
                            card.flip_up()
                        self.game_state_manager.has_drawn = True
                        self.game_state_manager.drawn_card_original_pile = pile_index
                        self.game_state_manager.last_move = self.game_state_manager.moves
                        reset_position = False
                else:
                    pass

            elif button == arcade.MOUSE_BUTTON_RIGHT:
                pile_index = self.game_state_manager.held_cards_original_pile

                if pile_index != self.player_manager.current_player.hand_index:
                    pass

                elif pile_index == self.player_manager.current_player.hand_index:
                    if not self.game_state_manager.has_drawn or self.game_state_manager.has_discarded:
                        pass

                    elif self.game_state_manager.has_drawn:
                        self.handle_discard()
                        reset_position = False

            else:
                pass

            # Keeps track of moves for Undo button purposes.
            self.game_state_manager.moves += 1

            # Resets card position if an illegal move was made.
            if reset_position:
                for card in self.game_state_manager.held_cards:
                    self.card_manager.move_card_to_new_pile(
                        card,
                        self.game_state_manager.held_cards_original_pile,
                        self.game_state_manager.held_cards_original_pile
                    )

    def handle_buttons_on_mouse_release(self, x, y):
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
                if self.game_state_manager.has_discarded:
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)
                else:
                    pass
            elif self.buttons_pressed[0] == self.undo_button:
                self.undo_button.texture = arcade.load_texture(UNDO)

    def on_text(self, text):
        """
        Handles key presses that are letters.
        Used for typing letters into the center pile when creating words.
        """
        for i in self.card_manager.card_dict:

            # Get best matching card Sprite for keyboard input
            if text.lower() in self.card_manager.card_dict[i]:
                card_input: card_class.Card = i

                if card_input in self.card_manager.piles[self.player_manager.current_player.hand_index]:
                    self.card_manager.move_card_to_new_pile(
                        card_input,
                        GO_DOWN_PILE,
                        self.player_manager.current_player.hand_index
                    )
                    self.go_down_text += text
                    # print(self.go_down_text)
                    break

    def on_update(self, delta_time):
        """
        Update card positions every 1/60 second based on the card's pile.
        """

        # Update card positions
        for card in self.card_manager.piles[FACE_DOWN_PILE]:
            card.position = self.ui_manager.face_down_position
        for card in self.card_manager.piles[DISCARD_PILE]:
            card.position = self.ui_manager.discard_position
        for card in self.card_manager.piles[COMPLETED_CARDS]:
            card.position = self.ui_manager.completed_card_position
        self.get_go_down_pile_position()
        self.get_hand_position(self.player_manager.current_player)

        # Handle text in go_down pile
        text = ''
        for card in self.card_manager.piles[GO_DOWN_PILE]:
            text += self.card_manager.card_dict[card]
        self.go_down_text = text

        self.score_manager.update()

        # Handle which buttons should be flashing based on turn state
        if len(self.card_manager.piles[GO_DOWN_PILE]) < 2:
            self.save_word_flash_timer = 0
            self.save_word_flash_timer_change = -1
            self.save_word_button.texture = arcade.load_texture(SAVE_WORD)

        if len(self.card_manager.piles[COMPLETED_CARDS]) == self.game_state_manager.rnd_hand_count and self.game_state_manager.has_discarded:
            if self.go_down_button not in self.buttons_pressed:
                if self.go_down_flash_timer >= 30:
                    self.go_down_button.texture = arcade.load_texture(GO_DOWN)
                    self.go_down_flash_timer_change = -self.go_down_flash_timer_change
                elif self.go_down_flash_timer <= 0:
                    self.go_down_button.texture = arcade.load_texture(GO_DOWN_FLASH)
                    self.go_down_flash_timer_change = -self.go_down_flash_timer_change
                self.go_down_flash_timer += self.go_down_flash_timer_change

        elif len(self.card_manager.piles[GO_DOWN_PILE]) > 1:
            if self.save_word_button not in self.buttons_pressed:
                if self.save_word_flash_timer >= 30:
                    self.save_word_button.texture = arcade.load_texture(SAVE_WORD)
                    self.save_word_flash_timer_change = -self.save_word_flash_timer_change
                elif self.save_word_flash_timer <= 0:
                    self.save_word_button.texture = arcade.load_texture(SAVE_WORD_FLASH)
                    self.save_word_flash_timer_change = -self.save_word_flash_timer_change
                self.save_word_flash_timer += self.save_word_flash_timer_change

        elif self.player_manager.current_player.has_gone_down:
            if self.next_turn_button not in self.buttons_pressed:
                if self.next_turn_flash_timer >= 30:
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN)
                    self.next_turn_flash_timer_change = -self.next_turn_flash_timer_change
                elif self.next_turn_flash_timer <= 0:
                    self.next_turn_button.texture = arcade.load_texture(NEXT_TURN_FLASH)
                    self.next_turn_flash_timer_change = -self.next_turn_flash_timer_change
                self.next_turn_flash_timer += self.next_turn_flash_timer_change

    def update_player_colors(self):
        """Update player box color based on player turn"""
        for p in self.player_manager.player_list:
            if p == self.player_manager.current_player:
                p.color = GOLD_TRANSPARENT
            else:
                p.color = WHITE_TRANSPARENT

    def recall_sequence(self):
        """
        Called when cards are to be recalled to the player's hand
        from the completed cards pile when Recall button is pressed.
        """

        # Check that completed cards pile isn't empty
        if len(self.card_manager.piles[COMPLETED_CARDS]) != 0:
            for _ in range(len(self.card_manager.piles[COMPLETED_CARDS])):
                self.card_manager.move_card_to_new_pile(
                    self.card_manager.piles[COMPLETED_CARDS][0],
                    self.player_manager.current_player.hand_index,
                    COMPLETED_CARDS
                )
            arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)
            self.completed_words_text_list = []
            self.completed_words_card_list = []

    def round_end_sequence(self):
        """
        Called at the end of the round.
        Calculates scores, bonuses, and resets state variables for the next round
        before calling setup().
        """
        self.player_manager.round_end_sequence()
        self.game_state_manager.round_end_sequence()
        self.card_manager.round_end_sequence()

        if len(self.card_manager.piles[COMPLETED_CARDS]) != 0 \
                or len(self.card_manager.piles[self.player_manager.current_player.hand_index]) != 0:
            self.get_completed_words(self.player_manager.current_player)
        self.determine_highest_score()
        # Reset buttons_pressed
        self.buttons_pressed = []

        # If game is over, call game_end sequence
        if self.game_state_manager.rnd > self.game_state_manager.rnd_max:
            self.game_end_sequence()

        # Else, reset the board for the next round, with the dealer rotating to the next player
        else:
            self.player_manager.set_round_start_player(self.game_state_manager)
            game_view = splash_screen.SplashScreen(
                self,
                self.player_manager.current_player,
                player_1=self.player_manager.player_list[0],
                player_2=self.player_manager.player_list[1],
                rnd_end=True,
                rnd_number=self.game_state_manager.rnd,
                piles=self.card_manager.piles
            )
            self.window.show_view(game_view)

            self.setup()

    def game_end_sequence(self):
        self.get_high_scores()
        self.background_music.stop(self.sound_player)
        game_view = game_end.GameEnd(player_1_name=self.player_manager.player_list[0].player_name,
                                     player_1_score=self.player_manager.player_list[0].total_score,
                                     player_2_name=self.player_manager.player_list[1].player_name,
                                     player_2_score=self.player_manager.player_list[1].total_score, )
        self.window.show_view(game_view)

    def determine_highest_score(self):
        cur_high_score: int = 0
        player_to_get_bonus: player.Player = None
        for p in self.player_manager.player_list:
            if p.longest_words[self.game_state_manager.rnd] > cur_high_score:
                player_to_get_bonus = p
        if player_to_get_bonus:
            self.score_manager.add_bonus_to_score(player_to_get_bonus)

    def save_game(self):
        """
        Save variable states to a file for future loading.
        """
        file = shelve.open('quiddler_saved_game', protocol=2)
        for p in self.player_manager.player_list:
            i = p.player_number
            file[f'player_{i}_name'] = p.player_name
            file[f'player_{i}_score'] = p.total_score
            file[f'player_{i}_longest_words'] = p.longest_words
            file[f'player_{i}_has_gone_down'] = p.has_gone_down
        file['current_player'] = self.player_manager.current_player.hand_index
        file['round'] = self.game_state_manager.rnd
        file['total_rounds'] = self.game_state_manager.rnd_max
        file['total_cards'] = self.game_state_manager.rnd_hand_count
        file['has_drawn'] = self.game_state_manager.has_drawn
        file['has_discarded'] = self.game_state_manager.has_discarded
        new_piles = [[] for _ in range(PILE_COUNT)]
        for index, pile in enumerate(self.card_manager.piles):
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
                for _ in range(len(self.card_manager.piles[GO_DOWN_PILE])):
                    card = self.card_manager.piles[GO_DOWN_PILE][0]
                    self.card_manager.move_card_to_new_pile(
                        card,
                        COMPLETED_CARDS,
                        GO_DOWN_PILE
                    )
                    self.completed_words_card_list[-1].append(card)

                self.completed_words_text_list.append(self.go_down_text)
                arcade.play_sound(SAVE_WORD_SOUND)

                # logging.warning(self.completed_words_text_list)

            # Else, return cards to player hand
            else:
                arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)
                for _ in range(len(self.card_manager.piles[GO_DOWN_PILE])):
                    card = self.card_manager.piles[GO_DOWN_PILE][0]
                    self.card_manager.move_card_to_new_pile(
                        card,
                        self.player_manager.current_player.hand_index,
                        GO_DOWN_PILE
                    )

                self.go_down_text = ''

            self.go_down_text = ''

        # Return cards to player hand if the word is too short
        else:
            arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)
            for card in self.card_manager.piles[GO_DOWN_PILE]:
                self.card_manager.move_card_to_new_pile(
                    card,
                    self.player_manager.current_player.hand_index,
                    GO_DOWN_PILE
                )
            self.go_down_text = ''

    def straight_line(self, i, current_player_hand):
        """
        Math for spacing the cards out evenly.
        """
        return 110 * self.ui_manager.scale * i - \
               ((((len(self.card_manager.piles[current_player_hand])) - 1) * 110 * self.ui_manager.scale) / 2) + self.ui_manager.screen_width / 2

    def take_computer_turn(self, computer_player: player.Player):
        if not self.player_manager.is_players_final_turn():
            self.card_manager.piles[FACE_DOWN_PILE], self.card_manager.piles[DISCARD_PILE], self.card_manager.piles[computer_player.hand_index], result = \
                self.computer_turn.take_turn(self.card_manager.piles[FACE_DOWN_PILE], self.card_manager.piles[DISCARD_PILE],
                                             self.card_manager.piles[computer_player.hand_index], False)
        else:
            self.card_manager.piles[FACE_DOWN_PILE], self.card_manager.piles[DISCARD_PILE], self.card_manager.piles[computer_player.hand_index], result = \
                self.computer_turn.take_turn(self.card_manager.piles[FACE_DOWN_PILE], self.card_manager.piles[DISCARD_PILE],
                                             self.card_manager.piles[computer_player.hand_index], True)
        self.game_state_manager.has_drawn = True
        self.game_state_manager.has_discarded = True
        logging.debug(f'valid hand: {result}')
        if result:
            self.completed_words_card_list = result
            for card in self.card_manager.piles[computer_player.hand_index]:
                self.card_manager.move_card_to_new_pile(card, COMPLETED_CARDS, self.card_manager.piles[computer_player.hand_index])
            for word in result:
                w = ""
                for card in word:
                    w += card.value
                self.completed_words_text_list.append(w)
            self.get_completed_words(self.player_manager.current_player)
            computer_player.has_gone_down = True






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

