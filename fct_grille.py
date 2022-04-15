"""
Sur la grille de jeu
"""
import doctest
import fct_acces as acces

def doc_vers_grille(nom):
    """
    La fonction prend en parametre un document texte et renvoie 
    une liste de liste

    Parameter
    ----------
    doc : document.txt
        C'est la grille sous forme de document texte.

    Return
    -------
    grille : liste de liste de caractères
        c'est la grille que l'on pourra manipuler.
        
    >>> doc_vers_grille('grille-triviale.txt')
    [['2', '2'], ['2', '2']]
    """
    doc =open (nom, 'r')
    grille = []
    lignes = doc.readlines()
    for ligne in lignes:
        etape = list(ligne) # on cree une liste avec les elements de la ligne
        etape.pop(etape.index('\n'))
        grille.append(etape)
    doc.close()
    return grille
    
def grille_indices(nom):
    """
    La fonction prend en parametre une grille valide et renvoi les valeurs 
    et positions des indices, représentées par une liste de listes d’entiers 

    Parameter
    ----------
    grille : liste de liste de caracteres
        La grille du jeu.

    Return
    -------
    indices : liste de liste d'entiers
        Les valeurs et les positions des indices.
        
    >>> grille_indices('grille-triviale.txt')
    [[2, 2], [2, 2]]

    """
    indices = []
    grille = doc_vers_grille(nom)
    for liste in grille:
        lst = []
        for numero in liste: # on parcourt la grille pour la traduire en liste
            if numero == '_':
                lst.append(None)
            elif numero == '1' or numero == '2' or numero == '3' or numero == '0':
                lst.append(int(numero))
            else:
                return False
        indices.append(lst)
    return indices
    
def couleur_indices(indices, etat):
    """
    La fonction determine la couleur des indices en fonction de leur statut.

    Parameter
    ----------
    indices : liste de liste 
        les indices du jeu.
    etat : dictionaire
        contient des segment et leur état dans la grille.

    Return
    -------
    couleurs_indices : liste de liste de chaine de caractères
        La couleur de chaque indices.
        
    
    >>> indices = [[None, None, 0, 1, None], [3, 2, None, None, None,]]
    >>> etat = {((1, 3), (1, 4)): 1, ((1, 1), (2, 1)): 1, ((2, 1), (2, 2)): 1, ((1, 2), (2, 2)): 1, ((1, 2), (1, 3)): -1}
    >>> couleur_indices(indices, etat)
    [['black', 'black', 'blue', 'blue', 'black'], ['black', 'red', 'black', 'black', 'black']]
    """
    # liste des couleurs 
    couleurs_indices = []
    for i in range(len(indices)): 
        couleurs = []
        for j in range(len(indices[0])):
            # on recupere l'etat de la case pour connaitre sa couleur 
            statut = acces.statut_case(indices, etat, (i,j))
            if statut == 0: # indice satisfait
                couleurs.append('blue')
            elif statut and statut < 0: # statut != None et trop de segments tracés
                couleurs.append('red')
            else:
                couleurs.append('black')
        couleurs_indices.append(couleurs)
    return couleurs_indices


def dimension_fenetre(indices, infos):
    """
    La fonction determine les dimensions des différents elements de la fenetre.

    Parameter
    ----------
    indices : liste de liste 
        les indices du jeu.
    infos : dictionaire
        contient la taille de la grille.

    Return
    -------
    infos : dictionaire
        contient les dimensions des différents elements de la fenetre.
        
    >>> indices = [[2, 2], [2, 2]]
    >>> dimension_fenetre(indices, {'dim fenetre': 515})
    {'dim fenetre': 515, 'hauteur': 2, 'largeur': 2, 'case': [133.0, 133.0], 'marge': [124.0, 124.0]}
    >>> indices = [[2,2], [2,2], [2,2]]
    >>> dimension_fenetre(indices, {'dim fenetre': 515})
    {'dim fenetre': 515, 'hauteur': 3, 'largeur': 2, 'case': [106.0, 133.0], 'marge': [98.0, 124.0]}
    """
    fenetre = infos['dim fenetre']
    hauteur = len(indices)
    largeur = len(indices[0])
    
    if hauteur == largeur: # grille carré
        # [x, y]
        case = fenetre // (hauteur + 24/13)
        case = [case, case]
        marge = case[0] - 5
        # on recupère la difference entre la taille de la fenetre et la somme des cases et de la marge
        a = fenetre - (case[0] * hauteur + marge * 2)
        if a < 0:
            # difference négative donc on doit réduire la marge 
            marge += a//2 # + un a négatif
        elif a > 0:
            # difference positive donc on doit agrandire la marge
            marge += a//2 # + un a positif
        # [x, y]
        marge = [marge, marge]
        
    else:
        case = [fenetre // (largeur + 24/13), fenetre // (hauteur + 24/13)]
        marge = [case[0] - 5, case[1] - 5]

        a = fenetre - (case[0] * largeur + marge[0] * 2) # difference en x
        b = fenetre - (case[1] * hauteur + marge[1] * 2) # différence en y
        if a < 0:
            marge[0] += a//2
        elif a > 0:
            marge[0] += a//2
        if b < 0:
            marge[1] += b//2
        elif b > 0:
            marge[1] += b//2
            
            
    infos['hauteur'] = hauteur
    infos['largeur'] = largeur
    infos['case'] = case
    infos['marge'] = marge
    return infos

#doctest.testmod(verbose=True)