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
    archers_p2 = []
    swordsmen_p1 = []
    swordsmen_p2 = []
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
    archer_index_p2 = 0
    swordsman_index_p2 = 0
    count_archer_p2 = 0
    num_archer_p2 = 0
    count_swordsmen_p2 = 0
    num_swordsmen_p2 = 0
    p2_total_soldiers = 0

    # Fonts
    default_font = pg.font.SysFont("comicsans", 12)
    resource_font = pg.font.SysFont("comicsans", 20)

    def in_range(object1):
        if isinstance(object1, Archer):
            match object1.type:
                case "p1":
                    if object1.x >= WIDTH - (random.randint(0, 100) + 700) and object1.deploy:
                        object1.run = False
                        object1.ready_to_shoot("p1")
                case "p2":
                    if object1.x <= 0 + (300 - random.randint(0, 100)) and object1.deploy:
                        object1.run = False
                        object1.ready_to_shoot("p2")
        return object1

    def redraw_window():
        screen.blit(BG, (0, 0))

        ready_archers_label_1 = default_font.render(f"Ready Archers: {num_archer_p1}", True, (255, 0, 255))
        ready_swordsmen_label_1 = default_font.render(f"| Ready Swordsmen: {num_swordsmen_p1}", True, (255, 0, 255))
        archers_in_training_1 = default_font.render(f"Issued archers: {count_archer_p1}", True, (255, 0, 255))
        swordsmen_in_training_1 = default_font.render(f"| Issued swordsmen: {count_swordsmen_p1}", True, (255, 0, 255))
        player1_resource_label = resource_font.render(f"Resource: {player1_resource}", True, (255, 0, 0))
        tot_soldiers_p1_label = default_font.render(f"Total number of soldiers: {len(archers_p1) + len(swordsmen_p1)}",
                                                    1, (0, 0, 0))
        ready_archers_label_2 = default_font.render(f"Ready Archers: {num_archer_p2}", True, (255, 0, 255))
        ready_swordsmen_label_2 = default_font.render(f"| Ready Swordsmen: {num_swordsmen_p2}", True, (255, 0, 255))
        archers_in_training_2 = default_font.render(f"Issued archers: {count_archer_p2}", True, (255, 0, 255))
        swordsmen_in_training_2 = default_font.render(f"| Issued swordsmen: {count_swordsmen_p2}", True, (255, 0, 255))
        player2_resource_label = resource_font.render(f"Resource: {player2_resource}", True, (255, 0, 0))
        tot_soldiers_p2_label = default_font.render(f"Total number of soldiers: {len(archers_p2) + len(swordsmen_p2)}",
                                                    1, (0, 0, 0))

        screen.blit(player1_resource_label, (10, 5))
        screen.blit(ready_archers_label_1, (10, 35))
        screen.blit(ready_swordsmen_label_1, (ready_archers_label_1.get_width() + 15, 35))
        screen.blit(archers_in_training_1, (10, 45))
        screen.blit(swordsmen_in_training_1, (archers_in_training_1.get_width() + 15, 45))
        screen.blit(tot_soldiers_p1_label, (10, 60))

        screen.blit(player2_resource_label, (WIDTH - player2_resource_label.get_width(), 5))
        screen.blit(ready_archers_label_2, (WIDTH - ready_archers_label_2.get_width(), 35))
        screen.blit(ready_swordsmen_label_2, (WIDTH - ready_archers_label_2.get_width() - 15, 35))
        screen.blit(archers_in_training_2, (WIDTH - archers_in_training_2.get_width(), 45))
        screen.blit(swordsmen_in_training_2, (WIDTH - archers_in_training_2.get_width() - 15, 45))
        screen.blit(tot_soldiers_p2_label, (WIDTH - tot_soldiers_p2_label.get_width(), 60))

        Functions.draw(archers_p1, screen)
        Functions.draw(archers_p2, screen)
        Functions.draw(swordsmen_p1, screen)
        Functions.draw(swordsmen_p2, screen)

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

                if event.key == pg.K_i:
                    if player2_resource >= 0:
                        player2_resource -= Archer.COST
                        count_archer_p2 += 1

                    else:
                        player2_resource = 0

                if event.key == pg.K_w:
                    if player1_resource > 0:
                        player1_resource -= SwordMan.COST
                        count_swordsmen_p1 += 1
                    else:
                        player1_resource = 0

                if event.key == pg.K_o:
                    if player2_resource > 0:
                        player2_resource -= SwordMan.COST
                        count_swordsmen_p2 += 1
                    else:
                        player2_resource = 0

                if event.key == pg.K_f:
                    if num_archer_p1 > 0:
                        archer_index_p1, num_archer_p1 = Functions.attack(archers_p1, archer_index_p1, num_archer_p1)

                if event.key == pg.K_h:
                    if num_archer_p2 > 0:
                        archer_index_p2, num_archer_p2 = Functions.attack(archers_p2, archer_index_p2, num_archer_p2)

                if event.key == pg.K_d:
                    if num_swordsmen_p1 > 0:
                        swordsman_index_p1, num_swordsmen_p1 = Functions.attack(swordsmen_p1, swordsman_index_p1,
                                                                                num_swordsmen_p1)
                if event.key == pg.K_j:
                    if num_swordsmen_p2 > 0:
                        swordsman_index_p2, num_swordsmen_p2 = Functions.attack(swordsmen_p2, swordsman_index_p2,
                                                                                num_swordsmen_p2)

                if event.key == pg.K_z:
                    Functions.deploy_all(archers_p1)
                    Functions.deploy_all(swordsmen_p1)
                    num_archer_p1 = 0
                    num_swordsmen_p1 = 0

        # PLAYER 1 ARCHERS
        Functions.add_to_queue(archers_p1, count_archer_p1, "archers_p1", screen)
        num_archer_p1, count_archer_p1, total_archer_p1 = Functions.check_added(archers_p1, num_archer_p1,
                                                                                count_archer_p1, "archers_p1",
                                                                                p1_total_soldiers)
        # PLAYER 2 ARCHERS
        Functions.add_to_queue(archers_p2, count_archer_p2, "archers_p2", screen)
        num_archer_p2, count_archer_p2, total_archer_p2 = Functions.check_added(archers_p2, num_archer_p2,
                                                                                count_archer_p2, "archers_p2",
                                                                                p2_total_soldiers)

        Functions.add_to_queue(swordsmen_p1, count_swordsmen_p1, "swordsmen_p1", screen)
        num_swordsmen_p1, count_swordsmen_p1, p1_total_soldiers = Functions.check_added(swordsmen_p1, num_swordsmen_p1,
                                                                                        count_swordsmen_p1,
                                                                                        "swordsmen_p1",
                                                                                        p1_total_soldiers)
        Functions.add_to_queue(swordsmen_p2, count_swordsmen_p2, "swordsmen_p2", screen)
        num_swordsmen_p2, count_swordsmen_p2, p2_total_soldiers = Functions.check_added(swordsmen_p2, num_swordsmen_p2,
                                                                                        count_swordsmen_p2,
                                                                                        "swordsmen_p2",
                                                                                        p2_total_soldiers)

        if count_archer_p1 <= 0:
            count_archer_p1 = 0
        if count_archer_p2 <= 0:
            count_archer_p2 = 0
        if count_swordsmen_p1 <= 0:
            count_swordsmen_p1 = 0
        if count_swordsmen_p2 <= 0:
            count_swordsmen_p2 = 0

        Functions.training(archers_p1)
        Functions.training(archers_p2)

        Functions.training(swordsmen_p1)
        Functions.training(swordsmen_p2)

        Functions.deploy(archers_p1)
        Functions.deploy(archers_p2)

        Functions.deploy(swordsmen_p1)
        Functions.deploy(swordsmen_p2)

        Functions.collide(archers_p1, archers_p2)
        Functions.collide(swordsmen_p1, swordsmen_p2)

        # for i in range(len(swordsmen_p1)):
        #     # if soldier is dispatchable it gets deployed
        #     if swordsmen_p1[i].deploy and swordsmen_p1[i].run:
        #         swordsmen_p1[i].move()
        #         swordsmen_p1[i].update()
        #     # in_range(swordsmen_p1[i])


if __name__ == '__main__':
    main()
