import arcade
import confirm_exit
import instructions
from constants import WHITE, BACKGROUND_MUSIC, EXIT, EXIT_PRESSED, CANCEL, CANCEL_BUTTON_PRESSED, SAVE, SAVE_PRESSED,\
    ON, ON_PRESSED, OFF, OFF_PRESSED


class PauseMenu(arcade.View):
    """"
    Pause Menu View.
    """
    def __init__(self, game_view, sound_list):
        super().__init__()
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.game_view = game_view
        self.background = arcade.Sprite(
            filename="images/game_menu.png",
            scale=self.scale
        )
        self.background.position = self.screen_width / 2, self.screen_height / 2

        self.sound_list = sound_list

        # Create list of buttons
        self.button_list = arcade.SpriteList()
        self.sound_on_button = arcade.Sprite(ON, scale=self.scale)
        self.sound_on_button.position = self.screen_width / 2 - 100 * self.scale, 400 * self.scale
        self.button_list.append(self.sound_on_button)
        self.sound_off_button = arcade.Sprite(OFF, scale=self.scale)
        self.sound_off_button.position = self.screen_width / 2 + 100 * self.scale, 400 * self.scale
        self.button_list.append(self.sound_off_button)
        self.save_button = arcade.Sprite(SAVE, scale=self.scale)
        self.save_button.position = self.screen_width / 2, 300 * self.scale
        self.button_list.append(self.save_button)
        self.cancel_button = arcade.Sprite(CANCEL, scale=self.scale)
        self.cancel_button.position = self.screen_width / 2, 600 * self.scale
        self.button_list.append(self.cancel_button)
        self.instructions_button = arcade.Sprite("images/instructions_button.png", scale=self.scale)
        self.instructions_button.position = self.screen_width / 2, 200 * self.scale
        self.button_list.append(self.instructions_button)
        self.exit_button = arcade.Sprite(EXIT, scale=self.scale)
        self.exit_button.position = self.screen_width / 2, 100 * self.scale
        self.button_list.append(self.exit_button)

        self.buttons_pressed = []

        self.background_music = BACKGROUND_MUSIC
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        self.background.draw()
        self.button_list.draw()

        arcade.draw_text(
            'Music:',
            self.screen_width / 2,
            475 * self.scale,
            color=WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center",
        )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.buttons_pressed = arcade.get_sprites_at_point((x, y), self.button_list)

        if self.instructions_button in self.buttons_pressed:
            self.instructions_button.texture = arcade.load_texture("images/instructions_button_pressed.png")
        elif self.exit_button in self.buttons_pressed:
            self.exit_button.texture = arcade.load_texture(EXIT_PRESSED)
        elif self.cancel_button in self.buttons_pressed:
            self.cancel_button.texture = arcade.load_texture(CANCEL_BUTTON_PRESSED)
        elif self.save_button in self.buttons_pressed:
            self.save_button.texture = arcade.load_texture(SAVE_PRESSED)
        elif self.sound_on_button in self.buttons_pressed:
            self.sound_on_button.texture = arcade.load_texture(ON_PRESSED)
        elif self.sound_off_button in self.buttons_pressed:
            self.sound_off_button.texture = arcade.load_texture(OFF_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):

        if self.instructions_button in self.buttons_pressed:
            game_view = instructions.InstructionsMenu1(game_view=self)
            game_view.setup()

            self.window.show_view(game_view)
        elif self.exit_button in self.buttons_pressed:

            game_view = confirm_exit.ConfirmExit(game_view=self.game_view)
            self.window.show_view(game_view)
        elif self.cancel_button in self.buttons_pressed:
            self.window.show_view(self.game_view)
        elif self.save_button in self.buttons_pressed:
            self.game_view.save_game()
        elif self.sound_on_button in self.buttons_pressed:
            self.background_music.set_volume(volume=.25)
        elif self.sound_off_button in self.buttons_pressed:
            self.background_music.set_volume(volume=0)

        self.sound_on_button.texture = arcade.load_texture(ON)
        self.sound_off_button.texture = arcade.load_texture(OFF)
        self.save_button.texture = arcade.load_texture(SAVE)
        self.instructions_button.texture = arcade.load_texture("images/instructions_button.png")
        self.exit_button.texture = arcade.load_texture(EXIT)
        self.buttons_pressed = []

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.F9:
            if self.background_music.get_volume() != 0:
                self.background_music.set_volume(volume=0.0)
            else:
                self.background_music.set_volume(volume=0.25)

        elif key == arcade.key.F8:
            if self.game_view.card_move_sound.get_volume() != 0:
                for sound in self.game_view.sound_list:
                    sound.set_volume(volume=0)
            else:
                self.game_view.card_move_sound.set_volume(volume=1)
                self.game_view.save_word_sound.set_volume(volume=1)
                self.game_view.go_down_sound.set_volume(volume=0.2)
                self.game_view.wrong_word_sound.set_volume(volume=0.5)
