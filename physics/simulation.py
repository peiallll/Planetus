import pygame as pg
import random as r
import math as m

from physics.body import Body
from settings import settings as s

class Simulation:
    def __init__(self):
        self.bodies = []
        self.current_body = None
        self.current_mass = 5000
        self.current_body_vx = 0
        self.current_body_vy = 0
        self.paused = False
        self.paused_text = ""

    def adjust_mass(self, amount):
        self.current_mass = max(10, self.current_mass + amount)

    def toggle_pause(self):
        self.paused = not self.paused
        self.paused_text = "PAUSED" if self.paused else ""

    def set_inital_velocity(self, body):
        x, y = pg.mouse.get_pos()

        dx = x - body.x
        dy = y - body.y

        self.current_body_vx = dx / 5
        self.current_body_vy = dy / 5
        
        body.vx = self.current_body_vx
        body.vy = self.current_body_vy

    def add_random_body(self):
        self.paused = True
        self.paused_text = "PAUSED" if self.paused else ""

        x, y = pg.mouse.get_pos()

        if x > 0 and x < s.WIDTH - 5 and y > 0 and y < s.HEIGHT - 5:
            new_body = Body(
                    x,
                    y,
                    0,
                    0,
                    self.current_mass,
                    self.current_mass ** (1/5),
                    (r.randint(0,255), r.randint(0,255), r.randint(0,255))
                )
            
            self.current_body = new_body
            self.bodies.append(new_body)

    def update(self, dt):
        if self.paused:
            return
        
        for body in self.bodies:
            total_fx = 0
            total_fy = 0
            for neighbour in self.bodies:
                if neighbour is body:
                    continue

                dx = neighbour.x - body.x
                dy = neighbour.y - body.y

                distance = m.sqrt(dx**2 + dy**2)
                #
                direction_x = dx / distance
                direction_y = dy / distance

                force = s.G * body.mass * neighbour.mass / (distance**2 + 0.1) #Newton's law

                fx = force * direction_x
                fy = force * direction_y

                total_fx += fx
                total_fy += fy

            ax = total_fx / body.mass
            ay = total_fy / body.mass

            body.vx += ax * dt
            body.vy += ay * dt

        for body in self.bodies:
            body.x += body.vx * dt
            body.y += body.vy * dt

        for body in self.bodies:
            if body.x > s.WIDTH * 2 or body.x < -s.WIDTH * 2 or body.y > s.HEIGHT * 2 or body.y < -s.HEIGHT * 2:
                self.bodies.remove(body)