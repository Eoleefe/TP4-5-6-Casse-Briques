

import




class Brique: #définition de la brique, le rectangle qui sera détruit par la balle

    def __init__(self, canvas, x, y, largeur, hauteur, couleur, points):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.points = points
        self.canvas = canvas
        self.graph = canvas.create_rectangle(x, y, x + largeur, y + hauteur, fill=couleur)

    def supprimer(self): #sera utilisé pour supprimer la brique lorsqu'elle est touchée par la balle
        self.canvas.delete(self.graph)
