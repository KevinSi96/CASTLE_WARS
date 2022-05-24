from abc import abstractmethod, ABC


class Arrow(ABC):
    def __init__(self, arrow_speed, position_X, position_Y):
        self.arrow_speed = arrow_speed
        self.position_X = position_X
        self.position_Y = position_Y

    @abstractmethod
    def hit(self, position_X, position_Y, target_X, target_Y ):
        ...