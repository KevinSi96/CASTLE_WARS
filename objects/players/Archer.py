import random
import time

import pygame as pg

from implementable import Functions
from objects.Arrow import Arrow
from objects.Constants import BARRACKS_POS, SCREEN_WIDTH, GROUND_HEIGHT, SCREEN_HEIGHT, ARCHER_SPEED, ARCHER_DAMAGE, \
    ARCHER_TRAIN, ARCHER_RANGE, ARCHER_REST, ARCHER_COST, ARCHER_HEALTH
from objects.Wall import Wall


class Archer:
    TRAIN_TIME = ARCHER_TRAIN
    RANGE = ARCHER_RANGE
    HIT_DAMAGE = ARCHER_DAMAGE
    REST = ARCHER_REST
    COST = ARCHER_COST
    SPEED = ARCHER_SPEED
    MAX_HEALTH = ARCHER_HEALTH

    PLAYER1_READY = "sprites/player1/bow/ready.png"
    PLAYER2_READY = "sprites/player2/bow/ready.png"
    PLAYER1_RUN = {"root": "sprites/player1/bow/run/run-", "extension": ".png"}
    PLAYER2_RUN = {"root": "sprites/player2/bow/run/run-", "extension": ".png"}
    PLAYER1_SHOOT = {"root": "sprites/player1/bow/shoot/shoot-", "extension": ".png"}
    PLAYER2_SHOOT = {"root": "sprites/player2/bow/shoot/shoot-", "extension": ".png"}
    PLAYER1_FALLEN = {"root": "sprites/player1/bow/fallen/fallen-", "extension": ".png"}
    PLAYER2_FALLEN = {"root": "sprites/player2/bow/fallen/fallen-", "extension": ".png"}
    PLAYER1_ARROW = {"root": "sprites/player1/bow/", "extension": ".png"}
    PLAYER2_ARROW = {"root": "sprites/player2/bow/", "extension": ".png"}

    def __init__(self, player_type):
        self.hb_width = 15
        self.target_unit = None
        self.animation = None
        self.deploy = False
        self.ready_to_dispatch = False
        self.health = Archer.MAX_HEALTH
        self.falling = False
        self.run = False
        self.wait = True
        self.dead = False
        self.enemy_killed = False
        self.a_count = 0
        self.x = BARRACKS_POS if player_type == "p1" else SCREEN_WIDTH - BARRACKS_POS
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.image = pg.image.load(Archer.PLAYER1_READY if player_type == "p1" else Archer.PLAYER2_READY)
        self.current_time = 0
        self.start_action = 0
        self.shooting = False
        self.added = False
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
                    self.animation = Functions.loadImage(self.PLAYER1_RUN, 11, False)
                case "p2":
                    self.animation = Functions.loadImage(self.PLAYER2_RUN, 11, False)

    def ready_to_shoot(self):
        if not self.falling and not self.dead:
            if not self.run and not self.shooting:
                self.start_action = time.time()
                match self.player_type:
                    case "p1":
                        self.image = pg.image.load(self.PLAYER1_READY)
                        if not self.shooting:
                            self.shooting = True
                            self.a_count = 0
                            self.load_shoot(self.PLAYER1_SHOOT)
                            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

                    case "p2":
                        self.image = pg.image.load(self.PLAYER2_READY)
                        if not self.shooting:
                            self.shooting = True
                            self.a_count = 0
                            self.load_shoot(self.PLAYER2_SHOOT)
                            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def load_dead(self):
        if self.falling:
            match self.player_type:
                case "p1":
                    self.animation = Functions.loadImage(self.PLAYER1_FALLEN, 6, False)

                case "p2":
                    self.animation = Functions.loadImage(self.PLAYER2_FALLEN, 6, False)

    def update(self):
        self.range.midbottom = self.rect.midbottom

        if not self.dead:
            if self.shooting and not self.falling and not self.run:
                arrow = None
                self.enemy_killed = False

                if self.rest(self.REST):
                    match self.player_type:
                        case "p1":
                            arrow = Arrow(self.rect.right, self.rect.centery, self.PLAYER1_ARROW, True, 0)
                        case "p2":
                            arrow = Arrow(self.rect.left, self.rect.centery, self.PLAYER2_ARROW, False, 0)
                    arrow.shoot = True
                    self.arrows.append(arrow)
                    self.a_count = 1
                    self.image = self.animation[self.a_count]
                    self.rect = self.image.get_rect(midbottom=(self.x, self.y))
                    self.start_action = time.time()
                elif self.rest(random.randint(1, 10) * 0.1):
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
                self.shooting = False
                self.load_run()
                if self.rest(random.randint(1, 2)):
                    self.run = True
                elif not self.enemy_killed and not self.run:
                    self.image = pg.image.load(
                        Archer.PLAYER1_READY if self.player_type == "p1" else Archer.PLAYER2_READY)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for arrow in self.arrows:
            arrow.draw_arrows(screen)
        if not self.dead and self.health < self.MAX_HEALTH:
            self.draw_health_bar(screen)

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
            if arrow.rect.colliderect(obj.rect) and self.arrows and obj.health > 0:
                obj.health -= self.HIT_DAMAGE
                del self.arrows[i]
            elif obj.health <= 0:
                self.enemy_killed = True
                del self.arrows[i]

    def load_shoot(self, image_map):
        self.animation = Functions.loadImage(image_map, 2, False)

    def rest(self, rest_amount):
        if rest_amount > (self.current_time - self.start_action):
            self.current_time = time.time()
            return False
        else:
            return True

    def train(self):
        if round(self.current_time - self.start_time) < self.TRAIN_TIME:
            self.current_time = time.time()
        else:
            self.ready_to_dispatch = True

    def draw_health_bar(self, screen):
        red_hb_rect = pg.Rect(self.x, self.y - 5, self.hb_width, 3)
        red_hb_rect.center = (self.x, self.y - self.rect.h - 5)
        pg.draw.rect(screen, (255, 0, 0), red_hb_rect)

        green_hb_rect = pg.Rect(self.x, self.y - 5, self.hb_width * (self.health / self.MAX_HEALTH), 3)
        green_hb_rect.topleft = red_hb_rect.topleft
        pg.draw.rect(screen, (0, 255, 0), green_hb_rect)
