import arcade
from constants import EXIT, CANCEL, EXIT_PRESSED, CANCEL_BUTTON_PRESSED

class ConfirmExit(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.screen_width, self.screen_height = self.window.get_size()
        self.scale = min(self.screen_width / 1920, self.screen_height / 1080)
        self.background = arcade.Sprite(
            filename="images/confirm_exit.png",
            scale=self.scale
        )
        self.background.position = self.screen_width / 2, self.screen_height / 2

        self.button_list = arcade.SpriteList()
        self.exit_button = arcade.Sprite(EXIT, scale=self.scale)
        self.exit_button.position = self.screen_width / 2 - 200 * self.scale, self.screen_height / 2 - 100 * self.scale
        self.button_list.append(self.exit_button)
        self.cancel_button = arcade.Sprite(CANCEL, scale=self.scale)
        self.cancel_button.position = self.screen_width / 2 + 200 * self.scale, self.screen_height / 2 - 100 * self.scale
        self.button_list.append(self.cancel_button)
        self.buttons_pressed = []

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        self.button_list.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.buttons_pressed = arcade.get_sprites_at_point((x, y), self.button_list)

        if self.exit_button in self.buttons_pressed:
            self.exit_button.texture = arcade.load_texture(EXIT_PRESSED)
        elif self.cancel_button in self.buttons_pressed:
            self.cancel_button.texture = arcade.load_texture(CANCEL_BUTTON_PRESSED)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):

        if self.exit_button in self.buttons_pressed:
            arcade.close_window()
        elif self.cancel_button in self.buttons_pressed:
            self.window.show_view(self.game_view)

        self.exit_button.texture = arcade.load_texture(EXIT)
        self.cancel_button.texture = arcade.load_texture(CANCEL)
        self.buttons_pressed = []
