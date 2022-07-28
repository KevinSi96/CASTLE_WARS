import os
import time

import pygame as pg

from objects.Arrow import Arrow
from objects.players.Player import Player


class Archer(Player):
    TRAIN_TURNS = 3
    RANGE = 10
    HIT_DAMAGE = 3
    REST = 3
    COST = 3
    SPEED = 5
    PLAYER1_READY = "sprites/player1/bow/ready.png"
    PLAYER2_READY = "sprites/player2/bow/ready.png"
    PLAYER1_RUN = {"root": "sprites/player1/bow/run/run-", "extension": ".png"}
    PLAYER2_RUN = {"root": "sprites/player2/bow/run/run-", "extension": ".png"}
    PLAYER1_SHOOT = {"root": "sprites/player1/bow/shoot/shoot-", "extension": ".png"}
    PLAYER2_SHOOT = {"root": "sprites/player2/bow/shoot/shoot-", "extension": ".png"}

    def __init__(self, health, x, y, deploy, screen, type):
        super().__init__(health, x, y, deploy)
        self.shoot_count = 0
        self.a_count = 0
        self.current_time = 0
        self.start_shoot = 0
        self.archer_added = False
        self.type = type
        self.arrows = []
        self.shooting = False

        match type:
            case "p1":
                self.animation = self.loadImage(self.PLAYER1_RUN.get("root"), self.PLAYER1_RUN.get("extension"), 11)
            case "p2":
                self.animation = self.loadImage(self.PLAYER2_RUN.get("root"), self.PLAYER2_RUN.get("extension"), 11)
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
                        self.load_shoot(self.PLAYER1_SHOOT.get("root"), self.PLAYER1_SHOOT.get("extension"))
                case "p2":
                    self.image = pg.image.load(self.PLAYER2_READY)
                    if not self.shooting:
                        self.shooting = True
                        self.a_count = 0
                        self.load_shoot(self.PLAYER2_SHOOT.get("root"), self.PLAYER2_SHOOT.get("extension"))

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
                match self.type:
                    case "p1":
                        arrow = Arrow(self.x, self.y + 5, "sprites/player1/bow/arrow_hor/arrowhor-", ".png")
                        arrow.shoot = True
                        self.arrows.append(arrow)
                    case "p2":
                        arrow = Arrow(self.x, self.y + 5, "sprites/player2/bow/arrow_hor/arrowhor-", ".png")
                        arrow.shoot = True
                        self.arrows.append(arrow)
                self.image = self.animation[1]
                self.start_shoot = time.time()
            elif self.rest(1):
                self.image = self.animation[0]

        else:
            self.image = self.animation[self.a_count]
            self.a_count += 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for arrow in self.arrows:
            arrow.draw_arrows(screen)

    def move(self):
        if self.run:
            match self.type:
                case "p1":
                    self.x += self.SPEED
                case "p2":
                    self.x -= self.SPEED

    def move_arrows(self):
        for arrow in self.arrows:
            arrow.move_arrow(self.type)

    def load_shoot(self, image_path_root, img_extension):
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
