# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 19:47:10 2018

@author: Lenovo
"""
import sys
import pygame
from pygame.locals import Color, KEYUP, K_ESCAPE, K_RETURN
import spritesheet


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
        self.images = ss.load_strip(rect, count, colorkey)
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


surface = pygame.display.set_mode((100,100))
FPS = 36
frames = FPS / 2
strips = [
    SpriteStripAnim('Guy.png', (0,0,32,36), 1, 0, True, frames)+
    SpriteStripAnim('Guy.png', (46,0,32,36), 1, 1, True, frames)+
    SpriteStripAnim('Guy.png', (92,0,32,36), 1, 1, True, frames),
    SpriteStripAnim('Guy.png', (0,36,32,36), 1, 0, True, frames)+
    SpriteStripAnim('Guy.png', (46,36,32,36), 1, 1, True, frames)+
    SpriteStripAnim('Guy.png', (92,36,32,36), 1, 1, True, frames),
    SpriteStripAnim('Guy.png', (0,72,32,36), 1, 0, True, frames)+
    SpriteStripAnim('Guy.png', (46,72,32,36), 1, 1, True, frames)+
    SpriteStripAnim('Guy.png', (92,72,32,36), 1, 1, True, frames),
    SpriteStripAnim('Guy.png', (0,108,32,36), 1, 0, True, frames)+
    SpriteStripAnim('Guy.png', (46,108,32,36), 1, 1, True, frames)+
    SpriteStripAnim('Guy.png', (92,108,32,36), 1, 1, True, frames)
    
#    SpriteStripAnim('Explode3.bmp', (0,0,48,48), 4, 1, True, frames) +
#    SpriteStripAnim('Explode3.bmp', (48,48,48,48), 4, 1, True, frames),
#    SpriteStripAnim('Explode4.bmp', (0,0,24,24), 6, 1, True, frames),
    #SpriteStripAnim('Explode1.bmp', (48,48,48,48), 4, 1, True, frames),
]
black = Color('black')
clock = pygame.time.Clock()
n = 0
strips[n].iter()
image = strips[n].next()
while True:
    for e in pygame.event.get():
        if e.type == KEYUP:
            if e.key == K_ESCAPE:
                sys.exit()
            elif e.key == K_RETURN:
                n += 1
                if n >= len(strips):
                    n = 0
                strips[n].iter()
    surface.fill(black)
    surface.blit(image, (0,0))
    pygame.display.flip()
    image = strips[n].next()
    clock.tick(FPS)
#events that are a dictionary of types, with entries being a dictionary, of event attributes and possible values.
#event type is keyup, event attribute is key, possible value is k_escape, and then need make something happen.
#need function for event in there at some point, or use the different things to call afunction that handles it.