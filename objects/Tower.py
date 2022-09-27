import math

import pygame as pg

from objects.Arrow import Arrow
from objects.Constants import GROUND_HEIGHT, SCREEN_HEIGHT


class Tower:
    RANGE = 100
    TOWER_HIT = 10
    TOWER_REST = 1

    def __init__(self, img, tower_x, player):
        self.player_type = player
        self.img = img
        self.rect = self.img.get_rect(midbottom=(tower_x, SCREEN_HEIGHT - GROUND_HEIGHT))
        self.arrows = []

        # Resting cooldown
        self.attack_timer = 0

        # Tower's states
        self.resting = True
        self.attacking = False
        self.range = pg.Rect(0, 0, self.rect.w + (self.RANGE * 2), self.rect.h)


    def rest(self):
        pass

    def attack(self, target):
        x = abs(self.rect.centerx - target.rect.centerx)
        y = target.rect.centery - self.rect.top
        arrow_angle = math.atan(y / x)

        self.arrows.append(Arrow(self.rect.centerx, self.rect.top, self.player_type, arrow_angle))
        self.attack_timer = pg.time.get_ticks()

    def update(self, target, enemy_units):
        # Updates all the arrows positions
        for i, arrow in enumerate(self.arrows):
            arrow.update()

            # If the arrow hits the ground, it disappears
            if arrow.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
                del self.arrows[i]

            # Check if arrow collides with enemy unit
            for unit in enemy_units:
                if unit.alive and arrow.rect.colliderect(unit.rect) and self.arrows:
                    unit.health -= Tower.TOWER_HIT
                    del self.arrows[i]

        # Calls the right function according to the character state
        if self.resting:
            self.rest()
        elif self.attacking:
            self.attack(target)

        # Checks if the rest time is over and if the target is in range
        if pg.time.get_ticks() - self.attack_timer >= self.rest_time and abs(
                self.rect.centerx - target.rect.centerx) <= Tower.TOWER_RANGE:
            self.attacking = True
            self.resting = False
        else:
            self.attacking = False
            self.resting = True

    def draw(self, screen):
        # Draws all the arrows
        for arrow in self.arrows:
            arrow.draw(screen)

        # Draws the tower
        screen.blit(self.img, self.rect)
