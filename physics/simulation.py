import pygame as pg
import random as r
import math as m

from physics.body import Body
from settings import settings as s

class Simulation:
    def __init__(self):
        self.bodies = []
        self.current_mass = 5000

    def adjust_mass(self, amount):
        self.current_mass = max(10, self.current_mass + amount)

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
                    self.current_mass,
                    8,
                    (r.randint(0,255), r.randint(0,255), r.randint(0,255))
                )
            )

    def update(self, dt):
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
            if body.x > s.WIDTH * 2 or body.y > s.HEIGHT * 2:
                self.bodies.remove(body)