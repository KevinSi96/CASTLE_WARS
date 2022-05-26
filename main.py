import collections
import random
from itertools import cycle

import pygame as pg

from objects.players.Archer import Archer
from objects.players.SwordMan import SwordMan

WIDTH, HEIGHT = 1000, 250

INITIAL_RESOURCE = 30000

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
BG = pg.transform.scale(pg.image.load("sprites/background/BG.jpg"), (WIDTH, HEIGHT))


def main():
    archer_index_p1 = 0
    swordsman_index_p1 = 0
    archers_p1 = []
    swordsmen_p1 = []
    player1_resource = INITIAL_RESOURCE
    player2_resource = INITIAL_RESOURCE

    count_archer_p1 = 0
    num_archer_p1 = 0
    count_swordsmen_p1 = 0
    num_swordsmen_p1 = 0

    def attack(soldiers, soldier_index, soldier_counter):
        if isinstance(soldiers, list):
            if len(soldiers) > 0:
                if soldier_index >= len(soldiers):
                    soldier_index = 0
                soldier = soldiers[soldier_index]
                soldier_index += 1
                if soldier.ready_to_dispatch:
                    soldier.deploy = True
                    soldier_counter -= 1
        return soldier_index, soldier_counter

    def deploy_all(soldiers):
        if isinstance(soldiers, list):
            for soldier in soldiers:
                soldier.deploy = True

    def redraw_window():
        screen.blit(BG, (0, 0))

        for archer in archers_p1:
            if archer.ready_to_dispatch:
                archer.draw(screen)
            if archer.x > WIDTH - 100:
                archers_p1.remove(archer)
            if archer.dead:
                archers_p1.remove(archer)

        for swordsman in swordsmen_p1:
            if swordsman.ready_to_dispatch:
                swordsman.draw(screen)
            if swordsman.x > WIDTH - 100:
                swordsmen_p1.remove(swordsman)

        pg.display.update()

    loop = 1

    while loop:

        clock.tick(15)
        redraw_window()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = 0
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_e:
                    if player1_resource > 0:
                        player1_resource -= Archer.COST
                        count_archer_p1 += 1
                    else:
                        player1_resource = 0

                if event.key == pg.K_w:
                    if player1_resource > 0:
                        player1_resource -= SwordMan.COST
                        count_swordsmen_p1 += 1
                    else:
                        player1_resource = 0

                if event.key == pg.K_f:
                    archer_index_p1, num_archer_p1 = attack(archers_p1, archer_index_p1, num_archer_p1)

                if event.key == pg.K_d:
                    swordsman_index_p1, num_swordsmen_p1 = attack(swordsmen_p1, swordsman_index_p1, num_swordsmen_p1)

                if event.key == pg.K_z:
                    deploy_all(archers_p1)
                    deploy_all(swordsmen_p1)
                    num_archer_p1 = 0
                    num_swordsmen_p1 = 0

        for i in range(count_archer_p1):
            archer = Archer(100, random.randrange(10, 30), 165, False, screen)
            if len(archers_p1) >= 1:
                prev_archer = archers_p1[len(archers_p1) - 1]
                if prev_archer.ready_to_dispatch:
                    archers_p1.append(archer)
                    num_archer_p1 += 1
                    count_archer_p1 -= 1
            elif len(archers_p1) == 0:
                num_archer_p1 += 1
                archers_p1.append(archer)

        for i in range(count_swordsmen_p1):
            swordsman = SwordMan(100, random.randrange(10, 30), 165, False, screen)
            if len(swordsmen_p1) >= 1:
                prev_swordsman = swordsmen_p1[len(swordsmen_p1) - 1]
                if prev_swordsman.ready_to_dispatch:
                    swordsmen_p1.append(swordsman)
                    num_swordsmen_p1 += 1
                    count_swordsmen_p1 -= 1
            elif len(swordsmen_p1) == 0:
                num_swordsmen_p1 += 1
                swordsmen_p1.append(swordsman)

        for archer in archers_p1:
            if archer.ready_to_dispatch is False:
                archer.train()
        for swordsman in swordsmen_p1:
            if swordsman.ready_to_dispatch is False:
                swordsman.train()

        if count_archer_p1 <= 0:
            count_archer_p1 = 0
        if count_swordsmen_p1 <= 0:
            count_swordsmen_p1 = 0

        print("issued archers: " + str(count_archer_p1) + " no. of archers: " + str(len(archers_p1)) + " index: " + str(
            archer_index_p1) + " ready archers: " + str(num_archer_p1) + " | "
              + "issued swordsman: " + str(count_swordsmen_p1) + " no. of swordsmen: " + str(
            len(swordsmen_p1)) + " index: " + str(swordsman_index_p1) + " resources: " + str(player1_resource))

        for archer in archers_p1:
            # if soldier is dispatchable it gets deployed
            if archer.deploy:
                archer.move()
                archer.update()

        for swordsman in swordsmen_p1:
            # if soldier is dispatchable it gets deployed
            if swordsman.attack:
                swordsman.move()
                swordsman.update()


if __name__ == '__main__':
    main()
