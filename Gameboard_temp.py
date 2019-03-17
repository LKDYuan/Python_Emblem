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
from time import sleep


# #########
# Variables
# #########

# Dimensions du plateau de jeu
vert_scale = 0.47  # facteur d'étirement vertical (effet 3D) [modifiable]
win_dim = min((660 * 19 / 20) / vert_scale, 1260)  # dimensions maximales
space = win_dim / 20  # espace vide au-dessus du plateau (effet 3D)
center = win_dim / 2  # case du milieu (référentiel)
board_side = 9  # nombre de cases sur un côté du plateau hexagonal [modifiable]
rotate = 0  # rotation du plateau en radians [modifiable]

# Dimensions des cases
tl_side = win_dim / (2 * (3 * board_side ** 2 - 3 * board_side + 2) ** 0.5)
tl_size = tl_side * (3 ** 0.5)

# Liste des cases dans le plateau
gameboard = [[0]]
for layer in range(1, board_side):
    gameboard.append(layer * 6 * [0])


# ##########
# Programmes
# ##########

# Sommets d'une case hexagonale
def Hex_points(tile):
    tmp_l = []
    for pt in range(6):
        tmp_l.append([tile.x + tl_side * cos(pt * pi / 3 - pi / 6 + rotate),
                      tile.y + tl_side * sin(pt * pi / 3 - pi / 6 + rotate)])
    return tmp_l


# Couleurs d'un case [provisoire]
def Tile_type():
    return choice(["#ff0000", "#00ff00", "#0000ff",
                   "#00ffff", "#ff00ff", "#ffff00"])


# Rotation du plateau complet
def Rotate_board(mouse):
    global rotate
    rotate = (rotate + pi / 1440) % (2 * pi)

    # mise à jour de la position de chaque case
    for layer in gameboard:
        for tile in layer:
            Tile.Position(tile)
    sleep(0.005)


# ######
# Objets
# ######

# Les cases
class Tile:

    # Création de la case
    def __init__(self, layer, indice):
        global _gameboard

        # attributs qualitatifs de la case
        self.color = Tile_type()
        self.type = self.color
        self.clicked = False

        # coordonnées de la case
        '''couche'''
        self.layer = layer
        '''côté'''
        try:
            self.side = indice // layer
        except ZeroDivisionError:
            self.side = 0
        '''index'''
        try:
            self.pos = indice % layer
        except ZeroDivisionError:
            self.pos = 0

        # représentation graphique de la case
        self.gui = _gameboard.create_polygon(0, 0,
                                             fill=self.type, outline=self.type)

        # actions sur les cases
        _gameboard.tag_bind(self.gui, "<Button-1>", self.Cursor_click)
        _gameboard.tag_bind(self.gui, "<Enter>", self.Cursor_enter)
        _gameboard.tag_bind(self.gui, "<Leave>", self.Cursor_leave)

        # calcul de la position de la case sur le canevas
        Tile.Position(self)

    # Position de la case
    def Position(self):
        # distance au centre (référentiel)
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
        self.points = Hex_points(self)

        # coordonnées des cases après étirement par vert_scale
        self.disp = []
        for point in self.points:
            self.disp.append(point[0])
            self.disp.append(point[1] * vert_scale + space)

        # création de la case sur le plateau
        _gameboard.coords(self.gui, self.disp)

    # Lorsqu'une case est cliquée
    def Cursor_click(self, mouse):
        # basculer entre couleur d'origine et blanc [provisoire]
        if self.clicked:
            self.type = self.color
        else:
            self.type = "White"
        _gameboard.itemconfig(self.gui, fill=self.type, outline=self.type)
        self.clicked = not(self.clicked)

    # Lorsque la souris est au-dessus d'une case
    def Cursor_enter(self, mouse):
        # colorer en noir [provisoire]
        _gameboard.itemconfig(self.gui, fill="Black", outline="Black")

    # Lorsque la souris n'est plus au-dessus d'une case
    def Cursor_leave(self, mouse):
        # rendre couleur d'origine [provisoire]
        _gameboard.itemconfig(self.gui, fill=self.type,  outline=self.type)


# ###################
# Programme principal
# ###################

# Fenêtre de jeu
_game_win = tk.Tk()
_game_win.title("Honey Emblem")

# Canevas sur lequel se déroulera le jeu
_gameboard = tk.Canvas(_game_win, width=win_dim,
                       height=win_dim * vert_scale + space, bg="#000000")
_gameboard.pack()

# Tourner le plateau quand la souris bouge [provisoire]
_gameboard.bind("<Motion>", Rotate_board)

# Création des cases
for layer in gameboard:
    for tile in range(len(layer)):
        layer[tile] = Tile(gameboard.index(layer), tile)

# Création de la fenêtre
_game_win.mainloop()
