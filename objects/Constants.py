import pygame

pygame.init()

PLAYER_START_RESOURCES = 100

PLAYER1_KEY_COMMANDS = {
    "worker_train": "q",
    "sword_train": "w",
    "archer_train": "e",
    "to_mine": "a",
    "to_wall": "s",
    "sword_attack": "d",
    "archer_attack": "f",
    "unleash": "z"
}

PLAYER2_KEY_COMMANDS = {
    "worker_train": "p",
    "sword_train": "o",
    "archer_train": "i",
    "to_mine": "l",
    "to_wall": "k",
    "sword_attack": "j",
    "archer_attack": "h",
    "unleash": "m"
}

# ARCHER CONTANTS
ARCHER_COST = 5
ARCHER_TRAIN = 0
ARCHER_SPEED = 2
ARCHER_DAMAGE = 20
ARCHER_RANGE = 100
ARCHER_REST = 2
ARCHER_HEALTH = 100

# SWORD CONTANTS
SWORD_COST = 5
SWORD_TRAIN = 0
SWORD_SPEED = 2
SWORD_DAMAGE = 20
SWORD_RANGE = 10
SWORD_REST = 2

# WORKER CONTANTS
WORKER_COST = 5
WORKER_TRAIN = 2
WORKER_SPEED = 1
WORKER_PROD = 3
WORKER_REPAIR = 10

# GLOBAL
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 300
GROUND_HEIGHT = 70
WALL_POS = 180
WALL_WIDTH = 62
WALL_HEIGHT = 80
WALL_HEALTH = 1000
MINE_POS = 40
MINE_WIDTH = 58
MINE_HEIGHT = 37
BARRACKS_POS = 106
BARRACKS_WIDTH = 62
BARRACKS_HEIGHT = 50
TOWER_HEIGHT = 160

# SPRITE MAPS

P1_SPRITES = {"building":
    {
        "barracks": pygame.image.load("./sprites/player1/building/barracks.png"),
        "mine": pygame.image.load("./sprites/player1/building/mine.png"),
        "tower": pygame.image.load("./sprites/player1/building/tower.png"),
        "wall": pygame.image.load("./sprites/player1/building/wall.png")
    }
}

P2_SPRITES = {"building":
    {
        "barracks": pygame.image.load("./sprites/player2/building/barracks.png"),
        "mine": pygame.image.load("./sprites/player2/building/mine.png"),
        "tower": pygame.image.load("./sprites/player2/building/tower.png"),
        "wall": pygame.image.load("./sprites/player2/building/wall.png")
    }
}
