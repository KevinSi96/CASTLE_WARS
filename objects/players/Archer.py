import os
import time

import pygame as pg

from objects.players.Player import Player


class Archer(Player, pg.sprite.Sprite):
    TRAIN_TURNS = 3
    RANGE = 10
    HIT_DAMAGE = 3
    REST = 2
    COST = 3
    SPEED = 5

    def __init__(self, health, x, y, deploy, screen, image_path_root, img_extension):
        super().__init__(health, x, y, deploy)
        self.shoot_count = 0
        self.a_count = 0
        self.current_time = 0
        self.start_shoot = 0
        self.archer_added = False
        self.run = False
        self.dead = False
        self.deploy = False
        self.ready_to_dispatch = False
        self.animation = self.loadImage(image_path_root, img_extension, 11)
        self.start_time = time.time()
        self.screen = screen
        self.rect = self.image.get_rect()

    def ready_to_shoot(self):
        if self.run is False and self.shoot_count == 0:
            self.start_shoot = time.time()
            self.shoot_count += 1
        self.image = pg.image.load("sprites/player1/bow/ready.png")
        if self.rest():
            self.shoot()
            self.shoot_count = 0

    def loadImage(self, image_path_root, img_extension, num_img):
        images = {}
        for i in range(num_img):
            self.image = pg.image.load(image_path_root + str(i) + img_extension)
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
        if self.run:
            self.x += self.SPEED

    def shoot(self):
        self.animation = self.loadImage("sprites/player1/bow/shoot/shoot-", ".png", 2)

    def rest(self):
        if self.REST > (self.current_time - self.start_shoot):
            self.current_time = time.time()
            # print("rest timer: " + str(self.current_time - self.start_shoot))
            return False
        else:
            return True

    def train(self):
        if round(self.current_time - self.start_time) < self.TRAIN_TURNS:
            self.current_time = time.time()
        else:
            self.ready_to_dispatch = True
    # we set ready to dispatch once the training time is done, then in the main when the dispatch order is issued, the dispatch variable gets set to True
    # and the soldiers gets deployed into the battle field
