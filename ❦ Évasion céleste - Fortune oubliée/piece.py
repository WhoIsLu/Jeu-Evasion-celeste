import pyxel
import random

# Poids des pièces de 1 : 0.03
# Poids des pièces de 3 : 0.05

class Piece :
    def __init__(self, taille) :
        self.valeur = random.randint(1, 5) # La pièce vaudra 3 lorsque 'valeur' vaudra 1 (20% de chance)
        self.taille = taille
        self.coord_x = random.randint(20, 100)
        self.coord_y = -40
        self.etat = random.randint(1,50) # L'attribut 'etat' prend une valeur qui va permettre de déterminer si la pièce doit se constituer en sachet, ou si elle doit être isolée
                                         # Il permet aussi de déterminer la valeur des sachets
                                         # Si 'etat' < 5, c'est un sachet (10% de chance)
                                         # Si 'etat' == 1, le sachet est constitué de pièces de 3 (20% de chances parmis les 10%)
        
    def EstUnSachet(self) :
        """ Entrée : Une instance de la classe pièce
            Sortie : Un booléen, True si c'est un sachet de pièces, False sinon"""
        if self.etat < 5 :
            return True
        else :
            return False

    def valeur_piece(self) :
        """	Entrée : Une instance de la classe pièce
            Sortie : Un entier qui contient la valeur de la / les pièces (si c'est un sachet)"""
        if self.EstUnSachet() :
            if self.etat == 1 :
                valeur = 3
            else :
                valeur = 1
        else :
            if self.valeur == 1 :
                valeur = 3
            else :
                valeur = 1
        return valeur
        
    def draw(self) : # On dessine des de cercles de différentes couleurs et taille selon leur valeur
        if self.EstUnSachet() : 		# Il y a 10% de chance que les pièces se constituent en sachet. Si "etat" vaut 1, les pièces se mettent en sachet
            if self.valeur_piece() == 3 :	# Il y a 20% de chance que le sachet contienne 3 pièces qui valent 3 (violet)
                pyxel.blt(self.coord_x,self.coord_y, 2, 128, 204, 137, 217, 0)
            else : # Il y a donc 80% de chance que le sachet contienne 5 pièces qui valent 1 (rose)
                pyxel.blt(self.coord_x,self.coord_y, 2, 108, 238, 117, 255, 0)
        else : # Dans les autres cas elle est isolée
            if self.valeur_piece() == 3 : # Il y a 20% de chance que la pièce isolée prenne la valeur 3
                pyxel.blt(self.coord_x,self.coord_y, 0, 168, 16, 177, 25, 0)
            else : # Dans les autres cas la pièce isolée vaut 1
                pyxel.blt(self.coord_x,self.coord_y, 0, 128, 40, 137, 49, 0)

            
    def deplacer(self, ralentissement) :
        self.coord_y = self.coord_y + 3 - ralentissement
        