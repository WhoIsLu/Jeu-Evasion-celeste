import pyxel

class Ecran_titre :
    def __init__(self) : # On définit dans une listes le différents menus qu'aura l'écran titre
        
        self.game_over = False
        self.victoire = False

        self.afficher_menus = True
        self.menus = ['Menu principal', 'Scores', 'Options', 'Game_over', 'Victoire'] 
        self.boutons = {'Menu principal':['Jouer', 'Scores', 'Options', 'Quitter'], # Et dans un dictionnaire les différents boutons en valeurs, associés aux menus en clés
                        'Scores':['Retour'],
                        'Options':['Regles', 'Commandes', 'Changer de pseudo ', 'Retour'],
                        'Page 0':['Retour ', 'Suivant'],
                        'Page 1':['Retour ', 'Suivant', 'Precedent'],
                        'Page 2':['Retour ', 'Precedent'],
                        'Commandes':['Retour '],
                        'Game_over':['Rejouer', 'Changer de pseudo', 'Menu principal'],
                        'Victoire':['Rejouer', 'Menu principal'] # Comme dans ce dictionnaire, il y a 2 boutons 'Changer de pseudo', l'un d'entre eux aura un espace à la fin ('Changer de pseudo ') pour les différencier, sans pour autant que ce soit visible en jeu
                        }															  # Idem avec le bouton retour, qui revient soit à 'Menu principal', soit à 'Options'
        self.menu_courant = ['Menu principal', 0] # On a ici le menu courant, ainsi que sa position dans la liste
        self.coord_y = 120 # Il s'agit de la hauteur du bouton le plus haut
        self.reinitialiser_jeu = False # On se servira de cet attribut pour remettre le jeu à son état initiale à chaque partie lancée
        self.pseudo = ''
        self.page = 0
        self.score = 0
        
        
    def enregistrer_score(self, score_courant) :
        meilleurs_scores = open("scores.txt")
        lignes = meilleurs_scores.readlines()
        meilleurs_scores.close()
        pseudo_courant = self.pseudo + "\n"
        if not len(lignes) == 0 :
            
            if score_courant < int(lignes[-1]) :
                score_a_ecrire = str(score_courant) + "\n"
                lignes.append(pseudo_courant)
                lignes.append(score_a_ecrire)
            
            else :
                for indice in range(1, len(lignes), 2) :
                    score_ecrit = int(lignes[indice])
                    pseudo_ecrit = lignes[indice - 1]
                
                    if score_ecrit < score_courant :
                        score_inferieur = score_ecrit
                        lignes[indice] = str(score_courant) + "\n"
                        score_courant = score_inferieur
                
                        pseudo_inferieur = pseudo_ecrit
                        lignes[indice - 1] = pseudo_courant
                        pseudo_courant = pseudo_inferieur
                
                score_a_ecrire = str(score_courant) + "\n"
                lignes.append(pseudo_courant)
                lignes.append(score_a_ecrire)
            
            while len(lignes) > 10 :
                del lignes[10]
                
        else :
            score_a_ecrire = str(score_courant) + "\n"
            lignes.append(pseudo_courant)
            lignes.append(score_a_ecrire)
        
        meilleurs_scores = open("scores.txt", "w")
        meilleurs_scores.write('')
        meilleurs_scores.close()
        
        meilleurs_scores = open("scores.txt", "a")
        for element in lignes :
            meilleurs_scores.write(str(element))
        meilleurs_scores.close()
            
        
                
        
        
    def afficher_boutons(self, dico_boutons, menu_courant, x, coord_y) :
        decalage = 0
        for bouton in dico_boutons[menu_courant[0]] :
            if bouton == 'Menu principal' : # Comme le bouton 'Menu_principal' est plus large que les autres, il est nécessaire de le décaler un peu sur la gauche pour que ça reste esthétique
                coord_x = x - 15
            else:
                if bouton == 'Changer de pseudo' or bouton == 'Changer de pseudo ' : # Pareil pour le bouton 'Changer de pseudo,' qui est plus long
                    coord_x = x - 21
                else :
                    if bouton == 'Commandes' : # Pareil pour le bouton 'Commandes', mais en moins accentué
                        coord_x = x - 6
                    else :
                        coord_x = x
            if bouton == dico_boutons[menu_courant[0]][menu_courant[1]] : # On affiche dans l'ordre le nom de chaque boutons correspondant au menu, les uns en dessous des autres
                pyxel.text(coord_x, coord_y + decalage, bouton, 8) # Si le bouton à afficher est celui sur lequel le joueur se trouve, on l'affiche dans une couleur distincte
            else :
                pyxel.text(coord_x, coord_y + decalage, bouton, 2) # Les autres boutons sont affichés dans une couleur plus générique
            decalage = decalage + 13

    def afficher_scores(self) :
        meilleurs_scores = open("scores.txt")
        lignes = meilleurs_scores.readlines()
        index = 0
        for indice in range(1, len(lignes), 2) :
            pyxel.text(32, 72 + index, lignes[indice - 1], 4)
            pyxel.text(75, 72 + index, lignes[indice], 4)
            index = index + 9
        meilleurs_scores.close()
        
            
    def afficher_fond(self, menu_courant) :
        if menu_courant[0] == 'Menu principal' :
            pyxel.blt(0, 0, 1, 0, 0, 120, 200)
            pyxel.text(5, 5, "Joueur(se) :", 8)
            pyxel.text(58, 5, self.pseudo, 8)
            self.game_over = False
            self.victoire = False
            
        if menu_courant[0] == 'Scores' :
            pyxel.blt(0, 0, 2, 0, 0, 120, 200)
            self.afficher_scores()
        
        if menu_courant[0] == 'Options' :
            pyxel.blt(0, 0, 1, 122, 0, 241, 200)
            pyxel.blt(11, 15, 1, 138, 204, 240, 244, 8)
        
        if menu_courant[0] == 'Commandes' :
            pyxel.blt(0, 0, 1, 122, 0, 241, 200)
            commandes_texte = open("commandes.txt")
            commandes = commandes_texte.readlines()
            index = 0
            for ligne in commandes :
                if index == 0 or index == 30 : # Les noms des touches s'affichent en 
                    pyxel.text(10, 30 + index, ligne, 8)
                else :
                    pyxel.text(10, 30 + index, ligne, 4)
                index = index + 10
            
            commandes_texte.close()
        
        if menu_courant[0] == 'Page 0' or menu_courant[0] == 'Page 1' or menu_courant[0] == 'Page 2' :
            pyxel.blt(0, 0, 1, 122, 0, 241, 200)
            regles_texte = open("regles.txt")
            regles = regles_texte.readlines()
            indice = 9 * int(menu_courant[0][-1])
            index = 0
            for ligne in range(indice, indice + 9) :
                pyxel.text(10, 10 + index, regles[ligne], 0)
                index = index + 10
            
            regles_texte.close()
                
            pyxel.text(49, 102, menu_courant[0][:5] + str(int(menu_courant[0][5:]) + 1) , 4)

            if 'Suivant' in self.boutons[menu_courant[0]] :
                pyxel.blt(75, 100, 2, 244, 3, 254, 11, 4)

            if 'Precedent' in self.boutons[menu_courant[0]] :
                pyxel.blt(35, 100, 2, 244, 15, 254, 23, 4)
                
            
        if menu_courant[0] == 'Game_over' :
            pyxel.blt(0, 125, 2, 122, 0, 242, 75, 0)
            pyxel.blt(17, 35, 2, 0, 202, 206, 120, 10) # 'Game Over'
            self.reinitialiser_jeu = True
        
        if menu_courant[0] == 'Victoire' :
            pyxel.blt(0, 125, 2, 122, 0, 242, 75, 0)
            pyxel.blt(15, 50, 2, 141, 79, 233, 141, 0) # Cadre
            pyxel.blt(10, 10, 1, 0, 227, 103, 255, 3) # 'Victoire'
            
            pyxel.text(44 - len(self.pseudo)*1.7, 70, "Bravo " + self.pseudo + " !", 5)
            pyxel.text(80, 88, str(self.score), 9)
                
            self.reinitialiser_jeu = True
        
       
    def draw(self) :
        if self.afficher_menus :
            self.afficher_fond(self.menu_courant)
            if self.menu_courant[0] == 'Menu principal' :
                self.afficher_boutons(self.boutons, self.menu_courant, 49, 120)
            else:
                if self.menu_courant[0] == 'Options' :
                    self.afficher_boutons(self.boutons, self.menu_courant, 49, 148)
                else :
                    self.afficher_boutons(self.boutons, self.menu_courant, 49, 150)
            
            
           
    def update(self) :
        pass
    

    def deplacer(self) :
        if self.afficher_menus :
            bouton_clique = self.boutons[self.menu_courant[0]][self.menu_courant[1]]
            if pyxel.btnp(pyxel.KEY_UP) and self.menu_courant[1] > 0 :
                pyxel.play(0,[6]) # Pour naviguer dans le menu, il ne faut pas que le curseur puisse aller au delà du nombre de boutons, présents dans la dictionnaire
                self.menu_courant[1] = self.menu_courant[1] - 1
                

            if pyxel.btnp(pyxel.KEY_DOWN) and self.menu_courant[1] < len(self.boutons[self.menu_courant[0]]) - 1 :
                pyxel.play(0,[6])
                self.menu_courant[1] = self.menu_courant[1] + 1
                

            if pyxel.btnp(pyxel.KEY_SPACE) : 
                pyxel.play(0,[6])# Lorsque la barre espace est pressée, on regarde le bouton sur lequel le curseur est, et on effectue l'action correspondante
                if bouton_clique == 'Jouer' or bouton_clique == 'Rejouer' :
                    self.afficher_menus = False
                    self.game_over = False
                    self.victoire = False
                
                if bouton_clique == 'Scores' or 'Options' :
                    self.menu_courant[0] = bouton_clique
                    self.menu_courant[1] = 0
                    
                if bouton_clique == 'Retour' or bouton_clique == 'Menu principal' :
                    self.menu_courant[0] = 'Menu principal'
                    self.menu_courant[1] = 0
                    
                if bouton_clique == 'Retour ' :
                    self.menu_courant[0] = 'Options'
                    self.menu_courant[1] = 0
                    
                if bouton_clique == 'Quitter' :
                    pyxel.quit()
                    
                if bouton_clique == 'Changer de pseudo' : # Celui là est le bouton 'Changer de pseudo' du menu de Victoire
                    self.pseudo = input("Entrez votre nouveau pseudo (Max. 9 caractères) : ")
                    pyxel.blt(0, 88, 2, 0, 246, 120, 255)
                    self.menu_courant[0] = 'Game_over'

                if bouton_clique == 'Changer de pseudo ' : # Celui là est le bouton 'Changer de pseudo' du menu des règles
                    self.pseudo = input("Entrez votre nouveau pseudo (Max. 9 caractères) : ")
                    pyxel.blt(0, 88, 2, 0, 246, 120, 255)
                    self.menu_courant[0] = 'Options'
                    
                
                if bouton_clique == 'Regles' :
                    self.page = 0
                    self.menu_courant[0] = 'Page 0'
                    
                if bouton_clique == 'Suivant' :
                    self.page = self.page + 1
                    self.menu_courant[0] = 'Page ' + str(self.page)
                    
                if bouton_clique == 'Precedent' :
                    self.page = self.page - 1
                    self.menu_courant[0] = 'Page ' + str(self.page)