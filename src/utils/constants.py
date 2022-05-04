"""
List of constants used in the Quiddler namespace.
"""
import arcade
from src.utils.word_list import get_word_list

SOUNDS_FILE_PATH = 'D:/Python Games/Quiddler_Arcade/src/sounds/'
IMAGE_FILE_PATH = 'D:/Python Games/Quiddler_Arcade/src/images/'
WORD_LIST = get_word_list()
BACKGROUND_IMAGE_WIDTH, BACKGROUND_IMAGE_HEIGHT = 2560, 1920
GAME_END_BACKGROUND_WIDTH, GAME_END_BACKGROUND_HEIGHT = 1920, 1080
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

GAME_END_BACKGROUND = f"{IMAGE_FILE_PATH}game_end_background.png"
GAME_MENU_BASE_BACKGROUND = f"{IMAGE_FILE_PATH}game_menu_base_background.png"
HIGHSCORES_BACKGROUND = f"{IMAGE_FILE_PATH}highscores_background.png"

FACE_DOWN_IMAGE = f"{IMAGE_FILE_PATH}card_back.png"
GO_DOWN = f"{IMAGE_FILE_PATH}go_down.png"
GO_DOWN_PRESSED = f"{IMAGE_FILE_PATH}go_down_pressed.png"
GO_DOWN_FLASH = f"{IMAGE_FILE_PATH}go_down_flash.png"
NEXT_TURN = f"{IMAGE_FILE_PATH}next_turn.png"
NEXT_TURN_PRESSED = f"{IMAGE_FILE_PATH}next_turn_pressed.png"
NEXT_TURN_FLASH = f"{IMAGE_FILE_PATH}next_turn_flash.png"
SAVE_WORD = f"{IMAGE_FILE_PATH}save_word.png"
SAVE_WORD_PRESSED = f"{IMAGE_FILE_PATH}save_word_pressed.png"
SAVE_WORD_FLASH = f"{IMAGE_FILE_PATH}save_word_flash.png"
RECALL = f"{IMAGE_FILE_PATH}recall.png"
RECALL_PRESSED = f"{IMAGE_FILE_PATH}recall_pressed.png"
UNDO = f"{IMAGE_FILE_PATH}undo.png"
UNDO_PRESSED = f"{IMAGE_FILE_PATH}undo_pressed.png"
EXIT = f"{IMAGE_FILE_PATH}exit_button.png"
EXIT_PRESSED = f"{IMAGE_FILE_PATH}exit_button_pressed.png"
MENU = f"{IMAGE_FILE_PATH}menu_button.png"
MENU_PRESSED = f"{IMAGE_FILE_PATH}menu_button_pressed.png"
CANCEL = f"{IMAGE_FILE_PATH}cancel_button.png"
CANCEL_BUTTON_PRESSED = f"{IMAGE_FILE_PATH}cancel_button_pressed.png"
SAVE = f"{IMAGE_FILE_PATH}save_game.png"
SAVE_PRESSED = f"{IMAGE_FILE_PATH}save_game_pressed.png"
CONTINUE = f"{IMAGE_FILE_PATH}continue.png"
CONTINUE_PRESSED = f"{IMAGE_FILE_PATH}continue_pressed.png"
ON = f"{IMAGE_FILE_PATH}on.png"
ON_PRESSED = f"{IMAGE_FILE_PATH}on_pressed.png"
OFF = f"{IMAGE_FILE_PATH}off.png"
OFF_PRESSED = f"{IMAGE_FILE_PATH}off_pressed.png"
YES = f"{IMAGE_FILE_PATH}yes.png"
YES_PRESSED = f"{IMAGE_FILE_PATH}yes_pressed.png"
NO = f"{IMAGE_FILE_PATH}no.png"
NO_PRESSED = f"{IMAGE_FILE_PATH}no_pressed.png"
HIGHSCORES_BUTTON = f"{IMAGE_FILE_PATH}highscores_button.png"
HIGHSCORES_BUTTON_PRESSED = f"{IMAGE_FILE_PATH}highscores_button_pressed.png"
EDIT_NAMES = f"{IMAGE_FILE_PATH}edit_names.png"
EDIT_NAMES_PRESSED = f"{IMAGE_FILE_PATH}edit_names_pressed.png"
BACK = f"{IMAGE_FILE_PATH}back.png"
BACK_PRESSED = f"{IMAGE_FILE_PATH}back_pressed.png"

CARD_MOVE_SOUND = arcade.load_sound(f"{SOUNDS_FILE_PATH}card_move.ogg")
SAVE_WORD_SOUND = arcade.load_sound(f"{SOUNDS_FILE_PATH}save_word.ogg")
GO_DOWN_SOUND = arcade.load_sound(f"{SOUNDS_FILE_PATH}go_down.ogg")
WRONG_WORD_SOUND = arcade.load_sound(f"{SOUNDS_FILE_PATH}wrong_word.ogg")
SOUND_LIST = [
    CARD_MOVE_SOUND,
    SAVE_WORD_SOUND,
    GO_DOWN_SOUND,
    WRONG_WORD_SOUND
]
BACKGROUND_MUSIC = arcade.load_sound(f"{SOUNDS_FILE_PATH}quiddler_theme_2.ogg")
MAIN_MENU_MUSIC = arcade.load_sound(f"{SOUNDS_FILE_PATH}quiddler_theme_1.ogg")
GAME_END_THEME = arcade.load_sound(f"{SOUNDS_FILE_PATH}game_end_theme.mp3")

SCALE = 1

PLAYER_HAND_Y = 225
GO_DOWN_MAT_Y = 450
BUTTON_Y = 50

PILE_COUNT = 6
FACE_DOWN_PILE = 0
DISCARD_PILE = 1
GO_DOWN_PILE = 2
COMPLETED_CARDS = 3
PLAYER_1_HAND = 4
PLAYER_2_HAND = 5
OTHER_PILES = [
    FACE_DOWN_PILE,
    DISCARD_PILE,
    GO_DOWN_PILE,
    COMPLETED_CARDS
]
PLAYER_PILE_MAT = 4

S_PILE_COUNT = 6
S_FACE_DOWN_PILE = 0
S_DISCARD_PILE = 1
S_GO_DOWN_PILE = 2
S_PLAYER_HAND = 3
S_COMPUTER_HAND = 4
S_COMPLETED_CARDS = 5

PLAYER_1 = 0
PLAYER_2 = 1
NUMBER_OF_PLAYERS = 2

S_PLAYER = 0
S_COMPUTER = 1

WHITE = arcade.color.WHITE
WHITE_TRANSPARENT = (255, 255, 255, 40)
GOLD_TRANSPARENT = (206, 201, 53, 100)
GREEN = arcade.color.GREEN
RED = arcade.color.RED