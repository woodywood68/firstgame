# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 18:37:54 2018

@author: Lenovo
"""

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
            for y in range(self.lvlr.height-int(self.size[1]/2)-self.chr.height, self.lvlr.height, self.chr.height)]
        self.tnb += self.b
#print(tnb)
        self.lnr = [[x,y] for x in range(0, int(self.size[0]/2), self.chr.width) 
            for y in range(0, self.lvlr.height, self.chr.height)]
        self.r= [[x,y] for x in range(self.lvlr.width - int(self.size[0]/2)-self.chr.height, self.lvlr.width, self.chr.width) 
            for y in range(0, self.lvlr.height, self.chr.height)]
        self.lnr += self.r
        self.indy = 0
        self.solid_positions = []


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
        startx = self.size[0]/2
        starty = self.size[1]/2
        
        #if the screen is at edge, changes character start positions to actual position.
        if -lvlx == 0.0 or  -lvlx == (self.lvl.size[0] - self.size[0]):
            startx = self.lvl.start_pos[0]
        if -lvly == 0.0 or  -lvly ==  (self.lvl.size[1] - self.size[1]):
            starty = self.lvl.start_pos[1]
            

            
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