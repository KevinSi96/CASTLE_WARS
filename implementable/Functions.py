import random

from objects.players.Player import Player
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
            if not soldier.run and not soldier.deploy:
                soldier.deploy = True
                soldier.run = True


def check_added(soldiers, num_soldiers, count_soldiers, type, total):
    if isinstance(soldiers, list):
        for i in range(len(soldiers)):
            match type:
                case "archers_p1":
                    if isinstance(soldiers[i], Archer):
                        if soldiers[i].ready_to_dispatch and not soldiers[i].archer_added:
                            soldiers[i].archer_added = True
                            num_soldiers += 1
                            count_soldiers -= 1
                            total += 1
                case "archers_p2":
                    if isinstance(soldiers[i], Archer):
                        if soldiers[i].ready_to_dispatch and not soldiers[i].archer_added:
                            soldiers[i].archer_added = True
                            num_soldiers += 1
                            count_soldiers -= 1
                            total += 1
                case "swordsmen_p1":
                    if isinstance(soldiers[i], SwordMan):
                        if soldiers[i].ready_to_dispatch and not soldiers[i].swordsman_added:
                            soldiers[i].swordsman_added = True
                            num_soldiers += 1
                            count_soldiers -= 1
                            total += 1
                case "swordsmen_p2":
                    if isinstance(soldiers[i], SwordMan):
                        if soldiers[i].ready_to_dispatch and not soldiers[i].swordsman_added:
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
                                     "p1")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.archer_added:
                            soldiers.append(soldier)
                    else:
                        soldiers.append(soldier)
                case "archers_p2":
                    soldier = Archer(100, random.randrange(900, 970), 165, False, screen,
                                     "p2")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.archer_added:
                            soldiers.append(soldier)
                    else:
                        soldiers.append(soldier)
                case "swordsmen_p1":
                    soldier = SwordMan(100, random.randrange(10, 30), 170, False, screen,
                                       "p1")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.swordsman_added:
                            soldiers.append(soldier)
                    else:
                        soldiers.append(soldier)

                case "swordsmen_p2":
                    soldier = SwordMan(100, random.randrange(900, 970), 170, False, screen,
                                       "p2")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.swordsman_added:
                            soldiers.append(soldier)
                    else:
                        soldiers.append(soldier)


def collide(soldiers1, soldiers2):
    if isinstance(soldiers1, list) and isinstance(soldiers2, list):
        for i in range(len(soldiers1)):
            for j in range(len(soldiers2)):
                offset_x = soldiers2[j].x - soldiers1[i].x
                if isinstance(soldiers1[i], Archer) and isinstance(soldiers2[j], Archer):
                    if offset_x < 300:
                        soldiers1[i].run = False
                        soldiers1[i].ready_to_shoot("p1")
                        soldiers2[j].run = False
                        soldiers2[j].ready_to_shoot("p2")
                if isinstance(soldiers1[i], SwordMan) and isinstance(soldiers2[j], SwordMan):
                    if offset_x < 20:
                        soldiers1[i].run = False
                        soldiers1[i].attack("p1")
                        soldiers2[j].run = False
                        soldiers2[j].attack("p2")


def training(soldiers):
    if isinstance(soldiers, list):
        for i in range(len(soldiers)):
            if isinstance(soldiers[i], Player):
                if soldiers[i].ready_to_dispatch is False:
                    soldiers[i].train()


def deploy(soldiers):
    if isinstance(soldiers, list):
        for i in range(len(soldiers)):
            if isinstance(soldiers[i], Player):
                if soldiers[i].deploy:
                    if soldiers[i].run:
                        soldiers[i].move()
                    soldiers[i].update()
                    if isinstance(soldiers[i], Archer):
                        if soldiers[i].shooting:
                            soldiers[i].move_arrows()

def draw(soldiers, screen):
    for i in range(len(soldiers)):
        if soldiers[i].ready_to_dispatch:
            soldiers[i].draw(screen)
        if soldiers[i].dead:
            soldiers.remove(soldiers[i])