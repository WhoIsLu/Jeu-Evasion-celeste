import pyxel
from crabe import *

class Vaisseau :
    def __init__(self,x, y, taille, pv, argent, temps) :
        self.x = x
        self.y = y
        self.taille = taille
        self.pv = pv
        self.argent = argent
        self.temps = temps
        self.inventaire = []
        self.poids_supp = 0
        self.collision_cocotier = False
        self.collision_crabe = False
        self.collision_rocher = False
        
    def les_collisions_cocotier(self, b) :
        self.collision_cocotier = b
    
    def les_collisions_crabe(self, b) :
        self.collision_crabe = b

    def les_collisions_rocher(self, b) :
        self.collision_rocher = b

    def draw(self) :
        #pyxel.circ(self.x, self.y, self.taille, 1)
        if any([self.collision_cocotier, self.collision_crabe, self.collision_rocher]):
            pyxel.blt(self.x, self.y, 0, 122, 240, 137, 255, 0)
            
        else :
            pyxel.blt(self.x,self.y, 0, 240, 72, 255, 87, 0)
        
    def deplacer(self) :
        
        if pyxel.btn(pyxel.KEY_RIGHT) and (self.x < 102) :
            self.x = self.x + 3 - self.poids_supp
        
        if pyxel.btn(pyxel.KEY_LEFT) and (self.x > 3) :
            self.x = self.x - 3 + self.poids_supp
         
        if pyxel.btn(pyxel.KEY_UP) and (self.y > 3) :
            self.y = self.y - 3 + self.poids_supp
            
        if pyxel.btn(pyxel.KEY_DOWN) and (self.y < 182) :
            self.y = self.y + 3 - self.poids_supp
            
    def jeter_pieces(self, liste_pieces_jetees) :
        if len(self.inventaire) != 0 :
            if pyxel.btnp(pyxel.KEY_SPACE) :
                if self.inventaire[-1].EstUnSachet() :
                    if self.inventaire[-1].valeur_piece() == 3 :
                        self.argent = self.argent - 3
                        self.poids_supp = self.poids_supp - 0.04
                    else :
                        self.argent = self.argent - 1
                        self.poids_supp = self.poids_supp - 0.02
                else :
                    if self.inventaire[-1].valeur_piece() == 3 :
                        self.argent = self.argent - 3
                        self.poids_supp = self.poids_supp - 0.04
                    else :
                        self.argent = self.argent - 1
                        self.poids_supp = self.poids_supp - 0.02
                        
                self.inventaire[-1].coord_y = self.y + 15
                self.inventaire[-1].coord_x = self.x
                liste_pieces_jetees.append(self.inventaire[-1])
                self.inventaire.pop()