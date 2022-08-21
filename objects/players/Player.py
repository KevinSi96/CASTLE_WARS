import os
from glob import glob
import pygame as pg

from objects.GameObject import GameObject


class Player(GameObject, pg.sprite.Sprite):
    def __init__(self, health, x, y, dispatch):
        super().__init__(health, x, y)
        self.dispatch = dispatch
        self.run = False
        self.dead = False
        self.falling = False
        self.deploy = False
        self.a_count = 0
        self.ready_to_dispatch = False

    def loadImage(self, image_path_root, img_extension, num_img):
        images = {}
        for i in range(num_img):
            self.image = pg.image.load(image_path_root + str(i) + img_extension)
            images[i] = self.image
        return images
