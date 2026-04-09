import pygame as pg
import random as r
import math as m
import time as t
import copy

from physics.body import Body
from physics.debris import DebrisParticle
from settings import settings as s

class Simulation:
    def __init__(self):
        self.bodies = []
        self.current_body = None
        self.current_mass = s.DEFAULT_BODY_MASS
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
        self.collision_x = None
        self.collision_y = None
        self.debris = []

    def toggle_pause(self):
        self.paused = not self.paused
        self.paused_text = "PAUSED" if self.paused else ""

    def set_inital_velocity(self, body):
        x, y = pg.mouse.get_pos()

        body_screen_x = int(body.x / s.DISTANCE_SCALE)
        body_screen_y = int(body.y / s.DISTANCE_SCALE)

        dx = x - body_screen_x
        dy = y - body_screen_y
        
        body.vx = dx * s.DISTANCE_SCALE * s.MOUSE_VELOCITY_FACTOR / s.TIME_SCALE / 5
        body.vy = dy * s.DISTANCE_SCALE * s.MOUSE_VELOCITY_FACTOR / s.TIME_SCALE / 5

        self.current_body_initial_velocity = round(m.sqrt((body.vx**2) + (body.vy**2)), 2)

    def ghost_orbit(self, steps=3000, dt=0.1, record_every=10):
        self.ghost_bodies = [copy.copy(b) for b in self.bodies]
        path_points = []
        dt_physical = dt * s.TIME_SCALE

        current_ghost = self.ghost_bodies[-1]

        for i in range(steps):
            for ghost in self.ghost_bodies:
                total_fx, total_fy = 0, 0
                for neighbour in self.ghost_bodies:
                    if neighbour is ghost:
                        continue
                    
                    dx = neighbour.x - ghost.x
                    dy = neighbour.y - ghost.y
                    distance = m.sqrt((dx**2) + (dy**2))
                    if distance == 0:
                        continue
                    
                    force = (s.G * ghost.mass * neighbour.mass) / (distance**2 + 1)

                    total_fx += force * (dx / distance)
                    total_fy += force * (dy / distance)
                
                ax = total_fx / ghost.mass
                ay = total_fy / ghost.mass

                ghost.vx += ax * dt_physical
                ghost.vy += ay * dt_physical

            for ghost in self.ghost_bodies:
                ghost.x += ghost.vx * dt_physical
                ghost.y += ghost.vy * dt_physical
                
            if i % record_every == 0:
                path_points.append((int(current_ghost.x / s.DISTANCE_SCALE), int(current_ghost.y / s.DISTANCE_SCALE)))
        return path_points

    def add_random_body(self):
        self.paused = True
        self.paused_text = "PAUSED" if self.paused else ""

        x, y = pg.mouse.get_pos()

        if x > 0 and x < s.WIDTH - 5 and y > 0 and y < s.HEIGHT - 5:
            x_m = x * s.DISTANCE_SCALE
            y_m = y * s.DISTANCE_SCALE
            physical_radius = ((3 * self.current_mass) / (4 * m.pi * s.DENSITY)) ** (1/3)
            radius_pixels = max(4, int(physical_radius / s.DISTANCE_SCALE))

            new_body = Body(
                    x_m,
                    y_m,
                    0,
                    0,
                    self.current_mass,
                    radius_pixels,
                    physical_radius,
                    (r.randint(0,255), r.randint(0,255), r.randint(0,255)),
                    f"{self.id}"
                )
            
            self.current_body = new_body
            self.bodies.append(new_body)
            self.id += 1

    def get_time(self, dt):
        if not self.paused:
            self.elapsed_time += dt * self.sim_speed * s.TIME_SCALE
        return self.elapsed_time
    
    def update(self, dt):
        dt_physical = dt * s.TIME_SCALE

        for body in self.bodies:
            if self.arrow_enabled:
                body.v_arrow_end = None

                screen_x = int(body.x / s.DISTANCE_SCALE)
                screen_y = int(body.y / s.DISTANCE_SCALE)

                direction_r = m.atan2(body.vy, body.vx)
                body.direction = direction_r * (180 / m.pi)
                    
                body.line_length = m.sqrt(body.vx**2 + body.vy**2) / s.DISTANCE_SCALE * s.ARROW_SCALE

                end_x = screen_x + (m.cos(direction_r) * body.line_length)
                end_y = screen_y + (m.sin(direction_r) * body.line_length)

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
                    if distance == 0:
                        continue
                    direction_x = dx / distance
                    direction_y = dy / distance

                    force = (s.G * body.mass * neighbour.mass) / (distance**2 + 1)

                    fx = force * direction_x
                    fy = force * direction_y

                    total_fx += fx
                    total_fy += fy

                ax = total_fx / body.mass
                ay = total_fy / body.mass

                body.vx += ax * dt_physical
                body.vy += ay * dt_physical

                body.v = m.sqrt(body.vx**2 + body.vy**2)

            for body in self.bodies:
                body.x += body.vx * dt_physical
                body.y += body.vy * dt_physical

                if self.trail_enabled:
                    if self.trail_decider % self.trail_decider_value == 0:
                        body_screen_x = int(body.x / s.DISTANCE_SCALE)
                        body_screen_y = int(body.y / s.DISTANCE_SCALE)
                        body.trail_points[(body_screen_x, body_screen_y)] = t.time()

                    while body.trail_points:
                        oldest_point = next(iter(body.trail_points))
                        if t.time() - body.trail_points[oldest_point] < 5:
                            break
                        del body.trail_points[oldest_point]
                else:
                    if len(body.trail_points) != 0:
                        body.trail_points.clear()

            self.bodies = [body for body in self.bodies if not self.out_of_bounds(body)]
            self.trail_decider += 1

        for particle in self.debris:
            particle.glide()

        self.debris = [particle for particle in self.debris if ((particle.x - particle.target_x)**2 + (particle.y - particle.target_y)**2)**0.5 > 2 and t.time() - particle.birth_time < 1]
        self.check_collision(dt)

    def out_of_bounds(self, body):
        if body.x > s.WIDTH * s.DISTANCE_SCALE * 2 or body.x < -s.WIDTH * s.DISTANCE_SCALE * 2 or body.y > s.HEIGHT * s.DISTANCE_SCALE * 2 or body.y < -s.HEIGHT * s.DISTANCE_SCALE * 2:
            return True
        
    def ruler_length(self, start_x, end_x, start_y, end_y):
        dx = end_x - start_x
        dy = end_y - start_y

        return m.sqrt(dx**2 + dy**2) * s.DISTANCE_SCALE

    def check_collision(self, dt):
        to_collide = []
        for i, body in enumerate(self.bodies):
            for neighbour in self.bodies[i+1:]:
                dx = neighbour.x - body.x
                dy = neighbour.y - body.y
                distance = m.sqrt(dx**2 + dy**2)
                radii_total = body.physical_radius + neighbour.physical_radius
                if distance < max(radii_total, body.v * dt * s.TIME_SCALE * 2) or distance < radii_total * 3:
                    to_collide.append((body, neighbour))

        for body, neighbour in to_collide:
            if body in self.bodies and neighbour in self.bodies:
                self.collide(body, neighbour)

    def collide(self, body, neighbour):
        print("collision")

        self.collision_x = (body.x + neighbour.x) / 2 / s.DISTANCE_SCALE
        self.collision_y = (body.y + neighbour.y) / 2 / s.DISTANCE_SCALE

        final_vx = ((body.mass * body.vx) + (neighbour.mass * neighbour.vx)) / (body.mass + neighbour.mass)
        final_vy = ((body.mass * body.vy) + (neighbour.mass * neighbour.vy)) / (body.mass + neighbour.mass)

        final_mass = body.mass + neighbour.mass

        new_x = (body.x * body.mass + neighbour.x * neighbour.mass) / final_mass
        new_y = (body.y * body.mass + neighbour.y * neighbour.mass) / final_mass

        physical_radius = ((3 * final_mass) / (4 * m.pi * s.DENSITY)) ** (1/3)
        radius_pixels = max(4, int(physical_radius / s.DISTANCE_SCALE))

        new_body = Body(
            new_x,
            new_y,
            final_vx,
            final_vy, 
            final_mass,
            radius_pixels,
            physical_radius,
            body.colour if body.physical_radius > neighbour.physical_radius else neighbour.colour,
            f"{self.id}"
        )

        self.bodies.append(new_body)
        
        particle_count = r.randint(100, 300)

        for particle in range(particle_count):
            new_debris_particle = DebrisParticle(
                self.collision_x,
                self.collision_y,
                body.colour if body.physical_radius < neighbour.physical_radius else neighbour.colour,
            )

            self.debris.append(new_debris_particle)
      
        self.bodies.remove(body)
        self.bodies.remove(neighbour)
        self.id += 1