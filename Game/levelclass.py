# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 18:38:57 2018

@author: Lenovo
"""

class Level:

"""
def loadSolidPositions(self):
    pass

def addSolidPosition(self):
    pass

def removeSolidPosition(self):
    pass
    
def addResource(self):
    pass

def removeResource(self):
    pass

def addItem(self):
    pass
    
def removeItem(self):
    pass

So level should create surface. And then create sprite groups for solids, 
positions and resources(all different RenderPlain
groups) so need classes inheriting from sprite for them aswell
"""
    def __init__(self, tmx_file):
        self.tmx_bk = load_pygame(tmx_file)
        self.size = (self.tmx_bk.width * self.tmx_bk.tilewidth,
        self.tmx_bk.height * self.tmx_bk.tileheight)
        # layers as named in the tmx file
        self.layer_names = {'background': self.tmx_bk.get_layer_by_name('background'),
                            #'objects': self.tmx_bk.get_layer_by_name('objects'), 
                            'solids': self.tmx_bk.get_layer_by_name('solids'), 
                            'materials': self.tmx_bk.get_layer_by_name('materials')}
        #self.start_pos = self.layer_names['objects'].properties['start_pos']
        self.start_pos = (self.tmx_bk.get_object_by_name("start_pos").x,
        self.tmx_bk.get_object_by_name("start_pos").y)
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