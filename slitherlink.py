import fltk
import fct_grille 
import fct_menu as menu

# programme principal
if __name__ == "__main__":
    # initialisation du jeu
    framerate = 10
    jeu = {'game': True}
    grilles = {'grille1': 'grille1.txt', 'grille2': 'grille2.txt', 'grille-triviale': 'grille-triviale.txt', 
           'grille3': 'grille3.txt', 'grille4': 'grille4.txt', 'grille5': 'grille5.txt'}
    infos = {'dim fenetre': 515}
    # menu
    menu.menu(infos)
    
    while jeu['game']:
        jeu = {'etat': {}, 'interdit': [], 'tracé': [], 'game': True, 'sol etat': {},
               'sol tracé': [], 'sol interdit': []}
        
        doc_grille = menu.menu_cartes(infos, grilles)
        indices = fct_grille.grille_indices(doc_grille)
        if not indices:
            dim = infos['dim fenetre']
            fltk.efface_tout()
            fltk.texte(dim//2, dim//2, "désolé mais cette grille n'est pas valide",
                       taille=30, ancrage='center')
            continue
        else:
            jeu['indices'] = indices 
            infos = fct_grille.dimension_fenetre(jeu['indices'], {'dim fenetre': 515})
            fenetre = infos['dim fenetre']
            retour = menu.maj_grille(jeu, infos)
            
            if retour == False: # on veut quitter 
                jeu['game'] = False
            elif retour == 'quitte':
                break
        
    fltk.attend_ev()
    # fermeture et sortie
    fltk.ferme_fenetre() 