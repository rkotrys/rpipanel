#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from functools import partial
import Appconfig as Conf
import conf, panels



class Rpipanel:

    state={}
    frames={}
    width=0
    height=0
    scrmode=0
    curent_frame=None
    cnf=None
    inst=None

    def __init__(self,scrmode=0,ini="rpipanel.ini"):

        Rpipanel.inst=self
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
        # panels dictionary dclaration
        Rpipanel.panels={"p1":conf.P1,"p2":conf.P2,"p3":conf.P3}
        # main frame declaration
        Rpipanel.frm_names={ "Startpage":panels.Startpage, "Conf":conf.Conf, "Shutdown":panels.Shutdown }
        # create main frames
        for name in Rpipanel.frm_names:
            Rpipanel.frames[name] = Rpipanel.frm_names[name](Rpipanel, Rpipanel.window, name)
            Rpipanel.frames[name].hide()

        # main frames content initialization
        # -----------------------------------
        # Conf frame
        #------------------------------------
        # buttons declaration
        self.buttons = [ [ "BACK", self.frame_replace ],
                    ["p1",partial(Rpipanel.frames["Conf"].switch,"p1") ],
                    ["p2",partial(Rpipanel.frames["Conf"].switch,"p2") ],
                    ["p3",partial(Rpipanel.frames["Conf"].switch,"p3") ] ]
        # drow all
        Rpipanel.frames["Conf"].drow(self.buttons)
        #------------------------------------

        # set the start frame
        Rpipanel.curent_frame=Rpipanel.frames[[*Rpipanel.frames][0]]
        self.frame_replace("Startpage")

        # run the app main loop
        Rpipanel.window.mainloop()

    def next_frame_name(self,c_name=None):
        if c_name == None:
            c_name =  Rpipanel.curent_frame.name()
        i=0
        r=0
        for name in  Rpipanel.frm_names:
            if name==c_name:
                if i+1<len(Rpipanel.frm_names):
                    r=i+1
                break
            i=i+1
        return [*Rpipanel.frm_names][r]


    def frame_replace(self,name=None):
        if name==None:
            name = self.next_frame_name( Rpipanel.curent_frame.name() )
        Rpipanel.curent_frame.hide()
        Rpipanel.curent_frame=Rpipanel.frames[name]
        Rpipanel.curent_frame.show()
