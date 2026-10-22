



class Noeud:
    #Maillon de base : une valeur + un lien vers le maillon suivant

    def __init__(self, valeur):
        self.valeur = valeur
        self.suivant = None
