from typing import List


from src import score_change_object, player


class ScoreManager:
    def __init__(self):
        self.score_dict = {}
        # List of scores that are animated above each player
        # whenever their score changes
        self.score_change_list: List[score_change_object.ScoreChangeObject] = []

    def add_score_boxes(self, score_boxes: dict):
        self.score_dict = score_boxes

    def draw_score_boxes(self):
        for s_box in self.score_dict.values():
            s_box.draw()

        for score_object in self.score_change_list:
            s_box = self.score_dict[score_object.player]
            s_box.draw_score_change(score_object)

    def update(self):

        # Timer for score-change animation
        for score_change_object in self.score_change_list:
            if score_change_object.timer > 200:
                self.score_change_list.remove(score_change_object)
            else:
                score_change_object.timer += 1

    def add_bonus_to_score(self, cur_player: player.Player):
        """ Adds longest word bonus to player's round score. """
        bonus = 10
        cur_player.total_score += bonus
        for score in self.score_change_list:
            if score.player == cur_player:
                score.score += bonus
            else:
                self.score_change_list.append(
                    score_change_object.ScoreChangeObject(
                        player=cur_player,
                        score=bonus,
                        timer=0
                    )
                )
                break