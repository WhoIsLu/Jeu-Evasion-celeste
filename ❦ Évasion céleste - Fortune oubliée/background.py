import pyxel

class Background :
    def __init__(self, coord_y) :
        self.coord_y = coord_y
        
    def draw(self) :
        pyxel.blt(0, self.coord_y, 0, 0, 0, 120, 200, 4) # Dessin du background

    def deplacer(self, ralentissement) :
        self.coord_y = self.coord_y + 3 - ralentissement