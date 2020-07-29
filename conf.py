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
        self.app=app
        dml=self.app.dml
        self.master=master
        self.window_name=name
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

    def btn_img_make(self, label, fg, fname="btn_gold_black_50.png", size=(50,50)):
        dml=self.app.dml
        scrmode=self.app.scrmode
        scrsize=self.app.scrsize
        #
        img_bg = Image.open( dml["global"]["images"] + fname )
        font_size = int( size[1] * (28.0/50.0) )
        if img_bg.size!=size:
            img_bg = img_bg.resize(size,resample=Image.BICUBIC)
        font =  ImageFont.truetype( dml["global"]["fonts"]+"segmdl2.ttf", font_size )
        label_str = chr(label)+u""
        draw = ImageDraw.Draw(img_bg)
        label_size = draw.textsize(label_str,font=font)
        t_place = ( int((img_bg.size[0]-label_size[0])/2), int((img_bg.size[0]-label_size[0])/2) )
        draw.text( t_place, text=label_str, font=font, fill=fg )
        return ImageTk.PhotoImage(img_bg)


class Conf(Switchpanel):
    """ create pannel with top bar and switchable content  """
    def __init__(self, app, master, name):
        Switchpanel.__init__(self,app,master,name)

    def drow(self,buttons=None):
        dml=self.app.dml
        if buttons == None:
            # dummy [BACK] button
            self.buttons = [ [ "BACK", partial(print,"[BACK] btn is press") ] ]
        else:
            self.buttons = buttons
        # create menu bar instance
        self.tb = Topbar(self.app,self.frame,"tb",self.buttons)

        ## Load the panels
        self.panels = {}
        # list of instaled pannels names is read form ini file
        for item in dml["conf"]["pannels"]:
            # selectet panels instance inicialization
            self.panels[item]=self.app.panels[item](self.app, self.frame, item)
        # get the first panel
        self.curent_panel=[*self.panels][0]
        # activate the panel
        self.panels[self.curent_panel].show()


    def switch(self,item):
        for name in self.panels:
            if name==item:
                self.panels[name].show()
            else:
                self.panels[name].hide()

class Topbar:
    """ simple top bar with buttons  """
    def __init__(self,app,master,label_text,buttons):
        dml=app.dml
        scrsize=app.scrsize
        scrmode=app.scrmode
        self.master=master
        font=( dml['topbar']['font'], dml['global']['fonts_size'][scrmode])
        self.frame = tk.Frame(master,relief=tk.FLAT,borderwidth=1, bg=dml['topbar']['bar_bg'], height=dml['topbar']['height'])
        self.frame.pack_propagate(0) # don't shrink
        self.frame.pack(fill=tk.X,side=tk.BOTTOM)
        hostname=hlp.readfile("/etc/hostname")
        lbl_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=dml['topbar']['bar_bg'], width=len(hostname)*dml['global']['fonts_size'][scrmode])
        lbl_frame.pack_propagate(0) # don't shrink
        lbl_frame.pack(fill=tk.Y, side=tk.LEFT)
        lbl=tk.Label(lbl_frame,text=hostname,anchor="w",justify=tk.LEFT,font=font,bg=dml['topbar']['lbl_bg'],fg=dml['topbar']['lbl_fg'])
        lbl.pack(side=tk.LEFT,padx=2)

        btn_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=dml['topbar']['bar_bg'])
        btn_frame.pack(fill=tk.Y, side=tk.RIGHT)
        for b in buttons:
            btn=tk.Button(btn_frame,text=b[0],command=b[1],relief=tk.RAISED,font=font,fg=dml['topbar']['btn_fg'],bg=dml['topbar']['btn_bg'],highlightbackground=dml['topbar']['lbl_bg'],padx=3,pady=0,bd=1,width=4)
            btn.pack(fill=tk.Y, side=tk.RIGHT)

class P1(Switchpanel):
    """ test p1 """
    def __init__(self,app,master,name):
        Switchpanel.__init__(self,app, master,name)
        dml=self.app.dml
        frm = tk.Frame(self.frame,relief=tk.FLAT, bg="green",width=100, height=100, )
        frm.pack_propagate(0) # don't shrink
        frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        lbl=tk.Label(frm,text="P1 test",justify=tk.LEFT,anchor=tk.W, font=(self.monofont,self.fontsize),width=20 )
        lbl.pack()


class P2(Switchpanel):
    """ test p3 """
    def __init__(self,app,master,name):
        Switchpanel.__init__(self,app, master,name)
        frm = tk.Frame(self.frame,relief=tk.FLAT, bg="orange",width=100, height=100, )
        frm.pack_propagate(0) # don't shrink
        frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.lbl=lbl=tk.Label(frm,text="P2 test",justify=tk.CENTER,anchor=tk.CENTER, font=(self.monofont,self.fontsize),width=20 )
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
        lbl=tk.Label(frm,text="P3 test",justify=tk.RIGHT,anchor=tk.E, font=(self.monofont,self.fontsize),width=20 )
        lbl.pack()


