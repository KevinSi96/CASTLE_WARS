import sys

import pygame as pg

from objects.Constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER1_KEY_COMMANDS, PLAYER2_KEY_COMMANDS
from objects.Inputs import Inputs
from objects.players.Player import Player

pg.init()


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
BG = pg.transform.scale(pg.image.load("sprites/background/BG.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
pg.font.init()

player1, player2 = None, None


def main():
    global player1, player2
    game_over = False
    winner = None

    player1_inputs = Inputs(PLAYER1_KEY_COMMANDS)
    player2_inputs = Inputs(PLAYER2_KEY_COMMANDS)

    player1 = Player("p1", player1_inputs)
    player2 = Player("p2", player2_inputs)

    player1.opponent = player2
    player2.opponent = player1

    # Fonts
    default_font = pg.font.SysFont("comicsans", 12)
    resource_font = pg.font.SysFont("comicsans", 20)
    game_over_font = pg.font.Font('font/pixel.ttf', 40)

    def redraw_window():
        screen.blit(BG, (0, 0))

        ready_archers_label_1 = default_font.render(f"Ready Archers: {player1.num_archer}", True, (255, 0, 255))
        ready_workers_label_1 = default_font.render(f" | Ready Workers: {player1.num_workers}", True, (255, 0, 255))
        ready_swordsmen_label_1 = default_font.render(f"| Ready Swordsmen: {player1.num_swordsmen}", True,
                                                      (255, 0, 255))
        archers_in_training_1 = default_font.render(f"Issued archers: {player1.count_archer}", True, (255, 0, 255))
        workers_in_training_1 = default_font.render(f" | Issued workers: {player1.count_workers}", True, (255, 0, 255))
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
        screen.blit(ready_workers_label_1, (ready_archers_label_1.get_width() + ready_swordsmen_label_1.get_width() + 15, 35))
        screen.blit(workers_in_training_1, (archers_in_training_1.get_width() + swordsmen_in_training_1.get_width() + 15, 45))
        screen.blit(tot_soldiers_p1_label, (10, 60))

        screen.blit(player2_resource_label, (SCREEN_WIDTH - player2_resource_label.get_width(), 5))
        screen.blit(ready_archers_label_2,
                    (SCREEN_WIDTH - ready_archers_label_2.get_width() - ready_swordsmen_label_2.get_width() - 5, 35))
        screen.blit(ready_swordsmen_label_2, (SCREEN_WIDTH - ready_archers_label_2.get_width() - 30, 35))
        screen.blit(archers_in_training_2,
                    (SCREEN_WIDTH - archers_in_training_2.get_width() - swordsmen_in_training_2.get_width() - 5, 45))
        screen.blit(swordsmen_in_training_2, (SCREEN_WIDTH - archers_in_training_2.get_width() - 30, 45))
        screen.blit(tot_soldiers_p2_label, (SCREEN_WIDTH - tot_soldiers_p2_label.get_width() - 5, 60))

        if game_over:
            game_over_label = game_over_font.render(f"{winner} player wins", True, (0, 0, 0))
            game_over_label_rect = game_over_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(game_over_label, game_over_label_rect)
        player1.draw(screen)
        player2.draw(screen)
        pg.display.update()


    loop = True

    while loop:

        clock.tick(60)
        redraw_window()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                player1.key_events(event.key)
                player2.key_events(event.key)
        if not game_over:
            game_over = player1.update(game_over)
            game_over = player2.update(game_over)
        else:
            player1.soldiers.clear()
            player2.soldiers.clear()
            if player1.castle.wall.health <= 0:
                winner = "BLUE"
            elif player2.castle.wall.health <= 0:
                winner = "RED"


if __name__ == '__main__':
    main()
