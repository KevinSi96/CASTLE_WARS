import random

import pygame as pg

from implementable import Functions
from objects.players.Archer import Archer
from objects.players.SwordsMan import SwordMan

WIDTH, HEIGHT = 1000, 250

INITIAL_RESOURCE = 30000

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
BG = pg.transform.scale(pg.image.load("sprites/background/BG.jpg"), (WIDTH, HEIGHT))
pg.font.init()


def main():
    archers_p1 = []
    swordsmen_p1 = []
    player1_resource = INITIAL_RESOURCE
    player2_resource = INITIAL_RESOURCE

    # counters
    archer_index_p1 = 0
    swordsman_index_p1 = 0
    count_archer_p1 = 0
    num_archer_p1 = 0
    count_swordsmen_p1 = 0
    num_swordsmen_p1 = 0
    p1_total_soldiers = 0

    # Fonts
    default_font = pg.font.SysFont("comicsans", 10)
    resource_font = pg.font.SysFont("comicsans", 20)

    def in_range(object1):
        if isinstance(object1, Archer):
            if object1.x >= WIDTH - (random.randint(0, 100) + 700) and object1.deploy:
                object1.run = False
                object1.ready_to_shoot("p1")
        return object1

    def redraw_window():
        screen.blit(BG, (0, 0))

        ready_archers_label_1 = default_font.render(f"Ready Archers: {num_archer_p1}", True, (255, 0, 255))
        ready_swordsmen_label_1 = default_font.render(f"| Ready Swordsmen: {num_swordsmen_p1}", True, (255, 0, 255))
        archers_in_training_1 = default_font.render(f"Issued archers: {count_archer_p1}", True, (255, 0, 255))
        swordsmen_in_training_1 = default_font.render(f"Issued swordsmen: {count_swordsmen_p1}", True, (255, 0, 255))
        player1_resource_label = resource_font.render(f"Resource: {player1_resource}", True, (255, 0, 0))
        tot_soldiers_p1_label = default_font.render(f"Total number of soldiers: {len(archers_p1) + len(swordsmen_p1)}",
                                                    1, (255, 255, 255))

        screen.blit(player1_resource_label, (10, 5))
        screen.blit(ready_archers_label_1, (10, 30))
        screen.blit(ready_swordsmen_label_1, (ready_archers_label_1.get_width() + 15, 30))
        screen.blit(archers_in_training_1, (10, 40))
        screen.blit(swordsmen_in_training_1, (archers_in_training_1.get_width() + 15, 40))
        screen.blit(tot_soldiers_p1_label, (10, 60))

        for i in range(len(archers_p1)):
            if archers_p1[i].ready_to_dispatch:
                archers_p1[i].draw(screen)
            if archers_p1[i].x > WIDTH - 100:
                archers_p1.remove(archers_p1[i])
            if archers_p1[i].dead:
                archers_p1.remove(archers_p1[i])

        for i in range(len(swordsmen_p1)):
            if swordsmen_p1[i].ready_to_dispatch:
                swordsmen_p1[i].draw(screen)
            if swordsmen_p1[i].x > WIDTH - 100:
                swordsmen_p1.remove(swordsmen_p1[i])
            if swordsmen_p1[i].dead:
                swordsmen_p1.remove(swordsmen_p1[i])

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
                    if player1_resource >= 0:
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
                    if num_archer_p1 > 0:
                        archer_index_p1, num_archer_p1 = Functions.attack(archers_p1, archer_index_p1, num_archer_p1)

                if event.key == pg.K_d:
                    if num_swordsmen_p1 > 0:
                        swordsman_index_p1, num_swordsmen_p1 = Functions.attack(swordsmen_p1, swordsman_index_p1,
                                                                                num_swordsmen_p1)

                if event.key == pg.K_z:
                    Functions.deploy_all(archers_p1)
                    Functions.deploy_all(swordsmen_p1)
                    num_archer_p1 = 0
                    num_swordsmen_p1 = 0

        Functions.add_to_queue(archers_p1, count_archer_p1, "archers_p1", screen)
        num_archer_p1, count_archer_p1, total_archer_p1 = Functions.check_added(archers_p1, num_archer_p1,
                                                                                count_archer_p1, "archers_p1",
                                                                                p1_total_soldiers)

        Functions.add_to_queue(swordsmen_p1, count_swordsmen_p1, "swordsmen_p1", screen)
        num_swordsmen_p1, count_swordsmen_p1, p1_total_soldiers = Functions.check_added(swordsmen_p1, num_swordsmen_p1,
                                                                                        count_swordsmen_p1,
                                                                                        "swordsmen_p1",
                                                                                        p1_total_soldiers)

        if count_archer_p1 <= 0:
            count_archer_p1 = 0
        if count_swordsmen_p1 <= 0:
            count_swordsmen_p1 = 0

        for i in range(len(archers_p1)):
            if archers_p1[i].ready_to_dispatch is False:
                archers_p1[i].train()
        for i in range(len(swordsmen_p1)):
            if swordsmen_p1[i].ready_to_dispatch is False:
                swordsmen_p1[i].train()

        for i in range(len(archers_p1)):
            # if soldier is dispatchable it gets deployed
            if archers_p1[i].deploy:
                if archers_p1[i].run:
                    archers_p1[i].move()
                archers_p1[i].update()
            in_range(archers_p1[i])

        for i in range(len(swordsmen_p1)):
            # if soldier is dispatchable it gets deployed
            if swordsmen_p1[i].deploy and swordsmen_p1[i].run:
                swordsmen_p1[i].move()
                swordsmen_p1[i].update()
            # in_range(swordsmen_p1[i])


if __name__ == '__main__':
    main()
