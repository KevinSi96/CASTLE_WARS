import collections
import random
from itertools import cycle

import pygame as pg

from objects.players.Archer import Archer

WIDTH, HEIGHT = 1000, 250

INITIAL_RESOURCE = 1000

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
BG = pg.transform.scale(pg.image.load("sprites/background/BG.jpg"), (WIDTH, HEIGHT))


def main():
    global next_arch
    archers = []
    player1_resource = INITIAL_RESOURCE
    player2_resource = INITIAL_RESOURCE

    def redraw_window():
        screen.blit(BG, (0, 0))

        for archer in archers:
            archer.draw(screen)

        pg.display.update()

    loop = 1
    index = 0
    while loop:

        clock.tick(15)
        redraw_window()
        # keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    archer = Archer(100, random.randrange(10, 30), 165, False, screen)
                    player1_resource -= archer.COST
                    if len(archers) >= 1:
                        prev_archer = archers[len(archers) - 1]
                        if prev_archer.ready_to_dispatch is True:
                            archers.append(archer)

                    else:
                        archers.append(archer)
                if event.key == pg.K_z:
                    for archer in archers:
                        # check if soldier is ready to be dispatched
                        if archer.ready_to_dispatch is True:
                            # set dispatch to true
                            archer.attack = True
                if event.key == pg.K_f:
                    if len(archers) > 0:
                        if index >= len(archers):
                            index = len(archers) - 1
                        this_archer = archers[index]
                        if this_archer.ready_to_dispatch is True:
                            this_archer.attack = True
                            index += 1

        for archer in archers:
            if archer.ready_to_dispatch is False:
                archer.train()
            # if soldier is dispatchable it gets deployed
            elif archer.attack is True:
                archer.move()
                archer.update()
            if archer.x > WIDTH - 100:
                archers.remove(archer)


if __name__ == '__main__':
    main()
