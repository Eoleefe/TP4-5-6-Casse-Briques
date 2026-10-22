
class Liste:
    #on code ici le fonctionnement de la liste, qu'on va utiliser pour les
    #briques, pour pouvoir retirer des briques peu importe si il y en a avant ou après

    def __init__(self):
        self.tete = None
        self.taille = 0

    def ajouter(self, valeur):
        noeud = Noeud(valeur)
        noeud.suivant = self.tete
        self.tete = noeud
        self.taille += 1

    def supprimer(self, valeur):
        precedent, courant = None, self.tete
        while courant is not None:
            if courant.valeur is valeur:
                if precedent is None:
                    self.tete = courant.suivant
                else:
                    precedent.suivant = courant.suivant
                self.taille -= 1
                return True
            precedent, courant = courant, courant.suivant
        return False

    def est_vide(self):
        return self.tete is None

    def __len__(self):
        return self.taille

    def __iter__(self):
        courant = self.tete
        while courant is not None:
            yield courant.valeur
            courant = courant.suivant
