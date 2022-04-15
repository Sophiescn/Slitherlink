""" 
Fonctions d’accès
"""

import doctest

def ordonne_segment(segment):
    """
    La fonction permet d'ordonner les sommets d'un segment.
    Parameter
    ----------
    sommets : tuple
        couple de couple de coordonees
    Return
    -------
    tuple 
    >>> ordonne_segment(((2, 3), (3, 4)))
    ((2, 3), (3, 4))
    >>> ordonne_segment(((3, 2), (2, 3)))
    ((2, 3), (3, 2))
    """
    if segment[0] < segment[1]:# si les premieres coordonéés sont inferieures au seconde
        return segment
    else : # sinon on retourne le meme segement mais avec les coordonées dans l'autre sens 
        return (segment[1], segment[0])
    
    
def est_trace(etat, segment):
    """
    La fonction permet de verifier si un segment est
    tracé dans le dictionnaire etat.
    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    segment : tuple de tuple
        couple de sommets.
    Return
    -------
    Booleen 
        True si segment est tracé dans etat, et False sinon 
    
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> est_trace(etat, ((1, 1), (2, 1)))
    True
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> est_trace(etat, ((0, 1), (1, 1)))
    False
    >>> est_trace({},((0, 1), (1, 1)))
    False
    """
    segment = ordonne_segment(segment) # on s'assure que les coordonées soient dans le bon ordre
    if segment in etat:
        return etat[segment]== 1 # renvoi True si le segment est bien tracé et False si il est interdit
    return False 

def est_interdit(etat, segment):
    """
    La fonction permet de verifier si un segment est 
    interdit dans le dictionnaire etat.
    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    segment : tuple de tuple
        couple de sommets.
    Return
    -------
    Booleen 
        True si segment est interdit dans etat, et False sinon
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> est_interdit(etat, ((0, 1), (1, 1)))
    True
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> est_interdit(etat, ((1, 1), (2, 1)))
    False
    >>> est_interdit({}, ((1, 1), (2, 1)))
    False
    """
    segment = ordonne_segment(segment)
    if segment in etat:
        return etat[segment]== -1
    return False


def est_vierge(etat, segment):
    """
    La fonction permet de verifier si un segment n'a pas encore de statut.
    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    segment : tuple de tuple
        couple de sommets.
    Return
    -------
    Booleen
        True si segment est vierge dans etat, et False sinon
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> est_vierge(etat, ((0, 1), (1, 1)))
    False
    >>> est_vierge({}, ((0, 1), (1, 1)))
    True
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> est_vierge(etat, ((1, 1), (2, 1)))
    False
    """
    segment = ordonne_segment(segment)
    return segment not in etat # return True si le segment n'est pas défini dans état (il est donc viegre)

def tracer_segment(etat, segment):
    """
    La fonction modifie le dictionnaire etat pour lui 
    ajouter la cle segment egale a 1.   
    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    segment : tuple de tuple
        couple de sommets.
        
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> tracer_segment(etat, ((0, 1), (1, 0)))
    >>> etat
    {((0, 1), (1, 1)): -1, ((1, 1), (2, 1)): 1, ((0, 1), (1, 0)): 1}
    >>> etat = {}
    >>> tracer_segment(etat, ((3, 2), (2, 3)))
    >>> etat
    {((2, 3), (3, 2)): 1}
    """
    segment = ordonne_segment(segment)
    if est_vierge(etat, segment): # on verifie que le segment n'est pas déja tracé
        etat[segment] = 1

def interdire_segment(etat, segment):
    """
    La fonction modifie le dictionnaire etat qu'elle recoit en parametre 
    pour lui ajouter la cle segment egale a -1.   
    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    segment : tuple de tuple
        couple de sommets.
        
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> interdire_segment(etat, ((0, 1), (1, 0)))
    >>> etat
    {((0, 1), (1, 1)): -1, ((1, 1), (2, 1)): 1, ((0, 1), (1, 0)): -1}
    >>> etat = {}
    >>> interdire_segment(etat, ((3, 2), (2, 3)))
    >>> etat
    {((2, 3), (3, 2)): -1}
    """
    segment = ordonne_segment(segment)
    if est_vierge(etat, segment):
        etat[segment] = -1


def effacer_segment(etat, segment):
    """
    La fonction modifie le dictionnaire etat qu'elle recoit en parametre 
    pour y effacer la cle segment.

    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    segment : tuple de tuple
        couple de sommets.

    >>> etat={((0, 1), (1, 1)): -1, ((1, 1), (2, 1)): 1, ((0, 1), (1, 0)): -1}
    >>> effacer_segment(etat, ((0, 1), (1, 0)))
    >>> etat
    {((0, 1), (1, 1)): -1, ((1, 1), (2, 1)): 1}
    """
    segment = ordonne_segment(segment)
    if segment in etat: 
        etat.pop(segment)
    

def segments_traces(etat, sommet):
    """
    La fonction permet de renvoyer la liste des segments trace, adjacents au 
    sommet dans etat.
    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    sommet : tuple
        represente une sommet.

    Returns
    -------
     lst_segment : Liste de tuples de tuples
         represente la liste des segments traces adjacents au sommet
    
    >>> etat = {((0, 1), (1, 1)): 1, ((1, 1), (1, 2)): 1}
    >>> segments_traces(etat, (1, 1))
    [((0, 1), (1, 1)), ((1, 1), (1, 2))]

    >>> etat={((0, 1), (1, 1)): 1, ((1, 1), (1, 2)): 1, ((0, 1), (1, 1)): -1}
    >>> segments_traces(etat, (2, 2))
    []
    """
    lst_segment = []
    
    for segment in etat: # on parcourt tous les segments
        if sommet in segment: # on regarde si le sommet que l'on a appartient au segment 
            if est_trace(etat, segment): 
                lst_segment.append(segment)
    return lst_segment


def segments_interdits(etat, sommet):
    """
    La fonction permet de renvoye une liste de segments interdits, 
    adjacents au sommet dans etat.
    
    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    sommet : tuple
        represente une sommet.

    Return
    -------
    lst_segment : Liste de tuples de tuples
        represente la liste des segments interdits adjacents au sommet
    
    >>> etat = {((0, 1), (1, 1)): 1, ((1, 1), (1, 2)): -1}
    >>> segments_interdits(etat, (1, 1))
    [((1, 1), (1, 2))]

    >>> etat={((0, 1), (1, 1)): 1, ((1, 1), (1, 2)): 1, ((0, 1), (1, 1)): -1}
    >>> segments_interdits(etat, (2, 2))
    []
    """ 
    lst_segment = []
    
    for segment in etat:
        if sommet in segment:
            if est_interdit(etat, segment):
                lst_segment.append(segment)
    return lst_segment


def segments_vierges(etat, sommet):
    """
    La fonction permet de renvoye une liste de segments vierges, adjacents au 
    sommet dans etat.

    Parameters
    ----------
    etat : dictionnaire
        decrit l'etat de la grille.
    sommet : tuple
        represente une sommet.

    Return
    -------
    lst_segments_vierges : Liste de tuples de tuples
        represente la liste des segments vierges adjacents au sommet

    >>> etat = {((0, 1), (1, 1)): 1, ((1, 1), (1, 2)): -1}
    >>> segments_vierges(etat, (1, 1))
    [((1, 0), (1, 1)), ((1, 1), (2, 1))]
    
    >>> segments_vierges({}, (1, 1))
    [((0, 1), (1, 1)), ((1, 0), (1, 1)), ((1, 1), (2, 1)), ((1, 1), (1, 2))]

    """ 
    x, y = sommet
    # cree la liste des segments qui sont etre autour du sommet
    segments_possibles = [((x-1,y),(x,y)), ((x,y-1),(x,y)), ((x,y),(x+1,y)),
                    ((x,y),(x,y+1))]
    segments_vierges = []
    for segment in segments_possibles:
        if est_vierge(etat, segment): # on teste si chaque sommet de la liste est vierge
            segments_vierges.append(segment)
    return segments_vierges

def statut_case(indices, etat, case):
    """
    La fonction permet de renvoyer l'état d'une case.

    Parameters
    ----------
    indices : Liste de liste 
        contient le nombre de segment possible autour une case.
    etat : dictionnaire
        decrit l'etat de la grille.
    case : tuple
        l'emplacement d'une case.

    Returns
    -------
    None : si l'indice est None
    0 : si l'indice de la case est satisfait
    -1 : si l'indice de la case ne peut plus etre satisfait
    1 : si l'indice de la case peut encore etre satisfait

    >>> indices = [[None, None, None, None, 0],[3, 3, None, None, 1]]
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> statut_case(indices,etat,(0, 0))

    
    >>> indices = [[None, None, None, None, 0],[3, None, None, 1, 1]]
    >>> etat = {((1, 3), (1, 4)): 1, ((1,3), (2, 3)): -1, ((0,3), (1,3)): -1}
    >>> statut_case(indices, etat, (1, 3))
    0
    
    >>> indices = [[None, None, None, None, 0],[3, 3, None, None, 1]]
    >>> etat={((0,1), (1, 1)): 1, ((1, 2), (1, 3)): -1, ((2, 3), (2, 4)): -1}
    >>> statut_case(indices, etat, (1, 1))
    1
    
    >>> indices = [[None, None, 2, None, 0],[3, 3, None, None, 1]]
    >>> etat = {((0, 2), (0, 3)): 1, ((0, 3), (1, 3)): 1, ((1, 2), (1, 3)): 1, ((1, 2), (1, 3)): 1}
    >>> statut_case(indices, etat, (0, 2))
    -1
    
    >>> indices = [[None, None, 2, None, 0],[2, 3, None, None, 1]]
    >>> etat = {((1, 0), (1, 1)): -1, ((1, 0), (2, 0)): -1, ((1, 1), (2, 1)): -1, ((2, 0), (2,1)):1}
    >>> statut_case(indices, etat, (1, 0))
    -1
    """
    x, y = case
    indice = indices[x][y] # indice de la case
    
    if indice == None: 
        return None
    #liste des sommets autour de la case
    sommets= [(x, y), (x+1, y), (x+1, y+1), (x, y+1)] 
    # liste des segments autour de la case
    segments_case = [(sommets[0], sommets[1]),
                     (sommets[1], sommets[2]), 
                     (sommets[2], sommets[3]), 
                     (sommets[3], sommets[0])]
    trace = 0
    interdit = 0
    for segment in segments_case:
        # on compte les segments tracés
        if est_trace(etat, segment):
            trace += 1 
        # on compte les segement interdits
        elif est_interdit(etat, segment):
            interdit += 1
    if trace == indice: # autant de segment tracés que l'indice le demande
        return 0
    
    elif interdit == indice and indice == 3:
        return -1
    elif interdit == 3 and indice == 2:
        return -1
    elif trace > indice: # Trop de segment tracés 
        return -1
    else :
        if trace + interdit == 4: # 4 = nombre de segments possibles 
            # on a plus de possibilités autour de la case et elle n'est pas déjà validé
            return -1
        else:
            return 1
        
def segment_vers_coordonees(segment, infos):
    """
    La fonction prend en parametre un segment et les dimensions du jeu et 
    renvoi l'emplacement du segment dans le jeu.
    
    Parameters
    ----------
    segment : tuple de tuple
        couple de sommets.

    Returns
    -------
    tuple de tuple

    >>> infos = {'case': (50, 50), 'marge': (50, 50), 'hauteur': 6, 'largeur': 6}
    >>> segment_vers_coordonees(((0, 4), (0, 5)), infos)
    ((250, 50), (300, 50))
    >>> segment_vers_coordonees(((0, 10), (1, 10)), infos)
    
    >>> segment_vers_coordonees(((1, 0), (2, 0)), infos)
    ((50, 100), (50, 150))
    
    >>> infos = {'case': (43, 133), 'marge': (42, 125), 'hauteur': 2, 'largeur': 10}
    >>> segment_vers_coordonees(((1, 0), (1, 1)), infos)
    ((42, 258), (85, 258))
    """
    taille_case = infos['case']
    taille_marge = infos['marge']
    x_top, y_top = segment[0] # premier sommet
    x_bas, y_bas = segment[1] # deuxieme sommet 
    
    if 0 > x_top or infos['hauteur'] < x_bas or y_top < 0 or infos['largeur'] < y_bas:
        return 
    
    x_top = x_top * taille_case[1] + taille_marge[1]
    y_top = y_top * taille_case[0] + taille_marge[0]
    x_bas = x_bas * taille_case[1] + taille_marge[1]
    y_bas = y_bas * taille_case[0] + taille_marge[0]
    # on inverse car les coordonnées en x des segment correspondent aux
    #coordonnées en y dans la fenetre
    return ((y_top, x_top), (y_bas, x_bas))


def ajoute_segment(jeu, infos, segment, droit):
    """
    La fonction ajoute un segment (tracé ou interdit) avec ses coordonnées
    dans la fenetre.
    
    Parameters
    ----------
    jeu : dictionaire
        dictionaire du jeu 
    infos : dictionaire
        dictionnaire des informations de la grille de jeu
    segment : tuple
        couple de sommets 
    droit : booleen
        True si c'est un on veut interdire False si on veut tracé (click droit)

    Returns
    -------
    couple de listes 
    
    >>> jeu = {'etat': {((0,0), (0,1)): 1, ((0,1), (1,1)): -1}, 'interdit':[((100, 50), (100, 100))], 'tracé': [((50, 50), (100, 50))]}
    >>> infos = {'case': (50, 50), 'marge': (50, 50), 'hauteur': 6, 'largeur': 6}
    >>> ajoute_segment(jeu, infos, ((0,0), (0,1)), False)
    ([((100, 50), (100, 100))], [])
    >>> jeu['etat']
    {((0, 1), (1, 1)): -1}
    """
    # on recupere les valeurs pour les manipuler plus facilement
    interdit = jeu["interdit"]
    trace = jeu['tracé']
    etat = jeu['etat']
    coordonees = segment_vers_coordonees(segment, infos)
    if not coordonees :
        return interdit, trace
    
    if est_vierge(etat, segment) and droit: # click droit + segment vierge
        interdit.append(coordonees)
        interdire_segment(etat, segment)
        
    elif est_vierge(etat, segment) and not droit: # click gauche + segment vierge
        tracer_segment(etat, segment)
        trace.append(coordonees)
    else :
        effacer_segment(etat, segment) # efface le se segment 
        # on le retire des listes de coordonnees
        if coordonees in interdit : 
            interdit.pop(interdit.index(coordonees))
        elif coordonees in trace:
            trace.pop(trace.index(coordonees))
    return interdit, trace
   
def premier_sommet(jeu):
    """
    La fonction determine le premier sommet avec lequel on va tenter de résoudre
    grille.
    
    Parameters
    ----------
    jeu : dictionaire
        dictionaire du jeu 
    Returns
    -------
    couple de sommets 
    
    
    >>> jeu = {'indices': [[None, 2, 3], [1, 1, None]]}
    >>> premier_sommet(jeu)
    ((0, 2), (0, 2))
    >>> jeu = {'indices' : [[1, 2, 1], [None, None, None]]}
    >>> premier_sommet(jeu)
    ((0, 1), (1, 2))
    >>> jeu ={'indices': [[1, 1, 1], [1, None, 1]]}
    >>> premier_sommet(jeu)
    ((0, 0), (1, 1))
    """
    indices = jeu['indices']
    for indice in range(len(indices)):
        if 3 in indices[indice]:
            sommet = (indice, indices[indice].index(3))
            return sommet, sommet
        
    for indice in range(len(indices)):
        if 2 in indices[indice]:
            # sommets opposés 
            sommet1 = (indice, indices[indice].index(2))
            sommet2 = (sommet1[0]+1, sommet1[1]+1)
            return sommet1, sommet2
        
    for indice in range(len(indices)):     
        if 1 in indices[indice]:
            # sommets opposés
            sommet1 = (indice, indices[indice].index(1))
            sommet2 = (sommet1[0]+1, sommet1[1]+1)
            return sommet1, sommet2

     
#doctest.testmod(verbose=True) 