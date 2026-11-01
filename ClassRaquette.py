"""Classe Raaquette
Casse brique
Author: William GIRARDET , Gaspard Naessens
Date: October 8-22th 2026
ToDo: nothing !
"""

class Raquette:
    def __init__(self, canvas, LARGEUR, HAUTEUR):
        self.canvas = canvas
        self.LARGEUR = LARGEUR
        self.HAUTEUR = HAUTEUR

        self.largeur = 140
        self.hauteur = 16
        self.x = (self.LARGEUR - self.largeur) / 2
        self.y = self.HAUTEUR - self.hauteur - 10
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
            if self.x + self.largeur < self.LARGEUR:
                self.x += self.vitesse
                if self.x + self.largeur > self.LARGEUR: # cas limite pour ne pas sortir de la fenêtre
                    self.x = self.LARGEUR - self.largeur
        # Mise à jour de la position du rectangle dans le caneva
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.largeur, self.y + self.hauteur)

    def reset(self):
        self.x = (self.LARGEUR - self.largeur) / 2
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.largeur, self.y + self.hauteur)
