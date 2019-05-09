
from tkinter import *

fen = Tk()
win_width = fen.winfo_screenwidth()
win_height = fen.winfo_screenheight()
_gameboard = Canvas(fen, width = win_width, height = win_height, bg="#7f7f7f")
_gameboard.pack()


def create_all_buttons() :
    play.create_button()
    quit.create_button()
    close.create_button()
    rematch.create_button()
    '''
#fonction pour jouer
def Play(Event) :
    _gameboard.delete(ALL)
    rotation = False
    create_gameboard()
    rotation()
    create_tiles()
    create_chara()
    _game_win.mainloop()'''

#fonction pour fermer le jeu
def Quit(Event) :
    #rotation = True
    fen.destroy()
'''
#fonction pour rejouer reset le terrain
def Rematch(Event) :
    _gameboard.delete(ALL)
    create_gameboard()
    rotation()
    create_tiles()
    create_chara()
    _game_win.mainloop()
'''

"""
def select_buttons() :
    if rotation :
        _gameboard.delete(rematch)
        _gameboard.delete(quit)
        #_gameboard.delete(options)
    elif rotation == false :
        _gameboard.delet(play)
        _gameboard.delete(close)
        #_gameboard.delete(settings)"""
        

class Button :

    buttons_count = 0

    #fonctions qui décolorent et recolorent les boutons quand on passe dessus
    def Enter(self, Event) :
        _gameboard.itemconfig(self.gui, fill = "#222222")
    
    def Leave(self, Event) :
        _gameboard.itemconfig(self.gui, fill = "#000000")


    
        
    #fonction qui récupère x0, y0, x1, y1 à partir des coordonnées du milieu
    def Coord_rec(xm, ym) :
        x0 = xm - 40
        y0 = ym + 20
        x1 = xm + 40
        y1 = ym -20
        
        return x0, y0, x1, y1
    
    def __init__(self, name):
        
        # index
        Button.buttons_count += 1
        
        self.name = name
        self.fill = "#000000"
        self.outline = "#ffffff"
        
        
        #chaque bouton à un nom et les coordonnées de son milieu
        #solution possible : créer listes à la place de button

        
        if self.name == "Play" :
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
        self.gui = _gameboard.create_rectangle(Button.Coord_rec(self.xm, self.ym), tag=self.name, outline=self.outline,fill=self.fill)
        self.txt = _gameboard.create_text(self.xm, self.ym, text = self.name, anchor = "center", fill = self.outline, tag=self.name)
        
        #actions
        _gameboard.tag_bind(self.name,'<Enter>', self.Enter)
        _gameboard.tag_bind(self.name,'<Leave>', self.Leave)

        
        
play = Button("Play")
close = Button("Close")
quit = Button("Quit")
rematch = Button("Rematch")

#_gameboard.tag_bind("Play",'<Button-1>', Play)
_gameboard.tag_bind("Quit",'<Button-1>', Quit)
_gameboard.tag_bind("Close",'<Button-1>', Quit)
#_gameboard.tag_bind("Rematch",'<Button-1>', Rematch)

#création des boutons
create_all_buttons()
#select_buttons()
#select_actions()
fen.mainloop()
