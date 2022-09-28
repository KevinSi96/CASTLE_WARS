import pygame

from implementable import Functions
from objects.Constants import SCREEN_HEIGHT, GROUND_HEIGHT
from objects.players.Archer import Archer
from objects.players.SwordsMan import SwordsMan
from objects.players.Worker import Worker


class Barracks:
    def __init__(self, img, barrack_x, player):
        self.player = player
        self.img = img
        self.rect = self.img.get_rect(midbottom=(barrack_x, SCREEN_HEIGHT - GROUND_HEIGHT))
        self.training_timer = 0
        self.unleashing_timer = 0
        self.unleashing_time_per_unit = 300
        self.is_training = False
        self.is_unleashing = False
        self.is_unleashing_unit = False
        self.training_queue = []
        self.unleashing_units = []
        self.swordsmen = []
        self.archers = []
        self.swordsman_index = 0
        self.num_swordsmen = 0
        self.archer_index = 0
        self.num_archer = 0
        self.count_sword = 0
        self.count_archer = 0
        self.count_workers = 0
        self.count_swords = 0
        # Initialize the barracks with one of each unit
        self.ready_units = [
            # Worker(self.player, self.player.isLeftPlayer),
            Archer(self.player.player_type)
            # SwordsMan(self.player.isLeftPlayer)
        ]

    def check_training_queue(self):
        if self.training_queue:
            if not self.is_training:
                self.is_training = True
                self.training_timer = pygame.time.get_ticks()
            elif self.is_training:
                if pygame.time.get_ticks() - self.training_timer >= self.training_queue[0].training_time * 100:
                    self.is_training = False
                    unit = self.training_queue.pop(0)
                    self.ready_units.append(unit)
                    print(f"{type(unit)} created")

    def train_archer(self):
        Functions.add_to_queue(self.archers, self.count_archer,
                               "archers_p1" if self.player.player_type == "p1" else "archers_p2")
        self.num_archer, self.count_archer, self.player.total_archer = Functions.check_added(self.archers,
                                                                                             self.num_archer,
                                                                                             self.count_archer,
                                                                                             "archers_p1" if self.player.player_type == "p1" else "archers_p2",
                                                                                             self.player.total_soldiers)

    def train_worker(self, player, isLeftPlayer):
        worker = Worker(player, isLeftPlayer)
        self.training_queue.append(worker)

    def unleash_worker(self, to_mine):
        for i, unit in enumerate(self.ready_units):
            if isinstance(unit, Worker):
                worker = self.ready_units.pop(i)
                if to_mine:
                    worker.to_mine()
                    self.player.mine_workers.append(worker)
                else:
                    worker.to_wall()
                    self.player.wall_workers.append(worker)
                break

    def unleash_swordsman(self):
        if any(isinstance(unit, SwordsMan) for unit in self.ready_units):
            for i, unit in enumerate(self.ready_units):
                if isinstance(unit, SwordsMan):
                    swordsman = self.ready_units.pop(i)
                    self.player.military_units.append(swordsman)
                    break

    def unleash_archer(self):
        if any(isinstance(unit, Archer) for unit in self.ready_units):
            print(self.ready_units)
            for i, unit in enumerate(self.ready_units):
                if isinstance(unit, Archer):
                    archer = self.ready_units.pop(i)
                    self.player.military_units.append(archer)
                    break

    def unleash_all(self):
        self.unleashing_units.extend(self.ready_units)
        self.ready_units.clear()

        if not self.is_unleashing:
            self.is_unleashing = True

    def unleash_update(self):
        # This method unleashes the units one at the time so they are spread out
        if self.is_unleashing:
            if self.unleashing_units and not self.is_unleashing_unit:
                self.is_unleashing_unit = True
                self.unleashing_timer = pygame.time.get_ticks()
            elif self.unleashing_units and self.is_unleashing_unit:
                if pygame.time.get_ticks() - self.unleashing_timer >= self.unleashing_time_per_unit:
                    unit = self.unleashing_units.pop(0)
                    if isinstance(unit, (Archer, SwordsMan)):
                        self.player.military_units.append(unit)
                    else:
                        self.player.mine_workers.append(unit)
                    self.is_unleashing_unit = False
            else:
                self.is_unleashing = False

    def update(self):
        Functions.training(self.archers)
        self.unleash_update()

    def draw(self, screen):
        screen.blit(self.img, self.rect)
