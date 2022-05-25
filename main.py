import collections
import random
from itertools import cycle

import pygame as pg

from objects.players.Archer import Archer
from objects.players.SwordMan import SwordMan

WIDTH, HEIGHT = 1000, 250

INITIAL_RESOURCE = 300

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
BG = pg.transform.scale(pg.image.load("sprites/background/BG.jpg"), (WIDTH, HEIGHT))


def main():
    archers_p1 = []
    swordsmen_p1 = []
    player1_resource = INITIAL_RESOURCE
    player2_resource = INITIAL_RESOURCE

    count_archer_p1 = 0
    count_swordsmen_p1 = 0

    def redraw_window():
        screen.blit(BG, (0, 0))

        for archer in archers_p1:
            if archer.ready_to_dispatch is True:
                archer.draw(screen)
        for swordsman in swordsmen_p1:
            if swordsman.ready_to_dispatch is True:
                swordsman.draw(screen)

        pg.display.update()

    loop = 1
    archer_index_p1 = 0
    swordsman_index_p1 = 0
    while loop:

        clock.tick(15)
        redraw_window()
        # keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = 0
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_e:
                    if player1_resource > 0:
                        count_archer_p1 += 1

                if event.key == pg.K_w:
                    if player1_resource > 0:
                        count_swordsmen_p1 += 1

                if event.key == pg.K_f:
                    if len(archers_p1) > 0:
                        if archer_index_p1 >= len(archers_p1):
                            archer_index_p1 = len(archers_p1) - 1
                        this_archer = archers_p1[archer_index_p1]
                        if this_archer.ready_to_dispatch is True:
                            archer_index_p1 += 1
                            this_archer.attack = True
                if event.key == pg.K_d:
                    if len(swordsmen_p1) > 0:
                        if swordsman_index_p1 >= len(archers_p1):
                            swordsman_index_p1 = len(archers_p1) - 1
                        this_swordsman = swordsmen_p1[swordsman_index_p1]
                        if this_swordsman.ready_to_dispatch is True:
                            swordsman_index_p1 += 1
                            this_swordsman.attack = True

                if event.key == pg.K_z:
                    for archer in archers_p1:
                        # check if soldier is ready to be dispatched
                        if archer.ready_to_dispatch is True:
                            # set dispatch to true
                            archer.attack = True
                    for swordsman in swordsmen_p1:
                        # check if soldier is ready to be dispatched
                        if swordsman.ready_to_dispatch is True:
                            # set dispatch to true
                            swordsman.attack = True

        for i in range(count_archer_p1):
            archer = Archer(100, random.randrange(10, 30), 165, False, screen)
            if len(archers_p1) >= 1:
                player1_resource -= archer.COST
                prev_archer = archers_p1[len(archers_p1) - 1]
                if prev_archer.ready_to_dispatch is True:
                    archers_p1.append(archer)
                    count_archer_p1 -= 1
            elif len(archers_p1) == 0:
                archers_p1.append(archer)
                count_archer_p1 -= 1

        for i in range(count_swordsmen_p1):
            swordsman = SwordMan(100, random.randrange(10, 30), 165, False, screen)
            if len(swordsmen_p1) >= 1:
                player1_resource -= swordsman.COST
                prev_swordsman = swordsmen_p1[len(swordsmen_p1) - 1]
                if prev_swordsman.ready_to_dispatch is True:
                    swordsmen_p1.append(swordsman)
                    count_swordsmen_p1 -= 1
            elif len(swordsmen_p1) == 0:
                swordsmen_p1.append(swordsman)
                count_swordsmen_p1 -= 1

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
            archer_index_p1) + " | "
              + "issued swordsman: " + str(count_swordsmen_p1) + " no. of swordsmen: " + str(
            len(swordsmen_p1)) + " index: " + str(swordsman_index_p1))

        for archer in archers_p1:
            # if soldier is dispatchable it gets deployed
            if archer.attack is True:
                archer.move()
                archer.update()
            if archer.x > WIDTH - 100:
                archers_p1.remove(archer)

        for swordsman in swordsmen_p1:
            # if soldier is dispatchable it gets deployed
            if swordsman.attack is True:
                swordsman.move()
                swordsman.update()
            if swordsman.x > WIDTH - 100:
                swordsmen_p1.remove(swordsman)


if __name__ == '__main__':
    main()
