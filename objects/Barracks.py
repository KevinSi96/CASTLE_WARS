from objects.Constants import SCREEN_HEIGHT, GROUND_HEIGHT


class Barracks:
    def __init__(self, img, barrack_x):
        self.img = img
        self.rect = self.img.get_rect(midbottom=(barrack_x, SCREEN_HEIGHT - GROUND_HEIGHT))

    def draw(self, screen):
        screen.blit(self.img, self.rect)
