from objects.Constants import SCREEN_HEIGHT, GROUND_HEIGHT


class Mine:
    def __init__(self, img, mine_x):
        self.img = img
        self.rect = self.img.get_rect(midbottom=(mine_x, SCREEN_HEIGHT - GROUND_HEIGHT))

    def draw(self, screen):
        screen.blit(self.img, self.rect)
