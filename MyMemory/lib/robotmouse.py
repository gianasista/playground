
import pygame
from pygame.locals import *
import random 

from loader import Loader
from lib.vec2d import vec2d


class RobotMouse(object):
    def __init__(self):
        self.loader = Loader()
        self.img = self.loader.load_image("mouse.png",True)
        self.moving = False
        self.visible = False
        
        self.pos = vec2d(400.0,300.0)
        self.to_pos = vec2d(400.0,300.0)
        self.heading = vec2d(1.0,0.0) 
        self.dist = 0
        
    def hide(self):
        self.visible = False
       
    def is_moving(self):
        return self.moving
               
    def goto(self,pos):
        self.to_pos = vec2d(float(pos[0]),float(pos[1]))
        self.visible = True
        self.moving = True
        
        self.heading = self.to_pos - self.pos
        self.dist = self.heading.length
        
        self.heading.length = 12.0
                
    def _update(self):
        if not self.moving:
            return            
        
        self.pos += self.heading
        self.dist-=self.heading.length
        if self.dist<=0:
            self.pos = self.to_pos.clone()
            self.moving = False
                
    def draw(self,dest):
        if not self.visible:
            return
        self._update()
        dest.blit(self.img,self.pos.get_int_pos())
