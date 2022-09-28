import pygame as pg

from implementable import Functions
from objects.Castle import Castle
from objects.Constants import ARCHER_COST, SWORD_COST, PLAYER_START_RESOURCES, WALL_POS, SCREEN_WIDTH


class Player:
    def __init__(self, player_type, keys):
        self.total_swords = 0
        self.targeted_unit = None
        self.total_soldiers = 0
        self.total_archer = 0
        self.swordsmen = []
        self.archers = []
        self.swordsman_index = 0
        self.num_swordsmen = 0
        self.archer_index = 0
        self.num_archer = 0
        self.count_sword = 0
        self.count_archer = 0
        self.count_workers = 0
        self.image = None
        self.keys = keys
        self.player_type = player_type
        self.castle = Castle(self)
        self.player_resource = PLAYER_START_RESOURCES
        self.a_count = 0
        self.soldiers = []
        self.workers = []
        self.opponent = None

    def choose_target(self):
        alive_soldiers = [soldier for soldier in self.opponent.soldiers if not soldier.dead]
        if alive_soldiers:
            selected_target = min(alive_soldiers, key=lambda unit: abs(self.castle.wall.rect.x - unit.x))
            self.targeted_unit = selected_target if WALL_POS <= selected_target.rect.centerx <= SCREEN_WIDTH - WALL_POS else self.opponent.castle.wall
        else:
            self.targeted_unit = self.opponent.castle.wall

    def key_events(self, key):
        if key == self.keys.archer_train_key:
            if self.player_resource >= 0:
                self.player_resource -= ARCHER_COST
                self.count_archer += 1

            else:
                self.player_resource = 0

        if key == self.keys.sword_train_key:
            if self.player_resource > 0:
                self.player_resource -= SWORD_COST
                self.count_sword += 1
            else:
                self.player_resource = 0

        if key == self.keys.archer_attack_key:
            if self.num_archer > 0:
                self.archer_index, self.num_archer = Functions.attack(self.archers, self.archer_index, self.num_archer)

        if key == self.keys.sword_attack_key:
            if self.num_swordsmen > 0:
                self.swordsman_index, self.num_swordsmen = Functions.attack(self.swordsmen, self.swordsman_index,
                                                                            self.num_swordsmen)

        if key == pg.K_z:
            Functions.deploy_all(self.archers)
            Functions.deploy_all(self.swordsmen)
            self.num_archer = 0
            self.num_swordsmen = 0

    def update(self, game_over):
        Functions.add_to_queue(self.soldiers, self.archers, self.count_archer,
                               "archers_p1" if self.player_type == "p1" else "archers_p2")
        self.num_archer, self.count_archer, self.total_archer = Functions.check_added(self.archers, self.num_archer,
                                                                                      self.count_archer,
                                                                                      "archers_p1" if self.player_type == "p1" else "archers_p2",
                                                                                      self.total_soldiers)
        Functions.add_to_queue(self.soldiers, self.swordsmen, self.count_sword,
                               "swordsmen_p1" if self.player_type == "p1" else "swordsmen_p2")
        self.num_swordsmen, self.count_sword, self.total_swords = Functions.check_added(self.swordsmen,
                                                                                        self.num_swordsmen,
                                                                                        self.count_sword,
                                                                                        "swordsmen_p1" if self.player_type == "p1" else "swordsmen_p2",
                                                                                        self.total_soldiers)
        if self.count_archer <= 0:
            self.count_archer = 0
        if self.count_sword <= 0:
            self.count_sword = 0

        if self.opponent.castle.wall.health <= 0:
            game_over = True
            return game_over

        self.choose_target()

        Functions.training(self.soldiers)
        Functions.deploy(self.soldiers)
        Functions.collide(self.soldiers, self.targeted_unit)
        Functions.check_health(self.soldiers)
        Functions.check_dead(self.soldiers)
        self.castle.update(self.targeted_unit)
        return game_over

    def draw(self, screen):
        self.castle.draw(screen)
        Functions.draw(self.soldiers, screen)
