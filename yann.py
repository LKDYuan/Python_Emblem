
from tkinter import *

fen = Tk()
_gameboard = Canvas(fen, width = fen.winfo_screenwidth() - 20, height = fen.winfo_screenheight() - 20 )

"""
def create_all_buttons() :
    create_button()
    create_button()
    create_button()
    create_button()
"""

def select_buttons() :
    if rotation :
        _gameboard.delete(rematch)
        _gameboard.delete(quit)
        #_gameboard.delete(options)
    elif rotation == false :
        _gameboard.delet(play)
        _gameboard.delete(close)
        #_gameboard.delete(settings)

class Button :

    buttons_count = 0

    #fonctions qui décolorent et recolorent les boutons quand on passe dessus
    def Enter(Event) :
        _gameboard.configure(fill = "#222222")

    def Leave(Event) :
        _gameboard.configure(fill = "#000000")

    #fonction pour jouer
    def Click_play(Event) :
        gameboard.delete(ALL)
        rotation = False
        create_gameboard()
        rotation()
        create_tiles()
        create_chara()
        _game_win.mainloop()

    #fonction pour fermer le jeu
    def Click_quit(Event) :
        rotation = True
        _game_win.destroy()

    #fonction pour rejouer reset le terrain
    def Click_rematch(Event) :
        _gameboard.delete(ALL)
        create_gameboard()
        rotation()
        create_tiles()
        create_chara()
        _game_win.mainloop()
        
    #fonction qui récupère x0, y0, x1, y1 à partir des coordonnées du milieu
    def Coord_rec(xm, ym) :
        x0 = xm - 40
        y0 = ym + 20
        x1 = xm + 40
        y1 = ym -20
        
        return x0, y0, x1, y1
    
    def __init__(self, name, xm, ym):
        
        # index
        self.tag = float(Button.buttons_count)
        Button.buttons_count += 1
        
        self.name = name
        self.fill = "#000000"
        self.outline = "#ffffff"
        self.anchor = center
        
        
        #chaque bouton à un nom et les coordonnées de son milieu
        #solution possible : créer listes à la place de button
        play = Button("Play", win_width/2, 0.75*win_height)
        close = Button("Close", win_width/2, 0.75*win_height + 60)
        quit = Button("Quit", 0.8*win_width + 50, 0.625*win_height)
        rematch = Button("Rematch", 0.8*win_width, 0.625*win_height)
        
        if self.name == "play" :
            self.xm = win_width/2
            self.ym = 0.75*win_height
        elif self.name == "Close" :
            self.xm = win_width/2
            self.ym = 0.75*win_height + 60
        elif self.name == "Quit" :
            self.xm = 0.8*win_width + 50
            self.ym = 0.625*win_height
        elif self.name == "Rematch" :
            self.xm = 0.8*win_width
            self.ym = 0.625*win_height
         
    def create_button(self) :
        self.gui = _gameboard.create_rectangle(self.Coord_rec(self.xm, self.ym))
        self.txt = _gameboard.create_text(self.xm, self.ym, text = self.name, anchor = center)
        
        #actions
        _gameboard.bind(self.gui,'<Enter>', Enter)
        _gameboard.bind(self.txt,'<Enter>', Enter)
        _gameboard.bind(self.gui,'<Leave>', Leave)
        _gameboard.bind(self.txt,'<Leave>', Leave)
        
    def select_actions(self) :
        if self.name == "play" :
            _gameboard.bind(self.tag,'<Button-1>', Click_play)
        elif self.name == "close" or "quit" :
            _gameboard.bind(self.tag,'<Button-1>', Click_quit)
        elif self.name == "rematch" :
            _gameboard.bind(self.tag,'<Button-1>', Click_rematch)
        
        




#création des boutons
#create_all_buttons()
#select_buttons()
#select_actions()
#fen.mainloop()
