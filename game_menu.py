import arcade
import main
from constants import BACKGROUND_IMAGE_WIDTH, CONTINUE, EXIT, MAIN_MENU_MUSIC, EXIT_PRESSED, CONTINUE_PRESSED


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

        self.continue_button = arcade.Sprite(CONTINUE, scale=self.scale)
        self.continue_button.position = self.screen_width / 2, self.screen_height / 2 * self.scale
        self.button_list.append(self.continue_button)
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

        self.main_menu_music = MAIN_MENU_MUSIC

    def on_show(self):
        """ This is run once when we switch to this view """
        self.background.draw()
        self.button_list.draw()

        self.main_menu_music.play(volume=.25)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.background.draw()
        self.button_list.draw()

    def on_update(self, delta_time: float):
        if self.main_menu_music.is_complete():
            self.main_menu_music.play(volume=.25)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1 or symbol == arcade.key.NUM_1:
            game_view = main.Quiddler(rnd_number=8)
            game_view.setup()
            self.main_menu_music.stop()
            self.window.show_view(game_view)
        elif symbol == arcade.key.KEY_2 or symbol == arcade.key.NUM_2:
            game_view = main.Quiddler(rnd_number=16)
            game_view.setup()
            self.main_menu_music.stop()
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
            elif self.continue_button in self.buttons_pressed:
                self.continue_button.texture = arcade.load_texture(CONTINUE_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):

        button = arcade.get_sprites_at_point((x, y), self.button_list)

        if button:
            if self.half_game_button in self.buttons_pressed:
                if self.half_game_button == button[0]:

                    game_view = main.Quiddler(rnd_number=8)
                    game_view.setup()
                    self.main_menu_music.stop()
                    self.window.show_view(game_view)

            elif self.full_game_button in self.buttons_pressed:
                if self.full_game_button == button[0]:
                    game_view = main.Quiddler(rnd_number=16)
                    game_view.setup()
                    self.main_menu_music.stop()
                    self.window.show_view(game_view)

            elif self.instructions_button in self.buttons_pressed:
                if self.instructions_button == button[0]:
                    pass

            elif self.exit_button in self.buttons_pressed:
                if self.exit_button == button[0]:
                    arcade.close_window()

            elif self.continue_button in self.buttons_pressed:
                if self.continue_button == button[0]:
                    game_view = main.Quiddler(rnd_number=8)
                    game_view.setup()
                    game_view.continue_game()
                    self.main_menu_music.stop()
                    self.window.show_view(game_view)



        self.half_game_button.texture = arcade.load_texture("images/half_game_button.png")
        self.full_game_button.texture = arcade.load_texture("images/full_game_button.png")
        self.instructions_button.texture = arcade.load_texture("images/instructions_button.png")
        self.exit_button.texture = arcade.load_texture(EXIT)
        self.buttons_pressed = []