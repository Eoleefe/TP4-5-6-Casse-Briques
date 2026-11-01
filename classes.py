"""Fichier classe Jeu
Casse brique
Author: William GIRARDET , Gaspard Naessens
Date: October 8-22th 2026
ToDo: 
    Stocker les vies sous forme de pile XXX
    Stocker les niveaux sous forme de file
    Matrice de briques correspondant à chaque niveau XXX
        0 --> espace vide XXX
        1 --> brique classique XXX
        2 et + --> brique renforcée 
        -1 --> pouvoir 
        -2 --> brique spéciale (effet)

    Menu : ouvrir une nouvelle fenêtre XXX
    - Resume
    - Restart current level / game
    - Level select
    - Quit
    
    Effects ideas :
    - slowing the platform down for x seconds
    - "speedball" or "fireball", speed the ball up until next rebound

    Global optimizations :
    - do not redo something multiple time (initialization + init function = not optimal)
"""

import numpy as np
import tkinter as tk
import FichierFonctions as FF

from ClassMenu import Menu
from ClassRaquette import Raquette
from ClassBalle import Balle
from ClassBrique import Brique


# Dimensions de la fenêtre de jeu
LARGEUR = 720
HAUTEUR = 480

# -3: Effet à faire
# -2: Effet à faire
# -1: Effet à faire
#  1: Brique neutre
#  2: Brique x2 (double durabilité)
#  3: Brique x3 (ou xN, N > 3, brique à N durabilité)

# Vitesse du jeu / FPS
Delai = 16 # 16ms ~ 60 FPS

class Jeu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Casse brique")
        self.resizable(False, False)

        self.GameWindow = tk.Canvas(self, width=LARGEUR, height=HAUTEUR,
                                bg="black", highlightthickness=0)
        self.GameWindow.pack()

        self.raquette = Raquette(self.GameWindow,LARGEUR,HAUTEUR)
        self.balle = Balle(self.GameWindow,LARGEUR,HAUTEUR)
        self.menu = Menu(self.GameWindow)
        self.ListeBriques = [] 

        self.score = 0
        self.vies = "\u2665 \u2665 \u2665"
        self.jeu_en_cours = False
        self.fin_partie = False
        self.difficulty = 1
        self.message("Espace pour démarrer\nEchappe pour mettre en pause")
        self.texte_score = self.GameWindow.create_text(10, 10, anchor="nw", fill="white",
                                                   font=("Arial", 14), text="Score : 0")
        self.texte_vies = self.GameWindow.create_text(LARGEUR -10, 10, anchor="ne",
                                                        fill="white",font=("Arial", 14),
                                                        text=f"Vies : {self.vies}")
        self.texte_Niveaux = self.GameWindow.create_text(LARGEUR / 2, 10, anchor="n",
                                                        fill="white",font=("Arial", 14),
                                                        text=f"Niveaux {self.difficulty}")

        self.touches = set()
        self.bind("<KeyPress-Left>", lambda e: self._touche(e, True))
        self.bind("<KeyPress-Right>", lambda e: self._touche(e, True))
        self.bind("<KeyRelease-Left>", lambda e: self._touche(e, False))
        self.bind("<KeyRelease-Right>", lambda e: self._touche(e, False))
        self.bind("<r>", lambda e: self.rejouer())
        self.bind("<space>", lambda e: self.START())
        self.bind("<Escape>", lambda e: self.pause())
        self.bind("<k>", lambda e: self.niveau_suivant()) # For devs only

        self.Niveaux=self.File2Niveau()
        self.Aire2Jeu(self.Niveau0())

        self.CreateMenu()
        self.boucle()

    def START(self):
        if self.jeu_en_cours == False and self.fin_partie == False:
            self.effacer_message()
            self.jeu_en_cours = True

    def message(self, texte):
        self.effacer_message()
        self.GameWindow.create_text(LARGEUR / 2, HAUTEUR / 1.9, fill="white", tag="msg",
                                font=("Arial", 18, "bold"), text=texte, justify="center")

    def effacer_message(self):
        self.GameWindow.delete("msg")

    def _touche(self, event, pressed):
        if pressed:
            self.touches.add(event.keysym)
        else:
            self.touches.discard(event.keysym)
        # touches est une liste pouvant contenir "Left" et "Right"
        # Si "Right" est présent celà signifie que la flèche de droite est active, idem pour "Left"
        # Dès lors que la touche est relachée, "Right" (ou "Left") disparaît de la liste
        gauche = "Left" in self.touches
        droite = "Right" in self.touches
        self.raquette.direction = (1 if droite else 0) - (1 if gauche else 0)

    def Degats(self):
        vies = self.vies.split(" ")
        vies.pop() # on enlève l'élément du dessus
        ViesAJour = vies[0] # puis on reconstruit la pile par le bas
        vies.pop(0)
        for Coeur in vies:
            ViesAJour += " " + Coeur
        self.vies = ViesAJour
  
    def boucle(self):
        if self.jeu_en_cours:
            dscore = 0
            self.raquette.deplacer()
            vivant, rebond = self.balle.deplacer(self.raquette)

            if rebond :
                dscore += 1
                self.balle.dy = max(-8, self.balle.dy * 1.05) # Accélération à chaque rebond jusqu'à deux fois la vitesse initiale


            if not vivant :
                self.jeu_en_cours = False
                if len(self.vies) > 1:
                    self.go_again()
                else:
                    self.vies = ""
                    self.fin_de_partie()

            Collision = None
            # deviens la brique touchée lors d'une collision

            for brique in self.ListeBriques:
                if brique != 0 and self.balle.rebond_brique(brique):
                    Collision=brique
                    break   # collision détectée donc pas besoin de vérifier les autres briques 
                            # (on évite aussi le risque de supprimer plusieurs briques à la fois)

            if Collision is not None:
                dscore += 10
                self.ListeBriques[Collision.indice()]=0
                Collision.detruire()
                if self.CheckList():
                    self.niveau_suivant()

            
            if dscore != 0:
                self.score += dscore
                self.GameWindow.itemconfig(self.texte_score, text=f"Score : {self.score}")

        self.after(Delai, self.boucle)

    def niveau_suivant(self):
        if len(self.Niveaux) >= 1:
            self.difficulty += 1
            self.Niveaux.pop(0)
        else:
            self.Victoire()
        self.refresh_balle()

        self.message("Espace pour jouer")
        self.vies = "\u2665 \u2665 \u2665"
        self.ResetlistBriques()
        self.Aire2Jeu(self.Niveaux[0])

    def Victoire(self):
        self.fin_partie = True
        self.jeu_en_cours = False
        self.message(f"Victoire !\nScore final : {self.score}\nAppuier sur R pour rejouer")

    def CheckList(self):
        for i in self.ListeBriques:
            if i != 0:
                return False
        return True
                
    def fin_de_partie(self):
        self.fin_partie = True
        self.jeu_en_cours = False
        self.message("Perdu !\nAppuier sur R pour rejouer")

    def debut_de_jeu(self):
        if self.fin_partie == True:
            self.fin_partie = False
            self.refresh_balle()
            
            self.score = 0
            self.vies = "\u2665 \u2665 \u2665"
            self.difficulty = 0
            self.ResetlistBriques()
            self.Niveaux=self.File2Niveau()
            self.Aire2Jeu(self.Niveaux[0])
            self.message("Espace pour démarrer\nEchappe pour mettre en pause")

    def refresh_balle(self):
        self.jeu_en_cours = False
        self.balle.reset()
        self.raquette.reset()
        self.GameWindow.itemconfig(self.texte_score, text=f"Score : {self.score}")
        self.GameWindow.itemconfig(self.texte_vies, text=f"Vies : {self.vies}")
        self.GameWindow.itemconfig(self.texte_Niveaux, text=f"Niveau : {self.difficulty}")

    def FullReset(self):
        self.fin_partie = True
        self.debut_de_jeu()
        
    def rejouer(self):
        if self.fin_partie == True:
            self.debut_de_jeu()

    def go_again(self):
            self.refresh_balle()
            self.effacer_message()
            self.Degats()
            self.message("Espace pour démarrer")

    def pause(self):
        if self.jeu_en_cours:
            self.message("Pause")
            self.jeu_en_cours = False
        else:
            self.effacer_message()
            if not self.fin_partie:
                self.jeu_en_cours = True

    def CreateMenu(self):
        self.menubar = tk.Menu(self.GameWindow)

        OptionMenu = tk.Menu(self.menubar, tearoff=0)
        OptionMenu.add_command(label="Pause/Reprendre", command=self.pause)
        OptionMenu.add_command(label="Rejouer", command=self.FullReset)
        OptionMenu.add_separator()
        OptionMenu.add_command(label="Quitter", command=self.destroy)
        self.menubar.add_cascade(label="Manu le menu", menu=OptionMenu)

        InfoMenu = tk.Menu(self.menubar, tearoff=0)
        InfoMenu.add_command(label="Liste, Pile, File", command=self.menu.InfoListe)
        # InfoMenu.add_command(label="", command=None)
        self.menubar.add_cascade(label="Info", menu=InfoMenu)
        
        self.config(menu=self.menubar)

    def Niveau0(self):
        Niveau = np.zeros((5,3))
        Niveau[1][1] = 1
        Niveau[3][1] = 1
        return Niveau

    def Niveau1(self):
        Niveau = np.ones((9,5))
        return Niveau

    def Niveau2(self):
        size = (9,5)
        Niveau = np.ones(size)
        k = 0
        for i in range(size[0]):
            for j in range(size[1]):
                if k % 2 == 0:
                    Niveau[i][j] = 2
                else:
                    Niveau[i][j] = 0
                k += 1
        return Niveau

    def Niveau3(self):
            size = (9,5)
            Niveau = np.ones(size)
            k = 0
            for i in range(size[0]):
                for j in range(size[1]):
                    if k % 2 == 0:
                        Niveau[i][j] = 3
                    else:
                        Niveau[i][j] = 1
                    k += 1
            return Niveau

    def Niveau4(self):
            size = (9,6)
            Niveau = np.ones(size)
            for i in range(size[0]):
                for j in range(size[1]):
                    n = j - 3
                    if n < 0 :
                        Niveau[i][j] = n
                    else:
                        Niveau[i][j] = n + 1

            return Niveau

    def File2Niveau(self):
        File=[]
        File.append(self.Niveau0())  # XXX test dev
        File.append(self.Niveau1())
        File.append(self.Niveau2())
        File.append(self.Niveau3())
        File.append(self.Niveau4())
        return File

    def ResetlistBriques(self):
        for brique in self.ListeBriques:
            if brique != 0 :
                brique.detruire()
        self.ListeBriques = []
        
    def Aire2Jeu(self,Niveau):
        """
        
        """
        Nx, Ny = np.size(Niveau, 0), np.size(Niveau, 1)
        k = 0
        for i in range(Nx):
            for j in range(Ny):
                effet = Niveau[i][j]
                if effet != 0 and effet >= -3:
                    x , y = 20 + (LARGEUR - 40) / Nx * i , 40 + j * 24
                    l , h = (LARGEUR - 40) / Nx - 4, 20
                    # On laisse 4 pixels entre chaque briques pour aérer l'aire de jeu
                    
                    self.ListeBriques.append(Brique(x,y,l,h,effet,self.GameWindow,k))
                    k += 1

Jeu().mainloop()
