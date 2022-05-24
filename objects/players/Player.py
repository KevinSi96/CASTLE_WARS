import os
from glob import glob
import pygame as pg

from objects.GameObject import GameObject


class Player(GameObject):
    def __init__(self, health, x, y, deploy):
        super().__init__(health, x, y)
        self.deploy = deploy




