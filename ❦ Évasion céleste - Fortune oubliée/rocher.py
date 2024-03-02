import pyxel
import random

class Rocher :
    
    def __init__(self, degats, taille) :
        self.coord_x = random.randint(20, 100)
        self.coord_y = -30
        self.degats = degats
        self.taille = taille
    
    def draw(self) :
        pyxel.blt(self.coord_x,self.coord_y, 0, 129, 3, 142, 12, 0)
        
        
    def deplacer(self, ralentissement) :
        self.coord_y = self.coord_y + 3 - ralentissement