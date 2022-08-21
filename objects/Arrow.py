import pygame as pg

from implementable import Functions


class Arrow(pg.sprite.Sprite):
    SPEED = 10

    def __init__(self, position_X, position_Y, img_root, img_extension):
        super().__init__()
        self.shoot = False
        self.hit = False
        self.x = position_X
        self.y = position_Y
        self.animation = self.load_arrows(img_root, img_extension, 2)
        self.a_count = 0
        self.mask = pg.mask.from_surface(self.image)

    def load_arrows(self, img_root, img_extension, num_img):
        images = {}
        for i in range(num_img):
            self.image = pg.image.load(img_root + str(i) + img_extension)
            images[i] = self.image
        return images

    def update_arrow(self):
        if self.a_count == len(self.animation):
            self.a_count = 0
        self.image = self.animation[self.a_count]
        self.mask = pg.mask.from_surface(self.image)

    def move_arrow(self, type):
        if self.shoot and not self.hit:
            match type:
                case "p1":
                    self.x += self.SPEED
                case "p2":
                    self.x -= self.SPEED

    def draw_arrows(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collision(self, obj):
        return Functions.arrow_collide(obj, self)

    # def collision(self, obj):
    #     return Functions.collide(obj, self)
