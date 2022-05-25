import time

import pygame as pg
import random

from objects.players.Archer import Archer

WIDTH, HEIGHT = 1000, 250

INITIAL_RESOURCE = 1000

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
BG = pg.transform.scale(pg.image.load("sprites/background/BG.jpg"), (WIDTH, HEIGHT))


def main():
    archers = []

    player1_resource = INITIAL_RESOURCE
    player2_resource = INITIAL_RESOURCE

    def redraw_window():
        screen.blit(BG, (0, 0))

        for archer in archers:
            archer.draw(screen)

        pg.display.update()

    loop = 1
    while loop:
        clock.tick(24)
        redraw_window()
        keys = pg.key.get_pressed()

        if keys[pg.K_t]:
            archer = Archer(100, random.randrange(10, 30), 165, False, screen)
            player1_resource -= archer.COST
            archers.append(archer)
        if keys[pg.K_d]:
            for archer in archers:
                # check if soldier is ready to be dispatched
                if archer.ready_to_dispatch is True:
                    # set dispatch to true
                    archer.dispatch = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = 0

        for archer in archers:
            if archer.ready_to_dispatch is False:
                archer.train()
            # if soldier is dispatchable it gets deployed
            elif archer.dispatch is True:
                archer.move()
                archer.update()


if __name__ == '__main__':
    main()
