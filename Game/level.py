# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 10:02:12 2018

@author: Lenovo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 19:51:23 2017

@author: elwood
"""
import os, sys, pygame, spritesheet
from pygame.locals import *
import pytmx
#from pytmx.util_pygame import load_pygame
#import tilerender
import time
import pygame.time



class Monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = pygame.image.load("Boy1-Zombie.png")
        self.ss = spritesheet.spritesheet("Boy1-Zombie.png")
        self.width_guy = 40
        self.images = [pygame.transform.scale(x, (32,32)) for x in 
                   self.ss.images_at(((0,0,self.width_guy,self.width_guy),
                                 (0,self.width_guy,self.width_guy,self.width_guy),
                                 (0,2*self.width_guy+1,self.width_guy,self.width_guy),
                                 (0,3*self.width_guy,self.width_guy,self.width_guy)),
            colorkey=(255,255,255))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
    def update(self, args):
        pass
    
    def draw(self, surface):
        pass
    
    def clear(self, surface, background):
        pass
        
    

class Level:


    def __init__(self, tmx_file):
        self.tmx_bk = pytmx.util_pygame.load_pygame(tmx_file)
        self.size = (self.tmx_bk.width * self.tmx_bk.tilewidth,
        self.tmx_bk.height * self.tmx_bk.tileheight)
        # layers as named in the tmx file
        self.layer_names = {'background': self.tmx_bk.get_layer_by_name('background'),
                            #'objects': self.tmx_bk.get_layer_by_name('objects'), 
                            'solids': self.tmx_bk.get_layer_by_name('foreground'), 
                            'materials': self.tmx_bk.get_layer_by_name('topground')}
        #self.start_pos = self.layer_names['objects'].properties['start_pos']
        self.start_pos = (self.tmx_bk.get_object_by_name("start_position").x,
        self.tmx_bk.get_object_by_name("start_position").y)
        #print(self.start_pos)
        
    def layerss(self, layer_name):
        
        tiles = list(self.layer_names[layer_name].tiles())
        tiles = [(x*self.tmx_bk.tilewidth,y*self.tmx_bk.tileheight,z) for 
                 (x,y,z) in tiles]
        return tiles
     
    def blit_layer(self, tiles, pysurface  = None):
        if pysurface == None:
            pysurface = pygame.Surface(self.size)
        # try:
        for tile in tiles:
            #print(type(tile[0]))
            pysurface.blit(tile[2], (tile[0], tile[1]))
    
        return pysurface
        
    def create_level_surface(self):
        pysurface = pygame.Surface(self.size)
        for key in self.layer_names:
            #print(key)
            tiles = self.layerss(key)
            pysurface = self.blit_layer(tiles, pysurface)
        return pysurface
            
        #except:
         #   print('exception')
          #  return(pysurface)

        #create surface, from image layers
        
        #change into a function, properties, layers, creating objects, 
        #start places and transition zones.
class SpriteStripAnim(object):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = spritesheet.spritesheet(filename)
        self.images =[pygame.transform.scale(x, (32,32)) for x in ss.load_strip(rect, count, colorkey)]
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames
    def iter(self):
        self.i = 0
        self.f = self.frames
        return self
    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self


class Character:
    def __init__(self, images):
        self.imgs = images
        self.ss = spritesheet.spritesheet(images)
        self.width_guy = 36
        #self.ch = ss.images_at(((0,0,width_guy,width_guy),(0,width_guy,width_guy,width_guy),(0,2*width_guy+1,width_guy,width_guy),(0,3*width_guy,width_guy,width_guy)),colorkey=(255,255,255))
        self.ch = [pygame.transform.scale(x, (32,32)) for x in 
                   self.ss.images_at(((0,0,self.width_guy,self.width_guy),
                                 (0,self.width_guy,self.width_guy,self.width_guy),
                                 (0,2*self.width_guy+1,self.width_guy,self.width_guy),
                                 (0,3*self.width_guy,self.width_guy,self.width_guy)),
            colorkey=(255,255,255))]
#        self.inventory = [Fired_object('fireball.png')]
        self.FPS = 30
        self.frames = self.FPS / 2
        #direction = {K_DOWN:(0 ,0, self.chr.height), K_UP:(2 ,0, -self.chr.height), 
         #            K_LEFT:(3,-self.chr.height, 0), K_RIGHT:(1,self.chr.height, 0)}
        self.strips = [
     SpriteStripAnim('Guy.png', (0,0,32,36), 1, (255,255,255), True, self.frames)+
    SpriteStripAnim('Guy.png', (46,0,32,36), 1, (255,255,255), True, self.frames)+
    SpriteStripAnim('Guy.png', (92,0,32,36), 1, (255,255,255), True, self.frames),
    SpriteStripAnim('Guy.png', (0,36,32,36), 1, (255,255,255), True, self.frames)+
    SpriteStripAnim('Guy.png', (46,36,32,36), 1, (255,255,255), True, self.frames)+
    SpriteStripAnim('Guy.png', (90,36,32,36), 1, (255,255,255), True, self.frames),
    SpriteStripAnim('Guy.png', (0,72,32,36), 1, (255,255,255), True, self.frames)+
    SpriteStripAnim('Guy.png', (46,72,32,36), 1, (255,255,255), True, self.frames)+
    SpriteStripAnim('Guy.png', (92,72,32,36), 1, (255,255,255), True, self.frames),
    SpriteStripAnim('Guy.png', (0,108,32,36), 1, (255,255,255), True, self.frames)+
    SpriteStripAnim('Guy.png', (46,108,32,36), 1, (255,255,255), True, self.frames)+
    SpriteStripAnim('Guy.png', (92,108,32,36), 1, (255,255,255), True, self.frames)]
            
            
class Fired_object:
    def __init__(self, images):
        self.imgs = images
        self.fireball = pygame.transform.scale(pygame.image.load(images).convert(),(32,32))

class Game:
    
    def __init__(self, character, level):
        self.ch = character
        self.lvl = level
        self.lvlbk = level.create_level_surface()
        self.chr = self.ch.ch[0].get_rect()
        self.lvlr = self.lvlbk.get_rect()
        self.size = width, height = 640, 640
        self.bk_grid = [[x,y] for y in range(0, self.lvlr.height, self.chr.width) 
            for x in range(0, self.lvlr.width, self.chr.height)]
        self.tnb = [[x,y] for x in range(0, self.lvlr.width, self.chr.width) 
            for y in range(0, int(self.size[1]/2) + self.chr.height, self.chr.height)]
        self.b = [[x,y] for x in range(0, self.lvlr.width, self.chr.width) 
            for y in range(self.lvlr.height-int(self.size[1]/2), self.lvlr.height, self.chr.height)]
        self.tnb += self.b
#print(tnb)
        self.lnr = [[x,y] for x in range(0, int(self.size[0]/2), self.chr.width) 
            for y in range(0, self.lvlr.height, self.chr.height)]
        self.r= [[x,y] for x in range(self.lvlr.width - int(self.size[0]/2)-self.chr.height, self.lvlr.width, self.chr.width) 
            for y in range(0, self.lvlr.height, self.chr.height)]
        self.lnr += self.r
        self.indy = 0
        self.solid_positions = []
        self.strip_direction = {K_DOWN:self.ch.strips[0], K_UP:self.ch.strips[2], 
                     K_LEFT:self.ch.strips[3], K_RIGHT:self.ch.strips[1]}

        for i, layer in enumerate(self.lvl.tmx_bk.layers):
            try:
                if layer.properties['solid']=='true':
                    for x, y, _ in layer.tiles():
                        print('yes')
                        self.solid_positions.append([x*self.chr.width, y*self.chr.width])
            except:
                pass
#want character rect to be set on start item in item layer 'start_pos' is object 
        
    def blit_level(self):
        #finds a x,y value for top corner of levelsurface based on start_pos so map
        #is centered properly
        lvlx = (self.size[0]/2 - max(self.size[0]/2, min(self.lvl.size[0] - 
                            self.size[0]/2, self.lvl.start_pos[0])))
        
        lvly = self.size[1]/2 - max(self.size[1]/2, min( self.lvl.size[1] - 
                        self.size[1]/2, self.lvl.start_pos[1]))
      
        #sets character start positions to half way across and down screen
        startx = self.size[0]/2-32
        starty = self.size[1]/2
        
        #if the screen is at edge, changes character start positions to actual position.
        if -lvlx == 0.0 or  -lvlx == (self.lvl.size[0] - self.size[0]):
            startx = 0#self.lvl.start_pos[0]
        if -lvly == 0.0 or  -lvly ==  (self.lvl.size[1] - self.size[1]):
            starty = 0#self.lvl.start_pos[1]
            

            
        screen.blit(self.lvlbk, (lvlx, lvly))
        self.lvlr = self.lvlr.move(lvlx, lvly)
        
        screen.blit(self.ch.ch[0], (startx, starty))
        self.chr = self.chr.move(startx, starty)        

        pygame.display.update()
        print("startx: ", startx, "starty: ", starty)
        print(lvlx,lvly)
   
    #function to set screen position, set character within screen.
    #assume co-ordinates are legit.
    #if within level_height + or - screen height. blit background, else if 
    # greter than zero but less than height blit character
    
    def test(self):
        '''returns True when the background should be blitted becasue the charcter 
        is not in the border'''
        combx = self.chr.left-self.lvlr.left
        comby = self.chr.top - self.lvlr.top
        #if combx + self.ch.width_guy > self.lvlr.width or comby + width_guy > self.lvlr.height:
            #return False
        #if if combx < 0 or comby < 0:
            #return False
        if combx < self.lvlr.width- width/2 +self.ch.width_guy and combx > width/2 - self.ch.width_guy:
            if comby < self.lvlr.height - height/2 +self.ch.width_guy and comby > height/2 +self.ch.width_guy:
                return True
            
        return False
    
    def cum_distance(self):
        combx = self.chr.left-self.lvlr.left
        comby = self.chr.top - self.lvlr.top
        return (combx, comby)
        
    def general_position(self, rect):
        combx = rect.left-self.lvlr.left
        comby = rect.top - self.lvlr.top
        return (combx, comby)
        
        
    def firer(self, key, info = None):
        fire_direction = self.indy
        if info == None:
            print("fire!")
            info = self.ch.inventory[0]
            image = info.fireball
            imager = image.get_rect()
            
            #for y in range(chr.y)
            #order of images for fire.
            #list of images
            #self.ss = spritesheet.spritesheet(images)
            #access [indy] of ss
            #chr position.
            #for options difference between x and 0, x and width, y and 0, y and width
            #want to loop between the current x and finish as above.
            #(self.size/32)*[32]
            direction = {0:(0, (int(self.size[1]/32)*[32])), 2:(0, ((int(self.chr.top/32)+1)*[-32])),
                        3:(1,  ((int(self.chr.left/32)+1)*[-32])), 1:(1,  (int(self.size[1]/32)*[32]))}
            if direction[fire_direction][0] == 0:
                fire_movement = [(0,y) for y in direction[fire_direction][1]]
                
                
            else:
                fire_movement = [(x,0) for x in direction[fire_direction][1]]
                
            imager = imager.move(self.chr.left, self.chr.top)
            print('chrect: ', self.chr.top, '  ', self.chr.left)
            #screen.blit(image, imager)
            pygame.display.update()
            #yield fire_movement
            for m in fire_movement:
                #screen.blit(self.lvlbk, imager, Rect(*self.general_position(imager), self.chr.height, self.chr.height))
                #print('imager1: ', imager)
                imager = imager.move(m)
                print('imager2: ', imager)
                screen.blit(image, imager)   
                pygame.display.update()
                pygame.time.wait(100)
                screen.blit(self.lvlbk, imager, Rect(*self.general_position(imager), self.chr.height, self.chr.height))

                #print("cycle: ",m )
    def animate_character(self, strip):
        screen.blit(self.lvlbk, self.chr, Rect(*self.cum_distance(), self.chr.height, self.chr.height))

        screen.blit(strip.next(), self.chr)

        pygame.display.update()

   #surface.blit(image, (0,0)) 
#    SpriteStripAnim('Explode3.bmp', (0,0,48,48), 4, 1, True, frames) +
#    SpriteStripAnim('Explode3.bmp', (48,48,48,48), 4, 1, True, frames),
#    SpriteStripAnim('Explode4.bmp', (0,0,24,24), 6, 1, True, frames),
    #SpriteStripAnim('Explode1.bmp', (48,48,48,48), 4, 1, True, frames),

        
    def border(self, key):
        #user presses key, key read (maybe group keys by related actions, movement keys,
        #attack keys etc), movemnet key, pass to mover. Mover has character current
        #and direction of travel.
        #is the square in the level, is the square traversable, which blitting regime to use
        #regime 1 is blit character up or down, regime 2 is blit character left or right, need
        #list of solid positions, list of x positions out of border, list of y
        #x, y = 
        #dictionary relating movements and character image number to key pressed.
        direction = {K_DOWN:(0 ,0, self.chr.height), K_UP:(2 ,0, -self.chr.height), 
                     K_LEFT:(3,-self.chr.height, 0), K_RIGHT:(1,self.chr.height, 0)}
        #calculating the position of the character within the background
        unm_x, unm_y = self.cum_distance()
        #the additional movement the 
        m_x, m_y = direction[key][1], direction[key][2]
        x, y = unm_x + m_x, unm_y + m_y
        self.indy = direction[key][0]
        #print(unm_x, unm_y)
        #print(x,y)
        if [x, y] in self.solid_positions:
            screen.blit(self.ch.ch[self.indy], self.chr)   
            pygame.display.update()
            return False
        if key == K_DOWN or key == K_UP:
            if [x,y] in self.tnb and [unm_x,unm_y] in self.tnb:
                screen.blit(self.lvlbk, self.chr, Rect(*self.cum_distance(), self.chr.height, self.chr.height))
                self.chr = self.chr.move(*direction[key][1:])
                screen.blit(self.ch.ch[self.indy], self.chr)   
                pygame.display.update()
            elif [x,y] in self.bk_grid:
 
                self.lvlr = self.lvlr.move(-1*direction[key][1],-1*direction[key][2])
                screen.blit(self.lvlbk, self.lvlr)
                screen.blit(self.ch.ch[self.indy],self.chr)
                pygame.display.update()  
        if key == K_LEFT or key == K_RIGHT:
            if [x,y] in self.lnr and [unm_x,unm_y] in self.lnr:
                screen.blit(self.lvlbk, self.chr, Rect(*self.cum_distance(), self.chr.height, self.chr.height))
                self.chr = self.chr.move(*direction[key][1:])
                screen.blit(self.ch.ch[self.indy], self.chr)   
                pygame.display.update()
            elif [x, y] in self.bk_grid:
 
                self.lvlr = self.lvlr.move(-1*direction[key][1],-1*direction[key][2])
                screen.blit(self.lvlbk, self.lvlr)
                screen.blit(self.ch.ch[self.indy],self.chr)
                pygame.display.update()  
    
    
        
pygame.init()
size = width, height = 640, 640
screen = pygame.display.set_mode(size, RESIZABLE)
#w, h = pygame.display.get_surface().get_size()
level = Level('smallMap.tmx')
character = Character('Guy.png')
game = Game(character, level)
game.blit_level()
print(game.test())
#print(level.layers('background'))
#background = level.blit_layer(level.layers('background'))
#screen.blit(background, (0, 0))
#pygame.display.update()
print (level.start_pos)
#mon = Monster()
direction = [K_DOWN, K_UP, K_LEFT, K_RIGHT]
activate = [K_SPACE]
strip_direction = game.strip_direction[K_DOWN]

def keyboard():
    pass

while 1:
    mhh = pygame.time.Clock()
    
    event = pygame.event.poll()
    if event.type == pygame.QUIT: 
        sys.exit()
            
    elif event.type == KEYDOWN:
        if event.key in direction:
                    #p.border(event.key)
            strip_direction = game.strip_direction[event.key]
            game.border(event.key)
            
                #if event.key in activate:
                 #   p.fire()
        elif event.key in activate:
            game.firer(event.key)
    game.animate_character(strip_direction)
    mhh.tick(40)