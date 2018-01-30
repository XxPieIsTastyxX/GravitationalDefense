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
TIME_MODIFIER = 3

seed()

class Game_Engine():
    def __init__(self):
        self.paused = False
        self.timeThisFrame = 0
        self.hasStarted = False
        self.planet_health = 127
        self.wave_num = 1
        self.metal = 100
        
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
        
    def run(self):
        while True:
            self.mode_build()
            self.mode_onslaught()
            self.wave_num += 1
          
    
    def shoot(self, moon, ship):
        ship.damage(moon.tower.damage, moon.tower.category)
        moon.tower.last_shot = time.time()
        newline = Line(Point(moon.position[0] + 400,moon.position[1] + 400), Point(ship.position[0] + 400, ship.position[1] + 400))
        newline.setFill(moon.tower.color)
        newline.draw(self.win)
        self.shots.append((newline, time.time()))
        if ship.health < 0:
            self.destroy(ship, True)
        
    def destroy(self, ship, reward = False):
        if reward:
            self.metal += int(ship.power * LOOT_MODIFIER)
            self.metalText.setText(str(self.metal))
        ship.image.undraw()
        self.active.remove(ship)
                  
    def moon_tick(self):   
        for m in self.moonlist:
            phy.move_moon(m, self.timeThisFrame)
            m.image.move(m.last_move[0], m.last_move[1])
            
            if m.tower is not None and m.tower.last_shot + m.tower.cooldown / TIME_MODIFIER < time.time():
                for s in self.active:
                    if phy.distance(s, m) < m.tower.range:
                        self.shoot(m, s)
                        break
        
    def ship_tick(self):
        for s in self.active:
            phy.move_ship(s, self.moonlist, self.timeThisFrame)
            s.image.move(s.last_move[0], s.last_move[1])
            dist = phy.norm_sqr(s.position) 
            if dist > 320000:
                self.destroy(s)
            elif dist <= 625:
                self.planet_health -= s.power
                self.planet.setFill(color_rgb(127 - max(self.planet_health, 0), max(self.planet_health, 0), 0))
                self.destroy(s)
            elif phy.collided(s, self.moonlist):
                self.destroy(s, True)
            else:
                s.shieldgen(self.timeThisFrame)
            
            
    def mode_onslaught(self):
        self.active = []
        upcoming = []
        remaining_points = floor(4 + .4 * pow(self.wave_num, 2.4))
        while remaining_points > 0:
            print('Wave points: %d' % remaining_points)
            min_possible = min(ceil(log(remaining_points / 200, 2)), 4)
            if remaining_points >= 32:
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
                remaining_points -= 32
            
            print(upcoming[-1].name)
        self.active.append(upcoming.pop())  
        self.active[0].image.draw(self.win)
        last_spawn = time.time()
        while len(self.active) != 0 or len(upcoming) != 0:
            startTime = time.time()
            
            try:
                fps = min(int(TIME_MODIFIER/self.timeThisFrame), 999)
            except:
                pass
            else:
                print('FPS: %d' % fps)
            
            if len(upcoming) != 0 and startTime > last_spawn + 5 / TIME_MODIFIER:
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
            
            update()
            self.timeThisFrame = (time.time() - startTime) * TIME_MODIFIER   
                    
        
 
        
        
    def mode_build(self):
        print('Metal: %d' % self.metal)
        while True:
            print(self.metal)
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
                temp_tower = None
                if key2 == 49:
                    temp_tower = towers.Mass_Driver()
                
                elif key2 == 50:
                    temp_tower = towers.Laser_Turret()
                
                elif key2 == 51:
                    temp_tower = towers.Plasma_Launcher()
                
                elif key2 == 52:
                    temp_tower = towers.Tesla_Arc()
                
                elif key2 == 53:
                    temp_tower = towers.Kinetic_Artillery()
                        
                elif key2 == 54:
                    temp_tower = towers.Fusion_Cannon()
                    
                if temp_tower != None and self.metal >= temp_tower.cost:
                    self.metal -= temp_tower.cost
                    self.buildMenu.setSize(20)
                    self.buildMenu.setText('Moon %c\n\n%s\n\n Level 1' % (key, temp_tower.name))
                    temp_moon.tower = temp_tower
                    
                #assign tower or return back to moon selection
            else:
                self.buildMenu.setSize(20)
                self.buildMenu.setText('Moon %c\n\n%s\n\n Level %d\n\n Press 8 to upgrade \n\n Press 9 to destroy' % (key, temp_moon.tower.name, temp_moon.tower.level))
                update()
                
                key2 = ord(readchar.readchar())
                cost = temp_moon.tower.upgrade_cost
                if key2 == 56 and self.metal >= cost and temp_moon.tower.upgrade():
                    self.metal -= cost
                elif key2 == 57:
                    self.metal += cost 
                    temp_moon.tower = None
            
            self.buildMenu.setSize(20)        
            self.buildMenu.setText(self.defBuildText)
            self.exit.setText('Press N to start wave')
            
            update()

        
if __name__ == '__main__':
    ge = Game_Engine()
    ge.run()
            