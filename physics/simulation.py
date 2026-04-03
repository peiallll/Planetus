import pygame as pg
import random as r
from physics.body import Body
from settings import settings as s

class Simulation:
    def __init__(self):
        self.bodies = []

    def add_random_body(self):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]
        if x > 0 and x < s.WIDTH - 5 and y > 0 and y < s.HEIGHT - 5:
            self.bodies.append(
                Body(
                    x,
                    y,
                    0,
                    0,
                    5,
                    8,
                    (r.randint(0,255), r.randint(0,255), r.randint(0,255))
                )
            )
