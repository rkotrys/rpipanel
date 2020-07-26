#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys,os
import tkinter as tk
import datetime as dt
import time
from functools import partial
import helper as hlp
import Vkeypad as vk
import Appconfig as Conf
from PIL import Image,ImageDraw,ImageFont,ImageColor,ImageFilter,ImageTk,ImageEnhance
import subprocess as proc
import threading
import configparser as cnfp
import json


class Switchpanel:
    """ virtual class  """

    def __init__(self,app,master,name="switchpanel",size=None):
        dml=app.cnf.dml
        self.master=master
        self.window_name=name
        self.app=app
        self.run=False  # animation start/stop flag
        self.animation=None  # animation functor
        self.animation_step=1000
        if size != None:
            self.width=size[0]
            self.height=size[1]
        else:
            self.width=app.width
            self.height=app.height
        self.fbg=dml['switchwindow']['frm_bg']
        self.bfg=dml['switchwindow']['btn_fg']
        self.bbg=dml['switchwindow']['btn_bg']
        self.bpadx=dml["global"]["btn_pad"]["x"]
        self.bpady=dml["global"]["btn_pad"]["y"]
        self.monofont=dml['global']['font']
        self.fontsize=dml['global']["fonts_size"][app.scrmode]
        self.frame = tk.Frame(master,relief=tk.FLAT, bg=self.fbg, width=self.width, height=self.height, borderwidth=0 )
        self.frame.pack_propagate(0) # don't shrink
        #self.frame.pack(fill=tk.X, anchor=tk.CENTER)
        #self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame.pack(fill=tk.X)

    def run_animation(self):
        if self.run:
            if self.animation != None:
                self.animation()
            self.app.window.after(self.animation_step,self.run_animation)

    def show(self):
        self.frame.pack(fill=tk.X)
        self.run=True
        self.run_animation()

    def hide(self):
        self.frame.pack_forget()
        self.run=False

    def destroy(self):
        self.frame.destroy()

    def name(self):
        return self.window_name

class Conf(Switchpanel):
    """ create pannel with top bar and switchable content  """
    def __init__(self, app, master, name):
        Switchpanel.__init__(self,app,master,name)

    def drow(self,buttons=None):
        if buttons == None:
            self.buttons = [ [ "BACK", partial(print,"[BACK] btn is press") ] ]
        else:
            self.buttons = buttons
        self.tb = Topbar(self.app,self.frame,"tb",self.buttons)

        self.panels = {}
        for item in self.app.cnf.dml["conf"]["pannels"]:
            self.panels[item]=self.app.panels[item](self.app, self.frame, item)
        self.curent_panel=[*self.panels][0]
        self.panels[self.curent_panel].show()


    def switch(self,item):
        for name in self.app.panels:
            if name==item:
                self.panels[name].show()
            else:
                self.panels[name].hide()

class Topbar:
    """ simple top bar with buttons  """
    def __init__(self,app,master,label_text,buttons):
        cnf=app.cnf
        scrsize=app.scrsize
        scrmode=app.scrmode
        self.master=master
        font=( cnf.dml['topbar']['font'], cnf.dml['global']['fonts_size'][scrmode])
        self.frame = tk.Frame(master,relief=tk.FLAT,borderwidth=1, bg=cnf.dml['topbar']['bar_bg'], height=cnf.dml['topbar']['height'])
        self.frame.pack_propagate(0) # don't shrink
        self.frame.pack(fill=tk.X,side=tk.BOTTOM)
        hostname=hlp.readfile("/etc/hostname")
        lbl_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=cnf.dml['topbar']['bar_bg'], width=len(hostname)*cnf.dml['global']['fonts_size'][scrmode])
        lbl_frame.pack_propagate(0) # don't shrink
        lbl_frame.pack(fill=tk.Y, side=tk.LEFT)
        lbl=tk.Label(lbl_frame,text=hostname,anchor="w",justify=tk.LEFT,font=font,bg=cnf.dml['topbar']['lbl_bg'],fg=cnf.dml['topbar']['lbl_fg'])
        lbl.pack(side=tk.LEFT,padx=2)

        btn_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=cnf.dml['topbar']['bar_bg'])
        btn_frame.pack(fill=tk.Y, side=tk.RIGHT)
        for b in buttons:
            btn=tk.Button(btn_frame,text=b[0],command=b[1],relief=tk.RAISED,font=font,fg=cnf.dml['topbar']['btn_fg'],bg=cnf.dml['topbar']['btn_bg'],highlightbackground=cnf.dml['topbar']['lbl_bg'],padx=3,pady=0,bd=1,width=4)
            btn.pack(fill=tk.Y, side=tk.RIGHT)

class P1(Switchpanel):
    """ test p1 """
    def __init__(self,app,master,name):
        Switchpanel.__init__(self,app, master,name)
        frm = tk.Frame(self.frame,relief=tk.FLAT, bg="green",width=100, height=100, )
        frm.pack_propagate(0) # don't shrink
        frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        lbl=tk.Label(frm,text="P1",justify=tk.LEFT,anchor=tk.W, font=(self.monofont,self.fontsize),width=10 )
        lbl.pack()


class P2(Switchpanel):
    """ test p3 """
    def __init__(self,app,master,name):
        Switchpanel.__init__(self,app, master,name)
        frm = tk.Frame(self.frame,relief=tk.FLAT, bg="orange",width=100, height=100, )
        frm.pack_propagate(0) # don't shrink
        frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.lbl=lbl=tk.Label(frm,text="P2",justify=tk.CENTER,anchor=tk.CENTER, font=(self.monofont,self.fontsize),width=4 )
        self.lbl.pack(fill=tk.X)
        def animation():
            now = dt.datetime.now().strftime("%H:%M:%S")
            self.lbl.config(text=now)
        self.animation = animation

class P3(Switchpanel):
    """ test p3 """
    def __init__(self,app,master,name):
        Switchpanel.__init__(self,app, master,name)
        frm = tk.Frame(self.frame,relief=tk.FLAT, bg="lightblue",width=100, height=100, )
        frm.pack_propagate(0) # don't shrink
        frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        lbl=tk.Label(frm,text="P3",justify=tk.RIGHT,anchor=tk.E, font=(self.monofont,self.fontsize),width=10 )
        lbl.pack()


