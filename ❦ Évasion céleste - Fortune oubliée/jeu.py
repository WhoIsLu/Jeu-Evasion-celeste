
import pyxel
import random
import time

from piece import *
from crabe import *
from vaisseau import *
from cocotier import *
from rocher import *
from ligne_arrivee import *
from background import *
from ecran_titre import *

# Visuel : pyxel edit visuels.pyxres
#python -m pyxel edit visuels.pyxres
class Jeu :
    def __init__(self) :
        pyxel.init(120, 200, title = "Évasion Céleste : Fortune Oubliée")   

        pyxel.load("visuels.pyxres")
        pyxel.play(0, [7], loop=True)
        pyxel.play(1, [8], loop=True)
        pyxel.play(2, [9], loop=True)
        # Pièces
        self.liste_pieces = []
        self.liste_pieces_jetees = []

        # Background
        self.fond_initial = Background(0) # On a besoin de 3 motifs qui vont s'alterner pour donner l'illusion que le background défile
        self.fond_repete1 = Background(200)
        self.fond_repete2 = Background(400)

        # Écran titre
        self.ecran_titre1 = Ecran_titre()

        # Vaisseau
        self.vaisseau1 = Vaisseau(60, 160, 8, 100, 0, 30)

        # Cocotiers
        self.liste_cocotier = []

        # Crabe
        self.liste_crabe = []

        # Rocher
        self.liste_rocher = []


        # Ligne d'arrivée
        self.ligne_arrivee = Ligne_Arrivee(-2000)

        pyxel.run(self.update, self.draw)


    def update(self) :

        while self.ecran_titre1.pseudo == '' or len(self.ecran_titre1.pseudo) > 9 : # On demande au joueur son pseudo dès le début, qu'il pourra modifier plus tard
            self.ecran_titre1.pseudo = input("Entrez votre pseudo (Max. 9 caractères) : ")

        # Dès que la partie est lancée, tous les facteurs sont remis à leur état initial
        if self.ecran_titre1.reinitialiser_jeu :
            self.vaisseau1.pv = 100 # Les pv sont remis à 100
            self.liste_pieces.clear() # Les pièces sont retirées
            self.liste_pieces_jetees.clear()
            self.vaisseau1.collision_cocotier = False
            self.vaisseau1.collision_crabe = False
            self.vaisseau1.collision_rocher = False

            self.liste_rocher.clear() # Les obstacles sont retirés
            self.liste_cocotier.clear()
            self.liste_crabe.clear()
            

            self.ligne_arrivee.coord_y = -2000 # La ligne d'arrivée est remise à son point de départ

            self.vaisseau1.temps = 30 # Le chrono remis à 30 secondes
            self.vaisseau1.x = 60 # Le vaisseau replacé à sa position de départ
            self.vaisseau1.y = 160

            self.vaisseau1.argent = 0 # L'argent récolté par le vaisseau est vidé
            self.vaisseau1.inventaire.clear()
            self.vaisseau1.poids_supp = 0 # Et le poids est remis à son état initial

            self.ecran_titre1.reinitialiser_jeu = False # Et la variable reviens à son état False

        # Le jeu continue tant que le joueur n'a ni gagné, ni perdu, ou qu'il n'est pas dans les menus
        if not self.ecran_titre1.game_over and not self.ecran_titre1.victoire and not self.ecran_titre1.afficher_menus :
            
           # Crabe
            valeurs_compteur = [30, 35, 40, 45] # Cette liste contient les valeurs des délais qu'il peut y avoir entre les apparitions de pièces
            index = random.randint(0, 3)		    # Le tout est rendu aléatoire par cet index aléatoire
            if pyxel.frame_count % valeurs_compteur[index] == 0 and self.ligne_arrivee.coord_y < -50 :
                self.liste_crabe.append(Crabe(20, 3))
            for crabe in self.liste_crabe:
                crabe.deplacer(self.vaisseau1.poids_supp)
                if random.randint(1, 300) == 300 :
                    crabe.visible = False
                if crabe.visible:
                    if self.vaisseau1.y < crabe.coord_y + 7 and self.vaisseau1.y > crabe.coord_y - 10 and self.vaisseau1.x < crabe.coord_x + 9 and self.vaisseau1.x > crabe.coord_x - 12:
                        self.vaisseau1.les_collisions_crabe(True)  # Activation de la collision
                        pyxel.play(0, [2])
                        self.vaisseau1.pv -= crabe.degats
                        self.liste_crabe.remove(crabe)
                    else:
                        self.vaisseau1.les_collisions_crabe(False)  # Désactivation de la collision si le vaisseau n'est pas en collision
            
            # Pièces
            valeurs_compteur = [10, 15, 20, 25, 30] # Cette liste contient les valeurs des délais qu'il peut y avoir entre les apparitions de pièces
            index = random.randint(0, 4)		    # Le tout est rendu aléatoire par cet index aléatoire
            if pyxel.frame_count % valeurs_compteur[index] == 0 and self.ligne_arrivee.coord_y < -50 : # Les pièces continuent à apparaitre régulièrement tant que la ligne d'arrivée n'atteint pas un certain point (y = -50)
                self.liste_pieces.append(Piece(3))
            for piece in self.liste_pieces :
                piece.deplacer(self.vaisseau1.poids_supp)
                if self.vaisseau1.y < piece.coord_y + 10 and self.vaisseau1.y > piece.coord_y - 10 and self.vaisseau1.x < piece.coord_x + 15 and self.vaisseau1.x > piece.coord_x - 15 : # On met en place une zone de collision verticale et horizontale
                    if piece.EstUnSachet() : # Si il s'agit d'un sachet
                        pyxel.play(0,[5])
                        if piece.valeur_piece() == 3 :	# Si le vaisseau ramasse un sachet de pièces violettes, le score augmente de 3 x 3 = 9, et le poids de 3 x 0.04 = 0.10
                            for i in range(3) : # On ramasse les 3 pièces du sachet, donc on change l'objet 'sachet de pièces' pour 3 pièces distinctes
                                piece_a_ajouter = Piece(3) # On crée donc de nouveaux objets qui vont remplacer le sachet par des pièces lorsqu'il est ramassé
                                piece_a_ajouter.etat = 50  # Ainsi, cet objet est une pièce
                                piece_a_ajouter.valeur = 1 # Et sa valeur est 3

                                self.vaisseau1.argent = self.vaisseau1.argent + 3
                                self.vaisseau1.inventaire.append(piece_a_ajouter)
                                self.vaisseau1.poids_supp = self.vaisseau1.poids_supp + 0.05 # Et on alourdit le vaisseau

                        else : # Si le vaisseau ramasse un sachet de pièces roses, le score augmente de 5 x 1 = 5, et le poids de 5 x 0.02 = 0.10
                            for i in range(5) :
                                piece_a_ajouter = Piece(3)
                                piece_a_ajouter.etat = 50  # Ainsi, cet objet est une pièce
                                piece_a_ajouter.valeur = 5 # Et sa valeur est 1

                                self.vaisseau1.argent = self.vaisseau1.argent + 1
                                self.vaisseau1.inventaire.append(piece_a_ajouter)
                                self.vaisseau1.poids_supp = self.vaisseau1.poids_supp + 0.03
                    else : # Si il s'agit d'une pièce isolée
                        if piece.valeur_piece() == 3 : # Si le vaisseau ramasse une pièce violette, le score augmente de 3, et le poids de 0.04
                            pyxel.play(0,[4])
                            self.vaisseau1.argent = self.vaisseau1.argent + 3
                            self.vaisseau1.inventaire.append(piece)
                            self.vaisseau1.poids_supp = self.vaisseau1.poids_supp +  0.05
                        else : 		# Si le vaisseau ramasse une pièce rose, le score augmente de 1, et le poids de 0.02
                            pyxel.play(0,[3])
                            self.vaisseau1.argent = self.vaisseau1.argent + 1
                            self.vaisseau1.inventaire.append(piece)
                            self.vaisseau1.poids_supp = self.vaisseau1.poids_supp + 0.03
                    self.liste_pieces.remove(piece)

            # Pièces jetées
            for piece_jetee in self.liste_pieces_jetees :
                piece_jetee.deplacer(self.vaisseau1.poids_supp)

            # Background
            if self.fond_initial.coord_y > 200 :
                self.fond_initial.coord_y = self.fond_initial.coord_y - 600
            elif self.fond_repete1.coord_y > 200 :
                self.fond_repete1.coord_y = self.fond_repete1.coord_y - 600
            elif self.fond_repete2.coord_y > 200 :
                self.fond_repete2.coord_y = self.fond_repete2.coord_y - 600

            self.fond_initial.deplacer(self.vaisseau1.poids_supp)
            self.fond_repete2.deplacer(self.vaisseau1.poids_supp)
            self.fond_repete1.deplacer(self.vaisseau1.poids_supp)


            # Rocher
            valeurs_compteur = [30, 35, 40, 45] # Cette liste contient les valeurs des délais qu'il peut y avoir entre les apparitions de pièces
            index = random.randint(0, 3)		    # Le tout est rendu aléatoire par cet index aléatoire
            if pyxel.frame_count % valeurs_compteur[index] == 0 and self.ligne_arrivee.coord_y < -50 :
                self.liste_rocher.append(Rocher(15, 8))
            self
            for rocher in self.liste_rocher :
                rocher.deplacer(self.vaisseau1.poids_supp)
                if self.vaisseau1.y < rocher.coord_y +12 and self.vaisseau1.y > rocher.coord_y - 8 and self.vaisseau1.x < rocher.coord_x + 10 and self.vaisseau1.x > rocher.coord_x - 10 :
                    self.vaisseau1.les_collisions_rocher(True)
                    pyxel.play(0,[1])
                    self.vaisseau1.pv = self.vaisseau1.pv - rocher.degats
                    self.liste_rocher.remove(rocher)
                else :
                    self.vaisseau1.les_collisions_rocher(False)
                    

            # Cocotier
            if pyxel.frame_count % 67 == 0 and not 0 > self.ligne_arrivee.coord_y > -60 : # Les obstacles quant à eux ne doivent pas apparaitre par dessus la ligne d'arrivée, mais avant ou après
                self.liste_cocotier.append(Cocotier(100, 6))
            for cocotier in self.liste_cocotier :
                cocotier.deplacer(self.vaisseau1.poids_supp)
                if self.vaisseau1.y < cocotier.y + 18 and self.vaisseau1.y > cocotier.y - 10 and self.vaisseau1.x < cocotier.x + 12 and self.vaisseau1.x > cocotier.x - 8 :
                    self.vaisseau1.les_collisions_cocotier(True)
                    pyxel.play(0,[0])
                    self.vaisseau1.pv = self.vaisseau1.pv - cocotier.degats
                    self.liste_cocotier.remove(cocotier)
                else :
                    self.vaisseau1.les_collisions_cocotier(False)


            # Déplacements du vaisseau
            self.vaisseau1.deplacer()
            self.vaisseau1.jeter_pieces(self.liste_pieces_jetees)

            # Déplacements de la ligne d'arrivée
            self.ligne_arrivee.deplacer(self.vaisseau1.poids_supp)

            # Condition de victoire (dépasser la ligne d'arrivée)
            if self.vaisseau1.y < self.ligne_arrivee.coord_y + 25 :
                self.ecran_titre1.victoire = True

            # Conditions de défaite (Points de vie qui tombent à 0 ou temps écoulé)
            if self.vaisseau1.pv <= 0 or self.vaisseau1.temps == 0 :
                pyxel.play(0,[0])
                self.ecran_titre1.game_over = True

        # Écran titre
        self.ecran_titre1.deplacer()



    def draw(self) :
        # Le jeu continue tant que le joueur n'a ni gagné, ni perdu
        if not self.ecran_titre1.game_over and not self.ecran_titre1.victoire and not self.ecran_titre1.afficher_menus:
            # Création de la fenêtre de jeu
            pyxel.cls(0)
            pyxel.rect(0, 0, 120, 200, 10)

            # Background
            self.fond_initial.draw()
            self.fond_repete1.draw()
            self.fond_repete2.draw()

            # Ligne d'arrivée
            self.ligne_arrivee.draw()

            # Pièces générées naturellement
            for piece in self.liste_pieces :
                piece.draw()

            # Pièces jetées
            for piece_jetee in self.liste_pieces_jetees :
                piece_jetee.draw()

            # Cocotier
            for cocotier in self.liste_cocotier :
                cocotier.draw()

            # Rocher
            for rocher in self.liste_rocher :
                rocher.draw()

            # Crabe
            for crabe in self.liste_crabe:
                crabe.draw()

            # Vaisseau
            self.vaisseau1.draw()

            # Affichages des scores
            if self.vaisseau1.poids_supp >= 0.7 :
                pyxel.text(45, 100, "Trop lourd", pyxel.frame_count % 16)

                # Affichage de l'argent
            pyxel.text(102, 13, str(self.vaisseau1.argent), 0)
            pyxel.blt(90, 9, 0, 128, 40, 137, 49, 0)

                # Affichage du chronomètre
            if pyxel.frame_count % 30 == 0 :
                self.vaisseau1.temps = self.vaisseau1.temps - 1
            pyxel.text(10, 13, str("Chrono : {}".format(self.vaisseau1.temps)), 0)

                # Affichage des points de vie
            if self.vaisseau1.pv > 50 :
                pyxel.text(102, 25, str(self.vaisseau1.pv), 0)
                pyxel.blt(90, 23, 0, 139, 122, 147, 130, 0)

            else :
                pyxel.text(102, 25, str(self.vaisseau1.pv), 0)
                pyxel.blt(90, 10, 0, 123, 131, 152, 36, 0)


        # Affichage et gestion de l'écran titre
        self.ecran_titre1.draw()


        # Affichage du message de victoire et du score
        if self.ecran_titre1.victoire :
            self.ecran_titre1.menu_courant[0] = 'Victoire'

            self.ecran_titre1.score = (self.vaisseau1.temps*2) * (self.vaisseau1.argent*4) + self.vaisseau1.pv*3 # On donne plus d'importance aux pièces qu'au temps, et on multiplie les scores par des grandes valeurs pour que ce soit plus satisfaisant à jouer

            # Mise à jour du fichier.txt qui enregistre les 5 meilleurs scores
            self.ecran_titre1.enregistrer_score(self.ecran_titre1.score)

            self.ecran_titre1.afficher_menus = True
            self.ecran_titre1.victoire = False


        # Affichage du message de défaite
        if self.ecran_titre1.game_over :
            self.ecran_titre1.menu_courant[0] = 'Game_over'
            self.ecran_titre1.afficher_menus = True

Jeu()