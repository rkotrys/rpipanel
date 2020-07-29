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
        dml = self.app.dml
        scrsize=self.app.scrsize
        scrmode=self.app.scrmode

        self.frame.config(bg=dml['shutdown']['frm_self_bg'])
        self.canvas = tk.Canvas(self.frame,width=scrsize[0],height=scrsize[1],bg="black",bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH)
        self.drow()


    def drow(self):
        dml = self.app.dml
        scrsize=self.app.scrsize
        scrmode=self.app.scrmode
        fbg = dml['shutdown']['frm_bg']
        bfg = dml['shutdown']['btn_fg']
        bbg = dml['shutdown']['btn_bg']
        bpady=dml['shutdown']['btn_pady']
        font=( self.monofont, dml['shutdown']['btn_font_size'])
        padsize=dml['shutdown']['btn_pad']
        self.btn_img = { "cancel":self.btn_img_make( 0xE248, dml["global"]["theme_btn_colors"][dml["global"]["theme"]], dml["global"]["theme_btn"][dml["global"]["theme"]] ),
                         "reload":self.btn_img_make( 0xE117, dml["global"]["theme_btn_colors"][dml["global"]["theme"]], dml["global"]["theme_btn"][dml["global"]["theme"]] ),
                         "shutdown":self.btn_img_make( 0xE7E8, dml["global"]["theme_btn_colors"][dml["global"]["theme"]], dml["global"]["theme_btn"][dml["global"]["theme"]] ),
                         "color":self.btn_img_make( 0xE2B1, dml["global"]["theme_btn_colors"][dml["global"]["theme"]], dml["global"]["theme_btn"][dml["global"]["theme"]] ),
                         "lock":self.btn_img_make( 0xE1F6, dml["global"]["theme_btn_colors"][dml["global"]["theme"]], dml["global"]["theme_btn"][dml["global"]["theme"]] ) }

        self.canvas.delete("btn")
        self.bgimage = ImageTk.PhotoImage(Image.open( dml["global"]["images"] + dml["global"]["bgimage_names"][dml["global"]["theme"]] ).resize((scrsize[0],scrsize[1]),resample=Image.BICUBIC))
        self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2), image=self.bgimage, tag=("btn","bgphoto") )

        self.canvas.create_image( (int(scrsize[0]*(1.0/4.0)),int(scrsize[1]*(1.0/3.0))), image=self.btn_img['cancel'], tag=("btn","btn_cancel") )
        self.canvas.tag_bind( "btn_cancel", "<Button-1>", partial(self.app.inst.frame_replace, "Clock") )

        self.canvas.create_image( (int(scrsize[0]*(2.0/4.0)),int(scrsize[1]*(1.0/3.0))), image=self.btn_img['color'], tag=("btn","btn_color") )
        self.canvas.tag_bind( "btn_color", "<Button-1>", self.nexttheme )

        self.canvas.create_image( ( int(scrsize[0]*(3.0/4.0)), int(scrsize[1]*(1.0/3.0))), image=self.btn_img['lock'], tag=("btn","btn_lock") )
        self.canvas.tag_bind( "btn_lock", "<Button-1>", partial(self.app.inst.frame_replace, "Lockpin") )
        self.canvas.create_image( ( int(scrsize[0]*(1.0/3.0)), int(scrsize[1]*(2.0/3.0))), image=self.btn_img['reload'], tag=("btn","btn_reload") )
        self.canvas.tag_bind( "btn_reload", "<Button-1>", partial(self.system,"sudo reboot now") )
        self.canvas.create_image( (int(scrsize[0]*(2.0/3.0)),int(scrsize[1]*(2.0/3.0))), image=self.btn_img['shutdown'], tag=("btn","btn_shutdown") )
        self.canvas.tag_bind( "btn_shutdown", "<Button-1>", partial(self.system,"sudo shutdown now") )

    def show(self):
        self.frame.pack(fill=tk.X)
        self.drow()
        self.run=True
        self.run_animation()

    def nexttheme(self,event):
        """ switch to next global pannel theme """
        dml=self.app.dml
        keys = [*dml["global"]["bgimage_names"]]
        for k in range(0,len(keys)):
            if keys[k]==dml["global"]["theme"]:
                if k == len(keys)-1:
                    dml["global"]["theme"] = keys[0]
                else:
                    dml["global"]["theme"] = keys[k+1]
                break
        self.app.cnf.save()
        self.drow()

    def system(self,cmd,event=None):
        hlp.system_exec(cmd)

        #self.frm = tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #self.frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
"""
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
"""

class Startpage(panel.Switchpanel):
    """ shutdown & reload  """
    def __init__(self,app,master,name):
        panel.Switchpanel.__init__(self,app,master,name)
        self.app=app
        dml = self.app.dml
        font=(dml["global"]["font"],16)
        self.frame.config(bg="green")
        self.frm = tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg="gray",padx=2,pady=2)
        self.frm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        lbl=tk.Label(self.frm,text="page",anchor="center",justify=tk.CENTER,font=font,bg="gray",fg=dml['topbar']['lbl_fg'])
        lbl.pack(fill=tk.X)
        btn=tk.Button(self.frm,text="NEXT",command=self.app.inst.frame_replace,font=font,fg="black",bg="gray",width=10,pady=2)
        btn.pack(fill=tk.X)


class Lockpin(panel.Switchpanel):
    """ Lock the screen  """

    _keys = {"1":"btn_black_rect_1.png","2":"btn_black_rect_2.png","3":"btn_black_rect_3.png",
             "4":"btn_black_rect_4.png","5":"btn_black_rect_5.png","6":"btn_black_rect_6.png",
             "7":"btn_black_rect_7.png","8":"btn_black_rect_8.png","9":"btn_black_rect_9.png",
             "*":"btn_black_rect_asterix.png","0":"btn_black_rect_0.png","#":"btn_black_rect_#.png" }

    _keys_label3=["1","2","3","4","5","6","7","8","9","*","0","#" ]
    _keys_label4=["1","2","3","4","5","6","7","8","*","9","0","#" ]

    keys_im = {}
    keys_im_press = {}
    hostinfo = {}

    def __init__(self,app,master,name):
        panel.Switchpanel.__init__(self,app,master,name)
        self.app=app

        #self.app.dmp = Conf.Appconfig(self.app.ini)
        dml = self.app.dml
        scrsize=self.app.scrsize
        scrmode=self.app.scrmode
        self.hostname=hlp.readfile("/etc/hostname")
        Lockpin.hostinfo=hlp.hostinfo();
        self.bgimage= dml["global"]["bgimage_names"][ dml['global']['theme'] ]
        self.key_size_x = dml['lockpin']['keysize'][0]
        self.key_size_y = dml['lockpin']['keysize'][1]
        self.light_time = dml['lockpin']['lighttime']
        self.light_level = dml['lockpin']['lightlevel']
        self.keys_face ={}
        if scrmode==0:
            self.col_no=4
            self.y_start= dml['lockpin']['ystart'][scrmode]
            self.key_size_x = dml['lockpin']['keysize'][scrmode][0]
            self.key_size_y = dml['lockpin']['keysize'][scrmode][1]
            for k in Lockpin._keys_label4:
                self.keys_face[ k ] = Lockpin._keys[ k ]
        else:
            self.col_no=3
            self.y_start= dml['lockpin']['ystart'][scrmode]
            self.key_size_x =  dml['lockpin']['keysize'][scrmode][0]
            self.key_size_y =  dml['lockpin']['keysize'][scrmode][1]
            for k in Lockpin._keys_label3:
                self.keys_face[ k ] = Lockpin._keys[ k ]
        self.pin=""
        self.pin_active=dml['lockpin']['pinactive']
        self.x_start = int((scrsize[0]-self.key_size_x*self.col_no) / 2)
        self.y_start = int((scrsize[1]-self.key_size_y*len(self.keys_face)/self.col_no) / 2)+self.y_start
        self.canvas = tk.Canvas(self.frame,width=scrsize[0],height=scrsize[1],bg="black",bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH)

        self.drowlock()

    def drowlock(self):
        dml = self.app.dml
        scrsize=self.app.scrsize
        scrmode=self.app.scrmode
        self.btn={}
        for f in self.keys_face:
            #img = Image.open( dml["lockpin"]["images"]+self.keys_face[f] ).resize((self.key_size_x,self.key_size_y),resample=Image.BICUBIC)
            img = self.btn_img_make(f,dml["global"]["theme_colors"][dml["global"]["theme"]], dml["global"]["theme_btn"][dml["global"]["theme"]] )
            enhancer = ImageEnhance.Brightness(img)
            Lockpin.keys_im[ f ] = ImageTk.PhotoImage(img)
            Lockpin.keys_im_press[ f ] = ImageTk.PhotoImage( enhancer.enhance(self.light_level) )
        self.font = (dml['lockpin']['display_font'],dml['lockpin']['font_size_l'])
        self.font_s = (dml['lockpin']['font'],dml['lockpin']['font_size_s'])
        self.canvas.delete("lockpin")
        bgimage = Image.open( dml["global"]["images"]+dml["global"]["bgimage_names"][dml["global"]["theme"]]  ).resize((scrsize[0],scrsize[1]),resample=Image.BICUBIC)
        self.btn['bgphoto'] = ImageTk.PhotoImage(bgimage)
        self.btn["display"] = ImageTk.PhotoImage( Image.open( dml["global"]["images"]+dml["global"]["theme_display"][ dml["global"]["theme"] ] ).resize((self.key_size_x*self.col_no,int(self.key_size_y*0.9)),resample=Image.BICUBIC) )
        self.btn["serialbar"] = ImageTk.PhotoImage( Image.open( dml["global"]["images"]+dml["global"]["serial_bar"][ dml["global"]["theme"] ] ) )

        self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2), image=self.btn['bgphoto'], tag=("bgphoto", "lockpin") )
        self.display_y_pos = self.y_start-int(self.key_size_y*0.5)
        self.canvas.create_image( (scrsize[0]/2,self.display_y_pos), image=self.btn["display"], tag=("display", "lockpin") )
        self.canvas.create_image( (scrsize[0]/2,scrsize[1]-12), image=self.btn["serialbar"], tag=("serial", "lockpin") )
        if "Hardware"  in Lockpin.hostinfo:
            serial=Lockpin.hostinfo["Serial"]
        else:
            serial="12345678"
        self.canvas.create_text( scrsize[0]/2,scrsize[1]-12,text=self.hostname+": No "+serial,fill=dml['lockpin']['serial_color'], justify=tk.CENTER, font=self.font_s)
        self.canvas.create_text( scrsize[0]/2,self.display_y_pos,text="LOCKED",fill=dml["global"]["theme_colors"][dml["global"]["theme"]], justify=tk.CENTER, font=self.font, tag=("pintext", "lockpin"))
        for label in Lockpin.keys_im:
            ind=list(Lockpin.keys_im).index(label)
            tag="b_"+label
            col = ind%self.col_no
            row = int(ind / self.col_no)
            position=( self.x_start+self.key_size_x/2+col*self.key_size_x, self.y_start+self.key_size_y/2+row*self.key_size_y)
            btn = self.canvas.create_image( position, image=Lockpin.keys_im[label], tag=(tag, "locklin") )
            self.canvas.tag_bind( btn, "<Button-1>", partial( self.btn_click, tag, position ) )

    def show(self):
        self.frame.pack(fill=tk.X)
        self.run=True
        self.run_animation()
        self.drowlock()

    def clear(self):
        self.canvas.delete("pintext")
        self.pin=""

    def btn_click(self, tag, position, event):
        dml = self.app.dml
        scrsize=self.app.scrsize
        scrmode=self.app.scrmode

        label=tag.split("_",2)[1]
        self.canvas.delete(tag)
        btn=self.canvas.create_image( position, image=Lockpin.keys_im_press[label], tag=tag )
        self.press_tag=tag
        self.press_position=position
        self.master.after( self.light_time, self.btn_relise )
        if label=="#":
            if self.pin==self.pin_active:
                self.clear()
                self._unlock()
            else:
                self.clear()
        elif label=="*":
            self.clear()
            return
        elif len(self.pin)<len(self.pin_active):
            self.pin=self.pin+label
        else:
            self.pin=self.pin[1:]+label
        self.canvas.delete("pintext")
        _tmp=""
        for n in self.pin:
            _tmp=_tmp+"*"
        id = self.canvas.create_text( scrsize[0]/2,self.display_y_pos,text=_tmp,fill=dml["global"]["theme_colors"][dml["global"]["theme"]], justify=tk.CENTER, tag=("pintext", "lockpin"),font=self.font)

    def btn_relise(self):
        dml = self.app.dml
        scrsize=self.app.scrsize
        scrmode=self.app.scrmode
        label=self.press_tag.split("_",2)[1]
        self.canvas.delete(self.press_tag)
        btn=self.canvas.create_image( self.press_position, image=Lockpin.keys_im[label], tag=self.press_tag )
        self.canvas.tag_bind( btn, "<Button-1>", partial( self.btn_click, self.press_tag, self.press_position ) )

    def _unlock(self):
        self.app.inst.frame_replace()

    def btn_img_make(self, label, fg, fname="btn_gold_black_50.png", size=(40,40)):
        dml=self.app.dml
        scrmode=self.app.scrmode
        scrsize=self.app.scrsize
        #
        img_bg = Image.open( dml["global"]["images"] + fname )
        font_size = 28
        if img_bg.size!=size:
            img_bg = img_bg.resize(size,resample=Image.BICUBIC)
        font =  ImageFont.truetype( dml["global"]["fonts"]+dml["lockpin"]["btn_font"], font_size )
        label_str = u"{}".format(label)
        draw = ImageDraw.Draw(img_bg)
        label_size = draw.textsize(label_str,font=font)
        if label=="*": corect=5
        else: corect=0
        t_place = ( int((img_bg.size[0]-label_size[0])/2), int((img_bg.size[1]-label_size[1])/2)+corect )
        draw.text( t_place, text=label_str, font=font, fill=dml["global"]["theme_btn_colors"][ dml["global"]["theme"] ] )
        return img_bg



class Systeminfo(panel.Switchpanel):
    """ system info  """
    def __init__(self,app,master,name):
        panel.Switchpanel.__init__(self,app,master,name)
        dml=self.app.dml
        scrsize=self.app.scrsize
        scrmode=self.app.scrmode
        monofont=dml['global']['font']
        bpady=15
        padsize=5
        hi=hlp.hostinfo()
        dev=hi['dev']
        #print(hi)
        mt=int(hi['MemTotal'].split(" ",1)[0]) / 1000
        mf=int(hi['MemAvailable'].split(" ",1)[0]) / 1000
        self.frame.config(bg=dml['systeminfo']['frm_bg'])
        self.info_frame = tk.Frame(self.frame,relief=tk.FLAT, bg=dml['systeminfo']['frm_bg'])
        #self.frame.pack_propagate(0) # don't shrink
        self.info_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        hostname = hlp.readfile('/etc/hostname')
        if 'Hardware' in hi:
            info2=hi['model name']+", "+hi['processor']+" core\nHardware: "+hi['Hardware']+", Ser.: "+hi['Serial']+"\n"+hi['Distributor ID']+' '+hi['Release']+' '+hi['Codename']+" - "+hi['system']+"\nMemory: {:4.0f} MB total, {:4.0f} MB free".format(mt,mf)
        else:
            info2=hi['model name']+", "+hi['processor']+" core\n"+hi['Distributor ID']+' '+hi['Release']+' '+hi['Codename']+" - "+hi['system']+"\nMemory: {:4.0f} MB total, {:4.0f} MB free".format(mt,mf)
        info3="{:<6} {:<17} {}".format( "DEV:","MAC:", "IPv4:" )
        info4=""
        for d in dev:
            info4=info4+"{:<6} {:^16} {}\n".format( d[0],d[1], hlp.getip(d[0]).split("/",1)[0] )
        mmcinfo=hlp.getmmcinfo()
        info2 = info2 + "\nMMC: {}, {} free, PARTUUID: {}".format(mmcinfo['size'],mmcinfo['free'],mmcinfo['PARTUUID'])
        lbl=tk.Label(self.info_frame,text=hostname,justify=tk.CENTER,anchor=tk.CENTER,font=(monofont,dml['systeminfo']['font_size']['name']),bg=dml['systeminfo']['frm_bg'], fg=dml['systeminfo']['lbl_name_fg'],pady=3 )
        lbl.pack(fill=tk.X)
        lbl=tk.Label(self.info_frame,text=info2,justify=tk.CENTER,anchor=tk.CENTER, font=(monofont,dml['global']['fonts_size'][scrmode]), bg=dml['systeminfo']['frm_bg'], fg=dml['systeminfo']['lbl_sys_fg'])
        lbl.pack(fill=tk.X)
        lbl=tk.Label(self.info_frame,text=info3,justify=tk.LEFT,anchor="nw", font=(monofont,dml['global']['fonts_size'][scrmode]), bg=dml['systeminfo']['frm_bg'], fg=dml['systeminfo']['lbl_title_fg'])
        lbl.pack(fill=tk.X)
        self.lbl=tk.Label(self.info_frame,text=info4,justify=tk.LEFT,anchor="nw",font=(monofont,dml['global']['fonts_size'][scrmode]), bg=dml['systeminfo']['frm_bg'], fg=dml['systeminfo']['lbl_dev_fg'])
        self.lbl.pack(fill=tk.X)
        self.animation=self.getnetworks()

    def getnetworks(self):
        hi=hlp.hostinfo();
        dev=hi['dev']
        info=""
        for d in dev:
            info=info+"{:<6} {:^16} {}\n".format( d[0],d[1], hlp.getip(d[0]).split("/",1)[0] )
        error=False
        try:
            self.lbl.config(text=info)
        except:
            error=True
        if not error:
            self.master.after(10000, self.getnetworks)

