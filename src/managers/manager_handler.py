from typing import List

from src.managers.manager import Manager


class ManagerHandler:
    def __init__(self):
        self.manager_list: List[Manager] = []

    def add(self, manager: Manager):
        self.manager_list.append(manager)

    def setup(self):
        for m in self.manager_list:
            m.setup()

    def draw(self):
        for m in self.manager_list:
            m.draw()

    def update(self):
        for m in self.manager_list:
            m.update()

    def round_start_sequence(self):
        for m in self.manager_list:
            m.round_start_sequence()

    def round_end_sequence(self):
        for m in self.manager_list:
            m.round_end_sequence()

    def turn_start_sequence(self):
        for m in self.manager_list:
            m.turn_start_sequence()

    def turn_end_sequence(self):
        for m in self.manager_list:
            m.turn_end_sequence()