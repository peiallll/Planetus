import pygame as pg
import random as r
import math as m
import time as t
import copy

from physics.body import Body
from settings import settings as s

class Simulation:
    def __init__(self):
        self.bodies = []
        self.current_body = None
        self.current_mass = 5000
        self.current_body_initial_velocity = 0
        self.paused = False
        self.paused_text = ""
        self.id = 1
        self.ghost_bodies = []
        self.sim_speed = 1
        self.trail_points = []
        self.trail_decider = 0
        self.trail_decider_value = 1
        self.trail_enabled = True
        self.arrow_enabled = True
        self.elapsed_time = 0

    def adjust_mass(self, amount):
        self.current_mass = max(10, self.current_mass + amount)

    def toggle_pause(self):
        self.paused = not self.paused
        self.paused_text = "PAUSED" if self.paused else ""

    def set_inital_velocity(self, body):
        x, y = pg.mouse.get_pos()

        dx = x - body.x
        dy = y - body.y
        
        body.vx = dx / 5
        body.vy = dy / 5

        self.current_body_initial_velocity = round(m.sqrt((body.vx**2) + (body.vy**2)), 2)

    def ghost_orbit(self, current_body, steps=3000, dt=0.1, record_every=10):
        self.ghost_bodies = [copy.copy(b) for b in self.bodies]
        path_points = []

        current_ghost = self.ghost_bodies[-1]

        for i in range(steps):
            for ghost in self.ghost_bodies:
                total_fx, total_fy = 0, 0
                for neighbour in self.ghost_bodies:
                    if neighbour is ghost: continue
                    
                    dx = neighbour.x - ghost.x
                    dy = neighbour.y - ghost.y
                    distance = m.sqrt((dx**2) + (dy**2))
                    
                    force = (s.G * ghost.mass * neighbour.mass) / (distance**2 + 0.1)

                    total_fx += force * (dx / distance)
                    total_fy += force * (dy / distance)
                
                ax = total_fx / ghost.mass
                ay = total_fy / ghost.mass

                ghost.vx += ax * dt
                ghost.vy += ay * dt

            for ghost in self.ghost_bodies:
                ghost.x += ghost.vx * dt
                ghost.y += ghost.vy * dt
                
            if i % record_every == 0:
                path_points.append((current_ghost.x, current_ghost.y))
        return path_points

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
                    (r.randint(0,255), r.randint(0,255), r.randint(0,255)),
                    f"{self.id}"
                )
            
            self.current_body = new_body
            self.bodies.append(new_body)
            self.id += 1

    def get_time(self, dt):
        if not self.paused:
            self.elapsed_time += dt * self.sim_speed
        return self.elapsed_time
    
    def update(self, dt):
        for body in self.bodies:
            if self.arrow_enabled:
                body.v_arrow_end = None

                direction_r = m.atan2(body.vy, body.vx)
                body.direction = direction_r * (180 / m.pi)
                    
                body.line_length = m.sqrt(body.vx**2 + body.vy**2) * 2

                end_x = body.x + (m.cos(direction_r) * body.line_length)
                end_y = body.y + (m.sin(direction_r) * body.line_length)

                body.v_arrow_end = (end_x, end_y)

                body.left_tip_end = (end_x - m.cos(direction_r + 0.5) * 10, end_y - m.sin(direction_r + 0.5) * 10)
                body.right_tip_end = (end_x - m.cos(direction_r - 0.5) * 10, end_y - m.sin(direction_r - 0.5) * 10)

        if self.paused:
            return
        
        for _ in range(self.sim_speed):
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

                    force = (s.G * body.mass * neighbour.mass) / (distance**2 + 0.1) #Newton's law

                    fx = force * direction_x
                    fy = force * direction_y

                    total_fx += fx
                    total_fy += fy

                ax = total_fx / body.mass
                ay = total_fy / body.mass

                body.vx += ax * dt
                body.vy += ay * dt

                body.v = m.sqrt(body.vx**2 + body.vy**2)

            for body in self.bodies:
                body.x += body.vx * dt
                body.y += body.vy * dt

                if self.trail_enabled:
                    if self.trail_decider % self.trail_decider_value == 0:
                        body.trail_points[(body.x, body.y)] = t.time()

                    while body.trail_points:
                        oldest_point = next(iter(body.trail_points))
                        if t.time() - body.trail_points[oldest_point] < 5:
                            break
                        del body.trail_points[oldest_point]
                else:
                    if len(body.trail_points) != 0:
                        body.trail_points.clear()

            for body in self.bodies:
                if body.x > s.WIDTH * 2 or body.x < -s.WIDTH * 2 or body.y > s.HEIGHT * 2 or body.y < -s.HEIGHT * 2:
                    self.bodies.remove(body)

            self.trail_decider += 1