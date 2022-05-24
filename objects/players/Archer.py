import os
import pygame as pg

from objects.players.Player import Player


class Archer(Player, pg.sprite.Sprite):

    TRAIN_TURNS = 3
    RANGE = 10
    HIT_DAMAGE = 3
    REST = 1
    COST = 3
    SPEED = 5

    def __init__(self, health, x, y, deploy, screen):
        super().__init__(health, x, y, deploy)
        self.a_count = 0
        self.deploy = deploy
        self.animation = self.loadImage()
        self.rect = self.image.get_rect()
        self.draw(screen)

    def loadImage(self):
        images = {}
        for i in range(11):
            print(str(i))
            self.image = pg.image.load("sprites/player1/bow/run/run-" + str(i) + ".png")
            images[i] = self.image
        return images

    def update(self):
        self.a_count += 1
        if self.a_count == len(self.animation):
            self.a_count = 0
        self.image = self.animation[self.a_count]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.SPEED
