import time

from implementable import Functions
from objects.Castle import Castle
from objects.Constants import *
from objects.Wall import Wall


class Player:
    def __init__(self, player_type, keys):
        self.to_wall = False
        self.to_mine = False
        self.targeted_unit = None
        self.total_soldiers = 0
        self.deploy_all = False
        self.total_archer = 0
        self.swordsmen = []
        self.archers = []
        self.worker_index = 0
        self.num_workers = 0
        self.start_action = 0
        self.current_time = 0
        self.total_swords = 0
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
            if self.player_resource > 0:
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

        if key == self.keys.worker_train_key:
            if self.player_resource > 0:
                self.player_resource -= WORKER_COST
                self.count_workers += 1
            else:
                self.player_resource = 0

        if key == self.keys.to_mine_key:
            self.to_mine = True
        if key == self.keys.to_wall_key:
            self.to_wall = True
        if key == self.keys.unleash_key:
            self.deploy_all = True
            self.num_archer = 0
            self.num_swordsmen = 0

    def update(self, game_over):
        self.choose_target()

        Functions.add_to_queue(self.soldiers, self.archers, self.count_archer,
                               "a_p1" if self.player_type == "p1" else "a_p2")
        self.num_archer, self.count_archer, self.total_archer = Functions.check_added(self.archers, self.num_archer,
                                                                                      self.count_archer,
                                                                                      self.total_soldiers)
        Functions.add_to_queue(self.soldiers, self.swordsmen, self.count_sword,
                               "s_p1" if self.player_type == "p1" else "s_p2")
        self.num_swordsmen, self.count_sword, self.total_swords = Functions.check_added(self.swordsmen,
                                                                                        self.num_swordsmen,
                                                                                        self.count_sword,
                                                                                        self.total_soldiers)
        Functions.add_to_queue(self, self.workers, self.count_workers, "w_p1" if self.player_type == "p1" else "w_p2")
        self.num_workers, self.count_workers, NoneType = Functions.check_added(self.workers,
                                                                               self.num_workers,
                                                                               self.count_workers,
                                                                               None)

        if self.count_archer <= 0:
            self.count_archer = 0
        if self.count_sword <= 0:
            self.count_sword = 0
        if self.count_workers <= 0:
            self.count_workers = 0

        if self.opponent.castle.wall.health <= 0:
            game_over = True
        if self.castle.wall.health <= Wall.MAX_HEALTH / 2:
            self.to_wall = True

        self.total_soldiers = len(self.soldiers)

        if self.deploy_all:
            if self.rest(0.3):
                self.start_action = time.time()
                self.archer_index, self.num_archer = Functions.attack(self.archers, self.archer_index, self.num_archer)
                self.swordsman_index, self.num_swordsmen = Functions.attack(self.swordsmen, self.swordsman_index,
                                                                            self.num_swordsmen)
            self.deploy_all = Functions.deploy_all(self.soldiers)

        if self.to_mine:
            Functions.run_to_mine(self.workers)
            self.to_mine = Functions.at_mine(self.workers)
        elif self.to_wall:
            Functions.run_to_wall(self.workers)
            self.to_wall = Functions.at_wall(self.workers)

        Functions.training(self.soldiers)
        Functions.training(self.workers)
        Functions.collide(self.soldiers, self.targeted_unit)
        Functions.deploy(self.soldiers)
        Functions.deploy(self.workers)
        Functions.check_health(self.soldiers)
        Functions.check_dead(self.soldiers)
        Functions.tower_collide(self.castle.tower, self.targeted_unit)
        Functions.check_worker_action(self.workers)
        self.castle.update(self.targeted_unit)
        return game_over

    def draw(self, screen):
        self.castle.draw(screen)
        Functions.draw(self.soldiers, screen)
        Functions.draw(self.workers, screen)

    def rest(self, rest_amount):
        if rest_amount > (self.current_time - self.start_action):
            self.current_time = time.time()
            return False
        else:
            return True
