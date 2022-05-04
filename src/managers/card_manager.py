import logging
from typing import List

import arcade

from src.utils import card_class, player, card_utils, score_change_object
from src.managers.manager import Manager
from src.utils.constants import FACE_DOWN_PILE, GO_DOWN_PILE, COMPLETED_CARDS, CARD_MOVE_SOUND, PILE_COUNT, \
    DISCARD_PILE, CARD_LIST, PLAYER_HAND_Y, GO_DOWN_MAT_Y, WRONG_WORD_SOUND, CARD_SCORE, WORD_LIST, SAVE_WORD_SOUND

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class CardManager(Manager):
    def __init__(self, game_view, player_list):
        self.game_view = game_view
        self.card_list = None
        self.card_dict = {}
        self.small_card_list = None
        self.piles = None
        self.player_list = player_list
        self.completed_words_text_list = []
        self.completed_words_card_list = []

        # Text string representing letters in the go_down pile.
        self.go_down_text = None


    def setup(self):
        # Create a list of lists, each holds a pile of cards
        self.piles = [[] for _ in range(PILE_COUNT)]
        self.card_list = arcade.SpriteList()
        self.small_card_list = arcade.SpriteList()
        self.piles[FACE_DOWN_PILE] = arcade.SpriteList()
        self.piles[DISCARD_PILE] = arcade.SpriteList()
        self.piles[GO_DOWN_PILE] = arcade.SpriteList()
        for p in self.player_list:
            self.piles[p.hand_index] = arcade.SpriteList()
        self.piles[COMPLETED_CARDS] = arcade.SpriteList()

        self.setup_cards()
        self.go_down_text = ''

        # Holds words saved in the completed words pile, so that the original
        # word groupings are maintained for determining the longest word
        self.completed_words_text_list = []

    def draw(self):
        # Draw cards/buttons
        for pile in self.game_view.player_manager.current_player.pile_numbers_list:
            self.piles[pile].draw()
        for card in self.game_view.game_state_manager.held_cards:
            card.draw()
        self.small_card_list.draw()

    def update(self):
        # Update card positions
        for card in self.piles[FACE_DOWN_PILE]:
            card.position = self.game_view.screen_manager.face_down_position
        for card in self.piles[DISCARD_PILE]:
            card.position = self.game_view.screen_manager.discard_position
        for card in self.piles[COMPLETED_CARDS]:
            card.position = self.game_view.screen_manager.completed_card_position
        self.get_go_down_pile_position()
        self.get_hand_position(self.game_view.player_manager.current_player)
        # Handle text in go_down pile
        text = ''
        for card in self.piles[GO_DOWN_PILE]:
            text += self.card_dict[card]
        self.go_down_text = text

    def round_start_sequence(self):
        self.turn_start_sequence()

    def round_end_sequence(self):
        pass

    def turn_start_sequence(self):
        self.flip_all_cards_up()

    def turn_end_sequence(self):
        self.flip_all_cards_down()
        self.completed_words_text_list = []

    def flip_all_cards_up(self):
        for pile in self.piles[1:]:
            for card in pile:
                card.flip_up()

    def flip_all_cards_down(self):
        for pile in self.piles:
            for card in pile:
                card.flip_down()

    def return_cards(self, cur_player: player.Player):
        if len(self.piles[COMPLETED_CARDS]) != 0:
            for _ in range(len(self.piles[COMPLETED_CARDS])):
                self.move_card_to_new_pile(
                    self.piles[COMPLETED_CARDS][0],
                    cur_player.hand_index,
                    COMPLETED_CARDS
                )
        if len(self.piles[GO_DOWN_PILE]) != 0:
            for _ in range(len(self.piles[GO_DOWN_PILE])):
                self.move_card_to_new_pile(
                    self.piles[GO_DOWN_PILE][0],
                    cur_player.hand_index,
                    GO_DOWN_PILE
                )

    def move_card_to_new_pile(self, card: card_class.Card, destination_pile_index: int, original_pile_index: int):
        """
        Handles movement of a card from one pile to another,
        ensuring the sprite is never in two piles at once.
        """
        try:
            self.remove_card_from_pile(id(card))
        except:
            pass
        self.piles[destination_pile_index].append(card)

        if original_pile_index != destination_pile_index:
            if destination_pile_index != FACE_DOWN_PILE and destination_pile_index != COMPLETED_CARDS:
                arcade.play_sound(CARD_MOVE_SOUND, volume=0.5)

    def remove_card_from_pile(self, card_id):
        """
        Removes card from its pile.
        """
        for pile in self.piles:
            for card in pile:
                if id(card) == card_id:
                    pile.remove(card)
                    break

    def setup_cards(self):
        self.card_list, self.card_dict = card_utils.create_cards(
            card_values=CARD_LIST,
            position=self.game_view.screen_manager.face_down_position,
            scale=self.game_view.screen_manager.scale
        )
        self.card_list = card_utils.shuffle_cards(self.card_list)
        # Put all the cards in the face down pile
        self.piles[FACE_DOWN_PILE].extend(self.card_list)
        # Create Both Player Hands
        for p in self.game_view.player_manager.player_list:
            self.deal_hand(p)
            self.get_hand_position(p)
        # Pop top card into discard pile
        self.move_card_to_new_pile(self.piles[FACE_DOWN_PILE][-1], DISCARD_PILE, FACE_DOWN_PILE)

    def deal_hand(self, cur_player: player):
        for _ in range(self.game_view.game_state_manager.rnd_hand_count):
            card = self.piles[FACE_DOWN_PILE][-1]
            self.move_card_to_new_pile(card, cur_player.hand_index, FACE_DOWN_PILE)

    def get_hand_position(self, cur_player: player):
        """
        Positions the cards in the player's hand.
        """
        for i in range(len(self.piles[cur_player.hand_index])):
            card = self.piles[cur_player.hand_index][i]
            card.center_x = self.straight_line(i, cur_player.hand_index)
            card.center_y = PLAYER_HAND_Y * self.game_view.screen_manager.scale

    def straight_line(self, i, current_player_hand):
        """
        Math for spacing the cards out evenly.
        """
        return 110 * self.game_view.screen_manager.scale * i \
            - ((((len(self.piles[current_player_hand])) - 1) * 110 * self.game_view.screen_manager.scale) / 2) \
            + self.game_view.screen_manager.screen_width / 2

    def go_down_straight_line(self, i):
        """
        Same as straight_line, used for center pile.
        """
        return 120 * self.game_view.screen_manager.scale * i - \
               (((len(self.piles[GO_DOWN_PILE]) - 1) * 120 * self.game_view.screen_manager.scale) / 2) + self.game_view.screen_manager.screen_width / 2

    def get_go_down_pile_position(self):
        """
        Positions the cards in the center pile.
        """
        for i in range(len(self.piles[GO_DOWN_PILE])):
            card = self.piles[GO_DOWN_PILE][i]
            card.center_x = self.go_down_straight_line(i)
            card.center_y = GO_DOWN_MAT_Y * self.game_view.screen_manager.scale

    def get_all_card_positions(self):
        """
        Called when loading a game. Sets all cards to their correct position on the board.
        """
        for card in self.piles[FACE_DOWN_PILE]:
            card.set_position(*self.game_view.screen_manager.face_down_position)
            card.flip_down()
        for card in self.piles[DISCARD_PILE]:
            card.set_position(*self.game_view.screen_manager.discard_position)
        for card in self.piles[COMPLETED_CARDS]:
            card.set_position(*self.game_view.screen_manager.completed_card_position)
        self.get_go_down_pile_position()
        for p in self.game_view.player_manager.player_list:
            self.get_hand_position(p)

    def get_clicked_pile(self, pile_mats: List[arcade.Sprite], x, y):
        """
        Sets 'cards' variable to only the cards in the selected pile.
        pile: List[Sprite]
        """
        cards = []
        pile_mat_list = self.game_view.screen_manager.pile_mat_list
        for value in pile_mats:
            logging.debug(f'Pile #: {pile_mat_list.index(value)}')
        if len(pile_mats) > 1:
            pile_mats.remove(pile_mats[-1])
        if pile_mat_list.index(pile_mats[0]) == FACE_DOWN_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.piles[FACE_DOWN_PILE])
        elif pile_mat_list.index(pile_mats[0]) == DISCARD_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.piles[DISCARD_PILE])
        elif pile_mat_list.index(pile_mats[0]) == GO_DOWN_PILE:
            cards = arcade.get_sprites_at_point((x, y), self.piles[GO_DOWN_PILE])
        elif pile_mat_list.index(pile_mats[0]) == COMPLETED_CARDS:
            pass
        else:
            cards = arcade.get_sprites_at_point((x, y), self.piles[self.game_view.player_manager.current_player.hand_index])

        # Get only top card of pile
        if len(cards) > 0:
            self.game_view.game_state_manager.get_top_card(cards)

    def get_completed_words(self, cur_player: player.Player):
        """
        Returns words saved into the completed words pile during a player's turn.
        """

        # Recalls cards if a player went down using their entire hand plus the discard.
        if len(self.piles[COMPLETED_CARDS]) > self.game_view.game_state_manager.rnd_hand_count:
            self.recall_cards()

        # Does nothing if completed cards pile and player hand are empty.
        elif len(self.piles[COMPLETED_CARDS]) == 0 and len(self.piles[cur_player.hand_index]) == 0:
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
                    small_card = card_class.Card(completed_card.value, scale=.75 * self.game_view.screen_manager.scale)
                    self.small_card_list.append(small_card)
                    small_go_down_list[index].append(small_card)
                    small_card.position = self.game_view.screen_manager.get_small_go_down_card_position(
                        index,
                        small_go_down_list[index].index(small_card),
                        cur_player
                    )

            self.completed_words_card_list = []

            # Subtracts card values of unused cards from total score
            if len(self.piles[cur_player.hand_index]) != 0:
                for card in self.piles[cur_player.hand_index]:
                    current_score -= CARD_SCORE[card.value]
            # logging.warning(current_score)
            cur_player.total_score += current_score
            self.game_view.score_manager.score_change_list.append(
                score_change_object.ScoreChangeObject(
                    player=cur_player,
                    score=current_score,
                    timer=0
                )
            )

            # Get current player's longest word for the round
            if len(word_length_list) > 0:
                word_length_list.sort()
                cur_player.longest_words[self.game_view.game_state_manager.rnd] = word_length_list[-1]
            else:
                cur_player.longest_words[self.game_view.game_state_manager.rnd] = 0

            # Empty completed cards pile after score and words have been tabulated
            for _ in range(len(self.piles[COMPLETED_CARDS])):
                self.piles[COMPLETED_CARDS].pop()

    def get_pile_for_card(self, card):
        """
        Returns pile index of card.
        """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def recall_cards(self):
        """
        Called when cards are to be recalled to the player's hand
        from the completed cards pile when Recall button is pressed.
        """
        self.return_cards_to_hand(COMPLETED_CARDS)
        self.completed_words_text_list = []
        self.completed_words_card_list = []

    def save_word(self):
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
                arcade.play_sound(SAVE_WORD_SOUND)

                # logging.warning(self.completed_words_text_list)
                return

        # Else, return cards to hand
        self.return_cards_to_hand(GO_DOWN_PILE)
        self.go_down_text = ''

    def return_cards_to_hand(self, pile_index: int):
        if len(self.piles[pile_index]) != 0:
            for _ in range(len(self.piles[pile_index])):
                self.move_card_to_new_pile(
                    self.piles[pile_index][0],
                    self.game_view.player_manager.current_player.hand_index,
                    pile_index
                )
            arcade.play_sound(WRONG_WORD_SOUND, volume=0.2)

    def on_card_draw(self, pile_index):
        card = self.piles[pile_index][-1]
        self.move_card_to_new_pile(
            card,
            self.game_view.player_manager.current_player.hand_index,
            self.game_view.game_state_manager.held_cards_original_pile
        )
        card.flip_up()
