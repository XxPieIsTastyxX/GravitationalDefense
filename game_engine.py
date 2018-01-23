#import pynput
import time
from graphics import *
import moons
from random import randint, seed
import physics as phy
import ships
from math import *
import towers
import readchar

LOOT_MODIFIER = 3
DAMAGE_MODIFIER = .4

seed()

class Game_Engine():
    def __init__(self):
        self.paused = False
        self.timeThisFrame = 0
        self.hasStarted = False
        self.planet_health = 127
        self.wave_num = 1
        self.metal = 200
        
        self.active = []
        self.shots = []

        self.win = GraphWin('Test Wandow', 1000, 800, autoflush = False)
        
        self.backround = Circle(Point(500, 400), 700)
        self.backround.setFill("Black")
        self.backround.draw(self.win)
        
        line = Line(Point(800, 0), Point(800, 799))
        line.setFill("Cyan")
        line.draw(self.win)
        
        title = Text(Point(900, 40), 'Gravitational Defense')
        title.setSize(20)
        title.setTextColor('Cyan')
        title.draw(self.win)
        
        stats = Text(Point(840, 90), 'Wave:\n       Ships Left:\nMetal:')
        stats.setSize(20)
        stats.setTextColor('Cyan')
        stats.draw(self.win)
        
        self.exit = Text(Point(900, 740), 'Press N to start wave')
        self.exit.setSize(20)
        self.exit.setTextColor('Cyan')
        self.exit.draw(self.win)
        
        self.defBuildText = 'Build Menu:\nMoon A\nMoon B\nMoon C\nMoon D\nMoon E\nMoon F\nMoon G\nMoon H\nMoon I\nMoon J\nMoon K\nMoon L'
        
        self.buildMenu = Text(Point(900, 400), 'Build Menu:\nMoon A\nMoon B\nMoon C\nMoon D\nMoon E\nMoon F\nMoon G\nMoon H\nMoon I\nMoon J\nMoon K\nMoon L')
        self.buildMenu.setSize(20)
        self.buildMenu.setTextColor('Cyan')
        self.buildMenu.draw(self.win)
        
        self.metalText = Text(Point(894, 113), str(self.metal))
        self.metalText.setSize(20)
        self.metalText.setTextColor('Cyan')
        self.metalText.draw(self.win)
        
        self.planet = Circle(Point(400,400), 25)
        self.planet.setFill('Green')
        self.planet.draw(self.win)
        
        self.moonlist = []
        for i in range(12):
            size = randint(0,3)
            if size == 0:
                size = 2
            self.moonlist.append(moons.Moon(75 + i * 25, size))
            self.moonlist[i].image.draw(self.win)
            
        
        
            
            
            
            
        update()
        while True:
            self.mode_build()
            self.mode_onslaught()
    
    def distance(self, ship, moon):
        return sqrt(phy.norm_sqr(phy.vec_sum(moon.position, phy.vec_scale(ship.position, -1))))
          
    def collided(self, ship):
        if phy.norm_sqr(ship.position) < 625:
            self.planet_health -= ship.power + 5
            return True
        for m in self.moonlist:
            if self.distance(ship, m) < m.radius + ship.radius:
                return True
        return False
    
    def shoot(self, moon, ship):
        ship.damage(moon.tower.damage * DAMAGE_MODIFIER, moon.tower.category)
        if ship.health < 0:
            self.destroy(ship)
        moon.tower.last_shot = time.time()
        newline = Line(Point(moon.position[0] + 400,moon.position[1] + 400), Point(ship.position[0] + 400, ship.position[1] + 400))
        newline.setFill(moon.tower.rgb)
        newline.draw(self.win)
        self.shots.append((newline, time.time()))
        
    def destroy(self, ship):
        self.metal += int(ship.power * LOOT_MODIFIER)
        ship.image.undraw()
        self.metalText.setText(str(self.metal))
        update()
        self.active.remove(ship)
                  
    def moon_tick(self):   
        for m in self.moonlist:
            phy.move_moon(m, self.timeThisFrame)
            m.image.move(m.last_move[0], m.last_move[1])
            
            if m.tower is not None and m.tower.last_shot + m.tower.cooldown < time.time():
                for s in self.active:
                    if self.distance(s, m) < m.tower.range:
                        self.shoot(m, s)
                        break
        
    def ship_tick(self):
        for s in self.active:
            phy.move_ship(s, self.moonlist, self.timeThisFrame)
            s.image.move(s.last_move[0], s.last_move[1])
            if self.collided(s):
                self.destroy(s)
            
            
    def mode_onslaught(self):
        self.active = []
        upcoming = []
        remaining_points = pow(self.wave_num + 3, 2)
       
        while remaining_points > 0:
            min_possible = min(ceil(log(remaining_points / 40, 2)), 4)
            if remaining_points >= 64:
                max_possible = 4
            else:
                max_possible = min(floor(log(remaining_points, 2)), 3)
                
            num = randint(min_possible, 4) % (max_possible + 1)
            if num == 0:
                upcoming.append(ships.Corvette())
                remaining_points -= 1
            elif num == 1:
                upcoming.append(ships.Destroyer())
                remaining_points -= 2
            elif num == 2:
                upcoming.append(ships.Cruiser())
                remaining_points -= 4
            elif num == 3:
                upcoming.append(ships.Battleship())
                remaining_points -= 8
            else:
                upcoming.append(ships.Dreadnought())
                remaining_points -= 64
            
        self.active.append(upcoming.pop())  
        self.active[0].image.draw(self.win)
        last_spawn = time.time()
        while len(self.active) != 0 or len(upcoming) != 0:
            startTime = time.time()
            
            if startTime > last_spawn + 2 and len(upcoming) != 0:
                arriving = upcoming.pop()
                self.active.append(arriving)
                arriving.image.draw(self.win)
                last_spawn = startTime
            
            for s in self.shots:
                if s[1] + .1 < time.time():
                    s[0].undraw()
                    self.shots.remove(s)
            
            self.moon_tick()
            self.ship_tick()
            self.planet.setFill(color_rgb(127 - max(self.planet_health, 0), max(self.planet_health, 0), 0))
            
            update()
            self.timeThisFrame = time.time() - startTime
            fps = min(int(1/self.timeThisFrame), 999)
            print(fps)    
                    
        
 
        
        
    def mode_build(self):
        print(self.metal)
        while True:
            key = ord(readchar.readchar())
            if key == 110:
                return
            
            elif key < 97 or key > 108:
                continue
            
            temp_moon = self.moonlist[key - 97]

            if temp_moon.tower == None:
                
                self.buildMenu.setSize(15)
                self.buildMenu.setText('Moon ' + chr(key) + '\n\n(1)Mass Driver: 90\n\n(2)Laser Turret: 100\n\n(3)Plasma Launcher: 110\n\n(4)Tesla Arc: 120\n\n(5)Kinetic Artillery: 140\n\n(6)Fusion Cannon: 160')
            
                self.exit.setText('Press B to Exit')
                update()
                
                key2 = ord(readchar.readchar())
                if key2 == 49:
                    temp_moon.tower = towers.Mass_Driver()
                    if(self.metal >= temp_moon.tower.cost):
                        self.metal -= temp_moon.tower.cost
                        self.buildMenu.setSize(20)
                        self.buildMenu.setText('Moon ' + chr(key) + '\n\nMass Driver\n\n Level 1')
                    else:
                        temp_moon.tower = None
                
                elif key2 == 50:
                    temp_moon.tower = towers.Laser_Turret()
                    if(self.metal >= temp_moon.tower.cost):
                        self.metal -= temp_moon.tower.cost
                        self.buildMenu.setSize(20)
                        self.buildMenu.setText('Moon ' + chr(key) + '\n\nLaser Turret\n\n Level 1')
                    else:
                        temp_moon.tower = None
                
                elif key2 == 51:
                    temp_moon.tower = towers.Plasma_Launcher()
                    if(self.metal >= temp_moon.tower.cost):
                        self.metal -= temp_moon.tower.cost
                        self.buildMenu.setSize(20)
                        self.buildMenu.setText('Moon ' + chr(key) + '\n\nPlasma Launcher\n\n Level 1')
                    else:
                        temp_moon.tower = None
                
                elif key2 == 52:
                    temp_moon.tower = towers.Tesla_Arc()
                    if(self.metal >= temp_moon.tower.cost):
                        self.metal -= temp_moon.tower.cost
                        self.buildMenu.setSize(20)
                        self.buildMenu.setText('Moon ' + chr(key) + '\n\nTesla Arc\n\n Level 1')
                    else:
                        temp_moon.tower = None
                
                elif key2 == 53:
                    temp_moon.tower = towers.Kinetic_Artillery()
                    if(self.metal >= temp_moon.tower.cost):
                        self.metal -= temp_moon.tower.cost
                        self.buildMenu.setSize(20)
                        self.buildMenu.setText('Moon ' + chr(key) + '\n\nKinetic Artillery\n\n Level 1')
                    else:
                        temp_moon.tower = None
                        
                elif key2 == 54:
                    temp_moon.tower = towers.Fusion_Cannon()
                    if(self.metal >= temp_moon.tower.cost):
                        self.metal -= temp_moon.tower.cost
                        self.buildMenu.setSize(20)
                        self.buildMenu.setText('Moon ' + chr(key) + '\n\nFusion Cannon\n\n Level 1')
                    else:
                        temp_moon.tower = None
                update()
                #assign tower or return back to moon selection
            else:
                self.buildMenu.setSize(20)
                self.buildMenu.setText('Moon ' + chr(key) + "\n\n" + temp_moon.tower.name + "\n\n Level " + str(temp_moon.tower.level) + "\n\n Press 8 to upgrade \n\n Press 9 to destroy")
                update()
                
                key2 = ord(readchar.readchar())
                if key2 == 56 and self.metal >= temp_moon.tower.cost:
                    temp_moon.tower.upgrade()
                    self.metal -= temp_moon.tower.cost
                    temp_moon.tower.upgrade()
                if key2 == 57:
                    self.metal += temp_moon.tower.cost/2
                    temp_moon.tower = None
            
            self.buildMenu.setSize(20)        
            self.buildMenu.setText(self.defBuildText)
            self.exit.setText('Press N to start wave')
            update()
        
        
ge = Game_Engine()


            