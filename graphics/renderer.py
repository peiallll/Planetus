import pygame as pg
import pygame_widgets as widgets
import random as r
from settings import settings as s

pg.font.init()
mass_font = pg.font.SysFont('Arial', 30)
paused_font = pg.font.SysFont('Arial', 35)
instructions_font = pg.font.SysFont('Arial', 25)

v_font = pg.font.SysFont('Arial', 15)

class Renderer:
    def __init__(self):
        self.stars = [
            (r.randint(0, s.WIDTH), r.randint(0, s.HEIGHT))
            for _ in range(150)
        ]

    def draw_background(self, screen, sim_speed):
        for x, y in self.stars:
            pg.draw.circle(screen, (255,255,255), (x, y), 1)

        for i, line in enumerate("B to create new bodies\nSpace to pause\nX to clear all bodies on screen\n Shift/Control control speed of simulation".split("\n")):
            instructions_text = instructions_font.render(line, True, (255,255,255))
            screen.blit(instructions_text, (s.WIDTH * 0.025, (s.HEIGHT * 0.95) - i * 35))

        screen.blit(instructions_font.render(f"Simulation Speed: {sim_speed}x", True, (255,255,255)), (s.WIDTH * 0.4, s.HEIGHT * 0.95))

    def draw_bodies(self, screen, bodies):
        for body in bodies:
            pg.draw.circle(screen, body.colour, (body.x, body.y), body.radius)

    def draw_line(self, screen, body, v):
        mouse_pos = pg.mouse.get_pos()
        pg.draw.line(screen, (255,175,175), (body.x, body.y), mouse_pos, 5)

        line_midpoint_x = (body.x + mouse_pos[0]) // 2
        line_midpoint_y = (body.y + mouse_pos[1]) // 2

        v_text = v_font.render(f"velocity: {v}", True, (255, 255, 255))
        v_rect = v_text.get_rect(center=(line_midpoint_x, line_midpoint_y + 30))

        screen.blit(v_text, v_rect)

    def draw_ghost_orbit(self, screen, path_points):
        for point in path_points:
            pg.draw.circle(screen, (110,110,110), point, 2)

    def draw_body_trail(self, screen, bodies):
        for body in bodies:
            for point in body.trail_points:
                pg.draw.circle(screen, body.colour, point, 1)

    def draw_mass_text(self, screen, mass):
        mass_text = mass_font.render(f"Mass: {mass}", True, (255, 255, 255))
        text_rect = mass_text.get_rect(center=(s.WIDTH * 0.9, s.HEIGHT * 0.9))
        screen.blit(mass_text, text_rect)
    
    def enable_paused_text(self, screen, paused_state):
        paused_text = paused_font.render(f"{paused_state}", True, (200, 200, 200))
        text_rect = paused_text.get_rect(center=(s.WIDTH * 0.5, s.HEIGHT * 0.1))
        screen.blit(paused_text, text_rect)