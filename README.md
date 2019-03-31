# Python Emblem

This repository is to centralize all files used in this school project, Python Emblem.

<i>On centralisera ici tous les fichiers utilisés dans le projet de Python Emblem !</i>

<code>2019_ISN_Projet_Python-Emblem.py</code> <b><i>est obsolète, la version mise à jour est</i></b> <code>Gameboard_temp.py</code>


# Fonctions du programme

<i>Toutes les variables citées sont définies dans l'en-tête du programme, sauf indication contraire</i>


## Fonctions globales

#### <code>Rotate_board()</code>

Appelé toutes les <code>rotate_delay</code> millisecondes, il fait recalculer les coordonnées de chaque case en ajoutant une rotation de <code>rotate</code> radians dans le sens horaire.


## Fonctions spécifiques aux objets

### Objet <code>Tile</code>

#### <code>__init__()</code>

Lancé à chaque fois que l'on crée une case, pour en définir les caractères dont on aura besoin dans le jeu (type, position relative au centre sur le plateau, représentation graphique).

#### <code>Position()</code>

Sert à déterminer les coordonnées <code>Tile.x</code> et <code>Tile.y</code> d'une case sur le canevas, et à l'afficher avec un effet 3D grâce à <code>vert_scale</code> sur la fenêtre Tkinter (plus de détails dans le programme-même).

#### <code>Hex_points()</code>

À partir des coordonnées du centre d'une case <code>Tile.x</code> et <code>Tile.y</code>, et de la longueur d'un côté <code>tile_side</code>, retourne les coordonnées des sommets de la case hexagonale (en prenant en compte la rotation).

#### <code>Tile_type()</code>

Retourne une type de case au hasard, entre plusieurs types définis. [pour l'instant, seulement des couleurs différentes]

#### <code>Cursor_click()</code>

Commet une action lors du clic d'une case. [pour l'instant, change de couleur]

#### <code>Cursor_enter()</code>

Losrque le curseur est au-dessus d'une case, la blanchit. [à peaufiner, si on a le temps]

#### <code>Cursor_leave()</code>

Lorsque le curseur n'est plus au-dessus d'une case, lui rend sa couleur.

#### <code>Create_char()</code>

Crée un personnage sur une case. [à compléter: au lieu d'un personnage pour chaque case, en créer un nombre limité, et afficher des images au lieu de rectangles]
<i>Partie du code encore à finir, pour avoir un minimum de jeu…</i>

#### <code>Char_position()</code>

Comme <code>Tile.Position()</code>, mais détermine les coordonnées du personnage sur le canevas.


## Avancement du projet

* Plateau de jeu: <code>en cours</code>
  * Cases <code>fini</code>
  * GUI <code>à finir</code>
  * Personnages <code>en cours</code>
* Stratégie: <code>ébauche</code>
  * Mouvement <code>en cours</code>
  * Attaques, dégâts <code>en cours</code>
  * Sélection des actions <code>pas commencé</code>
  * Multijoueur <code>ébauche</code>


##### Atom link:
<code>Mettre à jour à chaque redémarrage de Atom</code>
