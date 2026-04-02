import random as r
from physics.body import Body
from settings import settings as s

class Simulation:
    def __init__(self):
        self.bodies = []

    def add_random_body(self):
        self.bodies.append(
            Body(
                r.randint(0, s.WIDTH),
                r.randint(0, s.HEIGHT),
                0,
                0,
                5,
                8,
                (r.randint(0,255), r.randint(0,255), r.randint(0,255))
            )
        )
