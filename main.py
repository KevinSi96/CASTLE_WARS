import sys

import pygame as pg

from implementable.Functions import redraw_window
from objects.Constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER1_KEY_COMMANDS, PLAYER2_KEY_COMMANDS
from objects.Inputs import Inputs
from objects.players.Player import Player

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

player1, player2 = None, None


def main():
    global player1, player2
    game_over = False
    restarted = False
    winner = None
    pause = False

    player1_inputs = Inputs(PLAYER1_KEY_COMMANDS)
    player2_inputs = Inputs(PLAYER2_KEY_COMMANDS)

    player1 = Player("p1", player1_inputs)
    player2 = Player("p2", player2_inputs)

    player1.opponent = player2
    player2.opponent = player1

    loop = True

    while loop:

        clock.tick(60)
        redraw_window(player1, player2, game_over, screen, winner, pause)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if not pause:
                    player1.key_events(event.key)
                    player2.key_events(event.key)
                if event.key == pg.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
                if event.key == pg.K_r and pause:
                    restarted = True
                    pause = False
            if game_over and not restarted:
                if event.type == pg.KEYDOWN:
                    restarted = True
                    game_over = False

        if not game_over:
            if restarted:
                player1 = Player("p1", player1_inputs)
                player2 = Player("p2", player2_inputs)
                player1.opponent = player2
                player2.opponent = player1
                winner = None
                restarted = False
            elif not restarted and not pause:
                game_over = player1.update(game_over)
                game_over = player2.update(game_over)
            elif pause:
                pass

        elif game_over:
            player1.soldiers.clear()
            player1.workers.clear()
            player2.soldiers.clear()
            player2.workers.clear()
            if player1.castle.wall.health <= 0:
                winner = "BLUE"
            elif player2.castle.wall.health <= 0:
                winner = "RED"


if __name__ == '__main__':
    main()
