
import pygame
from pygame.locals import *
import random 

from loader import Loader

class SidePanel(object):
    def __init__(self):
        
        self.x = 800
        
        self.loader = Loader()   

        self.fonts = []
        self.fonts.append(self.loader.load_font("scribble.TTF", 38)) 
        self.fonts.append(self.loader.load_font("scribble.TTF", 23)) 
        self.fonts.append(self.loader.load_font("scribble.TTF", 18)) 

        self.side = self.loader.load_image("side.png",True)
        self.back = self.side.copy()
        self.text(0,"Score",30)
        
        self.robot = self.loader.load_image("robot.png",True)
        self.player1 = self.loader.load_image("player.png",True)
        self.both = self.loader.load_image("both_win.png",True)
        
        self.signs = {}
        self.signs["1"] = self.loader.load_image("unknown.png",True)
        self.signs["2"] = self.loader.load_image("known.png",True)
        self.signs["11"] = self.loader.load_image("unknown_unknown.png",True)
        self.signs["12"] = self.loader.load_image("unknown_known.png",True)
        self.signs["22"] = self.loader.load_image("known_known.png",True)
                
        self.win = self.loader.load_image("win.png",True)
        self.player1_score = 0
        self.robot_score = 0
        self.games_stat = 0
        self.player_stat = 0
        self.robot_stat = 0
        self.ai_level = 0
        
        self.update_score()
        self.update_stats()
        self.show_player1(False)
        #self.show_robot(False,0,0)
    
    def clear_gfx_area(self):
        r = pygame.Rect(29,185,169,302)
        self.back.blit(self.side,r.topleft,r)
        #pygame.draw.rect(self.back, (0,0,0), r, 1) 
        
    def show_winner(self):
        if self.player1_score > self.robot_score:
            self.show_player1(True)
            return 1
        elif self.player1_score < self.robot_score:
            self.show_robot(True, 0, 0)
            return 2
        else:
            self.show_both()
            return 0

    def show_both(self):
        self.clear_gfx_area()
        
        r = self.player1.get_rect()
        r.center = (90,330)

        self.back.blit(self.both,r.topleft)

    def show_player1(self,win):
        self.clear_gfx_area()
        
        r = self.player1.get_rect()
        r.center = (110,340-10)

        self.back.blit(self.player1,r.topleft)

        if win:
            self.back.blit(self.win,(90,227-10))
            
    def show_player2(self,win):
        self.clear_gfx_area()
        
        r = self.robot.get_rect()
        r.center = (110,340-10)

        self.back.blit(self.robot,r.topleft)

        if win:
            self.back.blit(self.win,(90,227-10))

    def show_robot(self,win,card1,card2):
        self.clear_gfx_area()
        
        r = self.player1.get_rect()
        r.center = (110,340)

        self.back.blit(self.robot,r.topleft)
        
        if card1 and not card2:
            i = self.signs["%d" % card1]                
            r = i.get_rect()
            r.center = (110,255)
            self.back.blit(i,r.topleft)
        elif card1 and card2:
            i = self.signs["%d%d" % (card1,card2)]                
            r = i.get_rect()
            r.center = (110,255)
            self.back.blit(i,r.topleft)

        if win:
            self.back.blit(self.win,(85,237))
                
    def update_score(self):
        r = pygame.Rect(50,54,126,129)
        self.back.blit(self.side,r.topleft,r)
        
        self.text(1,"Julia",75)
        self.text(0,str(self.player1_score),75+25)

        self.text(1,"Oliver",75+60)
        self.text(0,str(self.robot_score),75+25+60)
        
    def update_stats(self):
        r = pygame.Rect(30,485,173,95)
        self.back.blit(self.side,r.topleft,r)
        
        y = 500
        r = 22
        #self.text(2,"Games: %d" % self.games_stat,y); y+=r
        self.text(2,"Julia: %d" % self.player_stat,y); y+=r
        self.text(2,"Oliver: %d" % self.robot_stat,y); y+=r
        #self.text(2,"AI Level: %d" % self.ai_level,y); y+=r

    def text(self,fnt,txt,y,x=None):
        color = (0,0,0)
        img = self.fonts[fnt].render(txt, True, color)
        r = img.get_rect()
        r.center = (110,y)
        if x is not None:
            r.left = x
        self.back.blit(img,r.topleft)
        
    def draw(self,dest):
        dest.blit(self.back,(self.x,0))
