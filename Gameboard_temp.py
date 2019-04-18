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
win_dim = min((scrn_h * 19 / 20) / vert_scale, scrn_w)  # dimensions maximales
space = win_dim / 20  # espace vide au-dessus du plateau (effet 3D)
center = win_dim / 2  # case du milieu (référentiel)
board_side = 5  # nombre de cases sur un côté du plateau hexagonal [modifiable]
rotate = 0  # rotation du plateau en radians [modifiable]
rotate_delay = 30  # temps en ms entre 2 mises à jour du plateau [modifiable]
rotation = False
tile_types = ["#00ff00", "#00ff00", "#00ff00", "#0000ff"]
unreachable = tile_types[3]
start_tile_type = "#ff0000"


# Dimensions des cases
tl_side = win_dim / (2 * (3 * board_side ** 2 - 3 * board_side + 2) ** 0.5)
tl_size = tl_side * (3 ** 0.5)

# Liste des cases dans le plateau
gameboard = [[0]]
for layer in range(1, board_side):
    gameboard.append(layer * 6 * [0])

# Liste des personnages
characters = {}
characters["Marth"] = {"ATK": 25, "HP": 200, "DEF": 5},
characters["God"] = {"ATK": 999999999999999, "HP": 1, "DEF": 99999999999999999}


# #########
# Fonctions
# #########

# Rotation du plateau complet
def Rotate_board():
    global rotate

    # mise à jour de la position de chaque case et de chaque personnage
    for layer in gameboard:
        for tile in layer:
            Tile.Position(tile)
    # afficher les personnages devant les cases [à compléter pour perspective]
    for layer in gameboard:
        for tile in layer:
            if tile.has_char:
                _gameboard.tag_raise(tile.char_gui)

    rotate = (rotate + pi / 1440) % (2 * pi)

    # attend avant de tourner de nouveau
    if rotation:
        _gameboard.after(rotate_delay, Rotate_board)
    return


# ######
# Objets
# ######

# Les cases
class Tile:
    clicked = False
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
        try:
            self.pos = indice % layer
        except ZeroDivisionError:
            self.pos = 0

        if self.layer == board_side - 1:
            if self.side == 1 or self.side == 4:
                self.color = start_tile_type
            if (self.side == 2 or self.side == 5) and self.pos == 0:
                self.color = start_tile_type

        self.type = self.color

        # représentation graphique de la case
        self.gui = _gameboard.create_polygon(0, 0, width=0, fill=self.type)

        # actions sur les cases
        _gameboard.tag_bind(self.gui, "<Button-1>", self.Cursor_click)
        _gameboard.tag_bind(self.gui, "<Enter>", self.Cursor_enter)
        _gameboard.tag_bind(self.gui, "<Leave>", self.Cursor_leave)

        # création d'un personnage sur la case [provisoire]
        self.has_char = False
        if self.color == start_tile_type:
            self.char = Tile.Character(self)

        # calcul de la position de la case sur le canevas
        self.Position()

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
        self.points = self.Hex_points()

        # coordonnées des cases après étirement par vert_scale
        self.disp_y = self.y * vert_scale + space
        self.disp = []
        for point in self.points:
            self.disp.append(point[0])
            self.disp.append(point[1] * vert_scale + space)

        # création de la case sur le plateau
        _gameboard.coords(self.gui, self.disp)

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
        # basculer entre couleur d'origine et blanc [provisoire]
        if self.has_char:
            if not Tile.clicked:
                Tile.tmp_tile = self
                self.Reachable_tiles()
                self.mvt_distance = 0
                Tile.clicked = not Tile.clicked
        elif Tile.clicked and self.type == "#ffffff":
            for layer in gameboard:
                for tile in layer:
                    tile.tmp_reachable = False
                    tile.type = tile.color
                    _gameboard.itemconfig(tile.gui, fill=tile.type)
            print(Tile.tmp_tile.char.mvt_range)
            Tile.tmp_tile.char.Move(self)
            Tile.clicked = not Tile.clicked
            Tile.mvt_count = 0

    # Cases adjacentes à une case sélectionnée
    def Reachable_tiles(self):
        self.type = "#ffffff"
        for layer in gameboard:
            for tile in layer:
                tile.tmp_reachable = False
                tile.Reachable_color()

        if self.layer == 0:
            for tile in gameboard[1]:
                tile.Reachable()
        else:
            for tile in gameboard[self.layer]:
                if tile.indice == (self.indice + 1) % len(gameboard[self.layer]):
                    tile.Reachable()
                if tile.indice == (self.indice - 1) % len(gameboard[self.layer]):
                    tile.Reachable()
            if self.pos == 0:
                for tile in gameboard[self.layer - 1]:
                    if tile.side == self.side and tile.pos == 0 or tile.layer == 0:
                        tile.Reachable()
                if self.layer != board_side - 1:
                    for tile in gameboard[self.layer + 1]:
                        if tile.side == self.side and tile.pos <= 1:
                            tile.Reachable()
                        if tile.side == (self.side - 1) % 6 and tile.pos == tile.layer - 1:
                            tile.Reachable()
            else:
                for tile in gameboard[self.layer - 1]:
                    if tile.side == self.side and (tile.pos == self.pos or tile.pos == self.pos - 1):
                        tile.Reachable()
                    if self.pos % tile.layer == 0 and tile.side == (self.side + 1) % 6 and tile.pos == 0:
                        tile.Reachable()
                if self.layer != board_side - 1:
                    for tile in gameboard[self.layer + 1]:
                        if tile.side == self.side and (tile.pos == self.pos or tile.pos == self.pos + 1):
                            tile.Reachable()

        _gameboard.itemconfig(self.gui, fill=self.type)

    def Reachable(self):
        if self.type != unreachable and self.type != "#ffffff" and not self.has_char:
            self.tmp_reachable = True
            self.Reachable_color()
        return

    def Reachable_color(self):
        if self.tmp_reachable:
            if self.type != "#ffffff" and self.type != unreachable:
                _gameboard.itemconfig(self.gui, fill="#ffff00")
        else:
            _gameboard.itemconfig(self.gui, fill=self.type)

    # Lorsque la souris est au-dessus d'une case
    def Cursor_enter(self, mouse):
        if self.tmp_reachable:
            Tile.mvt_count += 1
            self.mvt_distance = Tile.mvt_count
            if Tile.mvt_count <= Tile.tmp_tile.char.mvt_range:
                self.Reachable_tiles()
        elif self.type == "#ffffff":
            Tile.mvt_count = self.mvt_distance
            for layer in gameboard:
                for tile in layer:
                    try:
                        if tile.mvt_distance > self.mvt_distance:
                            del tile.mvt_distance
                            tile.type = tile.color
                            _gameboard.itemconfig(self.gui, fill=self.type)
                    except AttributeError:
                        pass
            self.Reachable_tiles()
        else:
            tmp_color = self.color.replace("00", "aa")
            _gameboard.itemconfig(self.gui, fill=tmp_color)

    # Lorsque la souris n'est plus au-dessus d'une case
    def Cursor_leave(self, mouse):
        _gameboard.itemconfig(self.gui, fill=self.type)

    class Character:
        def __init__(self, tile):
            self.tile = tile
            self.tile.has_char = True
            self.char = choice(["#eeeeee", "#222222"])
            self.mvt_range = choice(range(1, 4))
            self.gui = _gameboard.create_rectangle(0, 0, 0, 0, width=0,
                                                   fill=self.char)
            _gameboard.tag_bind(self.gui, "<Button-1>", tile.Cursor_click)
            _gameboard.tag_bind(self.gui, "<Enter>", tile.Cursor_enter)
            _gameboard.tag_bind(self.gui, "<Leave>", tile.Cursor_leave)

        def Move(self, tile):
            tmp = self.tile
            tmp.has_char = False
            tile.char = self
            del tmp.char
            self.tile = tile
            self.tile.has_char = True
            _gameboard.tag_bind(self.gui, "<Button-1>", tile.Cursor_click)
            _gameboard.tag_bind(self.gui, "<Enter>", tile.Cursor_enter)
            _gameboard.tag_bind(self.gui, "<Leave>", tile.Cursor_leave)
            self.Position(tile)

        def Position(self, tile):
            _gameboard.coords(self.gui, tile.x - 0.15 * tl_size,
                              tile.disp_y - space, tile.x + 0.15 * tl_size,
                              tile.disp_y)

    # Création d'un personnage sur la case
    def Create_char(self):

        # la case contient un personnage !
        self.has_char = True

        # couleur du personnage [provisoire]
        self.char_type = choice(["#eeeeee", "#222222"])
        self.char_mvt = choice(range(1, 4))

        # positionnement du personnage sur le plateau [provisoire]
        self.char_gui = _gameboard.create_rectangle(0, 0, 0, 0, width=0,
                                                    fill=self.char_type)

        # actions sur le personnage
        _gameboard.tag_bind(self.char_gui, "<Button-1>", self.Cursor_click)
        _gameboard.tag_bind(self.char_gui, "<Enter>", self.Cursor_enter)
        _gameboard.tag_bind(self.char_gui, "<Leave>", self.Cursor_leave)

    # Positionnement du personnage sur le plateau
    def Char_position(self):
        _gameboard.coords(self.char_gui, self.x - 0.15 * tl_size,
                          self.disp_y - space, self.x + 0.15 * tl_size,
                          self.disp_y)


# ###################
# Programme principal
# ###################

# Canevas sur lequel se déroulera le jeu
_gameboard = tk.Canvas(_game_win, width=win_dim,
                       height=win_dim * vert_scale + space, bg="#000000")
_gameboard.pack()

# Tourner le plateau [provisoire]
if rotation:
    _gameboard.after(rotate_delay, Rotate_board)

# Création des cases
for layer in gameboard:
    for tile in range(len(layer)):
        layer[tile] = Tile(gameboard.index(layer), tile)
for layer in gameboard:
    for tile in layer:
        if tile.has_char:
            tile.char.Position(tile)
            _gameboard.tag_raise(tile.char.gui)

# Création de la fenêtre
_game_win.mainloop()
