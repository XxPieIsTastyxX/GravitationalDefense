import random
import physics as phy
from math import pow, sqrt
import graphics

class Moon:
    def __init__(self, h, s):
        self.height = h
        self.size = s
        self.angle = random.randint(0,399)
        self.position = 0, 0
        self.last_move = None
        self.update_pos()
        self.tower = None
        self.radius = 2 * s + 4
        self.mass = pow(self.radius, 2)
        self.period = 6.28 * pow(h, 1.5)/sqrt(phy.GRAVITY_CONSTANT * phy.PLANET_MASS)
        
        self.image = graphics.Circle(graphics.Point(self.position[0] + 400, self.position[1] + 400), self.radius)
        self.image.setFill("Grey")
    
    def update_pos(self):
        old_position = self.position
        self.position = self.height * phy.approx_cos(self.angle), self.height * phy.approx_cos(self.angle + 300)
        self.last_move = phy.vec_sum(self.position, phy.vec_scale(old_position, -1))
        