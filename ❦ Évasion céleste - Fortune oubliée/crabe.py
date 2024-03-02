import pyxel
import random

class Crabe :
    
    def __init__(self, degats, taille) :
        self.degats = degats
        self.taille = taille
        self.coord_x = random.randint(20, 90)
        self.coord_y = -30
        self.limite = self.coord_x + 10
        self.animation = 0
        self.visible = True
    
    def draw(self) :
        if self.visible :
            if pyxel.frame_count % 15 == 0 :
                self.animation = self.animation + 1
            
            if self.animation % 2 == 0 :
                pyxel.blt(self.coord_x,self.coord_y, 0, 248, 0, 255, 7, 0)
            else :
                pyxel.blt(self.coord_x,self.coord_y, 0, 248, 8, 255, 15, 0)
        else :
            pyxel.blt(self.coord_x,self.coord_y, 2, 236, 240, 255, 255, 5)
        
      
            
    def deplacer(self, ralentissement) :
        self.coord_y = self.coord_y + 3 - ralentissement
        if self.visible :
            if self.coord_x < self.limite :
                self.coord_x = self.coord_x + 1
                if self.coord_x == self.limite :
                    self.limite = self.limite - 20
            if self.coord_x > self.limite :
                self.coord_x = self.coord_x - 1
                if self.coord_x == self.limite :
                    self.limite = self.limite + 20
                
            