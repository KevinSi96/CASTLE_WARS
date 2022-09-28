import time

import pygame as pg

from implementable import Functions
from objects.Arrow import Arrow
from objects.Constants import BARRACKS_POS, SCREEN_WIDTH, GROUND_HEIGHT, SCREEN_HEIGHT, ARCHER_SPEED, ARCHER_DAMAGE, \
    ARCHER_TRAIN, ARCHER_RANGE, ARCHER_REST, ARCHER_COST
from objects.Wall import Wall


class Archer:
    TRAIN_TURNS = ARCHER_TRAIN
    RANGE = ARCHER_RANGE
    HIT_DAMAGE = ARCHER_DAMAGE
    REST = ARCHER_REST
    COST = ARCHER_COST
    SPEED = ARCHER_SPEED

    PLAYER1_READY = "sprites/player1/bow/ready.png"
    PLAYER2_READY = "sprites/player2/bow/ready.png"
    PLAYER1_RUN = {"root": "sprites/player1/bow/run/run-", "extension": ".png"}
    PLAYER2_RUN = {"root": "sprites/player2/bow/run/run-", "extension": ".png"}
    PLAYER1_SHOOT = {"root": "sprites/player1/bow/shoot/shoot-", "extension": ".png"}
    PLAYER2_SHOOT = {"root": "sprites/player2/bow/shoot/shoot-", "extension": ".png"}
    PLAYER1_FALLEN = {"root": "sprites/player1/bow/fallen/fallen-", "extension": ".png"}
    PLAYER2_FALLEN = {"root": "sprites/player2/bow/fallen/fallen-", "extension": ".png"}

    def __init__(self, player_type):
        self.target_unit = None
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
        self.image = pg.image.load(Archer.PLAYER1_READY if player_type == "p1" else Archer.PLAYER2_READY)
        self.current_time = 0
        self.start_shoot = 0
        self.shooting = False
        self.archer_added = False
        self.player_type = player_type
        self.arrows = []

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

    def ready_to_shoot(self):
        if not self.falling and not self.dead:
            if not self.run and not self.shooting:
                self.start_shoot = time.time()
                match self.player_type:
                    case "p1":
                        self.image = pg.image.load(self.PLAYER1_READY)
                        if not self.shooting:
                            self.shooting = True
                            self.a_count = 0
                            self.load_shoot(self.PLAYER1_SHOOT.get("root"), self.PLAYER1_SHOOT.get("extension"))
                            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

                    case "p2":
                        self.image = pg.image.load(self.PLAYER2_READY)
                        if not self.shooting:
                            self.shooting = True
                            self.a_count = 0
                            self.load_shoot(self.PLAYER2_SHOOT.get("root"), self.PLAYER2_SHOOT.get("extension"))
                            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def load_dead(self):
        if self.falling:
            match self.player_type:
                case "p1":
                    self.animation = Functions.loadImage(self.PLAYER1_FALLEN.get("root"),
                                                         self.PLAYER1_FALLEN.get("extension"), 6)

                case "p2":
                    self.animation = Functions.loadImage(self.PLAYER2_FALLEN.get("root"),
                                                         self.PLAYER2_FALLEN.get("extension"), 6)

    def update(self):
        self.range.midbottom = self.rect.midbottom

        if not self.dead:
            if self.shooting and not self.falling and not self.run:
                arrow = None
                if self.rest(self.REST):
                    match self.player_type:
                        case "p1":
                            arrow = Arrow(self.rect.right, self.rect.centery, "sprites/player1/bow/arrow_hor/arrowhor-",
                                          ".png", True, 0)
                        case "p2":
                            arrow = Arrow(self.rect.left, self.rect.centery, "sprites/player2/bow/arrow_hor/arrowhor-",
                                          ".png", False, 0)
                    arrow.shoot = True
                    self.arrows.append(arrow)
                    self.a_count = 1
                    self.image = self.animation[self.a_count]
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))
                    self.start_shoot = time.time()
                elif self.rest(1):
                    self.a_count = 0
                    self.image = self.animation[self.a_count]
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))
            else:
                self.image = self.animation[int(self.a_count)]
                self.rect = self.image.get_rect(midbottom=(self.x, self.y))
                if not self.falling:
                    self.a_count += 0.2
                else:
                    self.a_count += 0.1
                if self.a_count > len(self.animation):
                    self.a_count = 0
                if self.falling and int(self.a_count) > 4:
                    self.dead = True
                    self.falling = False
            if self.target_unit is not None and not isinstance(self.target_unit, Wall) and self.target_unit.dead:
                self.run = True
                self.shooting = False
                self.arrows.clear()
                self.load_run()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for arrow in self.arrows:
            arrow.draw_arrows(screen)

    def move(self):
        if self.run:
            match self.player_type:
                case "p1":
                    self.x += Archer.SPEED
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))
                case "p2":
                    self.x -= Archer.SPEED
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def move_arrows(self, obj):
        self.target_unit = obj
        for i, arrow in enumerate(self.arrows):
            arrow.move_arrow()
            if arrow.rect.colliderect(obj.rect) and obj.health > 0:
                obj.health -= self.HIT_DAMAGE
                del self.arrows[i]

    def load_shoot(self, image_path_root, img_extension):
        self.animation = Functions.loadImage(image_path_root, img_extension, 2)

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
