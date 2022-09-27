import pygame as pg


class Inputs:
    def __init__(self, inputs):
        self.worker_train_key = pg.key.key_code(inputs['worker_train'])
        self.sword_train_key = pg.key.key_code(inputs['sword_train'])
        self.archer_train_key = pg.key.key_code(inputs['archer_train'])
        self.to_mine_key = pg.key.key_code(inputs['to_mine'])
        self.to_wall_key = pg.key.key_code(inputs['to_wall'])
        self.sword_attack_key = pg.key.key_code(inputs['sword_attack'])
        self.archer_attack_key = pg.key.key_code(inputs['archer_attack'])
        self.unleash_key = pg.key.key_code(inputs['unleash'])
