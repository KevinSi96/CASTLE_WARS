import random

import pygame as pg

from objects.players.Archer import Archer
from objects.players.SwordMan import SwordMan

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

    # Fonts
    default_font = pg.font.SysFont("comicsans", 10)
    resource_font = pg.font.SysFont("comicsans", 20)

    def in_range(object1):
        if isinstance(object1, Archer):
            if object1.x >= WIDTH - (random.randint(0, 100) + 300) and object1.deploy:
                object1.run = False
                object1.ready_to_shoot()
                print(str(round(object1.current_time - object1.start_shoot)))
        return object1

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

    def redraw_window():
        screen.blit(BG, (0, 0))

        ready_archers_label_1 = default_font.render(f"Ready Archers: {num_archer_p1}", 1, (255, 255, 255))
        ready_swordsmen_label_1 = default_font.render(f"Ready Swordsmen: {num_swordsmen_p1}", 1, (255, 255, 255))
        archers_in_training_1 = default_font.render(f"Issued archers: {count_archer_p1}", 1, (255, 255, 255))
        player1_resource_label = resource_font.render(f"Resource: {player1_resource}", 1, (255, 0, 0))
        tot_soldiers_p1_label = default_font.render(f"Total number of soldiers: {len(archers_p1) + len(swordsmen_p1)}", 1,(255, 255, 255))
        screen.blit(player1_resource_label, (10, 5))
        screen.blit(ready_archers_label_1, (10, 30))
        screen.blit(archers_in_training_1, (10, 40))
        screen.blit(tot_soldiers_p1_label, (10, 50))
        for i in range(len(archers_p1)):
            if archers_p1[i].ready_to_dispatch:
                archers_p1[i].draw(screen)
            if archer.x > WIDTH - 100:
                archers_p1.remove(archers_p1[i])
            if archers_p1[i].dead:
                archers_p1.remove(archers_p1[i])

        for swordsman in swordsmen_p1:
            if swordsman.ready_to_dispatch:
                swordsman.draw(screen)
            if swordsman.x > WIDTH - 100:
                swordsmen_p1.remove(swordsman)

        pg.display.update()

    loop = 1

    while loop:

        clock.tick(24)
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
                        archer_index_p1, num_archer_p1 = attack(archers_p1, archer_index_p1, num_archer_p1)
                #
                # if event.key == pg.K_d:
                #         swordsman_index_p1, num_swordsmen_p1 = attack(swordsmen_p1, swordsman_index_p1,
                #                                                       num_swordsmen_p1)

                if event.key == pg.K_z:
                    deploy_all(archers_p1)
                    # deploy_all(swordsmen_p1)
                    num_archer_p1 = 0
                    # num_swordsmen_p1 = 0
        for i in range(len(archers_p1)):
            if archers_p1[i].ready_to_dispatch and archers_p1[i].archer_added is False:
                num_archer_p1 += 1
                archers_p1[i].archer_added = True

        for i in range(count_archer_p1):
            archer = Archer(100, random.randrange(10, 30), 165, False, screen, "sprites/player1/bow/run/run-", ".png")
            if len(archers_p1) >= 1:
                prev_archer = archers_p1[len(archers_p1) - 1]
                if prev_archer.ready_to_dispatch:
                    archers_p1.append(archer)
                    count_archer_p1 -= 1

            elif len(archers_p1) == 0:
                count_archer_p1 -= 1
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

        for i in range(len(archers_p1)):
            if archers_p1[i].ready_to_dispatch is False:
                archers_p1[i].train()
        # for swordsman in swordsmen_p1:
        #     if swordsman.ready_to_dispatch is False:
        #         swordsman.train()

        if count_archer_p1 <= 0:
            count_archer_p1 = 0
        # if count_swordsmen_p1 <= 0:
        #     count_swordsmen_p1 = 0

        print("issued archers: " + str(count_archer_p1) + " no. of archers: " + str(len(archers_p1)) + " index: " + str(
            archer_index_p1) + " ready archers: " + str(num_archer_p1) + " | "
              + "issued swordsman: " + str(count_swordsmen_p1) + " no. of swordsmen: " + str(
            len(swordsmen_p1)) + " index: " + str(swordsman_index_p1) + " resources: " + str(player1_resource))

        for i in range(len(archers_p1)):
            # if soldier is dispatchable it gets deployed
            if archers_p1[i].deploy and archers_p1[i].run:
                archers_p1[i].move()
                archers_p1[i].update()
            in_range(archers_p1[i])
        # for swordsman in swordsmen_p1:
        #     # if soldier is dispatchable it gets deployed
        #     if swordsman.attack:
        #         swordsman.move()
        #         swordsman.update()


if __name__ == '__main__':
    main()
