from abc import (
  ABC,
  abstractmethod
)

import pygame as pg


class GameObject(ABC):
    def __init__(self, health, x, y):
        super().__init__()
        self.health = health
        self.x = x
        self.y = y
