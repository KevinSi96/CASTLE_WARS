import time

import pygame as pg

from implementable import Functions
from objects.Constants import BARRACKS_POS, SCREEN_WIDTH, GROUND_HEIGHT, SCREEN_HEIGHT, SWORD_RANGE, SWORD_TRAIN, \
    SWORD_DAMAGE, SWORD_REST, SWORD_COST, SWORD_SPEED


class SwordsMan:
    TRAIN_TURNS = SWORD_TRAIN
    RANGE = SWORD_RANGE
    HIT_DAMAGE = SWORD_DAMAGE
    REST = SWORD_REST
    COST = SWORD_COST
    SPEED = SWORD_SPEED

    PLAYER1_READY = "sprites/player1/sword/ready.png"
    PLAYER2_READY = "sprites/player2/sword/ready.png"
    PLAYER1_RUN = {"root": "sprites/player1/sword/run/run-", "extension": ".png"}
    PLAYER2_RUN = {"root": "sprites/player2/sword/run/run-", "extension": ".png"}
    PLAYER1_SHOOT = {"root": "sprites/player1/sword/attack/attack-", "extension": ".png"}
    PLAYER2_SHOOT = {"root": "sprites/player2/sword/attack/attack-", "extension": ".png"}

    def __init__(self, player_type):
        self.animation = None
        self.deploy = False
        self.ready_to_dispatch = False
        self.health = 100
        self.falling = False
        self.run = False
        self.dead = False
        self.a_count = 0
        self.x = BARRACKS_POS if player_type == "p1" else SCREEN_WIDTH - BARRACKS_POS
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.image = pg.image.load(SwordsMan.PLAYER1_READY if player_type == "p1" else SwordsMan.PLAYER2_READY)
        self.current_time = 0
        self.start_attack = 0
        self.attacking = False
        self.swordsman_added = False
        self.player_type = player_type
        self.target_unit = None

        self.start_time = time.time()
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

        self.range = pg.Rect(0, 0, self.rect.w + (self.RANGE * 2), self.rect.h)
        self.range.midbottom = self.rect.midbottom

    def load_run(self):
        if self.run:
            match self.player_type:
                case "p1":
                    self.animation = Functions.loadImage(self.PLAYER1_RUN.get("root"),
                                                         self.PLAYER1_RUN.get("extension"),
                                                         11)
                case "p2":
                    self.animation = Functions.loadImage(self.PLAYER2_RUN.get("root"),
                                                         self.PLAYER2_RUN.get("extension"),
                                                         11)

    def attack(self, target):
        self.target_unit = target
        if not self.falling and not self.dead:
            if not self.run and not self.attacking:
                match self.player_type:
                    case "p1":
                        self.image = pg.image.load(self.PLAYER1_READY)
                        if not self.attacking:
                            self.attacking = True
                            self.a_count = 0
                            self.load_attack(self.PLAYER1_SHOOT.get("root"), self.PLAYER1_SHOOT.get("extension"))
                    case "p2":
                        self.image = pg.image.load(self.PLAYER2_READY)
                        if not self.attacking:
                            self.attacking = True
                            self.a_count = 0
                            self.load_attack(self.PLAYER2_SHOOT.get("root"), self.PLAYER2_SHOOT.get("extension"))

    def load_attack(self, image_path_root, img_extension):
        self.animation = Functions.loadImage(image_path_root, img_extension, 8)

    def update(self):
        self.range.midbottom = self.rect.midbottom
        if not self.dead:
            if not self.falling:
                self.a_count += 0.2
            else:
                self.a_count += 0.1
            if self.a_count > len(self.animation):
                self.a_count = 0
            self.image = self.animation[int(self.a_count)]
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        if self.run:
            match self.player_type:
                case "p1":
                    self.x += self.SPEED
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))

                case "p2":
                    self.x -= self.SPEED
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def train(self):
        if round(self.current_time - self.start_time) < self.TRAIN_TURNS:
            self.current_time = time.time()
        # we set ready to dispatch once the training time is done, then in the main when the dispatch order is issued, the dispatch variable gets set to True
        # and the soldiers gets deployed into the battle field
        else:
            self.ready_to_dispatch = True

    def rest(self):
        if self.REST > (self.current_time - self.start_attack):
            self.current_time = time.time()
            # print("rest timer: " + str(self.current_time - self.start_shoot))
            return False
        else:
            return True
