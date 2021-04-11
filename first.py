

from __future__ import division, absolute_import
from tkinter import Canvas, Button, Scale,  Tk
from random import random
import tkinter


class App():
    """
    La classe principale de l'application.
    """

    def __init__(self, grille_taille=700):

        # Initialiser la taille de grille et de la fenetre
        self.grille_taille = grille_taille
        self.width = self.grille_taille + 150
        self.height = self.grille_taille

        # Initaliser la valeur par défault des 3 barres de définement, d'autres propriétés
        self.est_boucle_arret = True
        self.grille_taille_en_cellule = 30
        self.cellule_taille = self.grille_taille / self.grille_taille_en_cellule
        self.vitesse = 100  # en milliseconde
        self.p_en_vie = 0.2
        self.etat = []

        # La racine de l'application
        self.racine = Tk()
        self.racine.title("SR01 Jeu de la vie")
        self.racine.resizable(False, False)

        # Initialiser la grille et le controleur
        self.init_grille()
        self.init_controleur()

    def init_grille(self):
        """
        Initialiser l'interface de la grille.
        """

        # La disposition de la grille
        self.grille = Canvas(self.racine, width=self.grille_taille,
                             height=self.grille_taille, background='white')
        self.grille.pack(side=tkinter.LEFT)
        # self.grille.grid(row=0, column=0)

    def init_controleur(self):
        """
        Initialiser l'interface de la controleur.
        """

        # Les boutons du controleur avec ses fonctions correspodantes de l'app
        boutons = [('Initialiser', self.initialiser), ('Lancer', self.lancer),
                   ('Arreter', self.arreter), ('Quitter', self.quitter)]
        self.boutons = [Button(self.racine, text=texte, command=commande, width=15, font=10)
                        for (texte, commande) in boutons]

        # Les barres de définement du controleur de type liste (type, étiquette)
        barres = ("grille_taille_en_cellule", "Taille de la grille"), \
            ("p_en_vie", "% de vie"), ("vitesse", "Vitesse")
        self.barres = {type_barre: Scale(self.racine, from_=1, to=100, orient='horizontal',
                                         width=15, length=150, label=etiquette)
                       for type_barre, etiquette in barres}

        # Initialiser les 3 barres de définement
        self.barres['grille_taille_en_cellule'].set(self.grille_taille_en_cellule)
        self.barres['p_en_vie'].set(self.p_en_vie * 100)
        self.barres['vitesse'].set(self.vitesse / 1000)

        # Attache les 3 premiers boutons Lancer, Arreter et Initialiser en haut
        for bouton in self.boutons[:-1]:
            bouton.pack(side=tkinter.TOP)

        # Attache le bouton Quitter en bas
        self.boutons[-1].pack(side=tkinter.BOTTOM)

        # Attache les 3 barres en bas
        for barre in reversed(self.barres.values()):
            barre.pack(side=tkinter.BOTTOM)

        # Mettre la fonction self.quitter à supprimer la fenetre de l'application (quitter l'app)
        self.racine.protocol("WM_DELETE_WINDOW", self.quitter)

    def arreter(self):
        """
        La fonction du bouton « Arreter ».
        """

        self.est_boucle_arret = True

    def initialiser(self):
        """
        La fonction du bouton « Initialiser ».
        """

        # Arrêter l'app avant d'initialiser
        self.arreter()

        # Obtenir les valeurs des barres de définement
        self.grille_taille_en_cellule = int(self.barres['grille_taille_en_cellule'].get())
        self.cellule_taille = self.grille_taille/self.grille_taille_en_cellule
        self.p_en_vie = self.barres['p_en_vie'].get() / 100

        # Initaliser des cellules de la grille
        self.etat = [[random() < self.p_en_vie for _ in range(self.grille_taille_en_cellule)]
                     for _ in range(self.grille_taille_en_cellule)]

        # Dessiner la grille utilisant l'attribute self.etat
        self.dessier_grille()

    def dessier_grille(self):
        """
        Dessiner la grille utilisant la couleur rouge pour des cellules en vie et
        la couleur blanc pour des cellules mortes.
        """

        # Considérer toutes les cellules de la grille à dessiner
        for i in range(self.grille_taille_en_cellule):
            for j in range(self.grille_taille_en_cellule):
                rectangle = [i*self.cellule_taille, j * self.cellule_taille,
                             (i+1) * self.cellule_taille, (j+1)*self.cellule_taille]
                couleur = "red" if self.etat[i][j] else "white"
                self.grille.create_rectangle(*rectangle, fill=couleur)

    def lancer(self):
        """
        La fonction du bouton « Lancer ».
        """

        # Si l'utilisateur lance ou arrete avant d'initialiser, rien se passe
        if not self.etat:
            return

        if self.est_boucle_arret:
            self.est_boucle_arret = False
            self.periodique_mis_a_jour()

    def periodique_mis_a_jour(self):
        """
        Mis à jour la grille utilisant la fonction mis_a_jour après d'une durée spécifique
        qui est calculée à partir de la vitesse.
        """

        if self.est_boucle_arret:
            return

        self.mis_a_jour()

        # Obtenir la vitesse de la barre de définement et calculer la durée delta_t
        vitesse = self.barres["vitesse"].get()
        delta_t = 100 + vitesse * 10
        delta_t = int(delta_t)
        self.grille.after(delta_t, self.periodique_mis_a_jour)

    def mis_a_jour(self):
        """
        Mis à jour la grille en dessinant des cellules en vie.
        """

        # Contenir toutes les coordinées des cellules qui ont besoin de changer l'état
        cellule_changer_etat = []

        # Considerer toutes les cellules de la grille à trouver les cellules ayant besoin de changer
        for i in range(self.grille_taille_en_cellule):
            for j in range(self.grille_taille_en_cellule):
                est_en_vie = self.etat[i][j]

                # Le nombre des cellules voisins de la cellule considérée (8 totalement)
                cellule_voisin = [(i-1, j-1), (i-1, j), (j-1, j+1), (i, j-1),
                                  (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]

                # Le nombre des cellules voisins en vie de la cellule considérée
                nb_en_vie_voisin = sum([self.etat[i][j]
                                        if 0 <= i < self.grille_taille_en_cellule
                                        and 0 <= j < self.grille_taille_en_cellule
                                        else 0
                                        for i, j in cellule_voisin])

                # La cellule est en vie et le nombre de voisin en vie < 2 => Changer l'état à vide
                desertification = est_en_vie and nb_en_vie_voisin < 2
                # La cellule est en vie + le nombre de voisin en vie < 3 => Changer l'état à vide
                surpopulation = est_en_vie and nb_en_vie_voisin > 3
                # La cellule n'est pas en vie + le nombre de voisin en vie = 3 => Changer l'état occupé
                naissance = not est_en_vie and nb_en_vie_voisin == 3

                if desertification or surpopulation or naissance:
                    cellule_changer_etat.append([i, j])

        # Changer l'état des cellules dans la variable cellule_changer_etat
        for i, j in cellule_changer_etat:
            self.etat[i][j] = not self.etat[i][j]

        # Mis à jour la grille
        self.dessier_grille()

    def quitter(self):
        """
        La fonction du bouton « Quitter ».
        """
        self.arreter()
        self.racine.destroy()


# Exécuter l'application
if __name__ == "__main__":
    app = App()
    app.racine.mainloop()
