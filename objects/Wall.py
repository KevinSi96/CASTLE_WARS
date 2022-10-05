import pygame as pg

from objects.Constants import GROUND_HEIGHT, SCREEN_HEIGHT, WALL_HEALTH


class Wall:
    MAX_HEALTH = WALL_HEALTH

    def __init__(self, img, wall_x):
        self.img = img
        self.x = wall_x
        self.rect = self.img.get_rect(midbottom=(wall_x, SCREEN_HEIGHT - GROUND_HEIGHT))
        # Wall health variables
        self.health = self.MAX_HEALTH
        self.dead = self.health <= 0
        self.hb_width = 50

    def draw_health_bar(self, screen):
        # Red part of the health bar
        red_hb_rect = pg.Rect(0, 0, self.hb_width, 6)
        red_hb_rect.center = (self.rect.centerx, (self.rect.top // 2) - 15)
        pg.draw.rect(screen, (255, 0, 0), red_hb_rect)

        # Green part of the health bar
        green_hb_rect = pg.Rect(0, 0, self.hb_width * (self.health / self.MAX_HEALTH), 6)
        green_hb_rect.topleft = red_hb_rect.topleft
        pg.draw.rect(screen, (0, 255, 0), green_hb_rect)

    def draw(self, screen):
        screen.blit(self.img, self.rect)

        # If the walls health is lower than the max health, show health bar
        if self.health < self.MAX_HEALTH:
            self.draw_health_bar(screen)