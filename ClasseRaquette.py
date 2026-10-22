







class Raquette: #définition de la raquette, ce  qu'on fait bouger pour jouer au jeu

    def __init__(self, canvas,):
        self.canvas = canvas
        self.largeur = 90
        self.hauteur = 12
        self.vitesse = 8
        self.x = (Largeur - self.largeur) / 2
        self.y = Hauteur - 40
        self.graph = canvas.create_rectangle(0, 0, 0, 0, fill = "#e74c3c") #on la construit en position nulle, on la place après
        self.placement()

    def placement(self): #on place la raquette qui était en position nulle à la bonne position
        self.canvas.coords(self.graph, self.x, self.y, self.x + self.largeur, self.y + self.hauteur)
    
    def deplacer(self, input):
        if "Gauche" in input:
            self.x -= self.vitesse
        if "Droite" in input:
            self.x += self.vitesse
        self.x = max(0, min(Largeur-self.largeur, self.x)) #on bloque la raquette dans l'espace de jeu
        self.placement() #on replace la raquette à sa nouvelle position 
