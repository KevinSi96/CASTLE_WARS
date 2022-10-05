from objects.Barracks import Barracks
from objects.Constants import WALL_POS, BARRACKS_POS, MINE_POS, SCREEN_WIDTH, P1_SPRITES, P2_SPRITES
from objects.Mine import Mine
from objects.Tower import Tower
from objects.Wall import Wall


class Castle:
    def __init__(self, player):
        wall_x = WALL_POS if player.player_type == "p1" else SCREEN_WIDTH - WALL_POS
        barracks_x = BARRACKS_POS if player.player_type == "p1" else SCREEN_WIDTH - BARRACKS_POS
        mine_x = MINE_POS if player.player_type == "p1" else SCREEN_WIDTH - MINE_POS
        tower_x = WALL_POS if player.player_type == "p1" else SCREEN_WIDTH - WALL_POS
        player_sprites = P1_SPRITES if player.player_type == "p1" else P2_SPRITES

        self.wall = Wall(player_sprites['building']['wall'], wall_x)
        self.barracks = Barracks(player_sprites['building']['barracks'], barracks_x, player)
        self.mine = Mine(player_sprites['building']['mine'], mine_x)
        self.tower = Tower(player_sprites['building']['tower'], tower_x, player.player_type)

    def update(self, target, enemy_units):
        self.barracks.update()
        # self.tower.update(target, enemy_units)

    def draw(self, screen):
        self.mine.draw(screen)
        self.barracks.draw(screen)
        self.tower.draw(screen)
        self.wall.draw(screen)
