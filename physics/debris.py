import math as m
import random as r
import time as t

class DebrisParticle():
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y

        self.prev_x = 0
        self.prev_y = 0

        self.birth_time = t.time()
    
        self.target_x = self.x + r.randint(-200, 200)
        self.target_y = self.y + r.randint(-200, 200)

        self.radius = r.randint(1,3)
        self.colour = colour

        self.step = r.randint(3, 7) 

    def glide(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        distance = m.sqrt(dx**2 + dy**2)

        self.x += (dx / distance) * self.step
        self.y += (dy / distance) * self.step