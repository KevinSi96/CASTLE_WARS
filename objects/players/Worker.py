import pygame

from objects.Constants import WORKER_PROD, WORKER_REPAIR, WORKER_TRAIN, BARRACKS_POS, SCREEN_WIDTH, GROUND_HEIGHT, \
    SCREEN_HEIGHT, WORKER_SPEED


class Worker:
    production_rate = WORKER_PROD
    repair_rate = WORKER_REPAIR
    training_time = WORKER_TRAIN

    def __init__(self, player, isLeftPlayer):
        # Declaring position
        self.x = BARRACKS_POS if isLeftPlayer else SCREEN_WIDTH - BARRACKS_POS
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.speed = WORKER_SPEED

        # Player's info
        self.isLeftPlayer = isLeftPlayer
        self.player = player

        # Declaring images
        self.images = p1_images["worker"] if isLeftPlayer else p2_images["worker"]
        self.image = self.images['ready']
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        self.image_index = 0

        # Worker's State
        self.running_to_mine = True
        self.running_to_wall = False
        self.digging = False
        self.repairing = False

        # Repair and Mine timers
        self.repair_timer = 0
        self.mine_timer = 0

    def to_wall(self):
        # Resets the mining timer and goes to running state
        self.mine_timer = pygame.time.get_ticks()
        self.running_to_mine = False
        self.running_to_wall = True
        self.digging = False
        self.repairing = False

    def to_mine(self):
        # Resets the repair timer and goes to running state
        self.repair_timer = pygame.time.get_ticks()
        self.running_to_mine = True
        self.running_to_wall = False
        self.digging = False
        self.repairing = False

    def run_to_mine(self):
        # Handles the running animation
        self.image_index += 0.2
        if self.image_index > len(self.images['run_right']):
            self.image_index = 0

        # Moves the unit Rect by self.speed pixels
        if self.player.castle.mine.rect.centerx < self.rect.centerx:
            self.x -= self.speed
            self.image = self.images['run_left'][int(self.image_index)]
        elif self.player.castle.mine.rect.centerx > self.rect.centerx:
            self.x += self.speed
            self.image = self.images['run_right'][int(self.image_index)]
        else:
            # If the worker is at the mine, pass to digging state
            self.running_to_mine = False
            self.running_to_wall = False
            self.digging = True
            self.repairing = False

        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def run_to_wall(self):
        # Handles the running animation
        self.image_index += 0.2
        if self.image_index > len(self.images['run_right']):
            self.image_index = 0

        # Decides if the worker runs right or left
        if self.player.castle.wall.rect.centerx < self.rect.centerx:
            self.x -= self.speed
            self.image = self.images['run_left'][int(self.image_index)]
        elif self.player.castle.wall.rect.centerx > self.rect.centerx:
            self.x += self.speed
            self.image = self.images['run_right'][int(self.image_index)]
        else:
            # If the worker is at the mine, pass to digging state
            self.running_to_mine = False
            self.running_to_wall = False
            self.digging = False
            self.repairing = True

        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def dig(self):
        # Handles the attack animation
        self.image_index += 0.2
        if self.image_index >= len(self.images['dig']):
            self.image_index = 0

        # Adds the production to the player's resources
        self.player.resources += self.production_rate

        # Updates the image and position
        self.image = self.images['dig'][int(self.image_index)]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def repair(self):
        # Handles the attack animation
        self.image_index += 0.2
        if self.image_index >= len(self.images['repair']):
            self.image_index = 0

        # Adds the repairs to the player's wall's health
        self.player.castle.wall.health += self.repair_rate
        if self.player.castle.wall.health >= WALL_HEALTH:
            self.player.castle.wall.health = WALL_HEALTH

        # Updates the image and position
        self.image = self.images['repair'][int(self.image_index)]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def update(self):
        # Calls the right function according to the character state
        if self.running_to_mine:
            self.run_to_mine()
        elif self.running_to_wall:
            self.run_to_wall()
        elif self.digging:
            self.dig()
        elif self.repairing:
            self.repair()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
