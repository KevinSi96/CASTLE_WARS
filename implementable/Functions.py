import random

from objects.players.Archer import Archer
from objects.players.SwordsMan import SwordMan


def attack(soldiers, soldier_index, soldier_counter):
    if isinstance(soldiers, list):
        if len(soldiers) > 0:
            if soldier_index >= len(soldiers):
                soldier_index = 0
            soldier = soldiers[soldier_index]
            soldier_index += 1
            if soldier.ready_to_dispatch:
                soldier.deploy = True
                soldier.run = True
                soldier_counter -= 1
    return soldier_index, soldier_counter


def deploy_all(soldiers):
    if isinstance(soldiers, list):
        for soldier in soldiers:
            if soldier.run is False and soldier.deploy is False:
                soldier.deploy = True
                soldier.run = True


def check_added(soldiers, num_soldiers, count_soldiers, type, total):
    if isinstance(soldiers, list):
        for i in range(len(soldiers)):
            match type:
                case "archers_p1":
                    if isinstance(soldiers[i], Archer):
                        if soldiers[i].ready_to_dispatch and soldiers[i].archer_added is False:
                            soldiers[i].archer_added = True
                            num_soldiers += 1
                            count_soldiers -= 1
                            total += 1
                case "swordsmen_p1":
                    if isinstance(soldiers[i], SwordMan):
                        if soldiers[i].ready_to_dispatch and soldiers[i].swordsman_added is False:
                            soldiers[i].swordsman_added = True
                            num_soldiers += 1
                            count_soldiers -= 1
                            total += 1
    return num_soldiers, count_soldiers, total


def add_to_queue(soldiers, count_soldiers, type, screen):
    if isinstance(soldiers, list):
        for i in range(count_soldiers):
            match type:
                case "archers_p1":
                    soldier = Archer(100, random.randrange(10, 30), 165, False, screen,
                                     "sprites/player1/bow/run/run-", ".png")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.archer_added:
                            soldiers.append(soldier)
                    else:
                        soldiers.append(soldier)
                case "swordsmen_p1":
                    soldier = SwordMan(100, random.randrange(10, 30), 170, False, screen,
                                       "sprites/player1/sword/run/run-",
                                       ".png")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.swordsman_added:
                            soldiers.append(soldier)
                    else:
                        soldiers.append(soldier)
