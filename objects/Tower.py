import math
import time

import pygame as pg

from objects.Arrow import Arrow
from objects.Constants import GROUND_HEIGHT, SCREEN_HEIGHT


class Tower:
    RANGE = 200
    TOWER_HIT = 10
    TOWER_REST = 1

    PLAYER1_ARROW = {"root": f"sprites/player1/bow/", "extension": ".png"}
    PLAYER2_ARROW = {"root": f"sprites/player2/bow/", "extension": ".png"}

    def __init__(self, img, tower_x, player_type):
        self.start_action = 0
        self.current_time = 0
        self.target_unit = None
        self.img = img
        self.player_type = True if player_type == "p1" else False
        self.rect = self.img.get_rect(midbottom=(tower_x, SCREEN_HEIGHT - GROUND_HEIGHT))
        self.arrows = []
        self.resting = True
        self.attacking = False

        self.range = pg.Rect(0, 0, self.rect.w + (self.RANGE * 2), self.rect.h)
        self.range.midbottom = self.rect.midbottom

    def update(self, target):
        if self.attacking and not self.resting:
            if self.rest(1):
                x = abs(self.rect.centerx - target.rect.centerx)
                y = target.rect.centery - self.rect.top
                arrow_angle = math.atan(y / x)
                arrow = Arrow(self.rect.centerx, self.rect.top,
                              self.PLAYER1_ARROW if self.player_type else self.PLAYER2_ARROW,
                              self.player_type, arrow_angle)
                arrow.shoot = True
                self.start_action = time.time()
                self.arrows.append(arrow)

        self.move_arrows(target)

    def rest(self, rest_amount):
        if rest_amount > (self.current_time - self.start_action):
            self.current_time = time.time()
            return False
        else:
            return True

    def move_arrows(self, obj):
        self.target_unit = obj
        for i, arrow in enumerate(self.arrows):
            arrow.move_arrow()
            if arrow.rect.colliderect(obj.rect) and self.arrows:
                obj.health -= self.TOWER_HIT
                del self.arrows[i]
            if arrow.y > SCREEN_HEIGHT - GROUND_HEIGHT:
                del self.arrows[i]

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        for arrow in self.arrows:
            arrow.draw_arrows(screen)
