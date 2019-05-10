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
_game_win.attributes("-fullscreen", 1)  # plein écran (sur Mac, Linux)
scrn_w = _game_win.winfo_screenwidth()  # largeur de l'écran
scrn_h = _game_win.winfo_screenheight()  # longueur de l'écran
_game_win.title("Python Emblem")  # nom du jeu
vert_scale = 0.35  # facteur d'étirement vertical (effet 3D) [modifiable]
space = scrn_h / vert_scale * 0.05  # espace vide au-dessus du plateau
win_width = min(scrn_h / vert_scale - space, scrn_w)  # largeur du canevas
win_height = win_width * vert_scale + space  # hauteur du canevas
center = win_width / 2  # case du milieu (référentiel)
board_side = 5  # nombre de cases sur un côté du plateau hexagonal [modifiable]
is_player_1 = True  # à quel joueur de jouer?


# Paramètres de la rotation du plateau
original_rotate = 0.4  # rotation d'origine du plateau [modifiable]
rotate = original_rotate  # variable globale de rotation [ne pas modifier]
rotate_delay = 30  # temps en ms entre 2 mises à jour du plateau [modifiable]
rotate_speed = 2  # vitesse d'un demi-tour [modifiable]
rotate_multiplier = 0  # distance entre 2 mises à jour du plateau
is_slowing = False  # mesure de la vitesse de rotation [ne pas modifier]
rotation = True  # rotation au début [ne pas modifier]


# Dimensions des cases
tl_side = win_width / (2 * (3 * board_side ** 2 - 3 * board_side + 2) ** 0.5)
tl_size = tl_side * (3 ** 0.5)

# Liste des cases dans le plateau
gmbrd = [[0]]
for layer in range(1, board_side):
    gmbrd.append(layer * 6 * [0])

# Caractéristiques des cases
tile_types = ["#008800", "#aa0000", "#008800", "#0000bb"]  # Types [provisoire]
unreachable = tile_types[3]  # Sur quels types de cases ne peut-on pas aller?
start_tile_type = "#aaaa00"  # Type des cases de départ
selected_tile = "#ffffff"  # Coloration des cases sélectionnées
adj_tiles = "#ffff00"  # Coloration des cases adjacentes à la sélectionnée
enemy_tile = "#ff0000"  # Coloration des cases des ennemis


# Liste des personnages
characters = {}
characters["Saber"] = {
    "HP": 360, "ATK": 540, "DEF": 200, "MVT": 4, "COL": "#cfcf00",
    }
characters["Lancer"] = {
    "HP": 410, "ATK": 480, "DEF": 280, "MVT": 5, "COL": "#00cfcf",
    }
characters["Tanker"] = {
    "HP": 450, "ATK": 370, "DEF": 390, "MVT": 3, "COL": "#cf00cf",
    }

# Liste des boutons
buts_pos = {}
buts_pos["Play"] = [win_width * 5 / 13, win_height * 3 / 4]
buts_pos["Exit"] = [win_width * 8 / 13, win_height * 3 / 4]
buts_pos["Settings"] = [win_width * 1 / 2, win_height * 3 / 4]
buts_pos["Quit"] = [win_width * 19 / 20, win_height * 59 / 60]
buts_pos["Turn"] = [win_width * 1 / 20, win_height * 59 / 60]

# Caractéristiques des boutons
but_fill = "#000000"
but_outl = "#ffffff"


# #########
# Fonctions
# #########

# Arrêt du programme
def Quit(event=0):
    global _exit_win

    _exit_win = tk.Toplevel(_game_win)
    tk.Label(_exit_win, text="Arrêter le jeu ?"
             ).grid(column=0, columnspan=3, row=0, padx=80, pady=20)
    tk.Button(_exit_win, text="Retour",
              command=lambda: _exit_win.destroy()).grid(column=0, row=1)
    tk.Button(_exit_win, text="Recommencer",
              command=Play).grid(column=1, row=1)
    tk.Button(_exit_win, text="Quitter",
              command=lambda: _game_win.destroy()).grid(column=2, row=1)

    return


# À l'autre de jouer !
def Other_player(event=0):
    global is_player_1

    is_player_1 = not is_player_1
    for layer in gmbrd:
        for tile in layer:
            if tile.has_char:
                tile.char.MVT = characters[tile.char.char]["MVT"]
                tile.char.has_attacked = False
    Rotate_game()

    return


# écran de transition entre le menu de démarrage et le jeu
def Play(event=0):
    global rotation, rotate

    try:
        _exit_win.destroy()
    except NameError:
        pass
    _gmbrd.delete("all")
    _gmbrd.create_text(win_width / 2, win_height / 2, text="Chargement…",
                       font=("Georgia", round(win_width / 24)), tag="tmp",
                       fill="#ffffff")
    rotation = False
    rotate = original_rotate
    _gmbrd.after(1000, Recreate_gmbrd)

    return


# Fonction qui recrée les cases, personnages et boutons
def Recreate_gmbrd():

    _gmbrd.delete("tmp")
    Create_tiles()
    Create_char()
    Button("Quit")
    Button("Turn")

    return


# Création du plateau
def Create_gmbrd():
    global _gmbrd

    _gmbrd = tk.Canvas(_game_win, width=win_width, height=win_height,
                       bg="#000000")
    _gmbrd.pack()

    # créer les cases
    Create_tiles()

    # tourner le plateau [provisoire]
    _gmbrd.after(rotate_delay, Rotate_board)

    # affichage du titre [provisoire]
    _gmbrd.create_text(win_width/2, win_height/2, text="Python Emblem",
                       font=("Georgia", round(win_width / 8)),
                       fill="#ffffff", tag="Title")

    # boutons sur le programme [provisoire]
    Button("Play")
    Button("Exit")
    Button("Settings")

    return


# Création des cases
def Create_tiles():

    for layer in gmbrd:
        for tile in range(len(layer)):
            layer[tile] = Tile(gmbrd.index(layer), tile)

    return


# Création des personnages
def Create_char():

    for layer in gmbrd:
        for tile in layer:
            tile.Create_char()
            if tile.has_char:
                tile.char.Position()
                _gmbrd.tag_raise(tile.char.gui)
                _gmbrd.tag_raise(tile.char.txt)

    return


# Mise à jour de la position de chaque case et de chaque personnage
def Update_display():

    for layer in gmbrd:
        for tile in layer:
            tile.Position()
    for layer in gmbrd:
        for tile in layer:
            if tile.has_char:
                tile.char.Position()

    return


# Rotation du plateau entre le tour de 2 joueurs
def Rotate_game():
    global original_rotate, rotate, rotate_multiplier, is_slowing, rotation

    rotation = True

    # si on a tourné moins d'1/4 de tour, accélérer
    if (rotate - original_rotate) % pi < pi / 2:
        # arrêt de la rotation après 1/2 tour
        if is_slowing:
            rotation, rotate_multiplier, is_slowing = False, 0, False
        # sinon (début du 1/2 tour), accélérer
        else:
            rotate_multiplier += rotate_speed

    # sinon, ralentir
    else:
        rotate_multiplier -= rotate_speed
        is_slowing = True

    # mise à jour de la quantité de rotation du plateau
    rotate = (rotate + pi * rotate_multiplier / 1440) % (2 * pi)

    Update_display()

    # attend avant de tourner de nouveau
    if rotation:
        _gmbrd.after(rotate_delay, Rotate_game)

    return


# Rotation du plateau à vitesse constante (écran d'accueil)
def Rotate_board():
    global rotate, rotation

    rotate = (rotate + pi / 1440) % (2 * pi)

    Update_display()

    # attend avant de tourner de nouveau
    if rotation:
        _gmbrd.after(rotate_delay, Rotate_board)

    return


# Rend aux cases leur couleur d'origine, avant la sélection
def Clear_board(clear_all):

    for layer in gmbrd:
        for tile in layer:
            tile.tmp_reachable = False
            if clear_all:
                tile.type = tile.color
            if tile.has_char:
                tile.char.adj_enemy = False
            tile.Recolor()

    return


# Permet de couper un texte en parties de longueur égale
def Slice_str(string, slice_len):

    str_l = []
    for char in range(0, len(string), slice_len):
        str_l.append(string[char:char+slice_len])

    return str_l


# Change la couleur de quelque chose
def Change(color, change_type, int_col=1):

    # liste temporaire des valeurs de R, G et B
    tmp_l = Slice_str(color[1:], 2)

    # calcul de la nouvelle couleur
    new_color = "#"
    if change_type != "Opp":
        tmp_l2 = Slice_str(change_type[1:], 2)

    # il faut le faire pour chaque couleur primaire
    for i in range(3):
        hex_val = int("0x" + tmp_l[i], 16)

        # couleur inverse
        if change_type == "Opp":
            new_color += format(0xff - hex_val, "#04x")[2:]

        # rajout d'une couleur (par exemple, blanchir case)
        else:
            hex_val = int_col * int("0x" + tmp_l2[i], 16) + hex_val
            new_color += format(round(hex_val / (1 + int_col)), "#04x")[2:]

    return new_color


# ######
# Objets
# ######

# Les boutons
class Button:

    # Donne les coordonées des sommets à partir des points du milieu
    def Coord_but(center):

        return [center[0] - win_width / 20, center[1] - win_width / 60,
                center[0] + win_width / 20, center[1] + win_width / 60]

    # Création des boutons
    def __init__(self, name):

        # attributs qualitatifs des boutons
        self.name = name
        self.fill = "#7f7f7f" if name == "Settings" else but_fill
        self.outl = but_outl

        # position du bouton
        self.center = buts_pos[name]
        self.pos = Button.Coord_but(self.center)

        # représentation graphique
        self.gui = _gmbrd.create_rectangle(self.pos, tag=self.name,
                                           fill=self.fill, outline=self.outl)
        self.txt = _gmbrd.create_text(self.center, text=self.name,
                                      tag=self.name, fill=self.outl,
                                      font=("Georgia", round(win_width / 72)))

        if name == "Settings":
            return

        # actions sur les boutons
        _gmbrd.tag_bind(self.name, "<Enter>", self.Cursor_enter)
        _gmbrd.tag_bind(self.name, "<Leave>", self.Cursor_leave)

        return

    # Changent la couleur du fond quand on passe dessus
    def Cursor_enter(self, event=0):

        _gmbrd.itemconfig(self.gui, fill=Change(self.fill, "#ffffff"))

        return

    # Retour à la couleur d'origine
    def Cursor_leave(self, event=0):

        _gmbrd.itemconfig(self.gui, fill=self.fill)

        return


# Les cases
class Tile:

    # Combien de cases y a-t-il?
    tiles_count = 0
    # A-t-on initié un mouvement pour un personnage?
    clicked = False
    # Compteur des cases parcourues lors d'un mouvement
    MVT_count = 0

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
        _gmbrd.coords(self.gui, self.disp)

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

    # Cases adjacentes à une case sélectionnée [à peaufiner]
    def Reachable_tiles(self, only_enemies=False):

        global temp_bool
        temp_bool = only_enemies

        self.type = selected_tile
        _gmbrd.itemconfig(self.gui, fill=self.type)
        Clear_board(False)

        # pour la case du centre
        if self.layer == 0:
            for tile in gmbrd[1]:
                tile.Reachable()

        # pour les autres cases
        else:
            # cases adjacentes sur la même couche
            for tile in gmbrd[self.layer]:
                if tile.indice == (self.indice + 1) % (self.layer * 6):
                    tile.Reachable()
                if tile.indice == (self.indice - 1) % (self.layer * 6):
                    tile.Reachable()

            # cases adjacentes sur des couches différentes
            # pour les coins d'une couche
            if self.pos == 0:
                # cases sur la couche du dessous
                for tile in gmbrd[self.layer - 1]:
                    if self.layer == 1:
                        tile.Reachable()
                    elif tile.side == self.side and tile.pos == 0:
                        tile.Reachable()

                # cases sur la couche du dessus (sauf pour la dernière couche)
                if self.layer != board_side - 1:
                    for tile in gmbrd[self.layer + 1]:
                        if tile.side == self.side and tile.pos <= 1:
                            tile.Reachable()
                        if (tile.side == (self.side - 1) % 6 and
                           tile.pos == tile.layer - 1):
                            tile.Reachable()

            # pour les côtés d'un couche
            else:
                # cases sur la couche du dessous
                for tile in gmbrd[self.layer - 1]:
                    if (tile.side == self.side and
                       (tile.pos == self.pos or tile.pos == self.pos - 1)):
                        tile.Reachable()
                    if (self.pos % tile.layer == 0 and
                       tile.side == (self.side + 1) % 6 and tile.pos == 0):
                        tile.Reachable()

                # cases sur la couche du dessus (sauf pour la dernière couche)
                if self.layer != board_side - 1:
                    for tile in gmbrd[self.layer + 1]:
                        if (tile.side == self.side and
                           (tile.pos == self.pos or tile.pos == self.pos + 1)):
                            tile.Reachable()

        del temp_bool

        return

    # Cette case adjacente est-elle libre?
    def Reachable(self):

        global temp_bool

        if self.has_char:
            if self.char.player_1 != is_player_1:
                self.char.adj_enemy = True
                self.Reachable_enemy()
        elif (self.type != unreachable and self.type != selected_tile and
              not temp_bool):
            self.tmp_reachable = True
            _gmbrd.itemconfig(self.gui, fill=Change(self.type, adj_tiles, 2))

        return

    # Change la couleur de la case et du personnage ennemi adjacent
    def Reachable_enemy(self):

        _gmbrd.itemconfig(self.gui, fill=Change(self.type, enemy_tile, 3))
        _gmbrd.itemconfig(self.char.gui,
                          fill=Change(self.char.COL, enemy_tile, 3))

        return

    # Les autres cases reprennent leur couleur d'origine
    def Recolor(self):

        if not self.tmp_reachable:
            _gmbrd.itemconfig(self.gui, fill=self.type)
            if self.has_char:
                _gmbrd.itemconfig(self.char.gui, fill=self.char.COL)

        return

    # Création de la case
    def __init__(self, layer, indice):

        # attributs qualitatifs de la case
        self.color = Tile.Tile_type()
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
        self.gui = _gmbrd.create_polygon(0, 0, width=0, fill=self.type,
                                         tag=self.tag)

        # actions sur les cases
        _gmbrd.tag_bind(self.tag, "<Button-1>", self.Cursor_click)
        _gmbrd.tag_bind(self.tag, "<Enter>", self.Cursor_enter)
        _gmbrd.tag_bind(self.tag, "<Leave>", self.Cursor_leave)

        # création d'un personnage sur les cases de départ
        self.has_char = False

        self.Position()

        return

    # Lorsqu'une case est cliquée
    def Cursor_click(self, event=0):

        # rétablir la couleur des cases à la fin d'un mouvement
        if Tile.clicked and self.type == selected_tile:
            Clear_board(True)

            # déplacement du personnage à la case d'arrivée
            Tile.tmp_tile.char.Move(self)

        # enlève des points de vie au personnage adjacent
        elif self.char.adj_enemy and not Tile.tmp_tile.char.has_attacked:
            Clear_board(True)
            tmp = self.char.HP - Tile.tmp_tile.char.ATK + self.char.DEF
            self.char.HP = tmp if tmp < self.char.HP else self.char.HP
            Tile.tmp_tile.char.has_attacked = True
            Tile.tmp_tile.char.Move(Tile.tmp_tile2)
            if self.char.HP <= 0:
                _gmbrd.delete(self.char.gui)
                _gmbrd.delete(self.char.txt)
                self.has_char = False
                del self.char

        # commencer le mouvement lorsqu'on sélectionne un personnage
        elif self.has_char and not Tile.clicked:
            if self.char.player_1 == is_player_1 and self.char.MVT != 0:
                Tile.clicked = True
                Tile.tmp_tile = self
                Tile.tmp_tile2 = self

                # compteur des cases parcourues (pour respecter le mouvement)
                self.MVT_distance = 0
                self.Reachable_tiles()

        Update_display()

        return

    # Lorsque la souris est au-dessus d'une case
    def Cursor_enter(self, event=0):

        # si on passe sur une case déjà sélectionnée, recalculer la trajectoire
        if self.type == selected_tile:
            Tile.MVT_count = self.MVT_distance

            # désélection des cases plus loin dans la trajectoire
            for layer in gmbrd:
                for tile in layer:
                    try:
                        if tile.MVT_distance > self.MVT_distance:
                            del tile.MVT_distance
                            tile.type = tile.color
                            _gmbrd.itemconfig(self.gui, fill=self.type)
                    except AttributeError:
                        pass

            # calcul des cases adjacentes à la nouvelle
            if Tile.MVT_count != Tile.tmp_tile.char.MVT:
                self.Reachable_tiles()

        # si un mouvement a été commencé, continuer à sélectionner des cases
        elif self.tmp_reachable:
            Tile.tmp_tile2 = self
            # le mouvement ne peut pas être supérieur aux points de mouvement
            Tile.MVT_count += 1
            self.MVT_distance = Tile.MVT_count
            if self.MVT_distance < Tile.tmp_tile.char.MVT:
                self.Reachable_tiles()
            elif self.MVT_distance == Tile.tmp_tile.char.MVT:
                self.Reachable_tiles(True)
                self.tmp_reachable = True

        # dans les autres cas, blanchir la case
        else:
            tmp_color = Change(self.color, "#ffffff", 0.5)
            _gmbrd.itemconfig(self.gui, fill=tmp_color)
            if self.has_char:
                if self.char.adj_enemy:
                    self.Reachable_enemy()

        return

    # Lorsque la souris entre dans une case
    def Cursor_leave(self, event=0):

        # si c'est un ennemi qu'on peut attaquer
        if self.has_char and self.char.adj_enemy:
            return

        # sinon, juste blanchir la case
        self.Recolor()

        return

    # Création du personnage sur le plateau de jeu
    def Create_char(self):

        if self.color == start_tile_type:
            self.char = Tile.Character(self)

        return

    # Les cases peuvent contenir des personnages!
    class Character:

        # Attributs de chaque personnage
        def __init__(self, tile):

            # la case contient effectivement un personnage
            tile.has_char = True
            # le personnage appartient effectivement à une case
            self.tile = tile

            # nature des personnages
            # à quel camp appartient-il?
            if tile.side == 1 or tile.side == 2:
                self.player_1 = True
            else:
                self.player_1 = False
            self.adj_enemy = False
            # indication graphique du camp
            if self.player_1:
                self.out = "#ff0000"
            else:
                self.out = "#00ff00"
            # qui est-ce?
            self.char = choice(list(characters.keys()))
            self.HP = characters[self.char]["HP"]
            self.ATK = characters[self.char]["ATK"]
            self.DEF = characters[self.char]["DEF"]
            self.MVT = characters[self.char]["MVT"]
            self.COL = characters[self.char]["COL"]
            self.has_attacked = False

            # représentation graphique du personnage
            self.gui = _gmbrd.create_rectangle(0, 0, 0, 0, width=2,
                                               fill=self.COL,
                                               outline=self.out, tag=tile.tag)
            # affichage des HP
            self.txt = _gmbrd.create_text(0, 0, text=self.HP,
                                          fill=Change(self.COL, "Opp"),
                                          tag=tile.tag)

            return

        # Position du personnage
        def Position(self):

            # Position du personnage
            _gmbrd.coords(self.gui, self.tile.x - 0.15 * tl_size,
                          self.tile.disp_y - tl_side,
                          self.tile.x + 0.15 * tl_size,
                          self.tile.disp_y)

            # Position des HP
            _gmbrd.coords(self.txt, self.tile.x,
                          self.tile.disp_y - tl_side / 2)
            _gmbrd.itemconfig(self.txt, text=self.HP)

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
            self.MVT -= Tile.MVT_count

            # réinitialisation des variables pour un nouveau mouvement
            Tile.clicked = False
            Tile.MVT_count = 0

            # mise à jour des actions sur le personnage (nouvelle case)
            _gmbrd.itemconfig(self.gui, tag=tile.tag)
            _gmbrd.itemconfig(self.txt, tag=tile.tag)

            # mise à jour de la position du personnage sur le canevas
            self.Position()

            return


# ###################
# Programme principal
# ###################

# Canevas sur lequel se déroulera le jeu
Create_gmbrd()

# Actions sur les boutons
_gmbrd.tag_bind("Play", "<Button-1>", Play)
_gmbrd.tag_bind("Exit", "<Button-1>", Quit)
_gmbrd.tag_bind("Quit", "<Button-1>", Quit)
_gmbrd.tag_bind("Turn", "<Button-1>", Other_player)

# Création de la fenêtre
_game_win.mainloop()
