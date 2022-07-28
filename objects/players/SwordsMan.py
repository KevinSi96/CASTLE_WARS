import time

from objects.players.Player import Player
import pygame as pg


class SwordMan(Player):
    TRAIN_TURNS = 2
    RANGE = 10
    HIT_DAMAGE = 3
    REST = 1
    COST = 10
    SPEED = 5
    PLAYER1_READY = "sprites/player1/sword/ready.png"
    PLAYER2_READY = "sprites/player2/sword/ready.png"
    PLAYER1_RUN = {"root": "sprites/player1/sword/run/run-", "extension": ".png"}
    PLAYER2_RUN = {"root": "sprites/player2/sword/run/run-", "extension": ".png"}
    PLAYER1_SHOOT = {"root": "sprites/player1/sword/attack/attack-", "extension": ".png"}
    PLAYER2_SHOOT = {"root": "sprites/player2/sword/attack/attack-", "extension": ".png"}

    def __init__(self, health, x, y, deploy, screen, type):
        super().__init__(health, x, y, deploy)
        self.turns = 0
        self.current_time = 0
        self.start_shoot = 0
        self.attacking = False
        self.attack_count = 0
        self.swordsman_added = False
        self.type = type
        match type:
            case "p1":
                self.animation = self.loadImage(self.PLAYER1_RUN.get("root"), self.PLAYER1_RUN.get("extension"), 11)
            case "p2":
                self.animation = self.loadImage(self.PLAYER2_RUN.get("root"), self.PLAYER2_RUN.get("extension"), 11)
        self.start_time = time.time()
        self.screen = screen
        self.rect = self.image.get_rect()

    def attack(self, player):
        if not self.run and self.attack_count == 0:
            self.attack_count += 1
            match player:
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
        self.animation = self.loadImage(image_path_root, img_extension, 8)

    def update(self):
        self.a_count += 1
        if self.a_count == len(self.animation):
            self.a_count = 0
        self.image = self.animation[self.a_count]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if self.run:
            match self.type:
                case "p1":
                    self.x += self.SPEED
                case "p2":
                    self.x -= self.SPEED

    def train(self):
        print("training sword")
        if round(self.current_time - self.start_time) < self.TRAIN_TURNS:
            self.current_time = time.time()
        # we set ready to dispatch once the training time is done, then in the main when the dispatch order is issued, the dispatch variable gets set to True
        # and the soldiers gets deployed into the battle field
        else:
            print("ready ready sword")
            self.ready_to_dispatch = True

    def rest(self):
        if self.REST > (self.current_time - self.start_shoot):
            self.current_time = time.time()
            # print("rest timer: " + str(self.current_time - self.start_shoot))
            return False
        else:
            return True
