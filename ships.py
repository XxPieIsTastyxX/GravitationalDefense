import graphics
from random import randint

STARTING_VELOCITY = 11
SHIELD_REGEN = 2.5
BASE_THRUST = 1
HEALTH_MODIFIER = 1

class Ship:
    def __init__(self, h, a, s, p, t, r):
        self.health = h * HEALTH_MODIFIER
        self.max_health = self.health
        self.armor = a
        self.shields = s * HEALTH_MODIFIER
        self.power = p
        self.thrust = t * BASE_THRUST
        self.radius = r
        
        if s == 0:
            self.max_shields = 1
        else:
            self.max_shields = s
        
        self.position = randint(-50,50), -400
        self.velocity = -STARTING_VELOCITY, 0
        
        self.image = graphics.Circle(graphics.Point(self.position[0] + 400, self.position[1] + 400), r)
        self.image.setFill(graphics.color_rgb(255, self.armor * 5, int(127 * self.shields / self.max_shields)))
        
        self.last_move = 0, 0
        
    def damage(self, amt, category):
        multiplier = 1
        piercing = 0
        
        if category == 'energy':
            multiplier = .8
        elif category == 'kinetic':
            multiplier = 1.3 
        elif category == 'plasma':
            multiplier = .5
            piercing = 10
           
        damage = amt
        
        if self.shields - damage * multiplier > 0:
            self.shields -= damage * multiplier
        else:
            damage -= self.shields / multiplier
            self.shields = 0
            self.health -= max(damage - max(self.armor - piercing, 0), 0)
            
        self.image.setFill(graphics.color_rgb(int(127 * (1 + max(self.health / self.max_health, 0))), self.armor * 5, int(127 * max(self.shields / self.max_shields, 0))))
        
    def shieldgen(self, time):
        #if self.shields == 0:
        #    return
        self.shields += SHIELD_REGEN * time
        if self.shields > self.max_shields:
            self.shields = self.max_shields
            
            
class Corvette(Ship):
    def __init__(self):
        super().__init__(20, 0, 0, 1, .12, 2)
               
class Destroyer(Ship):
    def __init__(self):
        super().__init__(25, 0, 15, 2, .1, 2.5)
        
class Cruiser(Ship):
    def __init__(self):
        super().__init__(35, 5, 25, 4, .1, 3)
        
class Battleship(Ship):
    def __init__(self):
        super().__init__(50, 15, 10, 8, .09, 3.5)
        
class Dreadnought(Ship):
    def __init__(self):
        super().__init__(70, 25, 40, 32, .08, 5.5)
        
        