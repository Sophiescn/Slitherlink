"""
fonction d'affichage
"""
import fltk
import fct_grille as grille
import fct_acces as acces
import fct_clicks as clicks
import fct_menu as menu 
import fct_grille 

def affiche_segment(lst_traces):
    """
    La fonction permet de dessiner les segment entre deux sommets.
    
    Parameter
    ----------
    lst_trace : liste 
        liste des segments a tracé à l'ecrant.

    Return
    -------
    None
        
    """
    for segment in lst_traces:
        x_top, y_top = segment[0] # premier sommet 
        x_bas, y_bas = segment[1] # deuxieme sommet 
        fltk.ligne(x_top, y_top, x_bas, y_bas, epaisseur = 3)

    
def affiche_segment_barre(lst_interdits):
    """
    La fonction permet de dessiner les crois entre deux sommet pour les 
    segments interdits.
    
    Parameter
    ----------
    lst_trace : liste 
        liste des segments a interdits à l'ecrant.

    Return
    -------
    None
    
    """
    for segment in lst_interdits:
        x_top, y_top = segment[0] # premier sommet 
        x_bas, y_bas = segment[1] # deuxieme sommet 
        # centre du segment 
        x_milieu = (x_top + x_bas)/2 
        y_milieu = (y_top + y_bas)/2
        # deux traits qui forment la croi
        fltk.ligne(x_milieu - 3, y_milieu - 3, 
               x_milieu + 3, y_milieu + 3, couleur='red')
        fltk.ligne(x_milieu - 3, y_milieu + 3,
               x_milieu + 3, y_milieu - 3, couleur='red')
        
        
def affiche_grille(infos):
    """
    La fonction dessine la grille de points à partir d'un dictionnaire dans
    lequel sont mis les informations concernant les dimensions.
    
    Parameter
    ----------
    infos : dictionaire  
        dictionaire de la taille des éléments du jeu.

    Return
    -------
    None
    """
    case = infos['case']
    caseX = case[0]
    caseY = case[1]
    marge = infos['marge']
    margeX = marge[0]
    margeY = marge[1]
    
    x = margeX # on se décale de la valeur de la marge
    y = margeY
    for i in range(infos['hauteur']+1): # le nombre de sommets en hauteur
        for j in range(infos['largeur']+1): # le nombre de sommets en largeur
            fltk.cercle(x, y, 3, remplissage='black')
            x += caseX # on rajoute la taille d'une case
        # pour la ligne suivante on initialise x a la taille de la large
        x = margeX
        y += caseY # on ajoute une case puisqu'on descend

def affiche_indices(jeu, infos, etat):
    """
    La fonction va afficher les indices de la bonne couleur, 
    elle va appeler la fonction couleur_indices pour obtenir la liste
    des couleurs et va dessiner tous les indices différents de None.
    
    Parameter
    ----------
    jeu : dictionaire
        dictionaire du jeu 
    infos : dictionaire
        dictionnaire des informations de la grille de jeu
    etat : dictionaire
        dictionaire de l'etat des segments
        
    Return
    -------
    None
    """
    taille_case = infos['case']
    taille_marge = infos['marge']
    couleurs = fct_grille.couleur_indices(jeu['indices'], etat)
    
    y = taille_marge[1] + taille_case[1]//2 # on se place au centre de la case (0,0)
    i=0
    for lst_indices in jeu['indices']:
        x = taille_marge[0] + taille_case[0]//2 # on se place au centre de la case 
        j = 0
        for indice in lst_indices:
            if indice != None:
                couleur = couleurs[i][j]
                fltk.texte(x, y, str(indice), couleur=couleur, ancrage='center', taille= 30)
            x += taille_case[0]
            j += 1
        y += taille_case[1]
        i+=1
        
def affiche_indices_prop(jeu, infos, etat):
    """
    La fonction va afficher les indices de la bonne couleur, 
    elle va appeler la fonction couleur_indices pour obtenir la liste
    des couleurs et va dessiner tous les indices différents de None avec une 
    taille proportionelle a celle de la grille.
    
    Parameter
    ----------
    jeu : dictionaire
        dictionaire du jeu 
    infos : dictionaire
        dictionnaire des informations de la grille de jeu
    etat : dictionaire
        dictionaire de l'etat des segments
        
    Return
    -------
    None
    
    """
    taille_case = infos['case']
    taille_marge = infos['marge']
    couleurs = fct_grille.couleur_indices(jeu['indices'], etat)
    taille = taille_case[0] / 2
    
    y = taille_marge[1] + taille_case[1]//2 # on se place au centre de la case (0,0)
    i=0
    for lst_indices in jeu['indices']:
        x = taille_marge[0] + taille_case[0]//2 # on se place au centre de la case 
        j = 0
        for indice in lst_indices:
            if indice != None:
                couleur = couleurs[i][j]
                fltk.texte(x, y, str(indice), couleur=couleur, ancrage='center', taille= int(taille))
            x += taille_case[0]
            j += 1
        y += taille_case[1]
        i+=1
        

def boutons_sol(positions, boutons):
    """
    La fonction va parcourir les dictionaire positions et boutons pour afficher
    les boutons des modes du solver.

    Parameters
    ----------
    positions : dictionaire
        disctionaire des positions des boutons.
    boutons : dictionaire
        dictionaire des points formant les boutons.

    Returns
    -------
    None.

    """
    #on parcourt le dictionaire des positions des boutons pour les dessiner 
    for cle in positions:
        if len(positions[cle]) == 2: # correpond a du texte (2 coordonnées)
            x, y = positions[cle]
            fltk.texte(x, y, cle, couleur='darkgreen', ancrage='nw', taille=17)
        elif len(positions[cle]) == 4: # rectangle
            topx, topy, basx, basy = positions[cle]
            fltk.rectangle(topx, topy, basx, basy, couleur='darkgreen', remplissage='darkgreen')
        else: # les fleches 
            lst_points = positions[cle]
            fltk.polygone(lst_points, couleur='darkgreen', remplissage='darkgreen')
    for cle in boutons:
        if cle == 'solver':
            continue
        else: 
            # on ecrit en dessous du bouton a quoi il correspond
            x,y,bx,by = boutons[cle]
        fltk.texte(x,by, cle, couleur='black', taille=10, ancrage='nw')


def affichage(jeu, infos, positions=[], boutons=[]):
    """
    La fonction efface ce qu'il y a dans la fentre et affiche : les segments tracé, 
    les segments interdits, la grille, les indices, les boutons s'il y en a.
    
    Parameter
    ----------
    jeu : dictionaire
        dictionaire du jeu 
    infos : dictionaire
        dictionnaire des informations de la grille de jeu
        
    Return
    -------
    None
    """
    fltk.efface_tout()
    # avec le solver
    if 'sol tracé' in jeu and jeu['sol tracé']:
        fltk.efface_tout()
        affiche_segment(jeu['sol tracé'])
        affiche_segment_barre(jeu['sol interdit'])
        affiche_grille(infos)
        affiche_indices(jeu, infos, jeu['sol etat'])
        boutons_sol(positions, boutons)
    # quand le joueur joue
    else : 
        affiche_segment(jeu['tracé'])
        affiche_segment_barre(jeu['interdit'])
        affiche_grille(infos)
        affiche_indices(jeu, infos, jeu['etat']) 
        boutons_sol(positions, boutons)
    
def affiche_solution(etat, jeu, infos, positions=[], boutons=[]):
    """
    La fonction remplis le dictionaire jeu avec les segments que le solver
    utilise pour resoudre la grille. 
    
    Parameter
    ----------
    etat: dictionaire
        dictionaire de l'etat des différents segments
    jeu : dictionaire
        dictionaire du jeu 
    infos : dictionaire
        dictionnaire des informations de la grille de jeu
        
    Return
    -------
    None
    """
    jeu['sol tracé'] = []
    jeu['sol interdit'] = []
    # on parcour la liste des segment dans etat
    for segment in etat:
        if acces.est_trace(etat, segment):
             jeu['sol tracé'].append(acces.segment_vers_coordonees(segment, infos))
    jeu['sol etat'] = etat
    if positions: # si on a besoin des boutons
        affichage(jeu, infos, positions, boutons)
        fltk.mise_a_jour()
        return 
    affichage(jeu, infos)
    
    
def cree_infos_sol(infos, jeu):
    """
    La fonction crée les informations concerant les positions des boutons du solver.
    
    Parameter
    ----------
    infos : dictionaire
        dictionnaire des informations de la grille de jeu
    jeu : dictionaire
        dictionaire du jeu 
    
        
    Return
    -------
    positions : dictioanire des position des boutons 
    boutons : dictionaire des coordonées des boutons
    
    """
    # le nom du bouton est la clé et une liste des points qui l'entourent lui correspond
    boutons = {} 
    # le nom du bouton est la clé et une liste de points constituant la forme du bouton lui correspond
    positions = {}
    fenetre = infos['dim fenetre']
    marge = infos['marge']
    taille = (fenetre - marge[0]*2) // 6 # les deux cotés
    x = taille // 4 # case divisé par 4
    y = marge[1] // 4
    
    if len(jeu['indices'][0]) >= 2: # sinon la grille est trop petite
        X = taille
        # forme de deux flèches
        positions['rapide'] = [(X, y), (X+x, 2*y), (X+x, y), (X+2*x, 2*y), 
                               (X+x, 3*y), (X+x, 2*y), (X, 3*y)]
        boutons['rapide'] = [X, y, X+ X // 2, 3*y]
    
    X = taille*2
    # forme de fleche
    positions['lent'] = [(X, y+y//2), (X +x//2, y+y//2),(X+x//2, y), (X+x, y*2),
                          (X+x//2, 3*y), (X+x//2, 2*y+y//2), (X, 2*y+y//2)]
    boutons['lent'] = [X, y, X + x, 3*y]
    
    X = taille*5
    positions['solver'] = [X, y]
    boutons['solver'] = [X, y, X+3*x, 2*y+y//2]
    
    return positions, boutons

def choix_solver(jeu, infos):
    """
    La fonction permet au joueur de choisir le mode du solver.
    
    Parameter
    ----------
    jeu : dictionaire
        dictionaire du jeu 
    infos : dictionaire
        dictionnaire des informations de la grille de jeu
    
        
    Return
    -------
    bouton : chaine de caractère qui décrit le boutons choisi
    positions : dictioanire des position des boutons 
    boutons : dictionaire des coordonées des boutons
    """
    positions, boutons = cree_infos_sol(infos, jeu)
    
    while True:
        # affichage de la grille et des solveurs disponibles
        affichage(jeu, infos, positions, boutons)
        fltk.mise_a_jour()
        # attend un evenement click
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche":
            click = (fltk.abscisse(ev), fltk.ordonnee(ev))
            # on cherche quel solver est selectioné
            bouton = clicks.mode_solver(boutons, click)
            if bouton: # si le solver existe
                return bouton, positions, boutons