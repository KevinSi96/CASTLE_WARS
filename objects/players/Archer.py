import os
import time

import pygame as pg

from objects.players.Player import Player


class Archer(Player, pg.sprite.Sprite):
    TRAIN_TURNS = 3
    RANGE = 10
    HIT_DAMAGE = 3
    REST = 3
    COST = 3
    SPEED = 5
    PLAYER1_READY = "sprites/player1/bow/ready.png"
    PLAYER1_SHOOT = ["sprites/player1/bow/shoot/shoot-", ".png"]
    PLAYER2_READY = "sprites/player2/bow/ready.png"
    PLAYER2_SHOOT = ["sprites/player2/bow/shoot/shoot-", ".png"]

    def __init__(self, health, x, y, deploy, screen, image_path_root, img_extension):
        super().__init__(health, x, y, deploy)
        self.shoot_count = 0
        self.a_count = 0
        self.current_time = 0
        self.start_shoot = 0
        self.archer_added = False
        self.shooting = False
        self.run = False
        self.dead = False
        self.deploy = False
        self.ready_to_dispatch = False
        self.animation = self.loadImage(image_path_root, img_extension, 11)
        self.start_time = time.time()
        self.screen = screen
        self.rect = self.image.get_rect()

    def ready_to_shoot(self, player):
        if not self.run and self.shoot_count == 0:
            self.start_shoot = time.time()
            self.shoot_count += 1
            match player:
                case "p1":
                    self.image = pg.image.load(self.PLAYER1_READY)
                    if not self.shooting:
                        self.shooting = True
                        self.a_count = 0
                        self.shoot(self.PLAYER1_SHOOT[0], self.PLAYER1_SHOOT[1])
                        self.rest_amount = self.REST
                case "p2":
                    if not self.shooting:
                        self.image = pg.image.load(self.PLAYER2_READY)
                        self.shooting = True
                        self.shoot(self.PLAYER1_SHOOT[0], self.PLAYER1_SHOOT[1])

    def loadImage(self, image_path_root, img_extension, num_img):
        images = {}
        for i in range(num_img):
            self.image = pg.image.load(image_path_root + str(i) + img_extension)
            images[i] = self.image
        return images

    def update(self):
        if self.a_count == len(self.animation):
            self.a_count = 0

        if self.shooting:
            if self.rest(self.REST):
                self.image = self.animation[1]
                self.start_shoot = time.time()
            elif self.rest(1):
                self.image = self.animation[0]

        else:
            self.image = self.animation[self.a_count]
            self.a_count += 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if self.run:
            self.x += self.SPEED

    def shoot(self, image_path_root, img_extension):
        self.animation = self.loadImage(image_path_root, img_extension, 2)

    def rest(self, rest_amount):
        if rest_amount > (self.current_time - self.start_shoot):
            self.current_time = time.time()
            return False
        else:
            return True

    def train(self):
        if round(self.current_time - self.start_time) < self.TRAIN_TURNS:
            self.current_time = time.time()
        else:
            self.ready_to_dispatch = True

    def falling(self, image_path_root, img_extension, num_img):
        self.animation = self.loadImage(image_path_root, img_extension, 6)
    # we set ready to dispatch once the training time is done, then in the main when the dispatch order is issued, the dispatch variable gets set to True
    # and the soldiers gets deployed into the battle field
