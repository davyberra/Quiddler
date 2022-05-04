from src.utils import player


class ScoreChangeObject:
    def __init__(
            self,
            player: player.Player,
            score: int,
            timer: int
    ):
        self.player = player
        self.score = score
        self.timer = timer
