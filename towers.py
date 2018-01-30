from time import time

MAX_LEVEL = 9

class Tower:
    def __init__(self, d, c, r, t, m, rgb, n):
        self.damage = d
        self.cooldown = c
        self.base_cooldown = c
        self.range = r
        self.category = t
        self.cost = m
        self.level = 1
        self.name = n
        
        self.upgrade_cost = m * .6
        
        self.color = rgb
        
        self.last_shot = time()
        
    def upgrade(self):
        if self.level >= MAX_LEVEL:
            return False
        self.level += 1
        self.damage *= 1.0905
        self.cooldown *= .917
        self.range *= 1.052
        self.upgrade_cost += self.cost * .2
        return True
    
class Laser_Turret(Tower):
    def __init__(self):
        super().__init__(25, 1, 120, 'energy', 100, 'red', 'Laser Turret') #25 dps
            
class Tesla_Arc(Tower):
    def __init__(self):
        super().__init__(16, .36, 90, 'energy', 120, 'dodgerblue', 'Tesla Arc') #44.4 dps
            
class Mass_Driver(Tower):
    def __init__(self):
        super().__init__(12, .5, 150, 'kinetic', 90, 'darkorange', 'Mass Driver') #24 dps
            
class Kinetic_Artillery(Tower):
    def __init__(self):
        super().__init__(40, 2.4, 300, 'kinetic', 140, 'gold', 'Kinetic Artillery') #16.7 dps
            
class Plasma_Launcher(Tower):
    def __init__(self):
        super().__init__(24, 1.2, 130, 'plasma', 110, 'fuchsia', 'Plasma Launcher') #20 dps
            
class Fusion_Cannon(Tower):
    def __init__(self):
        super().__init__(80, 3.5, 200, 'plasma', 160, 'mediumspringgreen', 'Fusion Cannon') #22.9 dps