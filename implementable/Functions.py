import pygame as pg

from objects.Wall import Wall
from objects.players.Archer import Archer
from objects.players.SwordsMan import SwordsMan


def attack(soldiers, soldier_index, soldier_counter):
    if isinstance(soldiers, list):
        if len(soldiers) > 0:
            if soldier_index >= len(soldiers):
                soldier_index = 0
            soldier = soldiers[soldier_index]
            soldier_index += 1
            if soldier.ready_to_dispatch and isinstance(soldier, (Archer, SwordsMan)):
                soldier.deploy = True
                soldier.run = True
                soldier.load_run()
                soldier_counter -= 1
    return soldier_index, soldier_counter


def deploy_all(soldiers):
    if isinstance(soldiers, list):
        for soldier in soldiers:
            if not soldier.run and not soldier.deploy:
                soldier.deploy = True
                soldier.run = True


def check_added(soldiers, num_soldiers, count_soldiers, player_type, total):
    if isinstance(soldiers, list):
        for i in range(len(soldiers)):
            match player_type:
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
                    if isinstance(soldiers[i], SwordsMan):
                        if soldiers[i].ready_to_dispatch and not soldiers[i].swordsman_added:
                            soldiers[i].swordsman_added = True
                            num_soldiers += 1
                            count_soldiers -= 1
                            total += 1
                case "swordsmen_p2":
                    if isinstance(soldiers[i], SwordsMan):
                        if soldiers[i].ready_to_dispatch and not soldiers[i].swordsman_added:
                            soldiers[i].swordsman_added = True
                            num_soldiers += 1
                            count_soldiers -= 1
                            total += 1
    return num_soldiers, count_soldiers, total


def add_to_queue(military_unit, soldiers, count_soldiers, player_type):
    if isinstance(soldiers, list):
        for i in range(count_soldiers):
            match player_type:
                case "archers_p1":
                    soldier = Archer("p1")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.archer_added:
                            soldiers.append(soldier)
                            military_unit.append(soldier)
                    else:
                        soldiers.append(soldier)
                        military_unit.append(soldier)

                case "archers_p2":
                    soldier = Archer("p2")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.archer_added:
                            soldiers.append(soldier)
                            military_unit.append(soldier)
                    else:
                        soldiers.append(soldier)
                        military_unit.append(soldier)

                case "swordsmen_p1":
                    soldier = SwordsMan("p1")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.swordsman_added:
                            soldiers.append(soldier)
                            military_unit.append(soldier)
                    else:
                        soldiers.append(soldier)
                        military_unit.append(soldier)

                case "swordsmen_p2":
                    soldier = SwordsMan("p2")
                    if len(soldiers) > 0:
                        prev_soldier = soldiers[len(soldiers) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.swordsman_added:
                            soldiers.append(soldier)
                            military_unit.append(soldier)
                    else:
                        soldiers.append(soldier)
                        military_unit.append(soldier)


def collide(soldiers, target_unit):
    if isinstance(soldiers, list):
        for soldier in soldiers:
                if isinstance(soldier, Archer):
                    if soldier.range.colliderect(target_unit.range if not isinstance(target_unit, Wall) else target_unit.rect):
                        soldier.run = False
                        soldier.ready_to_shoot()
                        if soldier.shooting:
                            soldier.move_arrows(target_unit)
                elif isinstance(soldier, SwordsMan):
                    if soldier.rect.colliderect(target_unit.rect):
                        soldier.run = False
                        soldier.attack()
                        if soldier.attacking:
                            soldier.target_unit = target_unit


def training(soldiers):
    if isinstance(soldiers, list):
        for i in range(len(soldiers)):
            if soldiers[i].ready_to_dispatch is False:
                soldiers[i].train()


def deploy(soldiers):
    for i, soldier in enumerate(soldiers):
        if soldier.deploy:
            if soldier.run:
                soldier.move()
            if isinstance(soldier, Archer):
                soldier.update()
            elif isinstance(soldier, SwordsMan):
                soldier.update()


def check_dead(soldiers):
    for i, soldier in enumerate(soldiers):
        if isinstance(soldier, (Archer, SwordsMan)):
            if soldier.dead and soldier.rest(4):
                del soldiers[i]


def check_health(soldiers):
    for i, soldier in enumerate(soldiers):
        if isinstance(soldier, (Archer, SwordsMan)):
            if soldier.health <= 0:
                soldier.shooting = False
                soldier.attacking = False
                soldier.falling = True
                soldier.load_dead()


def draw(soldiers, screen):
    for i in range(len(soldiers)):
        if soldiers[i].ready_to_dispatch:
            soldiers[i].draw(screen)


def loadImage(image_path_root, img_extension, num_img):
    images = {}
    for i in range(num_img):
        image = pg.image.load(image_path_root + str(i) + img_extension)
        images[i] = image
    return images
