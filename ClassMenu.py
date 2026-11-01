"""Classe Menu
Casse brique
Author: William GIRARDET
Date: October 8-22th 2026
ToDo: nothing !
"""
import tkinter as tk
from tkinter import messagebox

class Menu:
    def __init__(self,canvas):
        self.GameWindow = canvas
        self.is_open = False

    def InfoListe(self):
        tk.messagebox.showinfo( 'Info',
                                'Liste: gestion des briques\n' \
                                'File: gestion des niveaux\n' \
                                'Pile: gestion des vies')
