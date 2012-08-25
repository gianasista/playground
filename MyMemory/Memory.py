# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random 
from pprint import pprint

from lib.loader import Loader
from lib.board import Card, Board
from lib.ai import AIPlayer
from lib.gameboard import GameBoard
from lib.robotmouse import RobotMouse
from lib.sidepanel import SidePanel

from lib.vec2d import vec2d 

class Star(object):
    def __init__(self,img,pos):
        self.img = img
        x,y = pos
        self.pos = vec2d(float(x),float(y))
        self.speed = vec2d(1.0,0.0)
        self.speed.length = float(random.randint(1,3))
        self.speed.angle = random.randint(0,359)
        self.g = vec2d(0.0,0.1)
        
        self.count = 50
        
    def draw(self,dest):
        if self.count > 0:
            self.count -= 1
            dest.blit(self.img,self.pos.get_int_pos())
            self.pos+=self.speed
            self.speed+=self.g
        
class StarBurstAnim(object):
    
    def __init__(self):
        loader = Loader()
        self.stars = []
        for i in range(1,6):
            self.stars.append(loader.load_image("star%d.png" % i, True))
        self.anims = []

    def stop(self):
        self.anims = []

    def anim_done(self):
        if len(self.anims):
            return False
        return True

    def add(self,pos):
        for i in range(20):
            self.anims.append(Star(random.choice(self.stars),pos))
        
    def draw(self,dest):
        dels=[]
        for s in list(self.anims):
            if s.count == 0:
                dels.append(s)
            else:
                s.draw(dest)
        
        for d in dels:
            self.anims.remove(d)

    
class StarDustAnim(object):
    def __init__(self):
        loader = Loader()
        self.stars = []
        for i in range(1,6):
            self.stars.append(loader.load_image("star%d.png" % i, True))
        self.anims = []
        
    def anim_done(self):
        if len(self.anims):
            return False
        return True
        
    def add(self,pos):
        self.anims.append([40,pos])
    
    def draw(self,dest):
        dels=[]
        for a in list(self.anims):
            if a[0] == 0:
                dels.append(a)
            else:
                a[0]-=1
                x,y = a[1]
                for i in range(6):
                    dest.blit(random.choice(self.stars),(x+random.randint(-30,30)-10, y+random.randint(-30,30)-10))
                                   
        for d in dels:
            self.anims.remove(d)
    
class Memory(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600),1)
        pygame.display.set_caption("Memory v1.0")
                
        self.loader = Loader()
                        
        self.game_board = GameBoard()        
        self.side_panel = SidePanel()
        self.robot_mouse = RobotMouse() 
        self.ai_player = AIPlayer(3)
        
        self.side_panel.ai_level = self.ai_player.level
        self.side_panel.update_stats()
        self.pair_snd = self.loader.load_sound("pair.wav")
        self.win_snd = self.loader.load_sound("win.wav")
        self.win_snd.set_volume(0.5)
        self.boom_snd = self.loader.load_sound("boom.wav")
        self.boom_snd.set_volume(0.3)
        
        self.stardust = StarDustAnim()
        self.starburst = StarBurstAnim()
              
    def setup_new_game(self):
        self.board = Board()
        self.ai_player.set_board(self.board)
        self.game_board.set_board(self.board.get_cards())

        self.side_panel.player_score = 0
        self.side_panel.robot_score = 0
        self.side_panel.update_score()

    def select_card(self,card):
        self.board.select_card(card)
        self.game_board.touch_card(card)

    def main_loop(self):            
        clock = pygame.time.Clock()

        SETUP_NEW_GAME = 0
        PLAYER1_SELECT_FIRST = 10
        PLAYER1_SELECT_SECOND = 11
        PLAYER1_DONE = 12
        PLAYER2_SELECT_FIRST = 50
        PLAYER2_SELECT_SECOND = 51
        PLAYER2_DONE = 52
        ROBOT_SELECT_FIRST = 20
        ROBOT_SELECT_FIRST_WAIT = 21
        ROBOT_SELECT_SECOND = 30
        ROBOT_SELECT_SECOND_WAIT = 31
        ROBOT_DONE = 40
        GAME_OVER = 98
        GAME_OVER_WAIT = 99
        START_SCREEN = 100
    
        DELAY = 40
        state_delay = 0
        
        state = START_SCREEN
        
        next_player = 0
        
        starburst_count = 0
        
        shown_cards = []

        while 1:
            clock.tick(30)
            
            mouse_clicked = False
            mouse_pos = (0,0)            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    #elif event.key == K_F1:
                    #    self.side_panel.player_score =18
                    #    self.side_panel.robot_score = 0
                    #    state = GAME_OVER 
                    #elif event.key == K_F2:
                    #    self.side_panel.player_score = 0
                    #    self.side_panel.robot_score = 18
                    #    state = GAME_OVER 
                    #elif event.key == K_F3:
                    #    self.side_panel.player_score = 9
                    #    self.side_panel.robot_score = 9
                    #    state = GAME_OVER 
                elif event.type == MOUSEBUTTONDOWN:
                    #if event.button == 3:
                    #    self.starburst.add(event.pos)
                    if event.button == 1:
                        mouse_clicked = True
                        mouse_pos = event.pos            
                
            # === STATE HANDLER ===

            is_select_event = False
            selected_card = Card(-1, False)
            
            if state_delay > 0:
                state_delay -= 1
            else:
                # --- NEW GAME ---
                if state == START_SCREEN and mouse_clicked:
                    state = SETUP_NEW_GAME
                    self.setup_new_game()
                    self.game_board.goto_game()
                elif state == SETUP_NEW_GAME:
                    if self.side_panel.x > 600:
                        self.side_panel.x-=10
                    else:
                        if next_player == 1:
                            self.side_panel.show_robot(False,0,0)
                            state = PLAYER2_SELECT_FIRST
                            next_player = 0
                        else:
                            self.side_panel.show_player1(False)
                            state = PLAYER1_SELECT_FIRST
                            next_player = 1
                # --- PLAYER1 STATES ---
                elif state == PLAYER1_SELECT_FIRST and self.stardust.anim_done() and self.game_board.is_init_done() and mouse_clicked:
                    c = self.game_board.location_to_card(mouse_pos)
                    is_select_event = True
                    selected_card = c
                    if c and not c.selected:
                        self.select_card(c)
                        state = PLAYER1_SELECT_SECOND
                elif state == PLAYER1_SELECT_SECOND and mouse_clicked:
                    c = self.game_board.location_to_card(mouse_pos)
                    is_select_event = True
                    selected_card = c
                    if c and not c.selected:
                        self.select_card(c)
                        state = PLAYER1_DONE
                        state_delay = DELAY
                elif state == PLAYER1_DONE:
                    pair = self.board.end_of_turn() 
                    if pair:
                        for p in pair:
                            self.stardust.add(self.game_board.card_to_location(p))
                        self.side_panel.player1_score+=1
                        self.side_panel.update_score()
                        state = PLAYER1_SELECT_FIRST
                        self.pair_snd.play() 
                    else:
                        self.side_panel.show_player2(False)
                        state = PLAYER2_SELECT_FIRST 
                    if self.board.is_game_over():
                        state = GAME_OVER
                # --- PLAYER2 STATES ---
                elif state == PLAYER2_SELECT_FIRST and self.stardust.anim_done() and self.game_board.is_init_done() and mouse_clicked:
                    c = self.game_board.location_to_card(mouse_pos)
                    is_select_event = True
                    selected_card = c
                    if c and not c.selected:
                        self.select_card(c)
                        state = PLAYER2_SELECT_SECOND
                elif state == PLAYER2_SELECT_SECOND and mouse_clicked:
                    c = self.game_board.location_to_card(mouse_pos)
                    is_select_event = True
                    selected_card = c
                    if c and not c.selected:
                        self.select_card(c)
                        state = PLAYER2_DONE
                        state_delay = DELAY
                elif state == PLAYER2_DONE:
                    pair = self.board.end_of_turn() 
                    if pair:
                        for p in pair:
                            self.stardust.add(self.game_board.card_to_location(p))
                        self.side_panel.robot_score+=1
                        self.side_panel.update_score()
                        state = PLAYER2_SELECT_FIRST
                        self.pair_snd.play() 
                    else:
                        self.side_panel.show_player1(False)
                        state = PLAYER1_SELECT_FIRST 
                    if self.board.is_game_over():
                        state = GAME_OVER
                # --- GAME OVER ---
                elif state == GAME_OVER and self.stardust.anim_done():         
                    r = self.side_panel.show_winner()
                    self.win_snd.play()
                    self.side_panel.games_stat+=1
                    if r == 1:
                        self.side_panel.player_stat+=1
                        self.ai_player.you_lose()
                    elif r == 2:
                        self.side_panel.robot_stat+=1
                        self.ai_player.you_win()
                    self.side_panel.ai_level = self.ai_player.level
                    self.side_panel.update_stats()
                    self.game_board.goto_gameover(r)
                    state = GAME_OVER_WAIT
                    starburst_count = 40
                    starburst_delay = 0
                elif state == GAME_OVER_WAIT:
                    if mouse_clicked:         
                        self.game_board.goto_game()
                        self.setup_new_game()
                        state = SETUP_NEW_GAME
                        self.starburst.stop()
                    else:
                        if starburst_count:
                            if starburst_delay == 0:
                                starburst_count-=1
                                self.boom_snd.play()
                                x = random.randint(50,550)
                                y = random.randint(50,550)
                                self.starburst.add((x,y))
                                starburst_delay = random.randint(15,30)
                            else:
                                starburst_delay -= 1

            # === DRAWING ===

            self.game_board.draw(self.screen)
            
            if is_select_event and  not (selected_card in shown_cards):
                self.game_board.render_large_image(self.screen, selected_card)
                shown_cards.append(selected_card)
            
            if state != START_SCREEN:
                self.side_panel.draw(self.screen)                            
                self.robot_mouse.draw(self.screen)
            
            self.stardust.draw(self.screen)
            self.starburst.draw(self.screen)
            
            pygame.display.flip()            

def main():
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    pygame.mixer.pre_init(44100,-16,2, 1024)
     
    pygame.init()

    g = Memory()
    g.main_loop()
 
if __name__ == '__main__': 
    main()
