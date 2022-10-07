import math

import pygame as pg


class Arrow:
    SPEED = 5

    def __init__(self, position_X, position_Y, image_map, player, angle):
        self.shoot = False
        self.x = position_X
        self.y = position_Y
        self.a_count = 0
        self.speedX = self.SPEED * math.cos(angle) if player else -self.SPEED * math.cos(angle)
        self.speedY = self.SPEED * math.sin(angle)
        if angle == 0:
            self.image_type = 'arrow_hor/arrowhor-'
        elif 0 < angle <= ((math.pi / 2) - (math.pi / 6)):
            self.image_type = 'arrow_diag/arrowdiag-'
        else:
            self.image_type = 'arrow_vert/arrowvert-'

        self.animation = self.load_arrows(image_map['root'], image_map['extension'], 2)
        self.image = self.animation[0]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def load_arrows(self, img_root, img_extension, num_img):
        images = {}
        for i in range(num_img):
            self.image = pg.image.load(img_root + self.image_type + str(i) + img_extension)
            images[i] = self.image
        return images

    def update_arrow(self):
        self.a_count += 0.2
        if self.a_count >= 1:
            self.a_count = 0
        self.image = self.animation[int(self.a_count)]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def move_arrow(self):
        self.update_arrow()
        if self.shoot:
            self.x += self.speedX
            self.y += self.speedY
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def draw_arrows(self, screen):
        screen.blit(self.image, self.rect)
