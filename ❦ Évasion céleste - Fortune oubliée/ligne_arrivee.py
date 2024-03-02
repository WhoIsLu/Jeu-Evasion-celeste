import pyxel

class Ligne_Arrivee :
    def __init__(self, coord_y) :
        self.coord_y = coord_y
        
    def draw(self) :
        pyxel.blt(0, self.coord_y, 0, 0, 210, 120, 240, 0) #Dessin de la ligne d'arrivée

    def deplacer(self, ralentissement) :
        self.coord_y = self.coord_y + 3 - ralentissement