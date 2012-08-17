
import random
    
class AIPlayer(object):
    def __init__(self,initial_level):
        self.last_selected = None
        self.first = 0
        self.second = 0 
        
        self.use_strategy = False
        self.give_hint = False
        self.maxage = None

        self.set_level(initial_level)
        
    def set_level(self,level):
        if level < 0:
            level = 0
        elif level > 32:
            level = 32

        self.use_strategy = False
        self.give_hint = False
            
        if level == 0:
            self.maxage = 0
            self.give_hint = True
        elif level >= 1 and level <= 30:
            self.maxage = level-1
        elif level == 31:
            self.maxage = None
        elif level == 32:
            self.maxage = None
            self.strategy = True

        self.level = level
        
    def set_board(self,board):
        self.board = board
        
    def you_win(self):
        self.set_level(self.level-1)

    def you_lose(self):
        self.set_level(self.level+1)

    def select_first_card(self):
        b = self.board
        self.first = 1            
        self.second = 0 
        # Do we know about a pair?
        c = b.search_known_for_pairs(self.maxage)
        if c is not None:
            self.first = 2
            self.last_selected = c
            return c
        # select an unknown card
        c = b.select_unknown(self.maxage)
        if c is not None:
            self.last_selected = c
            return c
        # select an known card
        c = b.select_known(self.maxage)
        if c is not None:
            self.last_selected = c
            return c
        
    def select_second_card(self):
        b = self.board
        self.second = 1 
        # do we know about a match?
        
        if self.give_hint:
            k = self.board.get_known(1)
            if len(k):
                random.shuffle(k)
                for kc in k:
                    c = b.search_known_for_match(3,kc)
                    if c is not None:
                        self.last_selected = c
                        return c
        
        c = b.search_known_for_match(self.maxage)
        if c is not None:
            self.second = 2 
            self.last_selected = c
            return c       
        if self.use_strategy and (len(b.known)%2==0):
            # select an known card
            c = b.select_known(self.maxage)
            if c is not None:
                self.last_selected = c
                return c
            # select an unknown card
            c = b.select_unknown(self.maxage)
            if c is not None:
                self.last_selected = c
                return c
        else:
            # select an unknown card
            c = b.select_unknown(self.maxage)
            if c is not None:
                self.last_selected = c
                return c
            # select an known card
            c = b.select_known(self.maxage)
            if c is not None:
                self.last_selected = c
                return c
        