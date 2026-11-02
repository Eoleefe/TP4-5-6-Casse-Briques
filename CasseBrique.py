"""Fichier principal
Casse brique
Author: William GIRARDET , Gaspard Naessens
Date: October 8-22th 2026
ToDo: 
"""

from ClassJeu import Jeu
import tkinter as tk
# Dimensions de la fenêtre de jeu
LARGEUR = 720
HAUTEUR = 480

# Vitesse du jeu / FPS
Delai = 16 # 16ms ~ 60 FPS

CasseBrique = Jeu(LARGEUR, HAUTEUR,Delai)
CasseBrique.mainloop()

