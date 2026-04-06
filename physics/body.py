class Body:
    def __init__(self, x, y, vx, vy, mass, radius, colour, name):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.v = 0

        self.mass = mass
        self.radius = radius

        self.colour = colour

        self.fx = 0
        self.fy = 0

        self.name = name

        self.trail_points = {}
        self.trail_count = 0

        self.line_length = 0
        self.v_arrow_end = (self.x, self.y)
        self.left_tip_end = (self.x, self.y)
        self.right_tip_end = (self.x, self.y)

        self.direction = 0

    def __repr__(self):
        return f"Body(id={self.name}, mass={self.mass})"