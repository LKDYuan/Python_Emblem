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
board_side = 6  # nombre de cases sur un côté du plateau hexagonal [modifiable]
rotate = 0  # rotation du plateau en radians [modifiable]
rotate_delay = 15  # temps en ms entre 2 mises à jour du plateau [modifiable]
pos = [100,100,200,150]

# Dimensions des cases
tl_side = win_dim / (2 * (3 * board_side ** 2 - 3 * board_side + 2) ** 0.5)
tl_size = tl_side * (3 ** 0.5)

# Liste des cases dans le plateau
gameboard = [[0]]
for layer in range(1, board_side):
    gameboard.append(layer * 6 * [0])

# Liste des personnages
characters = {}
characters["marth"]={"ATK":25, "HP":200, "DEF":5},
characters["GOD"]={"ATK":999999999999999, "HP":1, "DEF":99999999999999999999999999999999999999999999999999999999999}
'''
pray for your redemption
'''

'''
# #########
# Fonctions
# #########

# Rotation du plateau complet
def Rotate_board():
    global rotate
    rotate = (rotate + pi / 1440) % (2 * pi)

    # mise à jour de la position de chaque case et de chaque personnage
    for layer in gameboard:
        for tile in layer:
            Tile.Position(tile)
    # afficher les personnages devant les cases [à compléter pour perspective]
    for layer in gameboard:
        for tile in layer:
            if tile.has_char:
                _gameboard.tag_raise(tile.char_gui)

    # attend avant de tourner de nouveau
    _gameboard.after(rotate_delay, Rotate_board)


# ######
# Objets
# ######

# Les cases
class Tile:

    # Création de la case
    def __init__(self, layer, indice):
        # attributs qualitatifs de la case
        self.color = Tile.Tile_type()
        self.type = self.color
        self.clicked = False

        # coordonnées de la case
        self.layer = layer
        try:
            self.side = indice // layer
        except ZeroDivisionError:
            self.side = 0
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

        # création d'un personnage sur la case [provisoire]
        self.has_char = False
        if not self.color == "#0000ff":
            self.Create_char()

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

        # mise à jour de l'emplacement du personnage
        if self.has_char:
            self.Char_position()
    
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
        return choice(["#ff0000", "#00ff00", "#0000ff"])

    # Lorsqu'une case est cliquée
    def Cursor_click(self, mouse):
        # basculer entre couleur d'origine et blanc [provisoire]
        if self.clicked:
            self.type = self.color
        else:
            self.type = "#ffffff"
        _gameboard.itemconfig(self.gui, fill=self.type, outline=self.type)
        self.clicked = not self.clicked

    # Lorsque la souris est au-dessus d'une case
    def Cursor_enter(self, mouse):
        self.type1 = self.color.replace("00", "aa")
        _gameboard.itemconfig(self.gui, fill=self.type1, outline=self.type1)

    # Lorsque la souris n'est plus au-dessus d'une case
    def Cursor_leave(self, mouse):
        _gameboard.itemconfig(self.gui, fill=self.type, outline=self.type)

    # Création d'un personnage sur la case
    def Create_char(self):

        # la case contient un personnage !
        self.has_char = True

        # couleur du personnage [provisoire]
        self.char_type = choice(["white", "black"])

        # positionnement du personnage sur le plateau [provisoire]
        self.char_gui = _gameboard.create_rectangle(0, 0, 0, 0,
                                                    fill=self.char_type,
                                                    outline=self.char_type)

        # actions sur le personnage
        _gameboard.tag_bind(self.char_gui, "<Button-1>", self.Cursor_click)
        _gameboard.tag_bind(self.char_gui, "<Enter>", self.Cursor_enter)
        _gameboard.tag_bind(self.char_gui, "<Leave>", self.Cursor_leave)

    # Positionnement du personnage sur le plateau
    def Char_position(self):
        _gameboard.coords(self.char_gui, self.x - 0.15 * tl_size,
                          self.disp_y - space, self.x + 0.15 * tl_size,
                          self.disp_y)
'''

#crée un rectangle d'actions


def color(event) :
    _gameboard.itemconfig(rec_act, fill = "#404040", outline = "#ffffff")
    

def uncolor(event) :
    _gameboard.itemconfig(rec_act, fill = "#202020")

# ###################
# Programme principal
# ###################

# Canevas sur lequel se déroulera le jeu
_gameboard = tk.Canvas(_game_win, width=win_dim,
                       height=win_dim * vert_scale + space, bg="#000000")
_gameboard.pack()

rec_act = _gameboard.create_rectangle(pos, fill = "#202020", outline = "#ffffff")
rec_txt = _gameboard.create_text(((pos[0]+pos[2])/2,(pos[1]+pos[3])/2), text = "ATK", anchor ="center", fill = "#ffffff")
_gameboard.tag_bind(rec_act, "<Enter>",color)
_gameboard.tag_bind(rec_act, "<Leave>", uncolor)
_gameboard.tag_bind(rec_txt, "<Enter>",color)
_gameboard.tag_bind(rec_txt, "<Leave>", uncolor)



# Création de la fenêtre
_game_win.mainloop()
