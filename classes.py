"""Function file TP4
Casse brique
Author: William GIRARDET
Date: October 8-22th 2026
ToDo: 
    Stocker les vies sous forme de pile
    Stocker les niveaux sous forme de file
    Matrice de briques correspondant à chaque niveau 
        0 --> espace vide
        1 --> brique classique 
        2 et + --> brique renforcée
        -1 --> pouvoir 
        -2 --> brique spéciale (effet)

    Menu : ouvrir une nouvelle fenêtre 
    - Resume
    - Restart current level / game
    - Level select
    - Quit

    Revoir le déplacement 

    "Each frame" :
    - check bar displacement 
    - check ball position 

    Create multiple zones in playing field:
    - bar / dead zone (could be separate or not)
    - empty zone (middle space where nothing happens)
    - game zone (main outline of where the bricks are, actually the brick matrix)
    
    Effects ideas :
    - slowing the platform down for x seconds
    - "speedball" or "fireball", speed the ball up until next rebound
"""


import random   
import tkinter as tk
import FichierFonctions as FF


# Dimensions de la fenêtre de jeu
LARGEUR = 720
HAUTEUR = 480
COULEURS = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6"]
Effect2Color = FF.Color2Dico(COULEURS)

# {1: '#e74c3c', 2: '#e67e22', 3: '#f1c40f',
#  4: '#2ecc71', 5: '#3498db', 6: '#9b59b6'}



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

        self.raquette = Raquette(self.GameWindow)
        self.balle = Balle(self.GameWindow)
        self.menu = Menu(self.GameWindow)

        self.score = 0
        self.jeu_en_cours = True
        self.texte_score = self.GameWindow.create_text(10, 10, anchor="nw", fill="white",
                                                   font=("Arial", 14), text="Score : 0")

        self.touches = set()
        self.bind("<KeyPress-Left>", lambda e: self._touche(e, True))
        self.bind("<KeyPress-Right>", lambda e: self._touche(e, True))
        self.bind("<KeyRelease-Left>", lambda e: self._touche(e, False))
        self.bind("<KeyRelease-Right>", lambda e: self._touche(e, False))
        self.bind("<space>", lambda e: self.rejouer())
        self.bind("<Escape>", lambda e: self.open_menu())
 
        self.boucle()

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


    def boucle(self):
        if self.jeu_en_cours:
            self.raquette.deplacer()
            vivant, rebond = self.balle.deplacer(self.raquette)
            if rebond:
                self.score += 1
                self.balle.dy = max(-8, self.balle.dy * 1.05) # Accélération à chaque rebond jusqu'à deux fois la vitesse initiale
                self.GameWindow.itemconfig(self.texte_score, text=f"Score : {self.score}")

            if not vivant :
                self.fin_de_partie()

        self.after(Delai, self.boucle)

    def fin_de_partie(self):
        self.jeu_en_cours = False

    def rejouer(self):
        self.score = 0
        self.balle.reinitialiser()
        self.en_cours = True

    def open_menu(self):
        self.pause()
        self.menu.menuFrame()
    
    def pause(self):
        if self.jeu_en_cours:
            self.jeu_en_cours = False
        else:
            self.jeu_en_cours = True

    def menu_exit(self):
        self.menu.is_open = False
        self.pause()

    



class Menu:
    def __init__(self,canvas):
        self.GameWindow = canvas
        self.is_open = False
        self.MenuWindow = tk.Frame(self.GameWindow,relief='flat')

    def menuFrame(self):
        if not self.is_open:

            self.is_open = True
            self.MenuWindow.pack()
            tk.Label(self.MenuWindow,text="RDV dentiste samedi a 15h").pack(padx=10,pady=10)
            tk.Button(self.MenuWindow,text="Effacer",fg='navy',command=self.MenuWindow.destroy).pack(padx=10,pady=10)

        

class Raquette:
    def __init__(self, canvas):
        self.canvas = canvas
        self.largeur = 140
        self.hauteur = 16
        self.x = (LARGEUR - self.largeur) / 2
        self.y = HAUTEUR - self.hauteur - 10
        self.vitesse = 10
        self.direction = 0 # -1 gauche, 0 immobile, +1 droite
        self.rect = canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill="white")

    def deplacer(self):
        if self.direction == -1: # Gauche
            if self.x > 0:
                self.x -= self.vitesse
                if self.x < 0: # cas limite pour ne pas sortir de la fenêtre
                    self.x = 0
        elif self.direction == 1: # Droite
            if self.x + self.largeur < LARGEUR:
                self.x += self.vitesse
                if self.x + self.largeur > LARGEUR: # cas limite pour ne pas sortir de la fenêtre
                    self.x = LARGEUR - self.largeur
        # Mise à jour de la position du rectangle dans le caneva
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.largeur, self.y + self.hauteur)


class Brique:
    def __init__(self, x, y, largeur, hauteur, effet, canvas):
        self.x, self.y = x ,y
        self.l, self.h = largeur, hauteur
        self.effet = effet
        self.canvas = canvas

        self.id = canvas.create_rectangle(x, y, x + largeur, y + hauteur,fill = Effect2Color[self.effet])
        self.is_destroyed = False

    def destroy(self):
        self.is_destroyed = True

    def is_destroyed(self):
        return self.is_destroyed

class Balle:
    def __init__(self,canvas):
        self.canevas = canvas
        self.r = 8    # rayon de la balle
        self.id = self.canevas.create_oval(-self.r, -self.r, self.r, self.r, fill = 'white')

        self.reset()

    def reset(self):
        x = LARGEUR / 2
        y = HAUTEUR / 2
        self.canevas.coords(self.id, x - self.r, y - self.r, x + self.r, y + self.r)
        # on utilise la méthode de déplacement dx,dy 
        # avec la fonction "canvas.move(id, dx, dy)" afin de faciliter les calculs
        self.dx = random.choice([-4,4]) # Sens de départ aléatoire gauche/droite
        self.dy = -4

    def deplacer(self,raquette): # -> (vivant,rebond), deux booléens
        self.canevas.move(self.id, self.dx, self.dy)
        x1, y1, x2, y2 = self.canevas.coords(self.id) # Coordonnées de la balle

        # Gestion des rebonds sur les murs

        if x1 <= 0: # rebond gauche
            self.dx = abs(self.dx) # la balle repart à droite (=> dx > 0)
        elif x2 >= LARGEUR: # rebond droit
            self.dx = -abs(self.dx) # la balle repart à gauche (=> dx < 0)
        if y1 <= 0: # rebond haut
            self.dy = abs(self.dy) # la balle repart en bas (=> dy > 0)

        # rebond sur la raquette
        px1, py1, px2, py2 = raquette.canvas.coords(raquette.rect)
        if self.dy > 0 and x2 >= px1 and x1 <= px2 and y2 >= py1 and y1 <= py2:
            self.dy = -abs(self.dy) # rebond bas
            centre_balle = (x1 + x2) / 2
            centre_raquette = (px1 + px2) / 2
            position = (centre_balle - centre_raquette) / (px2 - px1) # postion de la balle relativement à la raquette, -1 -> tout à gauche, 0 -> au milieu, +1 -> tout à droite
            self.dx = position * 6.7 # nombre choisi arbitrairement et correspond à la vitesse du rebond
            return True,True

        # Balle perdue
        if y2 >= HAUTEUR:
            return False,False
        return True,False


Jeu().mainloop()
