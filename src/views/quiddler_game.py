import logging
import shelve

from typing import List

from src.views import game_end, pause_menu
from arcade.gui import UIManager
import src.views.splash_screen
import src.utils.player as player
import src.utils.card_class as card_class
import src.utils.computer_turn as computer_turn
from src.utils.constants import *
from src.managers import button_manager, card_manager, game_state_manager, manager_handler, player_manager, score_manager, screen_manager

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class Quiddler(arcade.View):
    """
    Main application class.
    """

    def __init__(self, rnd_number: int, players: List[dict]):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        self.manager_handler = manager_handler.ManagerHandler()

        self.game_state_manager = game_state_manager.GameStateManager(game_view=self, rnd_number=rnd_number)
        self.manager_handler.add(self.game_state_manager)
        self.score_manager = score_manager.ScoreManager(game_view=self)
        self.manager_handler.add(self.score_manager)

        # Initialize screen size and scale to be applied to screen elements
        screen_width, screen_height = self.window.get_size()
        self.screen_manager = screen_manager.ScreenManager(
            game_view=self,
            screen_width=screen_width,
            screen_height=screen_height
        )
        self.manager_handler.add(self.screen_manager)
        self.button_manager = button_manager.ButtonManager(game_view=self, screen_manager=self.screen_manager)
        self.manager_handler.add(self.button_manager)
        
        # Initialize players
        self.player_manager: player_manager.PlayerManager = player_manager.PlayerManager(game_view=self)
        self.manager_handler.add(self.player_manager)
        self.player_manager.create_players(players=players)
        self.card_manager = card_manager.CardManager(game_view=self, player_list=self.player_manager.player_list)
        self.manager_handler.add(self.card_manager)
        self.computer_turn = computer_turn.ComputerTurn()

        self.score_manager.score_dict = self.screen_manager.create_score_boxes(self.player_manager.player_list)

        # Initialize background and sound
        self.background = self.screen_manager.background
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
        self.manager_handler.setup()
        for button in self.button_manager.button_list:
            self.ui_manager.add(button)
                
        if self.player_manager.current_player.is_computer:
            self.take_computer_turn(self.player_manager.current_player)

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
                    card = card_class.Card(letter, scale=self.screen_manager.scale)
                    self.card_manager.card_list.append(card)
                    self.card_manager.card_dict[card] = letter
                    self.card_manager.piles[index].append(card)
            for i in range(2):
                pile = arcade.SpriteSolidColor(round(self.game_state_manager.rnd_hand_count * MAT_WIDTH * self.screen_manager.scale),
                                               round(MAT_HEIGHT * self.screen_manager.scale),
                                               (255, 255, 255, 10))
                pile.position = self.screen_manager.screen_width / 2, PLAYER_HAND_Y * self.screen_manager.scale
                self.screen_manager.pile_mat_list[i + 3] = pile
            file.close()
            self.card_manager.get_all_card_positions()
        except:
            pass

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

    def turn_start_sequence(self):
        self.manager_handler.turn_start_sequence()

    def turn_end_sequence(self):
        self.manager_handler.turn_end_sequence()
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

    def on_draw(self):
        """
        Called when this view should draw.
        Overrides arcade.View.on_draw().
        """
        arcade.start_render()
        self.clear()
        self.manager_handler.draw()
        self.ui_manager.draw()

    def handle_go_down_button_click(self):
        """ Called when Go Down button is clicked and released. """
        if len(self.card_manager.piles[GO_DOWN_PILE]) == 0 and len(
                self.card_manager.piles[self.player_manager.current_player.hand_index]) == 0:
            self.player_manager.current_player.has_gone_down = True

            self.card_manager.get_completed_words(self.player_manager.current_player)
            arcade.play_sound(GO_DOWN_SOUND, volume=0.3)

        else:
            arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)
            logging.warning("You can't go down yet.")

    def handle_next_turn_button_click(self):
        """ Called when Next Turn button is clicked and released. """
        if self.game_state_manager.has_discarded:
            self.button_manager.next_turn_button.texture.set_available()

            if self.player_manager.is_round_final_turn():
                # Round end is called only if all players have gone down
                self.round_end_sequence()
                return

            self.card_manager.return_cards(cur_player=self.player_manager.current_player)
            self.turn_end_sequence()

    def handle_recall_button_click(self):
        self.card_manager.recall_cards()

    def handle_menu_button_click(self):
        """ Called when menu button is clicked and released. """
        game_view = pause_menu.PauseMenu(
            game_view=self,
            sound_list=self.sound_list,
            sound_player=self.sound_player
        )
        self.window.show_view(game_view)

    def handle_save_word_button_click(self):
        self.card_manager.save_word()

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
                arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)

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
                self.handle_save_word_button_click()

        elif key == arcade.key.ESCAPE:
            self.handle_recall_button_click()

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
                    self.game_state_manager.handle_discard()

    def draw_card(self, pile_index: int):
        self.card_manager.on_card_draw(pile_index)
        self.game_state_manager.on_card_draw(pile_index)

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
        pile_mats = arcade.get_sprites_at_point((x, y), self.screen_manager.pile_mat_list)

        if pile_mats:
            self.card_manager.get_clicked_pile(pile_mats, x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """
        Handles events on mouse release. Button/card events are triggered here instead of
        on_mouse_press().
        """

        if self.player_manager.current_player.is_computer:
            self.handle_next_turn_button_click()
            return

        # Check if any cards are held or buttons are pressed
        if len(self.game_state_manager.held_cards) == 0:
            return

        self.handle_cards_on_mouse_release(button)

        # Resets cards held and buttons pressed after all logic is accounted for.
        self.game_state_manager.held_cards = []

    def handle_cards_on_mouse_release(self, button):
        if len(self.game_state_manager.held_cards) > 0:
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
                        self.game_state_manager.handle_discard()
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
                    self.card_manager.go_down_text += text
                    # print(self.go_down_text)
                    break

    def on_update(self, delta_time):
        """
        Update card positions every 1/60 second based on the card's pile.
        """
        self.manager_handler.update()

    def round_end_sequence(self):
        """
        Called at the end of the round.
        Calculates scores, bonuses, and resets state variables for the next round
        before calling setup().
        """
        self.manager_handler.round_end_sequence()

        if len(self.card_manager.piles[COMPLETED_CARDS]) != 0 \
                or len(self.card_manager.piles[self.player_manager.current_player.hand_index]) != 0:
            self.card_manager.get_completed_words(self.player_manager.current_player)
        self.determine_highest_score()

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
                self.card_manager.completed_words_text_list.append(w)
            self.card_manager. get_completed_words(self.player_manager.current_player)
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

