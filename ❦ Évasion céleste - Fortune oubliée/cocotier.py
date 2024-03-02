
import pyxel
import random

class Cocotier :
    
    
    def __init__(self, degats, taille) :
        
        self.degats = degats
        self.taille = taille
        self.x = random.randint(5, 102)
        self.y = -30
    
    def draw(self) :
        pyxel.blt(self.x,self.y, 0, 152, 96, 172, 115, 0)
        
        
    def deplacer(self, ralentissement) :
        self.y = self.y + 3 - ralentissement

