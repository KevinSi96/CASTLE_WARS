import sys

import pygame as pg

from objects.Constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER1_KEY_COMMANDS, PLAYER2_KEY_COMMANDS
from objects.Inputs import Inputs
from objects.players.Player import Player
from objects.players.SwordsMan import SwordsMan

pg.init()

INITIAL_RESOURCE = 30000

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
BG = pg.transform.scale(pg.image.load("sprites/background/BG.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
pg.font.init()

player1, player2 = None, None


def main():
    global player1, player2

    player1_inputs = Inputs(PLAYER1_KEY_COMMANDS)
    player2_inputs = Inputs(PLAYER2_KEY_COMMANDS)

    player1 = Player("p1", player1_inputs)
    player2 = Player("p2", player2_inputs)

    player1.opponent = player2
    player2.opponent = player1

    # Fonts
    default_font = pg.font.SysFont("comicsans", 12)
    resource_font = pg.font.SysFont("comicsans", 20)

    def redraw_window():
        screen.blit(BG, (0, 0))

        ready_archers_label_1 = default_font.render(f"Ready Archers: {player1.num_archer}", True, (255, 0, 255))
        ready_swordsmen_label_1 = default_font.render(f"| Ready Swordsmen: {player1.num_swordsmen}", True,
                                                      (255, 0, 255))
        archers_in_training_1 = default_font.render(f"Issued archers: {player1.count_archer}", True, (255, 0, 255))
        swordsmen_in_training_1 = default_font.render(f"| Issued swordsmen: {player1.count_sword}", True, (255, 0, 255))
        player1_resource_label = resource_font.render(f"Resource: {player1.player_resource}", True, (255, 0, 0))
        tot_soldiers_p1_label = default_font.render(f"Total number of soldiers: {player1.total_soldiers}",
                                                    1, (0, 0, 0))
        ready_archers_label_2 = default_font.render(f"Ready Archers: {player2.num_archer}", True, (255, 0, 255))
        ready_swordsmen_label_2 = default_font.render(f"| Ready Swordsmen: {player2.num_swordsmen}", True,
                                                      (255, 0, 255))
        archers_in_training_2 = default_font.render(f"Issued archers: {player2.count_archer}", True, (255, 0, 255))
        swordsmen_in_training_2 = default_font.render(f"| Issued swordsmen: {player2.count_sword}", True, (255, 0, 255))
        player2_resource_label = resource_font.render(f"Resource: {player2.player_resource}", True, (255, 0, 0))
        tot_soldiers_p2_label = default_font.render(f"Total number of soldiers: {player2.total_soldiers}",
                                                    1, (0, 0, 0))

        screen.blit(player1_resource_label, (10, 5))
        screen.blit(ready_archers_label_1, (10, 35))
        screen.blit(ready_swordsmen_label_1, (ready_archers_label_1.get_width() + 15, 35))
        screen.blit(archers_in_training_1, (10, 45))
        screen.blit(swordsmen_in_training_1, (archers_in_training_1.get_width() + 15, 45))
        screen.blit(tot_soldiers_p1_label, (10, 60))

        screen.blit(player2_resource_label, (SCREEN_WIDTH - player2_resource_label.get_width(), 5))
        screen.blit(ready_archers_label_2,
                    (SCREEN_WIDTH - ready_archers_label_2.get_width() - ready_swordsmen_label_2.get_width() - 5, 35))
        screen.blit(ready_swordsmen_label_2, (SCREEN_WIDTH - ready_archers_label_2.get_width() - 30, 35))
        screen.blit(archers_in_training_2,
                    (SCREEN_WIDTH - archers_in_training_2.get_width() - swordsmen_in_training_2.get_width() - 5, 45))
        screen.blit(swordsmen_in_training_2, (SCREEN_WIDTH - archers_in_training_2.get_width() - 30, 45))
        screen.blit(tot_soldiers_p2_label, (SCREEN_WIDTH - tot_soldiers_p2_label.get_width() - 5, 60))

        player1.draw(screen)
        player2.draw(screen)
        pg.display.update()

    loop = True

    while loop:

        clock.tick(60)
        redraw_window()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                loop = False
                sys.exit()
            if event.type == pg.KEYDOWN:
                player1.key_events(event.key)
                player2.key_events(event.key)

        player1.update()
        if len(player1.soldiers) > 0:
            if player1.soldiers[0].animation is not None:
                print(
                    f"{player1.soldiers[0].dead} +{player1.soldiers[0].target_unit.health if player1.soldiers[0].target_unit is not None else None} + {int(player1.soldiers[0].a_count)} + {player1.soldiers[0].health} + {len(player1.soldiers[0].animation)} + {player1.soldiers[0].attacking if isinstance(player1.soldiers[0], SwordsMan) else player1.soldiers[0].shooting}")
        player2.update()


if __name__ == '__main__':
    main()
