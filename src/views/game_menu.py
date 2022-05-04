"""
Main Menu for Quiddler - called on application start.
"""
import arcade
from src.views import quiddler_game, highscores, instructions, edit_player_names
from src.utils.constants import BACKGROUND_IMAGE_WIDTH, CONTINUE, EXIT, MAIN_MENU_MUSIC, EXIT_PRESSED, CONTINUE_PRESSED, \
    HIGHSCORES_BUTTON, HIGHSCORES_BUTTON_PRESSED, EDIT_NAMES, EDIT_NAMES_PRESSED

IMAGE_FILE_PATH = 'D:/Python Games/Quiddler_Arcade/src/images/'


class GameMenu(arcade.View):

    def __init__(self, player_1, player_2):
        super().__init__()
        self.window.set_fullscreen(True)
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.player_1 = player_1
        self.player_2 = player_2

        self.background = arcade.Sprite(filename=f"{IMAGE_FILE_PATH}/quiddler_main_menu_background(2).png",
                                        scale=self.screen_width / BACKGROUND_IMAGE_WIDTH)
        self.background.position = self.screen_width / 2, self.screen_height / 2

        self.button_list = arcade.SpriteList()

        self.continue_button = arcade.Sprite(CONTINUE, scale=self.scale)
        self.continue_button.position = self.screen_width / 2, self.screen_height / 2 + 100 * self.scale
        self.button_list.append(self.continue_button)
        self.solo_half_game_button = arcade.Sprite(f"{IMAGE_FILE_PATH}/half_game_button.png", scale=self.scale)
        self.solo_half_game_button.position = self.screen_width / 2 - 100 * self.scale, self.screen_height / 2
        self.button_list.append(self.solo_half_game_button)
        self.solo_full_game_button = arcade.Sprite(f"{IMAGE_FILE_PATH}/full_game_button.png", scale=self.scale)
        self.solo_full_game_button.position = self.screen_width / 2 + 100 * self.scale, self.screen_height / 2
        self.button_list.append(self.solo_full_game_button)
        self.half_game_button = arcade.Sprite(f"{IMAGE_FILE_PATH}/half_game_button.png", scale=self.scale)
        self.half_game_button.position = self.screen_width / 2 - 100 * self.scale, self.screen_height / 2 - 100 * self.scale
        self.button_list.append(self.half_game_button)
        self.full_game_button = arcade.Sprite(f"{IMAGE_FILE_PATH}/full_game_button.png", scale=self.scale)
        self.full_game_button.position = self.screen_width / 2 + 100 * self.scale, self.screen_height / 2 - 100 * self.scale
        self.button_list.append(self.full_game_button)
        self.edit_names_button = arcade.Sprite(EDIT_NAMES, scale=self.scale)
        self.edit_names_button.position = self.screen_width / 2, self.screen_height / 2 - 200 * self.scale
        self.button_list.append(self.edit_names_button)
        self.highscores_button = arcade.Sprite(HIGHSCORES_BUTTON, scale=self.scale)
        self.highscores_button.position = self.screen_width / 2, self.screen_height / 2 - 300 * self.scale
        self.button_list.append(self.highscores_button)
        self.instructions_button = arcade.Sprite(f"{IMAGE_FILE_PATH}/instructions_button.png", scale=self.scale)
        self.instructions_button.position = self.screen_width / 2, self.screen_height / 2 - 400 * self.scale
        self.button_list.append(self.instructions_button)
        self.exit_button = arcade.Sprite(EXIT, scale=self.scale)
        self.exit_button.position = self.screen_width / 2, self.screen_height / 2 - 500 * self.scale
        self.button_list.append(self.exit_button)

        self.buttons_pressed = []

        self.main_menu_music = MAIN_MENU_MUSIC
        self.sound_player = None
        self.sound_player = self.main_menu_music.play(volume=.50, loop=True)

    def on_show(self):
        """ This is run once when we switch to this view """
        self.background.draw()
        self.button_list.draw()

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.background.draw()
        self.button_list.draw()
        arcade.draw_text(
            "Solo:",
            self.screen_width / 2 - 225 * self.scale,
            self.screen_height / 2,
            arcade.color.WHITE,
            50,
            anchor_x='right',
            anchor_y='center'
        )
        arcade.draw_text(
            "2-P:",
            self.screen_width / 2 - 225 * self.scale,
            self.screen_height / 2 - 100 * self.scale,
            arcade.color.WHITE,
            50,
            anchor_x='right',
            anchor_y='center'
        )

    # def on_update(self, delta_time: float):
        # if self.main_menu_music.is_complete(self.sound_player):
        #     self.main_menu_music.play(volume=.25)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.F10:
            arcade.close_window()
        elif symbol == arcade.key.F9:
            game_view = quiddler_game.Quiddler(
                rnd_number=8,
                players=[
                    {
                        'player_name': self.player_1,
                        'is_computer': False
                    },
                    {
                        'player_name': 'Computer',
                        'is_computer': True
                    }
                ]
            )
            game_view.setup()
            self.main_menu_music.stop(self.sound_player)
            self.window.show_view(game_view)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.buttons_pressed = arcade.get_sprites_at_point((x, y,), self.button_list)

            if self.half_game_button in self.buttons_pressed:
                self.half_game_button.texture = arcade.load_texture(f"{IMAGE_FILE_PATH}/half_game_button_pressed.png")
            elif self.solo_half_game_button in self.buttons_pressed:
                self.solo_half_game_button.texture = arcade.load_texture(f"{IMAGE_FILE_PATH}/half_game_button_pressed.png")
            elif self.solo_full_game_button in self.buttons_pressed:
                self.solo_full_game_button.texture = arcade.load_texture(f"{IMAGE_FILE_PATH}/full_game_button_pressed.png")
            elif self.full_game_button in self.buttons_pressed:
                self.full_game_button.texture = arcade.load_texture(f"{IMAGE_FILE_PATH}/full_game_button_pressed.png")
            elif self.instructions_button in self.buttons_pressed:
                self.instructions_button.texture = arcade.load_texture(f"{IMAGE_FILE_PATH}/instructions_button_pressed.png")

            elif self.exit_button in self.buttons_pressed:
                self.exit_button.texture = arcade.load_texture(EXIT_PRESSED)
            elif self.continue_button in self.buttons_pressed:
                self.continue_button.texture = arcade.load_texture(CONTINUE_PRESSED)
            elif self.edit_names_button in self.buttons_pressed:
                self.edit_names_button.texture = arcade.load_texture(EDIT_NAMES_PRESSED)
            elif self.highscores_button in self.buttons_pressed:
                self.highscores_button.texture = arcade.load_texture(HIGHSCORES_BUTTON_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):

        button = arcade.get_sprites_at_point((x, y), self.button_list)

        if button:
            if self.half_game_button in self.buttons_pressed:
                if self.half_game_button == button[0]:
                    game_view = quiddler_game.Quiddler(
                        rnd_number=8,
                        players=[
                            {
                                'player_name': self.player_1,
                                'is_computer': False
                            },
                            {
                                'player_name': self.player_2,
                                'is_computer': False
                            }
                        ]
                    )
                    game_view.setup()
                    self.main_menu_music.stop(self.sound_player)
                    self.window.show_view(game_view)

            elif self.full_game_button in self.buttons_pressed:
                if self.full_game_button == button[0]:
                    game_view = quiddler_game.Quiddler(
                        rnd_number=16,
                        players=[
                            {
                                'player_name': self.player_1,
                                'is_computer': False
                            },
                            {
                                'player_name': self.player_2,
                                'is_computer': False
                            }
                        ]
                    )
                    game_view.setup()
                    self.main_menu_music.stop(self.sound_player)
                    self.window.show_view(game_view)

            elif self.solo_half_game_button in self.buttons_pressed:
                if self.solo_half_game_button == button[0]:
                    game_view = quiddler_game.Quiddler(
                        rnd_number=8,
                        players=[
                            {
                                'player_name': self.player_1,
                                'is_computer': False
                            },
                            {
                                'player_name': 'Computer',
                                'is_computer': True
                            }
                        ]
                    )
                    game_view.setup()
                    self.main_menu_music.stop(self.sound_player)
                    self.window.show_view(game_view)

            elif self.solo_full_game_button in self.buttons_pressed:
                if self.solo_full_game_button == button[0]:
                    game_view = quiddler_game.Quiddler(
                        rnd_number=16,
                        players=[
                            {
                                'player_name': self.player_1,
                                'is_computer': False
                            },
                            {
                                'player_name': 'Computer',
                                'is_computer': True
                            }
                        ]
                    )
                    game_view.setup()
                    self.main_menu_music.stop(self.sound_player)
                    self.window.show_view(game_view)

            elif self.instructions_button in self.buttons_pressed:
                if self.instructions_button == button[0]:
                    game_view = instructions.InstructionsMenu1(game_view=self)
                    game_view.setup()

                    self.window.show_view(game_view)

            elif self.exit_button in self.buttons_pressed:
                if self.exit_button == button[0]:
                    arcade.close_window()

            elif self.continue_button in self.buttons_pressed:
                if self.continue_button == button[0]:
                    game_view = quiddler_game.Quiddler(
                        rnd_number=8,
                        players=[
                            {
                                'player_name': self.player_1,
                                'is_computer': False
                            },
                            {
                                'player_name': self.player_2,
                                'is_computer': False
                            }
                        ]
                    )
                    game_view.setup()
                    game_view.continue_game()
                    self.main_menu_music.stop(self.sound_player)
                    self.window.show_view(game_view)

            elif self.edit_names_button in self.buttons_pressed:
                if self.edit_names_button == button[0]:
                    game_view = edit_player_names.EditPlayerNames(player_1=self.player_1,
                                                                  player_2=self.player_2,
                                                                  game_view=self)
                    self.window.show_view(game_view)

            elif self.highscores_button in self.buttons_pressed:
                if self.highscores_button == button[0]:
                    game_view = highscores.HighScores(game_view=self)
                    self.window.show_view(game_view)

        self.highscores_button.texture = arcade.load_texture(HIGHSCORES_BUTTON)
        self.edit_names_button.texture = arcade.load_texture(EDIT_NAMES)
        self.half_game_button.texture = arcade.load_texture(f"{IMAGE_FILE_PATH}/half_game_button.png")
        self.full_game_button.texture = arcade.load_texture(f"{IMAGE_FILE_PATH}/full_game_button.png")
        self.instructions_button.texture = arcade.load_texture(f"{IMAGE_FILE_PATH}/instructions_button.png")
        self.exit_button.texture = arcade.load_texture(EXIT)
        self.buttons_pressed = []