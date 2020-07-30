#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys,os
import tkinter as tk
import datetime as dt
import time
from functools import partial
import helper as hlp
import Vkeypad as vk
import subprocess as proc
import conf as panel


class Ipconfig(panel.Switchpanel):
    """ IP configuration  """
    def __init__(self,app,master,name):
        panel.Switchpanel.__init__(self,app,master,name)
        self.frames=[]
        self.drowpanel()


    def drowpanel(self):
        global cnf,scrmode,scrsize,dfont
        dml=self.app.dml
        scrmode=self.app.scrmode
        scrsize=self.app.scrsize
        #
        fbg = dml["config"]["frm_bg"]
        frm_padx = dml["config"]["frm_pad"]["x"]
        frm_pady = dml["config"]["frm_pad"]["y"]

        btn_font = (dml["config"]["lbl_font"], dml["global"]["fonts_size"][scrmode])
        bfg = dml["config"]["btn_color"]["fg"]
        bfg_red = dml["config"]["btn_color"]["fg_red"]
        bfg_green = dml["config"]["btn_color"]["fg_green"]
        bbg = dml["config"]["btn_color"]["bg"]
        btn_padx = dml["config"]["btn_pad"]["x"]
        btn_pady = dml["config"]["btn_pad"]["y"]

        lbl_font = (dml["config"]["btn_font"], dml["global"]["fonts_size"][scrmode]-1)
        lbg = dml["config"]["lbl_color"]["bg"]
        lfg = dml["config"]["lbl_color"]["fg"]
        lbl_padx = dml["config"]["lbl_pad"]["x"]
        lbl_pady = dml["config"]["lbl_pad"]["y"]

        hi=hlp.hostinfo();
        self.dev=hi['dev']
        no=0;
        ip={}
        mask={}
        if( len(self.frames)>0 ):
            for f in self.frames:
                f.destroy()
        for d in self.dev:
            frm = tk.Frame(self.frame, bg=fbg,padx=frm_padx,pady=frm_padx,borderwidth=1, relief=tk.RIDGE, width=self.width)
            frm.pack(fill=tk.X)
            self.frames.append(frm)
            dev=d[0]
            mac=d[1]
            ip[no]=tk.StringVar()
            mask[no]=tk.StringVar()

            link=self.linkstate(self)

            frm_dev=tk.Frame(frm, bg=fbg,padx=frm_padx,pady=frm_padx,borderwidth=0,relief=tk.FLAT,width=self.width)
            frm_dev.pack(fill=tk.X)
            lbl=tk.Label(frm_dev,text="{}: {} ".format(dev,mac), font=lbl_font,bg=lbg,fg=lfg,padx=lbl_padx,pady=lbl_pady )
            lbl.pack(side=tk.LEFT)

            btn=tk.Button(frm_dev,text="RM",command=partial(self.updown_btn,dev,"RM"), font=btn_font,bg=bbg,fg=dml["config"]["lbl_color"]["fg_red"],padx=btn_padx,pady=btn_pady,width=4)
            btn.pack(side=tk.RIGHT)
            if( dev.find(".") )<0:
                btn=tk.Button(frm_dev,text="+VLN",command=partial(self.vlanadd_btn,dev), font=btn_font,bg=bbg,fg=bfg,padx=btn_padx,pady=btn_pady,width=4)
                btn.pack(side=tk.RIGHT)
            btn=tk.Button(frm_dev,text="+IP",command=partial(self.addip,dev), font=btn_font,bg=bbg,fg=bfg,padx=btn_padx,pady=btn_pady,width=4)
            btn.pack(side=tk.RIGHT)
            if link[d[0]]=='UP':
                _state="U"
                _bfg=dml["config"]["lbl_color"]["fg_green"]
            else:
                _state="D"
                _bfg=dml["config"]["lbl_color"]["fg_red"]
            btn=tk.Button(frm_dev,text=_state,command=partial(self.updown_btn,dev,_state), font=btn_font,bg=bbg,fg=_bfg,padx=btn_padx,pady=btn_pady,width=4)
            btn.pack(side=tk.RIGHT)


            allip=hlp.getallip(dev)
            if len(allip)>0:
                for _ip in allip:
                    ip[no].set(_ip)
                    frm_ip=tk.Frame(frm, bg=fbg,padx=frm_padx,pady=frm_padx,borderwidth=0,relief=tk.FLAT,width=self.width)
                    frm_ip.pack(fill=tk.X)
                    lbl=tk.Label(frm_ip,text="IP ",font=lbl_font,bg=lbg,fg=lfg,padx=lbl_padx,pady=lbl_pady )
                    lbl.pack(side=tk.LEFT)
                    btn=tk.Button(frm_ip,textvariable=ip[no],command=partial(self.setip, ip[no]),font=btn_font,bg=bbg,fg=bfg,padx=btn_padx,pady=btn_pady,width=18)
                    btn.pack(side=tk.LEFT)
                    if link[d[0]]=='UP':

                        btn=tk.Button(frm_ip,text="RM",command=partial(self.ipset,d[0],ip[no],"delete"),font=btn_font,bg=bbg,fg=bfg_red,padx=btn_padx,pady=btn_pady,width=4)
                        btn.pack(side=tk.RIGHT)
                        btn=tk.Button(frm_ip,text="SET",command=partial(self.ipset,d[0],ip[no]),font=btn_font,bg=bbg,fg=bfg,padx=btn_padx,pady=btn_pady,width=4)
                        btn.pack(side=tk.RIGHT)
                    else:
                        lbl=tk.Label(frm_ip,text=link[d[0]],padx=3,fg="red").pack(side=tk.RIGHT)
                    no=no+1
                    ip[no]=tk.StringVar()
                    mask[no]=tk.StringVar()
            else:
                ip[no].set("")
                mask[no].set("")
                no=no+1
                ip[no]=tk.StringVar()
                mask[no]=tk.StringVar()
            if( dev.find(".") )==0:
                frm_vlan=tk.Frame(self.frame, bg=fbg,padx=frm_padx,pady=frm_padx,borderwidth=0,relief=tk.FLAT,width=self.width)
                frm_vlan.pack(fill=tk.X)
                self.frames.append(frm_vlan)
                btn=tk.Button(frm_vlan,text="Add VLAN Interface",command=partial(self.vlanadd_btn,dev), font=btn_font,bg=bbg,fg=bfg,padx=btn_padx,pady=btn_pady)
                btn.pack(side=tk.TOP)

    def show(self):
        self.frame.pack(fill=tk.X)
        self.run=True
        self.run_animation()
        self.drowpanel()


    def ipset(self, dev, ip, mode="replace"):
        if mode=="replace":
            oldip=hlp.getip(dev)
            cmd="sudo ip a del {} dev {}".format( oldip, dev )
            hlp.system_exec(cmd)
        elif mode=="delete":
            cmd="sudo ip a del {} dev {}".format( ip.get(), dev )
            hlp.system_exec(cmd)
        elif mode=="add":
            cmd="sudo ip a add {} dev {}".format( ip, dev )
            hlp.system_exec(cmd)
        elif mode != "delete":
            cmd="sudo ip a add {} dev {}".format( ip.get(), dev )
            hlp.system_exec(cmd)
        for f in self.frames:
            f.destroy()
        self.frames=[]
        self.drowpanel()


    def linkstate(self,dev):
        link={}
        buf = hlp.system_exec("ip link list")
        for l in buf:
            if l[0]==" ":
                continue
            parts=l.split(": ",3)
            if parts[1]=='lo':
                continue
            if parts[1].find("@") > 1:
                parts[1]=parts[1][:parts[1].find("@")]
            if parts[2].find(" state UP ")>1:
                link[parts[1]]="UP"
            else:
                link[parts[1]]="DOWN"
        return link

    def setip(self,ip):
        self.dialog=vk.Numpad(self.frame, ip.set, ip.get())

    def addip(self,dev):
        self.curent_dev = dev
        self.dialog=vk.Numpad(self.frame, lambda value: self.ipset(self.curent_dev,value,"add"), "192.168.1.100/24")

    def vlanadd_btn(self,dev):
        self.curent_dev = dev
        self.dialog=vk.Numpad(self.frame, self.vlanadd, "2")

    def vlanadd(self,name):
        cmd="sudo ip link add link {} name {}.{} type vlan id {}".format( self.curent_dev, self.curent_dev, name, name )
        hlp.system_exec(cmd)
        for f in self.frames:
            f.destroy()
        self.frames=[]
        self.drowpanel()

    def updown_btn(self,dev,state):
        if state=="U":
            cmd="sudo ip link set {} down".format(dev)
        elif state=="D":
            cmd="sudo ip link set {} up".format(dev)
        else:
            if dev.find(".")>0:
                cmd="sudo ip link delete {}".format(dev)
            else:
                return
        hlp.system_exec(cmd)
        for f in self.frames:
            f.destroy()
        self.frames=[]
        self.drowpanel()
