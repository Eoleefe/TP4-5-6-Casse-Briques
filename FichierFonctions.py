"""Fichier de fonctions
Casse brique
Author: William GIRARDET , Gaspard Naessens
Date: October 8-22th 2026
ToDo: Nothing !
"""

def Color2Dico(ListColor):
    D={}
    for i in range(-3,0):
        D[i] = ListColor[i+3]
    for i in range(1,len(ListColor)-2):
            D[i] = ListColor[i+2]
    return D
