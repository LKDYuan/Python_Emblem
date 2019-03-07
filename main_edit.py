#!/usr/bin/python
# -*- coding: UTF-8 -*-
##########
# DAI Linkai, TS4
# DJOUKA Yann, TS3
# Python Emblem
##########

import tkinter as tk  # pour tout le GUI
from random import choice  # pour choisir des couleurs au hasard
from math import ceil  # pour une opération spécifique dans le programme


##########
# Variables
##########

# Dimensions maximales du plateau de jeu (provisoire)
max_win_width = 1275
max_win_height = 660

# Cases dans le plateau de jeu (provisoire)
board_width = 10
board_height = 10

# Taille des cases dans le plateau (ne pas modifier)
tl_side = min(max_win_height / (board_height * 1.5 + 0.5),
              (2 * max_win_width * 3 ** 0.5) / (6 * board_width))
tl_size = ((tl_side ** 2 - (tl_side / 2) ** 2) ** 0.5) * 2

# Liste des cases sur le plateau de jeu (provisoire)
gameboard = (board_width * board_height - board_height // 2) * [0]
test_gb = (board_width * board_height - board_height // 2) * [0]


##########
# Programmes
##########

# Choix d'une couleur au hasard (à compléter)
def Tile_type():
    return choice(["Green", "Blue", "Red"])


# x <- x * côté d'une case / largeur d'une case (opération répétée)
def Op(value):
    return value * tl_side / tl_size


# Dans quelle case se trouve le clic?
def Cursor_tile(mouse):
    # initiation d'un compteur (provisoire)
    counter = -1
    # on teste chaque case individuellement (provisoire)
    for tile in gameboard:
        counter += 1

        # définition de variables pour calculer le placement, pour chaque case
        '''limite Ouest x = k1'''
        tmp_w = tile.w
        '''limite Est x = k2'''
        tmp_e = tile.e
        '''limite Nord-Ouest y = a1 * x + b1'''
        tmp_nw = -Op(mouse.x) + Op(tile.x) + tile.y - tl_side
        '''limite Nord-Est y = a2 * x + b2'''
        tmp_ne = Op(mouse.x) - Op(tile.x) + tile.y - tl_side
        '''limite Sud-Est y = a3 * x + b3'''
        tmp_se = -Op(mouse.x) + Op(tile.x) + tile.y + tl_side
        '''limite Sud-Ouest y = a4 * x + b4'''
        tmp_sw = Op(mouse.x) - Op(tile.x) + tile.y + tl_side

        # on teste si le clic est dans la case testée
        if (tmp_w < mouse.x and mouse.x < tmp_e and mouse.y > tmp_nw and
           mouse.y > tmp_ne and mouse.y < tmp_se and mouse.y < tmp_sw):

            # si elle est colorée, on la colorie en blanc (provisoire)
            if not(test_gb[counter] % 2):
                tile.type = "Yellow"
                _gameboard.itemconfig(tile.gui, fill="White")

            # si elle est blanche, on lui redonne sa couleur d'origine
            else:
                tile.type = "Yellow"
                _gameboard.itemconfig(tile.gui, fill=tile.type)
            test_gb[counter] += 1


def Cursor_hover(mouse):
    _gameboard.itemconfigure(tag, text="(%r, %r)" % (mouse.x, mouse.y))
    # on teste chaque case individuellement (provisoire)
    for tile in gameboard:
        # définition de variables pour calculer le placement, pour chaque case
        '''limite Ouest x = k1'''
        tmp_w = tile.w
        '''limite Est x = k2'''
        tmp_e = tile.e
        '''limite Nord-Ouest y = a1 * x + b1'''
        tmp_nw = -Op(mouse.x) + Op(tile.x) + tile.y - tl_side
        '''limite Nord-Est y = a2 * x + b2'''
        tmp_ne = Op(mouse.x) - Op(tile.x) + tile.y - tl_side
        '''limite Sud-Est y = a3 * x + b3'''
        tmp_se = -Op(mouse.x) + Op(tile.x) + tile.y + tl_side
        '''limite Sud-Ouest y = a4 * x + b4'''
        tmp_sw = Op(mouse.x) - Op(tile.x) + tile.y + tl_side

        if (tmp_w < mouse.x and mouse.x < tmp_e and mouse.y > tmp_nw and
           mouse.y > tmp_ne and mouse.y < tmp_se and mouse.y < tmp_sw):
            _gameboard.itemconfig(tile.gui, fill="White")
        else:
            _gameboard.itemconfig(tile.gui, fill=tile.type)


##########
# Éléments du plateau de jeu
##########

# Les cases
class Tile:
    "Dans le plateau, on a des cases à créer, sinon il n'y a pas de jeu"

    # chaque case a un type, des coordonnées et une représentation sur GUI
    def __init__(self, indice):
        global _gameboard

        # définition de la couleur de la case (provisoire)
        self.type = Tile_type()

        # calcul de la position des cases sur le plateau
        '''calcul de la colonne'''
        tmp_var = (indice) % (board_width * 2 - 1)
        if tmp_var >= board_width:
            self.column = tmp_var % board_width * 2 + 1
        else:
            self.column = tmp_var * 2
        '''calcul de la ligne'''
        self.line = ceil((2 * indice + 1) / (board_width * 2 - 1))

        # calcul de la position des cases sur le canevas
        '''quelle position x ?'''
        self.x = (self.column + 1) * (tl_size / 2)
        '''quelle position y ?'''
        self.y = tl_side * (self.line * 1.5 - 0.5)

        # calcul des coordonnées des points délimitant chaque case (provisoire)
        '''côtés gauche et droite'''
        self.w, self.e = self.x - tl_size / 2, self.x + tl_size / 2
        '''sommets haut et bas'''
        self.n, self.s = self.y - tl_side, self.y + tl_side
        '''sommets gauche et droite'''
        self.up, self.dw = self.y - tl_side / 2, self.y + tl_side / 2

        # liste des coordonnées de chaque point (x1, y1, x2, y2,…)
        self.pos = [self.w, self.up, self.x, self.n, self.e, self.up,
                    self.e, self.dw, self.x, self.s, self.w, self.dw]

        # création de la case sur le GUI
        self.gui = _gameboard.create_polygon(self.pos,
                                             fill=self.type, outline="#000000")


##########
# Plateau de jeu
##########

# Mise en place d'un plateau
def Setup_board():
    # le plateau sera accessible dans d'autres fonctions
    global _gameboard, tag

    # fenêtre contenant le plateau
    _game_win = tk.Tk()
    _game_win.title("Python Emblem")

    # taille du plateau
    wd, ht = board_width * tl_size, (board_height * 1.5 + 0.5) * tl_side
    _gameboard = tk.Canvas(_game_win, width=wd, height=ht, bg="#000000")
    # positionnement du plateau dans la fenêtre
    _gameboard.pack()

    # action à faire lors d'un clic
    _gameboard.bind("<Button-1>", Cursor_tile)

    # remplissage de la liste de cases, et du plateau de jeu
    for tl_count in range(len(gameboard)):
        gameboard[tl_count] = Tile(tl_count)
    
    _gameboard.bind("<Motion>", Cursor_hover)
    tag = _gameboard.create_text(0, 0, text="", anchor="nw", fill="white")

    # affichage de la fenêtre
    _game_win.mainloop()


Setup_board()
