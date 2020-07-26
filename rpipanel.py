#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from functools import partial
import Appconfig as Conf
import conf as config_panel
import panels



class Rpipanel:

    state={}
    frames={}
    width=0
    height=0
    scrmode=0
    curent_frame=None
    cnf=None

    def __init__(self,scrmode=0,ini="rpipanel.ini"):

        Rpipanel.cnf=Conf.Appconfig(ini)
        Rpipanel.window = tk.Tk()
        Rpipanel.width = self.window.winfo_screenwidth()
        Rpipanel.height = self.window.winfo_screenheight()

        if Rpipanel.width==320:
            Rpipanel.scrmode=0
            Rpipanel.scrsize=(320,240)
        elif Rpipanel.width==480:
            Rpipanel.scrmode=1
            Rpipanel.scrsize=(480,320)
        elif scrmode==0:
            Rpipanel.scrmode=0
            Rpipanel.scrsize=(320,240)
        else:
            Rpipanel.scrmode=1
            Rpipanel.scrsize=(480,320)

        geometry="{}x{}+0+0".format(Rpipanel.scrsize[0],Rpipanel.scrsize[1])
        Rpipanel.window.overrideredirect(True)
        Rpipanel.window.geometry(geometry)
        Rpipanel.window.config(bg=self.cnf.dml["global"]["frm_bg"])


    def run(self):
        """ App starting point """
        # create config_panal
        Rpipanel.frames["Conf"] = config_panel.Conf(Rpipanel, Rpipanel.window,"Conf")
        # panels dclaration
        Rpipanel.panels={"p1":config_panel.P1,"p2":config_panel.P2,"p3":config_panel.P3}
        # buttons declaration
        buttons = [ [ "BACK", partial(print,"[BACK] btn is press") ],
                    ["p1",partial(Rpipanel.frames["Conf"].switch,"p1") ],
                    ["p2",partial(Rpipanel.frames["Conf"].switch,"p2") ],
                    ["p3",partial(Rpipanel.frames["Conf"].switch,"p3") ],]
        # drow all
        Rpipanel.frames["Conf"].drow(buttons)

        Rpipanel.window.mainloop()

