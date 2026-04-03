import pygame as pg
import random as r
from settings import settings as s

pg.font.init()
mass_font = pg.font.SysFont('Arial', 30)

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

    def draw_bodies(self, screen, bodies):
        for body in bodies:
            pg.draw.circle(screen, body.colour, (body.x, body.y), body.radius)

    def draw_mass_text(self, screen, mass):
        mass_text = mass_font.render(f"Mass: {mass}", True, (255, 255, 255))
        text_rect = mass_text.get_rect(center=(s.WIDTH * 0.9, s.HEIGHT * 0.9))
        screen.blit(mass_text, text_rect)