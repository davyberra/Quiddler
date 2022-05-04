"""
Main entry point for entire game.
"""
import arcade
import shelve

from src.views import game_menu


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


def main():
    """
    Main function.
    """
    window = arcade.Window(fullscreen=True, title="Quiddler")
    window.center_window()

    # Initialize player names to last used values
    player_1, player_2 = get_player_names(filename='players')

    # Start game with GameMenu view
    start_view = game_menu.GameMenu(player_1=player_1,
                                    player_2=player_2)
    window.show_view(start_view)

    arcade.run()


if __name__ == "__main__":
    main()