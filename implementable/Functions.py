import pygame as pg

from objects.Wall import Wall
from objects.players.Archer import Archer
from objects.players.SwordsMan import SwordsMan
from objects.players.Worker import Worker


def attack(soldiers, soldier_index, soldier_counter):
    if len(soldiers) > 0:
        if soldier_index >= len(soldiers):
            soldier_index = 0
        soldier = soldiers[soldier_index]
        soldier_index += 1
        if soldier.ready_to_dispatch and isinstance(soldier, (Archer, SwordsMan)):
            soldier.deploy = True
            soldier.run = True
            if isinstance(soldier, Archer):
                if not soldier.shooting:
                    soldier.load_run()
                else:
                    soldier.ready_to_shoot()
            else:
                soldier.load_run()
            soldier_counter -= 1
        if soldier_counter <= 0:
            soldier_counter = 0
    return soldier_index, soldier_counter


def run_to_mine(workers):
    for worker in workers and workers:
        if worker.ready_to_dispatch and not worker.digging:
            worker.deploy = True
            worker.run = True
            worker.run_to_mine = True
            worker.digging = False
            worker.repairing = False
            worker.run_to_wall = False
            worker.to_mine()


def at_mine(workers):
    if all(worker.digging for worker in workers):
        return False
    else:
        return True


def run_to_wall(workers):
    for worker in workers and workers:
        # if worker.ready_to_dispatch and worker.player.castle.wall.health < Wall.MAX_HEALTH:
        if worker.ready_to_dispatch and not worker.repairing and worker.player.castle.wall.health < Wall.MAX_HEALTH:
            worker.deploy = True
            worker.run = True
            worker.digging = False
            worker.repairing = False
            worker.run_to_mine = False
            worker.run_to_wall = True
            worker.to_wall()


def at_wall(workers):
    if all(worker.repairing for worker in workers):
        return False
    else:
        return True


def deploy_all(soldiers):
    if all(soldier.deploy for soldier in soldiers):
        return False
    else:
        return True


def deploy(units):
    for i, soldier in enumerate(units):
        if soldier.deploy:
            if soldier.run:
                soldier.move()
            soldier.update()


def check_added(units, num_units, count_units, total):
    if isinstance(units, list):
        for i in range(len(units)):
            if isinstance(units[i], (Archer, SwordsMan, Worker)):
                if units[i].ready_to_dispatch and not units[i].added:
                    units[i].added = True
                    num_units += 1
                    count_units -= 1
                    total += 1
    return num_units, count_units, total


def add_to_queue(military_unit, units, count_soldiers, player_type):
    if isinstance(units, list):
        for i in range(count_soldiers):
            match player_type:
                case "a_p1":
                    soldier = Archer("p1")
                    if len(units) > 0:
                        prev_soldier = units[len(units) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.added:
                            units.append(soldier)
                            military_unit.append(soldier)
                    else:
                        units.append(soldier)
                        military_unit.append(soldier)

                case "a_p2":
                    soldier = Archer("p2")
                    if len(units) > 0:
                        prev_soldier = units[len(units) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.added:
                            units.append(soldier)
                            military_unit.append(soldier)
                    else:
                        units.append(soldier)
                        military_unit.append(soldier)

                case "s_p1":
                    soldier = SwordsMan("p1")
                    if len(units) > 0:
                        prev_soldier = units[len(units) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.added:
                            units.append(soldier)
                            military_unit.append(soldier)
                    else:
                        units.append(soldier)
                        military_unit.append(soldier)

                case "s_p2":
                    soldier = SwordsMan("p2")
                    if len(units) > 0:
                        prev_soldier = units[len(units) - 1]
                        if prev_soldier.ready_to_dispatch and prev_soldier.added:
                            units.append(soldier)
                            military_unit.append(soldier)
                    else:
                        units.append(soldier)
                        military_unit.append(soldier)
                case "w_p1":
                    worker = Worker(military_unit)
                    if len(units) > 0:
                        prev_worker = units[len(units) - 1]
                        if prev_worker.ready_to_dispatch and prev_worker.added:
                            units.append(worker)
                    else:
                        units.append(worker)
                case "w_p2":
                    worker = Worker(military_unit)
                    if len(units) > 0:
                        prev_worker = units[len(units) - 1]
                        if prev_worker.ready_to_dispatch and prev_worker.added:
                            units.append(worker)
                    else:
                        units.append(worker)


def collide(soldiers, target_unit):
    if isinstance(soldiers, list):
        for soldier in soldiers:
            if isinstance(soldier, Archer):
                if soldier.range.colliderect(
                        target_unit.range if not isinstance(target_unit,
                                                            Wall) else target_unit.rect) and not target_unit.dead:
                    soldier.run = False
                    soldier.ready_to_shoot()
                    if soldier.shooting:
                        soldier.move_arrows(target_unit)
            elif isinstance(soldier, SwordsMan):
                if soldier.rect.colliderect(target_unit.rect) and not target_unit.dead:
                    soldier.run = False
                    soldier.attack()
                    if soldier.attacking:
                        soldier.target_unit = target_unit


def training(units):
    if isinstance(units, list):
        for i in range(len(units)):
            if units[i].ready_to_dispatch is False:
                units[i].train()


def check_dead(soldiers):
    for i, soldier in enumerate(soldiers):
        if isinstance(soldier, (Archer, SwordsMan)):
            if soldier.dead and soldier.rest(3):
                del soldiers[i]


def check_health(soldiers):
    for i, soldier in enumerate(soldiers):
        if isinstance(soldier, (Archer, SwordsMan)):
            if soldier.health <= 0:
                soldier.run = False
                if isinstance(soldier, Archer):
                    soldier.arrows.clear()
                soldier.shooting = False
                soldier.attacking = False
                soldier.falling = True

                soldier.load_dead()


def check_worker_action(units):
    for i, unit in enumerate(units):
        if unit.digging:
            unit.dig()
        elif unit.repairing:
            unit.repair()


def draw(units, screen):
    for i in range(len(units)):
        if units[i].ready_to_dispatch:
            units[i].draw(screen)


def loadImage(image_map, num_img, flip):
    images = {}
    for i in range(num_img):
        image = pg.image.load(image_map['root'] + str(i) + image_map['extension'])
        if flip:
            image = pg.transform.flip(image, True, False)
        images[i] = image
    return images
