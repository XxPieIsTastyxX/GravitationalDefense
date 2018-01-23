from time import time
from graphics import color_rgb



class Tower():
    def __init__(self, d, c, r, t, m, rgb, n):
        self.damage = d
        self.cooldown = c
        self.base_cooldown = c
        self.range = r
        self.category = t
        self.cost = m * 1.1
        self.level = 1
        self. name = n
        
        
        self.rgb = rgb
        
        self.last_shot = time()
        
    def upgrade(self):
        self.level += 1
        self.cooldown /= 2
        self.cost = int(self.cost * 2.2)
    
class Laser_Turret(Tower):
    def __init__(self):
        super().__init__(25, 1, 100, 'energy', 100, 'red', 'Laser Turret') #25 dps
            
class Tesla_Arc(Tower):
    def __init__(self):
        super().__init__(16, .36, 50, 'energy', 120, 'dodgerblue', 'Tesla Arc') #44.4 dps
            
class Mass_Driver(Tower):
    def __init__(self):
        super().__init__(12, .5, 150, 'kinetic', 90, 'darkorange', 'Mass Driver') #24 dps
            
class Kinetic_Artillery(Tower):
    def __init__(self):
        super().__init__(40, 2.4, 320, 'kinetic', 140, 'gold', 'Kinetic Artillery') #16.7 dps
            
class Plasma_Launcher(Tower):
    def __init__(self):
        super().__init__(24, 1.2, 120, 'plasma', 110, 'fuchsia', 'Plasma Launcher') #20 dps
            
class Fusion_Cannon(Tower):
    def __init__(self):
        super().__init__(80, 3.5, 240, 'plasma', 160, 'mediumspringgreen', 'Fusion Cannon') #22.9 dps