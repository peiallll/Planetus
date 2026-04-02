import pygame as pg
import random as r
from settings import settings as s

class Renderer:
    def __init__(self):
        # generate stars once
        self.stars = [
            (r.randint(0, s.WIDTH), r.randint(0, s.HEIGHT))
            for _ in range(150)
        ]

    def draw_background(self, screen):
        for x, y in self.stars:
            pg.draw.circle(screen, (255,255,255), (x, y), 1)
