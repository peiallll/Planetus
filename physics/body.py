class Body:
    def __init__(self, x, y, vx, vy, mass, radius, colour):
        self.x = x
        self. y = y

        self.vx = vx
        self.vy = vy

        self.mass = mass
        self.radius = radius

        self.colour = colour

        self.fx = 0
        self.fy = 0

        def apply_force(self, fx, fy):
            self.fx += fx
            self.fy += fy
    
        def update(self, dt):
            ax = self.fx / self.mass # acceleration = force / mass
            ay = self.fy / self.mass

            self.vx = ax * dt # velocity = acceleration * time
            self.vy * ay * dt

            self.x += self.vx * dt # update pos
            self.y += self.vy * dt

            self.fx = 0 # reset forces
            self.fy = 0 