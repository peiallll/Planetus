import pygame as pg
import random as r
from settings import settings as s

pg.font.init()
mass_font = pg.font.SysFont('Arial', 30)
paused_font = pg.font.SysFont('Arial', 35)

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
    
    def enable_paused_text(self, screen, paused_state):
        paused_text = paused_font.render(f"{paused_state}", True, (200, 200, 200))
        text_rect = paused_text.get_rect(center=(s.WIDTH * 0.5, s.HEIGHT * 0.1))
        screen.blit(paused_text, text_rect)