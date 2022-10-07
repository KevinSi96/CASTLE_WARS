import time

import pygame as pg

from implementable import Functions
from objects.Constants import WORKER_PROD, WORKER_REPAIR, WORKER_TRAIN, BARRACKS_POS, SCREEN_WIDTH, GROUND_HEIGHT, \
    SCREEN_HEIGHT, WORKER_SPEED, WALL_HEALTH
from objects.Wall import Wall


class Worker:
    PRODUCTION_RATE = WORKER_PROD
    REPAIR_RATE = WORKER_REPAIR
    TRAINING_TIME = WORKER_TRAIN
    SPEED = WORKER_SPEED

    PLAYER1_READY = "sprites/player1/worker/ready.png"
    PLAYER2_READY = "sprites/player2/worker/ready.png"
    PLAYER1_RUN = {"root": "sprites/player1/worker/run/run-", "extension": ".png"}
    PLAYER2_RUN = {"root": "sprites/player2/worker/run/run-", "extension": ".png"}
    PLAYER1_DIG = {"root": "sprites/player1/worker/dig/dig-", "extension": ".png"}
    PLAYER2_DIG = {"root": "sprites/player2/worker/dig/dig-", "extension": ".png"}
    PLAYER1_REPAIR = {"root": "sprites/player1/worker/repair/repair-", "extension": ".png"}
    PLAYER2_REPAIR = {"root": "sprites/player2/worker/repair/repair-", "extension": ".png"}

    def __init__(self, player):
        self.production_rate = self.PRODUCTION_RATE
        self.repair_rate = self.REPAIR_RATE
        self.speed = Worker.SPEED
        self.a_count = 0
        self.start_action = 0
        self.ready_to_dispatch = False
        self.added = False
        self.deploy = False
        self.start_time = 0
        self.current_time = 0
        self.player = player
        self.x = BARRACKS_POS if player.player_type == "p1" else SCREEN_WIDTH - BARRACKS_POS
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.run = False
        self.player_type = player.player_type
        self.animation = None
        self.image = pg.image.load(Worker.PLAYER1_READY if self.player_type == "p1" else Worker.PLAYER2_READY)
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        self.run_to_mine = False
        self.run_to_wall = False
        self.digging = False
        self.repairing = False
        self.start_time = time.time()

    def to_wall(self):
        self.animation = Functions.loadImage(self.PLAYER1_RUN if self.player_type == "p1" else self.PLAYER2_RUN, 6,
                                             False)
        self.run = True
        if self.player.castle.wall.rect.centerx > self.rect.centerx:
            if self.speed < 0 and self.run_to_wall:
                self.speed *= -1

        elif self.player.castle.wall.rect.centerx < self.rect.centerx:
            if self.speed < 0 and self.run_to_wall:
                self.speed *= -1

    def to_mine(self):
        self.animation = Functions.loadImage(self.PLAYER1_RUN if self.player_type == "p1" else self.PLAYER2_RUN, 6,
                                             True)
        self.run = True
        if self.player.castle.mine.rect.centerx < self.rect.centerx:
            if self.speed > 0 and self.run_to_mine:
                self.speed *= -1
            elif self.speed < 0 and not self.run_to_mine:
                self.speed *= -1

        elif self.player.castle.mine.rect.centerx > self.rect.centerx:
            if self.speed > 0 and self.run_to_mine:
                self.speed *= -1
            elif self.speed < 0 and not self.run_to_mine:
                self.speed *= -1
    def move(self):
        if self.run:
            match self.player_type:
                case "p1":
                    self.x += self.speed
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))

                case "p2":
                    self.x -= self.speed
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def dig(self):
        self.animation = Functions.loadImage(self.PLAYER1_DIG if self.player_type == "p1" else self.PLAYER2_DIG, 9,
                                             True)

    def repair(self):
        self.animation = Functions.loadImage(self.PLAYER1_REPAIR if self.player_type == "p1" else self.PLAYER2_REPAIR,
                                             4,
                                             False)

    def update(self):

        if self.rect.collidepoint(self.player.castle.mine.rect.centerx,
                                  self.player.castle.mine.rect.centery) and not self.digging:
            self.run = False
            self.digging = True
            self.repairing = False
            self.run_to_mine = False

        elif self.rect.colliderect(self.player.castle.wall.rect) and not self.repairing:
            self.run = False
            self.digging = False
            self.repairing = True
            self.run_to_wall = False

        if self.digging and not self.run and self.a_count >= 8:
            if self.rest(1):
                self.player.player_resource += self.production_rate
                self.a_count = 0
                self.start_action = time.time()

        elif self.repairing and not self.run and self.a_count >= 3:
            if self.rest(1):
                self.a_count = 0
                if self.player.castle.wall.health < Wall.MAX_HEALTH:
                    self.player.castle.wall.health += self.repair_rate
                self.start_action = time.time()
        else:
            if self.run:
                self.a_count += 0.1
            else:
                self.a_count += 0.2
            if self.a_count > len(self.animation):
                self.a_count = 0
            self.image = self.animation[int(self.a_count)]
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def train(self):
        if round(self.current_time - self.start_time) < self.TRAINING_TIME:
            self.current_time = time.time()
        else:
            self.ready_to_dispatch = True

    def rest(self, rest_amount):
        if rest_amount > (self.current_time - self.start_action):
            self.current_time = time.time()
            return False
        else:
            return True
