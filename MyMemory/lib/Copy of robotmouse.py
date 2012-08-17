
import pygame
from pygame.locals import *
import random 

from loader import Loader

class RobotMouse(object):
    def __init__(self):
        self.loader = Loader()
        self.img = self.loader.load_image("mouse.png",True)
        self.pos = (400,300)
        self.to_pos = self.pos
        self.moving = False
        self.visible = False
        
    def hide(self):
        self.visible = False
       
    def is_moving(self):
        return self.moving
               
    def goto(self,pos):
        self.to_pos = pos
        self.visible = True
        self.moving = True
        
    def _speed(self,a,b):
        f = min(a,b)
        t = max(a,b)
        s = (t-f)/2        
        return min(s,10)
        
    def _update(self):
        if not self.moving:
            return
        
        cx,cy = self.pos
        tx,ty = self.to_pos
        
        if cx<tx:
            cx+=self._speed(cx,tx)
        elif cx>tx:
            cx-=self._speed(cx,tx)

        if cy<ty:
            cy+=self._speed(cy,ty)
        elif cy>ty:
            cy-=self._speed(cy,ty)

        if abs(cx-tx) <= 2:
            cx = tx
        if abs(cy-ty) <= 2:
            cy = ty

        self.pos = (cx,cy)

        if cx == tx and cy == ty:
            self.moving = False

    def draw(self,dest):
        if not self.visible:
            return
        self._update()
        dest.blit(self.img,self.pos)
