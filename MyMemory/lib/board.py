import random

class Card(object):
    def __init__(self,type,isFirst):
        self.type = type 
        self.age = 0
        self.selected = False
        self.active = True
        self.isFirst = isFirst
        self.mouse_over = False
        
    def is_same_card(self, other):
        self.type = other.type
            
class Board(object):
    def __init__(self):
        self.new_game()
                
    # --- Board functions ---
    def new_game(self):
        self.board = []
        for i in range(18):
            # add two of each type
            self.board.append(Card(i, True))
            self.board.append(Card(i, False))
        random.shuffle(self.board)
        self.unknown = list(self.board)
        self.known = []
        self.selected = []
    
    def get_cards(self):
        return self.board
            
    def select_card(self,c):
        c.age=0
        self.board.remove(c)
        if c in self.unknown:
            self.unknown.remove(c)
        elif c in self.known:
            self.known.remove(c)
        self.selected.append(c)
        c.selected = True
    
    def end_of_turn(self):
        pair = None
        if len(self.selected):
            if self.selected[0].type != self.selected[1].type:
                for c in self.selected:
                    c.selected = False
                    self.known.append(c)
                    self.board.append(c)
            else:
                for c in self.selected:
                    c.active = False
                pair = list(self.selected)                                 
        self.selected = []
        for c in self.known:
            c.age += 1
        return pair
    
    def is_game_over(self):
        if not len(self.board):
            return True
        return False
    
    # --- Help function for AI ---    
    def _build_temp_lists(self,maxage):
        k = []
        u = list(self.unknown)
        for c in self.known:
            if maxage is None:
                k.append(c)
            else:
                if c.age <= maxage:
                    k.append(c)
                else:
                    u.append(c)
        return (k,u)

    def search_known_for_pairs(self,maxage=None):
        known,unknown = self._build_temp_lists(maxage)
        for c1 in known:
            for c2 in known:
                if c2 != c1 and c2.type == c1.type:
                    return c1
        return None
    
    def search_known_for_match(self,maxage=None,card=None):
        if card is None:
            card = self.selected[0]
        known,unknown = self._build_temp_lists(maxage)
        for c in known:
            if c == card:
                continue
            if c.type == card.type:
                return c
        return None
    
    def get_known(self,maxage=None):
        known,unknown = self._build_temp_lists(maxage)
        return known
            
    def select_unknown(self,maxage=None):
        known,unknown = self._build_temp_lists(maxage)        
        if len(unknown):
            return(random.choice(unknown))
        else:
            return None
    
    def select_known(self,maxage=None):
        known,unknown = self._build_temp_lists(maxage)        
        if len(known):
            return(random.choice(known))
        else:
            return None
    
    def select_any(self):
        if len(self.board):
            return(random.choice(self.board))
        else:
            return None
        
