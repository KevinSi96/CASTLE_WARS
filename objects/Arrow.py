import math

import pygame as pg


class Arrow(pg.sprite.Sprite):
    SPEED = 5

    def __init__(self, position_X, position_Y, img_root, img_extension, player, angle):
        super().__init__()
        self.shoot = False
        self.x = position_X
        self.y = position_Y
        self.animation = self.load_arrows(img_root, img_extension, 2)
        self.a_count = 0
        self.speedX = self.SPEED * math.cos(angle) if player else -self.SPEED * math.cos(angle)
        self.speedY = self.SPEED * math.sin(angle)
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def load_arrows(self, img_root, img_extension, num_img):
        images = {}
        for i in range(num_img):
            self.image = pg.image.load(img_root + str(i) + img_extension)
            images[i] = self.image
        return images

    def update_arrow(self):
        self.a_count += 0.3
        if self.a_count == len(self.animation):
            self.a_count = 0
        self.image = self.animation[int(self.a_count)]

    def move_arrow(self):
        if self.shoot:
            self.x += self.speedX
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def draw_arrows(self, screen):
        screen.blit(self.image, self.rect)
