class Body:
    def __init__(self, x, y, vx, vy, mass, radius, colour):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.mass = mass
        self.radius = radius

        self.colour = colour

        self.fx = 0
        self.fy = 0