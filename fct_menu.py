"""
fonctions pour le menu 
"""

import fltk
import fct_grille 
import fct_acces as acces
import fct_clicks as clicks
import fct_victoire as victoire
import fct_solver as solver
import fct_interface as interface


def menu(infos):
    """
    La fonction affiche la page "d'entré" sur laquelle on arrive quand on lance le jeu.

    Parameters
    ----------
    infos : dictionaire
        contient la taille de la fenetre.

    Returns
    -------
    None.

    """
    dim = infos['dim fenetre']
    fltk.cree_fenetre(dim, dim)
    while True:
        fltk.image(dim//2, dim//2, 'image.png', ancrage='center')
        fltk.texte(dim//2, dim //10, 'bienvenu dans Slitherlink !', ancrage='center', taille=30, couleur='darkred')
        fltk.texte(dim//2, dim//10*9, 'cliquez pour commencer', ancrage='center', taille=20, couleur='darkred')
        fltk.mise_a_jour()
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == 'ClicDroit' or tev == 'ClicGauche':
            return

def boucle_solver(jeu, infos, d_boutons):
    """
    La boucle affiche la solution du solver et attend que le joueur réagisse.

    Parameters
    ----------
    jeu : dictionaire
        DESCRIPTION.
    infos : dictionaire
        DESCRIPTION.
    d_boutons : dictionaire
        dictionaire de la position des boutons.

    Returns
    -------
    bool
        False si on quitte le jeu.
    None sinon

    """
    jeu['etat'] = {}
    fenetre = infos['dim fenetre']
    solution = solver.lance_solver(jeu, infos)
    if solution == False: # si la grille peut etre résolu
        while True:
            fltk.efface_tout()
            fltk.texte(fenetre//2, fenetre//2, "Cette grille ne\npeut pas étre résolu", 
                       ancrage='center', couleur='darkred', taille=50)
            fltk.mise_a_jour()
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            if tev == "ClicGauche" or tev == "ClicDroit": 
                return 
    while True:
        interface.affiche_solution(jeu['sol etat'], jeu, infos)
        fltk.texte(20, 20, 'MENU', ancrage='nw', couleur='darkred', taille=15)
        fltk.texte(20, fenetre-40, 'QUITTER', ancrage='nw', taille=15, couleur='darkred')
        fltk.mise_a_jour()
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche" or tev == "ClicDroit": 
            click = (fltk.abscisse(ev), fltk.ordonnee(ev))
            if clicks.sur_bouton(d_boutons['menu'], click):
                return
            elif clicks.sur_bouton(d_boutons['quitter'], click):
                return False
        
def maj_grille(jeu, infos):
    """
    La fonction met a jour la grille c'est la boucle qui permet de jouer.

    Parameters
    ----------
    jeu : dictionaire
        DESCRIPTION.
    infos : dictionaire
        DESCRIPTION.

    Returns
    -------
    False
        si on quitte le jeu.
    None sinon

    """
    fenetre = infos['dim fenetre']
    boutons = {'menu': [20, 20, 65, 35], 'solver':[fenetre//2 - 30, 20-10, fenetre//2+30, 20+10], 
               'quitter':[20, fenetre-40, 90, fenetre-25]}
    while True:
        
        if victoire.partie_gagnee(jeu):
            fenetre = infos['dim fenetre']
            interface.affichage(jeu, infos)
            fltk.texte(fenetre//2, fenetre - 20, 'vous avez gagné', ancrage='center', couleur='darkred', taille=15)
            fltk.texte(20, 20, 'MENU', ancrage='nw', couleur='darkred', taille=15)
            fltk.texte(20, fenetre-40, 'QUITTER', ancrage='nw', taille=15, couleur='darkred')
            fltk.texte(fenetre//2, 20, 'solver', couleur='darkred', taille=15, ancrage='center')
            
        else :
            interface.affichage(jeu, infos) 
            fltk.texte(20, 20, 'MENU', ancrage='nw', couleur='darkred', taille=15)
            fltk.texte(20, fenetre-40, 'QUITTER', ancrage='nw', taille=15, couleur='darkred')
            fltk.texte(fenetre//2, 20, 'solver', couleur='darkred', taille=15, ancrage='center')
        fltk.mise_a_jour()
        
        # on recupere l'evenement 
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        
        if tev == 'Quitte':
           return 'quitte'
       
        if tev == "ClicGauche" or tev == "ClicDroit": # click avec la souris
            # on recupere les coordonnees du click
            click = (fltk.abscisse(ev), fltk.ordonnee(ev))
            
            if clicks.sur_bouton(boutons['menu'], click):
                return
            elif clicks.sur_bouton(boutons['quitter'], click):
                return False
            elif clicks.sur_bouton(boutons['solver'], click):
                return boucle_solver(jeu, infos, boutons) 
            # on cherche le segment correspondant
            else:
                segment = clicks.trouve_segment(click, infos)
                
                if segment : # on a bien clicker sur un segment (pas dans le vide)
                    
                    if tev == "ClicDroit": # on veut barrer le segment 
                        jeu['interdit'], jeu['tracé'] = acces.ajoute_segment(jeu, infos, segment, True)
                    else: # on veut tracer le segment
                        jeu['interdit'], jeu['tracé'] = acces.ajoute_segment(jeu, infos, segment, False)
                        
          
        
def rectangle(infos):
    """
    La fonction dessine un rectangle autour d'une grille.

    Parameters
    ----------
    infos : dictionaire
        dictionaire des dimensions du jeu.

    Returns
    -------
    bouton : liste
        coordonées du rectangle.

    """
    pos = infos['marge']
    marge = infos['pos in']
    case = infos['case']
    largeur = infos['largeur']
    hauteur = infos['hauteur']
    
    
    x_top = pos[0] - 10
    y_top = pos[1]-10
    
    if hauteur == 2:# quand la grille est plus petite il faut réduire certaine dimension
        y_bas = y_top + hauteur*case[1] + marge[1]//hauteur + 5
        if largeur == 2:
            x_bas = x_top + largeur*case[0] + marge[0]// largeur + 5
        else:
            x_bas = x_top + largeur*case[0] + marge[0] + 5                    
    else :
        y_bas =  y_top + hauteur*case[1] + marge[1] + 2
        if largeur == 2:
            x_bas = x_top + largeur*case[0] + marge[0]// largeur + 5
        else:
            x_bas = x_top + largeur*case[0] + marge[0] + 5    

    fltk.rectangle(x_top, y_top, x_bas, y_bas, epaisseur=4)
    bouton = [x_top, y_top, x_bas, y_bas]
    return bouton

def affichage_menu(jeu, infos):
    """
    La fonction affiche les différentes grilles avec lesquelles on peut jouer.

    Parameters
    ----------
    jeu : dictionaire
        dictionaire du jeu.
    infos : dictionaire
        contient les dimensions du jeu.

    Returns
    -------
    appelle la fonction qui dessine un rectangle

    """
    interface.affiche_segment(jeu['tracé'])
    interface.affiche_segment_barre(jeu['interdit'])
    interface.affiche_grille(infos)
    interface.affiche_indices_prop(jeu, infos, jeu['etat'])
    return rectangle(infos)

def affiche_grilles(infos_cartes, boutons, fenetre):
    """
    La fonction affiche les différentes grille.

    Parameters
    ----------
    infos_cartes : dictionaire
        dimensions des elements de la grille (de la carte).
    boutons : dictionaire 
        contient les coordonées des boutons qui correspondent aux grilles.
    fenetre : entier
        taille de la fenetre en pixels.

    Returns
    -------
   boutons : dictionaire 
        contient les coordonées des boutons qui correspondent aux grilles.

    """
    fltk.efface_tout()
    for cle in infos_cartes:
        infos_carte = infos_cartes[cle]
        c_infos = infos_carte[0]
        c_indices = infos_carte[1]
        c_jeu = {'etat': {}, 'interdit': [], 'tracé': [], 'indices': c_indices}# jeu courant
        bouton = affichage_menu(c_jeu, c_infos)
        boutons[cle] = bouton
    fltk.texte(fenetre-20, fenetre-20, 'suivant', ancrage='se', taille=20, couleur='darkblue')
    fltk.mise_a_jour()
    return boutons

def informations_cartes(infos, grilles):
    """
    La fonction crées les informations de dimension pour les différentes grille(cartes).

    Parameters
    ----------
    infos : dictionaire
        contien la taille de la fenetre.
    grilles : dictioanire
        dictionaire des grilles du jeu.

    Returns
    -------
    infos_cartes : dictionaire
        contien les dimensions de la grille(carte).

    """
    fenetre = infos['dim fenetre'] # taille de la fenetre ouverte
    posy = fenetre * 30/103 # on cherche la marge en y 
    posx = fenetre * 17/103 # on cherche la marge en x
    infos_cartes = {}
    
    y = 30
    x = int(posx)
    cmpt = 0
    for cle in grilles: # on parcourt le dictionaire des grilles
        grille = grilles[cle]
        # on regarde si on met la grille sur la gauche ou sur la droite
        if cmpt%2 == 1: 
            x = int(3*posx)
        else:
            x = int(posx)
            
        c_indices = fct_grille.grille_indices(grille) # indices courants
        
        c_infos = fct_grille.dimension_fenetre(c_indices, {'dim fenetre': 150}) # infos courantes
        c_infos['pos in'] = c_infos['marge']
        c_infos['marge'] = [x, y]
        infos_cartes[cle] = (c_infos, c_indices)
        
        y += int(posy)
        cmpt += 1 
    return infos_cartes

def dictionnaire_grilles(grilles):
    """
    la fonction crée deux dictionaires contenant trois grilles chacun.

    Parameters
    ----------
    grilles : dictionaire
        contient les grilles du jeu.

    Returns
    -------
    grilles1 : dictionaire
        contient trois des grilles du jeu.
    grilles2 : dictionaire
        contient trois des grilles du jeu.
    """
    cmpt = 1
    grilles1 = {}
    grilles2 = {}
    for grille in grilles:
        if cmpt <= 3:
            grilles1[grille] = grilles[grille]
        else:
            grilles2[grille] = grilles[grille]
        cmpt += 1
    return grilles1, grilles2

def numeros_grille(click, boutons, grilles):
    """
    La fonction renvoi la grille selectionnée par le joueur.

    Parameters
    ----------
    click : liste
        liste de coordonnées.
    boutons : dictionaire
        dictionaires des coorddonnées des boutons.
    grilles : dictionaire
        contenant les grilles du jeu.

    Returns
    -------
    string
        la grille choisi.

    """
    # on ne met que des if pour que la fonction vérifie bien toute les posibilités
    # on verifie d'abord s'il s'agit de la première fenetre de grille 
    if 'grille1' in boutons:
        if clicks.sur_bouton(boutons['grille1'], click):
            return grilles['grille1']
    if 'grille2' in boutons:
        if clicks.sur_bouton(boutons['grille2'], click):
            return grilles['grille2']
    if 'grille-triviale' in boutons:
        if clicks.sur_bouton(boutons['grille-triviale'], click):
            return grilles['grille-triviale']
    # on verifie s'il s'agit de la seconde fenetre de grille 
    if 'grille3' in boutons:
        if clicks.sur_bouton(boutons['grille3'], click):
            return grilles['grille3']
    if 'grille4' in boutons: 
        if clicks.sur_bouton(boutons['grille4'], click):
            return grilles['grille4']
    if 'grille5' in boutons :
        if  clicks.sur_bouton(boutons['grille5'], click):
            return grilles['grille5']
        
        
def menu_cartes(infos, grilles):
    """
    La foncion permet au joueur de selectioner la carte (la grille) qu'il désire.

    Parameters
    ----------
    infos : dictionaire 
        contient dimension des elements du jeu.
    grilles : dictionaire
        contient les differentes grille du jeu.

    Returns
    -------
    grille : string
        grille avec laquelle on va jouer.

    """
    suivant = [infos['dim fenetre']-100, infos['dim fenetre']-50, infos['dim fenetre'], infos['dim fenetre']]
    boutons1, boutons2 = dictionnaire_grilles(grilles)
    infos_cartes1 = informations_cartes(infos, boutons1)
    infos_cartes2 = informations_cartes(infos, boutons2)
    
    boutons = boutons1
    infos_cartes = infos_cartes1
    while True:
        boutons = affiche_grilles(infos_cartes, boutons, infos['dim fenetre'])
        fltk.mise_a_jour()
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == 'ClicDroit' or tev == 'ClicGauche':
            click = (fltk.abscisse(ev), fltk.ordonnee(ev))
            
            if clicks.sur_bouton(suivant, click):
                if boutons == boutons1:
                    boutons = boutons2
                    infos_cartes = infos_cartes2
                    continue
                else :
                    boutons = boutons1 
                    infos_cartes = infos_cartes1
                    continue
            grille = numeros_grille(click, boutons, grilles)
            if grille != None:
                return grille
            