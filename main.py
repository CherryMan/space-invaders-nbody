#! /usr/bin/env python
import sys
import time
import math
import numpy as np
import scipy
import pygame as pg
from pygame.locals import *


class Player:
    def __init__(self, m, x, v, a, angle, r):
        self.m = m
        self.x = np.array([x[0],x[1]])
        self.v = np.array([v[0],v[1]])
        self.a = np.array([a[0],a[1]])
        self.angle = angle
        self.r = r
        self.hp = 1

    def update(self, dt: float):
        '''Update given a time in seconds'''
        self.v += dt * self.a
        self.x += dt * self.v

    def draw(self, surf):
        w, h = surf.get_size()
        phi = self.angle
        l = self.r + 5 # Length of cannon in pixels

        # End of line position
        lp = self.x + [l*math.cos(phi)/w, l*math.sin(phi)/h]

        # Pixel positions
        x = int(w * self.x[0]) 
        y = int(h * (1 - self.x[1]))
        lx = int(w * lp[0]) 
        ly = int(h * (1 - lp[1]))

        # Draw the circle and the line
        pg.draw.circle(surf, (255,255,255), (x,y), self.r)
        pg.draw.line(surf, (255,255,255), (x,y), (lx,ly), 2)


class Bullets:
    x = np.empty(shape=(0, 2), dtype=np.float32)
    v = np.empty(shape=(0, 2), dtype=np.float32)
    a = np.empty(shape=(0, 2), dtype=np.float32)

    def add(self, x, v=[0.0, 0.0], a=[0.0, 0.0]):
        '''Add a bullet and return its index.'''
        self.x = np.append(self.x, [x], axis=0)
        self.v = np.append(self.v, [v], axis=0)
        self.a = np.append(self.a, [a], axis=0)
        return len(self.x) - 1

    def rem(self, index):
        self.x = np.delete(self.x, index, axis=0)
        self.v = np.delete(self.v, index, axis=0)
        self.a = np.delete(self.a, index, axis=0)

    def update(self, dt):
        self.v += dt * self.a
        self.x += dt * self.v

    def draw(self, bg):
        for pos in self.x:
            w, h = bg.get_size()
            x = int(pos[0] * w)
            y = int((1-pos[1]) * h)
            pg.draw.circle(bg, (255,255,255), (x, y), 3)


class Game:
    def __init__(self, dim):
        pg.init()

        self.prev_t = time.time()
        self.curr_t = None
        self.dt = 0

        # Intialize surface
        self.screen = pg.display.set_mode(dim)
        self.bg = pg.Surface(self.screen.get_size()).convert()

    def step(self):
        self.curr_t = time.time()
        self.dt = self.curr_t - self.prev_t
        self.prev_t = self.curr_t

    def clear(self):
        self.bg.fill((0, 0, 0))

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        pg.display.flip()


class Enemy:
    def __init__(self, m, x, v, a, angle, r):
        self.m = m
        self.x = np.array([x[0],x[1]])
        self.v = np.array([v[0],v[1]])
        self.a = np.array([a[0],a[1]])
        self.angle = angle
        self.r = r

    def update(self, dt: float):
        """Update given a time in seconds"""
        self.v += dt * self.a
        self.x += dt * self.v

    def draw(self, surf):
        w, h = surf.get_size()
        phi = self.angle
        l = self.r + 5 # Length of cannon in pixels

        # End of line position
        lp = self.x + [l*math.cos(phi)/w, l*math.sin(phi)/h]

        # Pixel positions
        x = int(w * self.x[0]) 
        y = int(h * (1 - self.x[1]))
        lx = int(w * lp[0]) 
        ly = int(h * (1 - lp[1]))

        # Draw the circle and the line
        pg.draw.circle(surf, (125,125,125), (x,y), self.r)
        pg.draw.line(surf, (125,125,125), (x,y), (lx,ly), 2)


if __name__ == '__main__':
    pg.init()
    green = (0, 255, 0) 
    blue = (0, 0, 128)

    # create the display surface object 
    # of specific dimension..e(X, Y). 
    display_surface = pg.display.set_mode((900, 900 )) 
  
    # set the pygame window name 
    pg.display.set_caption('Show Text') 
  
    # create a font object. 
    # 1st parameter is the font file 
    # which is present in pygame. 
    # 2nd parameter is size of the font 
    font = pg.font.Font('freesansbold.ttf', 32) 
  
    # create a text suface object, 
    # on which text is drawn on it. 
    text = font.render('You died', True, green, blue) 
  
    # create a rectangular object for the 
    # text surface object 
    textRect = text.get_rect()  
  
    # set the center of the rectangular object. 
    textRect.center = (450, 450)

    g = Game(dim=(900, 900))
    p = Player(
        m=1.0,
        x=(0.5,0.5),
        v=(0.0,0.0),
        a=(0.0,0.0),
        angle=math.pi,
        r=10,
    )
    b = Bullets()

    key_down = {}
    
    f = Enemy(
                m=1.0,
                x=(np.random.rand(),1),
                v=(0.0,-0.1),
                a=(0.0,0.0),
                angle=math.pi,
                r=10,
            )
    enn = [f]         #list of enemies
    frame = 0
    while True:
        g.step() # Compute dt
        p.update(g.dt)
        b.update(g.dt)

        i=0
        for en in enn:
            #print(i)
            i += 1
            en.update(g.dt)
        # Event loop
        for e in pg.event.get():
            if e.type == QUIT:      sys.exit()

            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    b.add(
                        x=p.x,
                        v=(p.v + [
                            .2 * math.cos(p.angle),
                            .2 * math.sin(p.angle),
                        ]),
                        a=[0, 0]
                    )

                key_down[e.key] = True
            elif e.type == KEYUP:
                key_down[e.key] = False

        if key_down.get(pg.K_UP):
            p.v = 0.3 * np.array([
                math.cos(p.angle),
                math.sin(p.angle),
            ])
        elif key_down.get(pg.K_DOWN):
            p.v = -0.3 * np.array([
                math.cos(p.angle),
                math.sin(p.angle),
            ])
        else:
            p.v = np.zeros(2)

        if key_down.get(pg.K_LEFT):  p.angle += math.pi*g.dt
        if key_down.get(pg.K_RIGHT): p.angle -= math.pi*g.dt

        #Random chance of ennemy spawning
        spawn_chance = 0.01
        
        if np.random.rand() < spawn_chance:
            f = Enemy(
                     m=1.0,
                     x=(np.random.rand(),1),
                     v=(0,-max(abs(-np.random.rand()/10),0.05)),
                     a=(0.0,0.0),
                     angle=math.pi,
                     r=10,
                 )
            ang = math.atan2(p.x[1] - f.x[1], p.x[0] - f.x[0])
            f.angle = ang
            print(f.x,p.x,ang)
            enn.append(f)
        
        if frame % 120 == 0:
            for en in enn:
                ang = math.atan2(p.x[1] - en.x[1], p.x[0] - en.x[0])
                en.angle = ang + np.random.rand()*2*math.pi/8
                b.add(
                        x=en.x,
                        v=(en.v + [
                            .2 * math.cos(en.angle),
                            .2 * math.sin(en.angle),
                        ]),
                        a=[0, 0]
                    )
        #print(b.x)
        for en in enn:
            if en.x[1] < 0 or en.x[0] < 0 or en.x[1] > 1 or en.x[0] > 1:
                enn.remove(en)

        test = abs(b.x - p.x)*g.bg.get_size() < p.r   #check if there is a collision between player and any particle in x or y
        collis = np.array([x.all() for x in test])        #there is a collision if happens in x or y
        #print(collis, np.where(collis)[0])
        b_rem = np.where(collis)[0]
        if len(b_rem) > 0:
            b.rem(b_rem)
            p.hp -= 1
            print(p.hp)
        if p.hp <= 0:
            display_surface.blit(text, textRect)
            
        pg.display.update()
        g.clear()
        p.draw(g.bg)
        b.draw(g.bg)
        for en in enn:
            en.draw(g.bg)
        g.draw()

        frame += 1
        time.sleep(.0166) # 60FPS
