"""
detection des clicks
"""
import doctest

def sur_bouton(bouton, click):
    """
    La fonction prend en argument un bouton et l'endroit ou le joueur a
    cliquer et renvoi si le joueur a cliquer sur le bouton.

    Parameters
    ----------
    bouton : Liste
        liste de deux coordonnees.

    click : Liste
        liste de deux coordonnees.

    Returns
    -------
    True ou False.

    >>> sur_bouton([0, 0, 10, 10], [5, 3])
    True
    >>> sur_bouton([0, 0, 10, 10], [12, 5])
    False
    >>> sur_bouton([0, 0, 10, 10], [10, 10])
    True
    """
    top_x = bouton[0]
    top_y = bouton[1]
    bas_x = bouton[2]
    bas_y = bouton[3]
    return top_x <= click[0] <= bas_x and top_y <= click[1] <= bas_y

def trouve_segment(click, infos):
    """
    La fonction prend en parametre un click, la taille des cases 
    du jeu et la taille de la marge.
    
    Parameters
    ----------
    click : Liste
        liste de deux coordonnees.
        
    Returns
    -------
    None : si le click n'es pas pres d'un segment.
    tuple : couple de coordonnes qui represente le sommet selectionne.

    >>> infos = {'case': (50, 50), 'marge': (50, 50)}
    >>> trouve_segment((270, 45), infos)
    ((0, 4), (0, 5))
    >>> trouve_segment((555, 70), infos)
    ((0, 10), (1, 10))
    >>> trouve_segment((45, 130), infos)
    ((1, 0), (2, 0))
    >>> trouve_segment((330, 230), infos)
    
    >>> trouve_segment((330, 405), infos)
    ((7, 5), (7, 6))
    >>> trouve_segment((350, 400), infos)
    
    """
    case = infos['case']
    caseX = case[0]
    caseY = case[1]
    marge = infos['marge']
    margeX = marge[0]
    margeY = marge[1]   
    
    if click[0] < margeX-3 or click[1] < margeY-3:
        return 
    
    dx = (click[0] - margeX)/caseX # position du click en x
    dy = (click[1] - margeY)/caseY # position du click en y
    # sommets correspondant au click
    x = int(dx)
    y = int(dy)
    
    #liste pour etre plus simples a manipuler
    sommet1 = [0, 0]
    sommet2 = [0, 0]   
    
    # click juste au dessus d'un segment horizontal 
    if 0.8 <= dx - x and 0.2 < dy - y < 0.8:
        # on prend le sommet suivant pour les x et on bouge sur l'axe des y
        sommet1[1] = x + 1 
        sommet2[1] = x + 1 
        sommet1[0] = y
        sommet2[0] = y + 1
     
    # click juste en dessous d'un segment horizontal
    elif 0.2 >= dx - x and 0.2 < dy - y < 0.8:
        # on garde le meme sommet pour les x et on bouge sur l'axe des y
        sommet1[1] = x
        sommet2[1] = x
        sommet1[0] = y
        sommet2[0] = y + 1
    
    # click juste devant un segment vertical
    elif 0.8 <= dy - y and 0.2 < dx - x < 0.8:
        # on prend le sommet suivant pour les y et on bouge sur l'axe des x
        sommet1[0] = y + 1
        sommet2[0] = y + 1
        sommet1[1] = x
        sommet2[1] = x + 1
     
    #click juste derrière un segment vertical 
    elif 0.2 >= dy - y and 0.2 < dx - x < 0.8:
        # on garde le meme sommet pour les y et on bouge sur l'axe des x
        sommet1[0] = y
        sommet2[0] = y
        sommet1[1] = x 
        sommet2[1] = x + 1
    else : # click ailleur que sur un segment 
        return 
    return (tuple(sommet1), tuple(sommet2)) 

def mode_solver(boutons, click):
    """
    La fonction determine le mode du solver.
    
    Parameters
    ----------
    boutons : dictionaire
        dictionaire des coordonées des boutons 
    click : Liste
        liste de deux coordonnees.
        
    Returns
    -------
    le mode du solver 
    
    """
    # si le mode rapide existe
    if sur_bouton(boutons['rapide'], click):
        return 'rapide'
    elif sur_bouton(boutons['lent'], click):
        return 'lent'
    elif sur_bouton(boutons['solver'], click):
        return 'solver'
                    
#doctest.testmod(verbose=True)