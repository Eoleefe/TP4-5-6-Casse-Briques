"""Classe Brique
Casse brique
Author: William GIRARDET , Gaspard Naessens
Date: October 8-22th 2026
ToDo: nothing !
"""

import FichierFonctions as FF
COULEURS = ["#9b59b6", "#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
Effect2Color = FF.Color2Dico(COULEURS)

class Brique:
    def __init__(self, x, y, largeur, hauteur, effet, canvas,k):
        self.x = x
        self.y = y
        self.l = largeur
        self.h = hauteur
        self.k = k
        self.effet = effet # [-3:+inf]
        self.canvas = canvas

        self.couleur = (Effect2Color[self.effet] if self.effet in [-3,-2,-1,1,2,3] else Effect2Color[3])
        self.id = canvas.create_rectangle(x, y, x + largeur, y + hauteur,fill = self.couleur)

    def indice(self):
        return self.k
    
    def detruire(self):
        self.canvas.delete(self.id)
