


class Bille: #déplace la bille et retourne false si elle tombe
    def __init__(self, canvas, vitesse):
        self.canvas = canvas
        self.rayon = 8
        self.vitesse = vitesse
        self.graph = canvas.create_oval(0, 0, 2*self.rayon, 2*self.rayon, fill ="deepskyblue")

        self.reinitialiser()


    def deplacer(self):
            self.x += self.dx
            self.y += self.dy
            self.dessiner()
    
    def deplacer(self, plateforme):

        self.canvas.deplacement(self.graph, self.dx, self.dy)
        x1, x2, y1, y2 = self.canvas.coords(self.graph)

        #rebonds sur les murs et le plafond
        if x1 <= 0:
            self.dx = abs(self.dx)
        if y1 <= 0:
            self.dy = abs(self.dy)
        elif x2 >= Largeur:
            self.dx = -abs(self.dx)

        #rebond sur la raquette

        px1, py1, px2, py2 = plateforme.coords()
        if x2 >= px1 and x1 <= px2 and y2 >= py1 and y1 <= py2 and self.dy >0:
            self.dy = -abs(self.dy)

            #on ajoute un angle en fonction de là ou la bille touche la plateforme
            centre_bille = (x1 + x2) / 2
            angle = (centre_bille - (px1 + px2) / 2) / ((px2 - px1) / 2)
            self.dx = angle*6
            #on ajoute une accélération pour le confort utilisateur
            self.dy = max(-9, self.dy * 1.03)
            return True, True

    def reinitialiser(self):
                x = Hauteur / 2
                y = Largeur / 2
                self.canvas.coords(self.graph, x - self.rayon, y - self.rayon, x + self.rayon, y + self.rayon)
                self.dx = random.choice([-4, 4])
                self.dy = -4

