#actions sur les boutons virtuels
# Liste des personnages
characters = {}
characters["Marth"] = {"ATK": 25, "HP": 200, "DEF": 5},
characters["God"] = {"ATK": 999999999999999, "HP": 1, "DEF": 99999999999999999}

_gameboard.tag_bind(,,)

_gameboard.tag_bind(self.tag, "<Button-1>", self.Cursor_click)
_gameboard.tag_bind(self.tag, "<Enter>", self.Cursor_enter)
_gameboard.tag_bind(self.tag, "<Leave>", self.Recolor)


_gameboard.create_rectangle(, , , )



.color.replace("00", "77")

#crÃ©er une liste pourles positions individuelles



#crÃ©er un dictionnaire pour les positions

pos_but = {}
pos_but["play"] = {["x0_p"] : 0.25*scrn_h-20, ["y0_p"] : 0.5*scrn_w-50, ["x1_p"] : 0.25*scrn_h+20, ["y1_p"] : 0.5*scrn_w+50}
pos_but["quit"] = {["x0_q"] : 0.25*scrn_h+40, ["y0_q"] : 0.5*scrn_w-50, ["x1_q"] : 0.25*scrn_h+80, ["y1_q"] : 0.5*scrn_w+50}
pos_but["quit2"] = {["x0_q2"] : 0.95*scrn_h+20, ["y0_q2"] : 0.9*scrn_w-20, ["x1_q2"] : 0.95*scrn_h+20, ["y1_q2"] : 0.9*scrn_w+20}
pos_but["sett"] = {["x0_s"] : 0.25*scrn_h+100, ["y0_s"] : 0.5*scrn_w-50, ["x1_s"] : 0.25*scrn_h+140, ["y1_s"] : 0.5*scrn_w+50}
pos_but["sett2"] = {["x0_s2"] : """Ã  complÃ©ter""", ["y0_s2"] : """Ã  complÃ©ter""", ["x1_s2"] : """Ã  complÃ©ter""", ["y1_s2"] : """Ã  complÃ©ter"""}
pos_but["re"]= {["x0_r"] : 0.95*scrn_h-20, ["y0_r"] : 0.9*scrn_w-20, ["x1_r"] : 0.95*scrn_h+20, ["y1_r"] : 0.9*scrn_w+20}

pos_txt = {}
pos_txt["play"] = (pos_but["play"]["x0_p"] + pos_but["play"]["x1_p"])/2, (pos_but["play"]["y0_p"] + pos_but["play"]["y1_p"])/2, anchor = CENTER
pos_txt["quit"] = 0.25*scrn_h+40, 0.5*scrn_w-50, 0.25*scrn_h+80, 0.5*scrn_w+50
pos_txt["quit2"] = 0.95*scrn_h+20, 0.9*scrn_w-20, 0.95*scrn_h+20, 0.9*scrn_w+20
pos_txt["sett"] = 0.25*scrn_h+100, 0.5*scrn_w-50, 0.25*scrn_h+140, 0.5*scrn_w+50
pos_txt["sett2"] = """Ã  complÃ©ter"""
pos_txt["re"]= 0.95*scrn_h-20, 0.9*scrn_w-20, 0.95*scrn_h+20, 0.9*scrn_w+20


class Button :
    
     def __init__(self, name, x0, y0, x1, y1):
        
         self.color = "#000000"
         
         play_but = _gameboard.create_rectangle(pos_but["play"]["x0_p"],["y0_p"]["x1_p"]["y1_p"])        
         quit_but = _gameboard.create_rectangle(pos_but["quit"])
         quit_but2 = _gameboard.create_rectangle(pos_but["quit2"])
         sett_but = _gameboard.create_rectangle(pos_but["sett"])
         sett_but2 = _gameboard.create_rectangle("""" Ã  complÃ©ter""")
         re_but = _gameboard.create_rectangle(pos_but["re"])
         
         
         txt_play = _gameboard.create_text((0.25*scrn_h-20, 0.5*scrn_w-50), text="Play", anchor = CENTER)
         txt_play = _gameboard.create_text((400, 190), text="Play")
         txt_play = _gameboard.create_text((400, 190), text="Quit")
         txt_play = _gameboard.create_text((400, 190), text="Settings")
         txt_play = _gameboard.create_text((400, 190), text="Rematch")
        
        
        self.name = name
        self.fill = "#000000"
        self.outline = "#ffffff"
        self.
        

         
         
"""         
     def Enter_but(Event) :
         _gameboard.configure(fill = "#222222")
         
     def Leave_but(Event) :
         _gameboard.configure(fill = "#000000")
     
     def Click_play_but(Event) :
         _gameboard.delete(ALL)
         rotation = False
         create_gameboard()
         rotation()
         create_tiles()
         create_chara()
         _game_win.mainloop()
     
     def Click_quit_but(Event) :
        rotation = True
        _game_win.destroy()
     
     def Click_re_but(Event) :
         _gameboard.delete(ALL)
         create_gameboard()
         rotation()
         create_tiles()
         create_chara()
         _game_win.mainloop()




















"""
