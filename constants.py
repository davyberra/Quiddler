import arcade
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

FACE_DOWN_IMAGE = "images/card_back.png"
GO_DOWN = "images/go_down.png"
GO_DOWN_PRESSED = "images/go_down_pressed.png"
GO_DOWN_FLASH = "images/go_down_flash.png"
NEXT_TURN = "images/next_turn.png"
NEXT_TURN_PRESSED = "images/next_turn_pressed.png"
NEXT_TURN_FLASH = "images/next_turn_flash.png"
SAVE_WORD = "images/save_word.png"
SAVE_WORD_PRESSED = "images/save_word_pressed.png"
SAVE_WORD_FLASH = "images/save_word_flash.png"
RECALL = "images/recall.png"
RECALL_PRESSED = "images/recall_pressed.png"
UNDO = "images/undo.png"
UNDO_PRESSED = "images/undo_pressed.png"
EXIT = "images/exit_button.png"
EXIT_PRESSED = "images/exit_button_pressed.png"
MENU = "images/menu_button.png"
MENU_PRESSED = "images/menu_button_pressed.png"
CANCEL = "images/cancel_button.png"
CANCEL_BUTTON_PRESSED = "images/cancel_button_pressed.png"
SAVE = "images/save_game.png"
SAVE_PRESSED = "images/save_game_pressed.png"
CONTINUE = "images/continue.png"
CONTINUE_PRESSED = "images/continue_pressed.png"
ON = "images/on.png"
ON_PRESSED = "images/on_pressed.png"
OFF = "images/off.png"
OFF_PRESSED = "images/off_pressed.png"

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