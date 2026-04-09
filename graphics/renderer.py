import pygame as pg
import pygame_widgets as widgets
import random as r
from settings import settings as s

pg.font.init()
mass_font = pg.font.SysFont('Arial', 30)
paused_font = pg.font.SysFont('Arial', 35)
small_medium_font = pg.font.SysFont('Arial', 25)

small_font = pg.font.SysFont('Arial', 15)

class Renderer:
    def __init__(self):
        self.stars = [
            (r.randint(0, s.WIDTH), r.randint(0, s.HEIGHT))
            for _ in range(150)
        ]

    def draw_background(self, screen, sim_speed, fps, time):
        for x, y in self.stars:
            pg.draw.circle(screen, (255,255,255), (x, y), 1)

        for i, line in enumerate("B: create new bodies\nSpace: pause simulation\nUP/DOWN arrow keys: control speed of simulation".split("\n")):
            instructions_text = small_medium_font.render(line, True, (255,255,255))
            screen.blit(instructions_text, (s.WIDTH * 0.025, (s.HEIGHT * 0.95) - i * 35))

        fps_text = small_medium_font.render(f"FPS: {fps}", True, (255,255,255))
        time_text = small_medium_font.render(f"Time: {round(time / 86400, 2)}d", True, (255,255,255))
        screen.blit(fps_text, (s.WIDTH * 0.9, s.HEIGHT * 0.025))
        screen.blit(time_text, (s.WIDTH * 0.8, s.HEIGHT * 0.05))
        screen.blit(small_medium_font.render(f"Simulation Speed: {sim_speed}x", True, (255,255,255)), (s.WIDTH * 0.4, s.HEIGHT * 0.95))

    def draw_bodies(self, screen, bodies):
        for body in bodies:
            px = int(body.x / s.DISTANCE_SCALE)
            py = int(body.y / s.DISTANCE_SCALE)
            pg.draw.circle(screen, body.colour, (px, py), body.radius)

    def draw_line(self, screen, body, v):
        mouse_pos = pg.mouse.get_pos()
        body_x = int(body.x / s.DISTANCE_SCALE)
        body_y = int(body.y / s.DISTANCE_SCALE)

        pg.draw.line(screen, (255,175,175), (body_x, body_y), mouse_pos, 5)

        line_midpoint_x, line_midpoint_y = self.line_midpoint(body_x, mouse_pos[0], body_y, mouse_pos[1])

        v_text = small_font.render(f"velocity: {v} m/s", True, (255,255,255))
        v_rect = v_text.get_rect(center=(line_midpoint_x, line_midpoint_y + 30))

        screen.blit(v_text, v_rect)

    def draw_ruler(self, screen, start_x, start_y, end_x, end_y, ruler_length):
        pg.draw.line(screen, (255, 255, 255), (start_x, start_y), (end_x, end_y), 3)
        
        line_midpoint_x, line_midpoint_y = self.line_midpoint(start_x, end_x, start_y, end_y)

        d_text = small_font.render(f"distance: {round(ruler_length / 1000, 2)}km", True, (255,255,255))
        d_rect = d_text.get_rect(center=(line_midpoint_x, line_midpoint_y + 30))

        screen.blit(d_text, d_rect)

    def line_midpoint(self, start_x, end_x, start_y, end_y):
        mid_x = (start_x + end_x) // 2
        mid_y = (start_y + end_y) // 2
        return mid_x, mid_y
    
    def draw_direction_arrow(self, screen, bodies):
        for body in bodies:
            pg.draw.line(screen, (255,255,255), (int(body.x / s.DISTANCE_SCALE), int(body.y / s.DISTANCE_SCALE)), body.v_arrow_end, 3)
            pg.draw.line(screen, (255,255,255), body.v_arrow_end, body.left_tip_end, 3)
            pg.draw.line(screen, (255,255,255), body.v_arrow_end, body.right_tip_end, 3)

            v_text = small_font.render(f"velocity: {round(body.v,2)} m/s", True, (255, 255, 255))
            v_rect = v_text.get_rect(center=(body.v_arrow_end[0], body.v_arrow_end[1] - 20))

            screen.blit(v_text, v_rect)

    def draw_ghost_orbit(self, screen, path_points):
        for point in path_points:
            pg.draw.circle(screen, (110,110,110), point, 2)

    def draw_body_trail(self, screen, bodies):
        for body in bodies:
            for point in body.trail_points:
                pg.draw.circle(screen, body.colour, point, 1)

    def draw_mass_text(self, screen, mass):
        mass_text = mass_font.render(f"Mass: {mass:.2e}", True, (255, 255, 255))
        text_rect = mass_text.get_rect(center=(s.WIDTH * 0.825, s.HEIGHT * 0.91))
        screen.blit(mass_text, text_rect)
    
    def enable_paused_text(self, screen, paused_state):
        paused_text = paused_font.render(f"{paused_state}", True, (200, 200, 200))
        text_rect = paused_text.get_rect(center=(s.WIDTH * 0.5, s.HEIGHT * 0.1))
        screen.blit(paused_text, text_rect)

    def collision_effect(self, screen, particles):
        for particle in particles:
            pg.draw.circle(screen, particle.colour, (particle.x, particle.y), particle.radius)