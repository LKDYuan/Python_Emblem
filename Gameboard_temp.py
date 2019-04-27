#!/usr/bin/python
# -*- coding: UTF-8 -*-
# #########
# DAI Linkai, TS4
# DJOUKA Yann, TS3
# Python Emblem
# #########

import tkinter as tk
from math import cos, sin, asin, pi
from random import choice


# #########
# Variables
# #########

# Dimensions du plateau de jeu
_game_win = tk.Tk()  # fenêtre principale
scrn_w = _game_win.winfo_screenwidth() - 20  # largeur de l'écran
scrn_h = _game_win.winfo_screenheight() - 20  # longueur de l'écran
_game_win.title("Honey Emblem")  # nom du jeu
vert_scale = 0.5  # facteur d'étirement vertical (effet 3D) [modifiable]
win_width = min((scrn_h * 19 / 20) / vert_scale, scrn_w)  # largeur du canevas
space = win_width / 20  # espace vide au-dessus du plateau (effet 3D)
win_height = win_width * vert_scale + space  # hauteur du canevas
center = win_width / 2  # case du milieu (référentiel)
board_side = 5  # nombre de cases sur un côté du plateau hexagonal [modifiable]


# Paramètres de la rotation du plateau
rotate = 0.75  # rotation du plateau en radians [modifiable]
rotate_delay = 30  # temps en ms entre 2 mises à jour du plateau [modifiable]
rotation = False  # Le plateau tourne-t-il?


# Dimensions des cases
tl_side = win_width / (2 * (3 * board_side ** 2 - 3 * board_side + 2) ** 0.5)
tl_size = tl_side * (3 ** 0.5)

# Liste des cases dans le plateau
gameboard = [[0]]
for layer in range(1, board_side):
    gameboard.append(layer * 6 * [0])

# Caractéristiques des cases
tile_types = ["#008800", "#008800", "#008800", "#0000bb"]  # Types [provisoire]
unreachable = tile_types[3]  # Sur quels types de cases ne peut-on pas aller?
start_tile_type = "#aaaa00"  # Type des cases de départ
selected_tile = "#ffffff"  # Coloration des cases sélectionnées
adj_tiles = "#ffff00"  # Coloration des cases adjacentes à la sélectionnée
enemy_tile = "#ff0000"  # Coloration des cases des ennemis


# Liste des personnages
characters = {}
characters["Marth"] = {"ATK": 25, "HP": 200, "DEF": 5},
characters["God"] = {"ATK": 999999999999999, "HP": 1, "DEF": 99999999999999999}

# Caractéristiques des personnages [provisoire, il faut remplir Liste ^]
char_types = ["#eeeeee", "#222222"]
mvt_types = range(2, 6)  # ! Attention, la limite supérieure est Off by One !


# #########
# Fonctions
# #########

# Rotation du plateau complet
def Rotate_board():
    global rotate

    # mise à jour de la position de chaque case et de chaque personnage
    for layer in gameboard:
        for tile in layer:
            tile.Position()
    # afficher les personnages devant les cases [à compléter pour perspective]
    for layer in gameboard:
        for tile in layer:
            if tile.has_char:
                tile.char.Position()
                _gameboard.tag_raise(tile.char.gui)
                _gameboard.tag_raise(tile.char.txt)

    rotate = (rotate + pi / 1440) % (2 * pi)

    # attend avant de tourner de nouveau
    if rotation:
        _gameboard.after(rotate_delay, Rotate_board)

    return


# Rend aux cases leur couleur d'origine, avant la sélection
def Clear_board(clear_all):
    for layer in gameboard:
        for tile in layer:
            tile.tmp_reachable = False
            if clear_all:
                tile.type = tile.color
            tile.Recolor()

    return


# ######
# Objets
# ######

# Les cases
class Tile:

    # Combien de cases y a-t-il?
    tiles_count = 0
    # A-t-on initié un mouvement pour un personnage?
    clicked = False
    # Compteur des cases parcourues lors d'un mouvement
    mvt_count = 0

    # Création de la case
    def __init__(self, layer, indice):

        # attributs qualitatifs de la case
        self.color = Tile.Tile_type()
        self.clicked = False
        self.tmp_reachable = False

        # coordonnées de la case
        # couche
        self.layer = layer
        # côté
        try:
            self.side = indice // layer
        except ZeroDivisionError:
            self.side = 0
        # index
        self.indice = indice
        self.tag = float(Tile.tiles_count)
        Tile.tiles_count += 1
        try:
            self.pos = indice % layer
        except ZeroDivisionError:
            self.pos = 0

        # différentiation des cases de départ
        if self.layer == board_side - 1:
            if self.side == 1 or self.side == 4:
                self.color = start_tile_type
            if (self.side == 2 or self.side == 5) and self.pos == 0:
                self.color = start_tile_type

        # coloration de la case
        self.type = self.color

        # représentation graphique de la case
        self.gui = _gameboard.create_polygon(0, 0, width=0, fill=self.type,
                                             tag=self.tag)

        # actions sur les cases
        _gameboard.tag_bind(self.tag, "<Button-1>", self.Cursor_click)
        _gameboard.tag_bind(self.tag, "<Enter>", self.Cursor_enter)
        _gameboard.tag_bind(self.tag, "<Leave>", self.Recolor)

        # création d'un personnage sur les cases de départ
        self.has_char = False
        if self.color == start_tile_type:
            self.char = Tile.Character(self)

        self.Position()

        return

    # Position de la case
    def Position(self):

        # distance au centre
        tmp_var = self.layer ** 2 + self.pos ** 2 - self.layer * self.pos
        self.center_d = tmp_var ** 0.5 * tl_size

        # angle par rapport à l'axe horizontal
        try:
            self.angle = asin(tl_side * 1.5 * self.pos / self.center_d)
        except ZeroDivisionError:
            self.angle = 0

        # coordonnées du point central de la case
        tmp_var = self.angle + self.side * pi / 3 + rotate
        self.x = center + self.center_d * cos(tmp_var)
        self.y = center + self.center_d * sin(tmp_var)

        # coordonnées des sommets de la case
        self.points = self.Hex_points()

        # coordonnées des cases après étirement par vert_scale
        self.disp_y = self.y * vert_scale + space
        self.disp = []
        for point in self.points:
            self.disp.append(point[0])
            self.disp.append(point[1] * vert_scale + space)

        # affichage de la case sur le canevas
        _gameboard.coords(self.gui, self.disp)

        return

    # Sommets d'une case hexagonale
    def Hex_points(self):

        tmp_l = []
        for pt in range(6):
            tmp_var = pt * pi / 3 - pi / 6 + rotate
            tmp_l.append([self.x + tl_side * cos(tmp_var),
                          self.y + tl_side * sin(tmp_var)])

        return tmp_l

    # Couleurs d'un case [provisoire]
    def Tile_type():

        return choice(tile_types)

    # Lorsqu'une case est cliquée
    def Cursor_click(self, mouse):

        # rétablir la couleur des cases à la fin d'un mouvement
        if Tile.clicked and self.type == selected_tile:
            Clear_board(True)

            # déplacement du personnage à la case d'arrivée
            Tile.tmp_tile.char.Move(self)

            # réinitialisation des variables pour un nouveau mouvement
            Tile.clicked = False
            Tile.mvt_count = 0

        # commencer le mouvement lorsqu'on sélectionne un personnage
        elif self.has_char and not Tile.clicked:
            Tile.clicked = True
            Tile.tmp_tile = self

            # compteur des cases parcourues (pour respecter le mouvement)
            self.mvt_distance = 0
            self.Reachable_tiles()

        return

    # Cases adjacentes à une case sélectionnée [à peaufiner]
    def Reachable_tiles(self):

        self.type = selected_tile
        _gameboard.itemconfig(self.gui, fill=self.type)
        Clear_board(False)

        # pour la case du centre
        if self.layer == 0:
            for tile in gameboard[1]:
                tile.Reachable()

        # pour les autres cases
        else:
            # cases adjacentes sur la même couche
            for tile in gameboard[self.layer]:
                if tile.indice == (self.indice + 1) % (self.layer * 6):
                    tile.Reachable()
                if tile.indice == (self.indice - 1) % (self.layer * 6):
                    tile.Reachable()

            # cases adjacentes sur des couches différentes
            # pour les coins d'une couche
            if self.pos == 0:
                # cases sur la couche du dessous
                for tile in gameboard[self.layer - 1]:
                    if self.layer == 1:
                        tile.Reachable()
                    elif tile.side == self.side and tile.pos == 0:
                        tile.Reachable()

                # cases sur la couche du dessus (sauf pour la dernière couche)
                if self.layer != board_side - 1:
                    for tile in gameboard[self.layer + 1]:
                        if tile.side == self.side and tile.pos <= 1:
                            tile.Reachable()
                        if tile.side == (self.side - 1) % 6 and tile.pos == tile.layer - 1:
                            tile.Reachable()

            # pour les côtés d'un couche
            else:
                # cases sur la couche du dessous
                for tile in gameboard[self.layer - 1]:
                    if tile.side == self.side and (tile.pos == self.pos or tile.pos == self.pos - 1):
                        tile.Reachable()
                    if self.pos % tile.layer == 0 and tile.side == (self.side + 1) % 6 and tile.pos == 0:
                        tile.Reachable()

                # cases sur la couche du dessus (sauf pour la dernière couche)
                if self.layer != board_side - 1:
                    for tile in gameboard[self.layer + 1]:
                        if tile.side == self.side and (tile.pos == self.pos or tile.pos == self.pos + 1):
                            tile.Reachable()

        return

    # Cette case adjacente est-elle libre?
    def Reachable(self):

        if self.type != unreachable and self.type != selected_tile and not self.has_char:
            self.tmp_reachable = True
            _gameboard.itemconfig(self.gui, fill=adj_tiles)

        return

    # Les autres cases reprennent leur couleur d'origine
    def Recolor(self, mouse=0):

        if not self.tmp_reachable:
            _gameboard.itemconfig(self.gui, fill=self.type)

        return

    # Lorsque la souris est au-dessus d'une case
    def Cursor_enter(self, mouse):

        # si un mouvement a été commencé, continuer à sélectionner des cases
        if self.tmp_reachable:
            # Le mouvement ne peut pas être supérieur aux points de mouvement
            Tile.mvt_count += 1
            self.mvt_distance = Tile.mvt_count
            if self.mvt_distance < Tile.tmp_tile.char.mvt_range:
                self.Reachable_tiles()
            elif self.mvt_distance == Tile.tmp_tile.char.mvt_range:
                self.type = selected_tile
                Clear_board(False)
                self.tmp_reachable = True

        # si on passe sur une case déjà sélectionnée, recalculer la trajectoire
        elif self.type == selected_tile:
            Tile.mvt_count = self.mvt_distance

            # désélection des cases plus loin dans la trajectoire
            for layer in gameboard:
                for tile in layer:
                    try:
                        if tile.mvt_distance > self.mvt_distance:
                            del tile.mvt_distance
                            tile.type = tile.color
                            _gameboard.itemconfig(self.gui, fill=self.type)
                    except AttributeError:
                        pass

            # calcul des cases adjacentes à la nouvelle
            self.Reachable_tiles()

        # si un mouvement n'a pas été commencé, blanchir la case
        else:
            tmp_color = self.color.replace("00", "77")
            _gameboard.itemconfig(self.gui, fill=tmp_color)

        return

    # Les cases peuvent contenir des personnages!
    class Character:

        # Attributs de chaque personnage
        def __init__(self, tile):

            # la case contient effectivement un personnage
            tile.has_char = True
            # le personnage appartient effectivement à une case
            self.tile = tile

            # nature des personnages [provisoire]
            # qui est-ce?
            self.char = choice(char_types)
            # quel est son déplacement?
            self.mvt_range = choice(mvt_types)

            # représentation graphique du personnage [provisoire - images]
            self.gui = _gameboard.create_rectangle(0, 0, 0, 0, width=0,
                                                   fill=self.char,
                                                   tag=tile.tag)
            # affichage du déplacement du personnage [provisoire]
            self.txt = _gameboard.create_text(0, 0, text=self.mvt_range,
                                              fill="#7fffff",
                                              tag=tile.tag)

            return

        # Position du personnage
        def Position(self):

            # Position du personnage en soit [provisoire]
            _gameboard.coords(self.gui, self.tile.x - 0.15 * tl_size,
                              self.tile.disp_y - space,
                              self.tile.x + 0.15 * tl_size,
                              self.tile.disp_y)

            # Position du déplacement du personnage [provisoire]
            _gameboard.coords(self.txt, self.tile.x,
                              self.tile.disp_y - space / 2)

            return

        # Bouger un personnage à une case
        def Move(self, tile):

            # on transfère le personnage entre cases de départ et d'arrivée
            tmp = self.tile
            tmp.has_char = False
            del tmp.char
            tile.char = self
            self.tile = tile
            self.tile.has_char = True

            # mise à jour des actions sur le personnage (nouvelle case)
            _gameboard.itemconfig(self.gui, tag=tile.tag)
            _gameboard.itemconfig(self.txt, tag=tile.tag)

            # mise à jour de la position du personnage sur le canevas
            self.Position()

            return


# ###################
# Programme principal
# ###################

# Canevas sur lequel se déroulera le jeu
_gameboard = tk.Canvas(_game_win, width=win_width,
                       height=win_height, bg="#000000")
_gameboard.pack()

# Tourner le plateau [provisoire]
if rotation:
    _gameboard.after(rotate_delay, Rotate_board)

# Création des cases
for layer in gameboard:
    for tile in range(len(layer)):
        layer[tile] = Tile(gameboard.index(layer), tile)

# Création des personnages
for layer in gameboard:
    for tile in layer:
        if tile.has_char:
            tile.char.Position()
            _gameboard.tag_raise(tile.char.gui)
            _gameboard.tag_raise(tile.char.txt)

# Création de la fenêtre
_game_win.mainloop()
