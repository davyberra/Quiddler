from abc import ABC, abstractmethod


class Manager(ABC):
    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def round_start_sequence(self):
        pass

    @abstractmethod
    def round_end_sequence(self):
        pass

    @abstractmethod
    def turn_start_sequence(self):
        pass

    @abstractmethod
    def turn_end_sequence(self):
        pass
