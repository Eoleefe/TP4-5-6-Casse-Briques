"""Classe Balle
Casse brique
Author: William GIRARDET , Gaspard Naessens
Date: October 8-22th 2026
ToDo: nothing !
"""

import random

class Balle:
    def __init__(self,canvas,LARGEUR,HAUTEUR):
        self.canevas = canvas
        self.HAUTEUR = HAUTEUR
        self.LARGEUR = LARGEUR
        self.r = 8    # rayon de la balle
        self.id = self.canevas.create_oval(-self.r, -self.r, self.r, self.r, fill = 'white')

        self.reset()

    def reset(self):
        x = self.LARGEUR / 2
        y = self.HAUTEUR / 1.5
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
        elif x2 >= self.LARGEUR: # rebond droit
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
        if y2 >= self.HAUTEUR:
            return False,False
        return True,False

    def rebond_brique(self,brique):
        x1, y1, x2, y2 = self.canevas.coords(self.id)
        gauche, droite = x1, x2
        haut, bas = y1, y2 # Coordonnées des côtés de la balle
        x, y, l ,h = brique.x, brique.y, brique.l, brique.h # Coordonnées de la brique

        if droite < x or gauche > x + l or bas < y or haut > y + h :
            return False # Balle en dehors de la brique

        PtX = min(droite - x, x + l - gauche) # Pénétration dans la brique selon x
        PtY = min(bas - y, y + h - haut) # Pénétration dans la brique selon y

        if PtX < PtY :
            self.dx = -self.dx
        else:
            self.dy = -self.dy

        return True
