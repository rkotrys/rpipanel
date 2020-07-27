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
import conf as panel


class Shutdown(panel.Switchpanel):
    """ shutdown & reload  """
    def __init__(self,app,master,name):
        panel.Switchpanel.__init__(self,app,master,name)

        cnf = self.app.cnf
        fbg = cnf.dml['shutdown']['frm_bg']
        bfg = cnf.dml['shutdown']['btn_fg']
        bbg = cnf.dml['shutdown']['btn_bg']
        bpady=cnf.dml['shutdown']['btn_pady']
        font=( self.monofont, cnf.dml['shutdown']['btn_font_size'])
        padsize=cnf.dml['shutdown']['btn_pad']

        self.frame.config(bg=cnf.dml['shutdown']['frm_self_bg'])

        self.frm = tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        self.frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        btn_frame=tk.Frame(self.frm,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #btn_frame.pack(fill=tk.X)
        btn_frame.grid(row=0,column=0,padx=5,pady=5)
        btn=tk.Button(btn_frame,text="RELOAD",command=partial(hlp.system_exec,"sudo reboot now"),font=font,fg=bfg,bg=bbg,width=10,pady=bpady)
        btn.pack(fill=tk.X)

        btn_frame=tk.Frame(self.frm,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #btn_frame.pack(fill=tk.X)
        btn_frame.grid(row=0,column=1,padx=5,pady=5)
        btn=tk.Button(btn_frame,text="SHUTDOWN",command=partial(hlp.system_exec,"sudo shutdown now"),font=font,fg=bfg,bg=bbg,width=10,pady=bpady)
        btn.pack(fill=tk.X)

        btn_frame=tk.Frame(self.frm,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #btn_frame.pack(fill=tk.X)
        btn_frame.grid(row=1,column=0,padx=5,pady=5)
        btn=tk.Button(btn_frame,text="QUIT",command=quit,font=font,fg=bfg,bg=bbg,width=10,pady=bpady)
        btn.pack(fill=tk.X)

        btn_frame=tk.Frame(self.frm,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #btn_frame.pack(fill=tk.X)
        btn_frame.grid(row=1,column=1,padx=5,pady=5)
        btn=tk.Button(btn_frame,text="CANCEL",command=app.inst.frame_replace,font=font,fg="green",bg=bbg,width=10,pady=bpady)
        btn.pack(fill=tk.X)


class Startpage(panel.Switchpanel):
    """ shutdown & reload  """
    def __init__(self,app,master,name):
        self.app=app
        cnf = self.app.cnf
        font=(cnf.dml["global"]["font"],16)
        panel.Switchpanel.__init__(self,app,master,name)
        self.frame.config(bg="green")
        self.frm = tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg="gray",padx=2,pady=2)
        self.frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        lbl=tk.Label(self.frm,text="Start Page",anchor="w",justify=tk.LEFT,font=font,bg="gray",fg=cnf.dml['topbar']['lbl_fg'])
        lbl.pack(fill=tk.X)
        btn=tk.Button(self.frm,text="NEXT",command=self.app.inst.frame_replace,font=font,fg="black",bg="gray",width=10,pady=2)
        btn.pack(fill=tk.X)


