"""
conditions de victoire
"""
import doctest
import fct_acces as acces


def indices_satisfaits(indices, etat):
    """
    La fonction verifie que si les indices des cases sont satisfaits.

    Parameters
    ----------
    indices : Liste de liste 
        contient le nombre de segment possible autour une case.
    etat : dictionnaire
        decrit l'etat de la grille.
    Returns
    -------
    Booleen : True si tous lesindices sont satisfait, False sinon.
    
    >>> indices = [[None, None, 1], [2, None, None]]
    >>> etat = {((0, 2), (0, 3)): 1, ((1, 0), (1, 1)): 1, ((1, 1), (2, 1)): 1}
    >>> indices_satisfaits(indices, etat)
    indices satisfaits
    True
    
    >>> indices = [[None, None, 1], [2, None, None]]
    >>> etat = {}
    >>> indices_satisfaits(indices, etat)
    indices non satisfaits
    False
    
    >>> indices = [[1, None, 1], [None, None, None]]
    >>> etat = {((0, 1), (1, 1)): 1, ((0, 2), (1, 2)): -1}
    >>> indices_satisfaits(indices, etat)
    indices non satisfaits
    False
    """
    # on parcourt tous les indices
    for x in range(len(indices)):
        for y in range(len(indices[x])):
            if indices[x][y]: # indice != None
                statut = acces.statut_case(indices, etat, (x, y))
                if statut == -1 or statut == 1: # trop de segment ou pas assez
                    print('indices non satisfaits')
                    return False
    print('indices satisfaits')
    return True

def longueur_boucle(etat, segment):
    """
    La fonction renvoit le nombre de segment parcourut si elle a effectuer une boucle
    et None sinon.

    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    sommets : tuple
        couple de couple de coordonees

    Returns
    -------
    entier : si la la fonction a fait une boucle,
    None : sinon.

    >>> etat = {((3, 3), (3, 4)):1, ((2,3), (3,3)): 1, ((2,3), (2,4)): 1, ((2,4), (3,4)): 1}
    >>> longueur_boucle(etat, ((3, 3), (3, 4)))
    est une boucle unique
    4
    >>> etat = {((2, 1), (2, 2)): 1, ((1,1), (2,1)): 1, ((0, 2), (1, 2)): 1}
    >>> longueur_boucle(etat, ((2, 1), (2, 2)))
    n'est pas une boucle unique
    >>> etat = {((0,0), (1,0)): 1, ((0,0), (0,1)): -1, ((1,0),(1,1)): 1}
    >>> longueur_boucle(etat, ((0,0), (1,0)))
    n'est pas une boucle unique
    >>> etat = {((0,0), (1,0)): 1, ((1,0),(1,1)): 1}
    >>> longueur_boucle(etat, ((0,0), (1,0)))
    n'est pas une boucle unique
    >>> etat = {((2, 1), (2, 2)): 1, ((1,1), (2,1)): 1, ((2,1), (3,1)): 1}
    >>> longueur_boucle(etat, ((2, 1), (2, 2)))
    n'est pas une boucle unique
    """
    depart = segment[1] # sommet de depart (arbitraire)
    precedent = depart 
    courant = segment[0] # l'autre sommet de segment 
    cmpt = 1
    # on regarde s'il y a plus ou moins de 2 segment tracés
    if len(acces.segments_traces(etat, depart)) != 2: 
        print("n'est pas une boucle unique")
        return 
    
    while True:
        segments = acces.segments_traces(etat, courant)
        if len(segments) != 2: # meme chose que precedement 
            print("n'est pas une boucle unique")
            return None
        
        # ici on a bien deux segments dans la liste segments et on les recupere
        segment1 = segments[0]
        segment2 = segments[1]
        
        # le sommet precedent n'est pas dans le segment1
        if precedent not in segment1: 
            precedent = courant # on se decale
            
            # si le segment courant est le meme que le premier sommet de segment1
            if courant == segment1[0]: 
                courant = segment1[1] 
            else :
                courant = segment1[0]
        else :
            precedent = courant
            if courant == segment2[0]:
                courant = segment2[1] 
            else :
                courant = segment2[0]
        cmpt += 1
        if depart == courant: # on est revenu au point de depart
            print("est une boucle unique")
            return cmpt 
        
def partie_gagnee(jeu):
    """
    La fonction vérifie si une partie est gagnée

    Parameters
    ----------
    jeu : dictionnaire
        dictionaire du jeu.

    Returns
    -------
    True si la partie est gagnée
    False sinon
    
    
    >>> indices = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, 3, 3]]
    >>> etat = {((3, 3), (3, 4)):1, ((2,3), (3,3)): 1, ((2,3), (2,4)): 1, ((2, 4), (2, 5)): 1, ((2, 5), (3, 5)): 1, ((3, 4), (3, 5)): 1}
    >>> jeu = {'etat': etat, 'indices': indices}
    >>> partie_gagnee(jeu)
    indices satisfaits
    est une boucle unique
    True
    
    >>> indices = [[None, None, None, None, 1], [None, None, None, None, None], [None, None, None, None, None]]
    >>> jeu = {'etat': {((0, 4), (0, 5)): 1}, 'indices': indices}
    >>> partie_gagnee(jeu)
    indices satisfaits
    n'est pas une boucle unique
    False
    
    >>> indices = [[None, None, None, None, None], [None, None, None, None, None], [None, None, None, 3, 3]]
    >>> jeu = {'etat': {}, 'indices': indices}
    >>> partie_gagnee(jeu)
    indices non satisfaits
    False
    """
    if not indices_satisfaits(jeu['indices'], jeu['etat']):
        return False
    nb_segments = 0
    etat = jeu['etat']
    for segment in etat:
        if etat[segment] == 1:
            nb_segments += 1
    if longueur_boucle(jeu['etat'], segment) == nb_segments:
        return True
    return False
        
#doctest.testmod(verbose= True)