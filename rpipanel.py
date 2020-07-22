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

dfont=[9,12]

class Topbar:
    """ simple top bar with buttons  """
    def __init__(self,master,label_text,buttons):
        global cnf,scrsize,scrmode
        self.master=master
        maxwidth=scrsize[0]
        maxheight=scrsize[1]
        font=( cnf.dml['topbar']['font'], cnf.dml['global']['fonts_size'][scrmode])
        self.frame = tk.Frame(master,relief=tk.FLAT,borderwidth=1,bg=cnf.dml['topbar']['bar_bg'],height=cnf.dml['topbar']['height'])
        self.frame.pack_propagate(0) # don't shrink
        self.frame.pack(fill=tk.X)
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


class Switchwindow:
    """ virtual class  """
    def __init__(self,master,name):
        global cnf,scrsize
        self.master=master
        self.window_name=name

        self.width=scrsize[0]
        self.height=scrsize[1]
        self.fbg=cnf.dml['switchwindow']['frm_bg']
        self.bfg=cnf.dml['switchwindow']['btn_fg']
        self.bbg=cnf.dml['switchwindow']['btn_bg']
        self.bpadx=2
        self.bpady=2
        self.monofont=cnf.dml['global']['font']
        self.frame = tk.Frame(master,relief=tk.FLAT, bg=self.fbg, width=self.width, height=(self.height-cnf.dml['topbar']['height']), borderwidth=0 )
        self.frame.pack_propagate(0) # don't shrink
        #self.frame.pack(fill=tk.X, anchor=tk.CENTER)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()

    def name(self):
        return self.window_name

class Shutdown(Switchwindow):
    """ shutdown & reload  """
    def __init__(self,master,name):
        global cnf
        Switchwindow.__init__(self,master,name)

        fbg = cnf.dml['shutdown']['frm_bg']
        bfg = cnf.dml['shutdown']['btn_fg']
        bbg = cnf.dml['shutdown']['btn_bg']
        bpady=cnf.dml['shutdown']['btn_pady']
        font=(cnf.dml['global']['font'], cnf.dml['shutdown']['btn_font_size'])
        padsize=cnf.dml['shutdown']['btn_pad']
        self.frame.config(bg=fbg)

        master.config(bg=fbg)
        btn_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #btn_frame.pack(fill=tk.X)
        btn_frame.grid(row=0,column=0,padx=5,pady=5)
        btn=tk.Button(btn_frame,text="RELOAD",command=partial(hlp.system_exec,"sudo reboot now"),font=font,fg=bfg,bg=bbg,width=10,pady=bpady)
        btn.pack(fill=tk.X)

        btn_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #btn_frame.pack(fill=tk.X)
        btn_frame.grid(row=0,column=1,padx=5,pady=5)
        btn=tk.Button(btn_frame,text="SHUTDOWN",command=partial(hlp.system_exec,"sudo shutdown now"),font=font,fg=bfg,bg=bbg,width=10,pady=bpady)
        btn.pack(fill=tk.X)

        btn_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #btn_frame.pack(fill=tk.X)
        btn_frame.grid(row=1,column=0,padx=5,pady=5)
        btn=tk.Button(btn_frame,text="QUIT",command=quit,font=font,fg=bfg,bg=bbg,width=10,pady=bpady)
        btn.pack(fill=tk.X)

        btn_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=padsize,pady=padsize)
        #btn_frame.pack(fill=tk.X)
        btn_frame.grid(row=1,column=1,padx=5,pady=5)
        btn=tk.Button(btn_frame,text="CANCEL",command=partial(_framereplace,"QUIT",master,Shutdown),font=font,fg="green",bg=bbg,width=10,pady=bpady)
        btn.pack(fill=tk.X)


class Lockpin(Switchwindow):
    """ Lock the screen  """
    global cnf
    images = "images/"
    _keys_label3={"1":"btn_black_rect_1.png","2":"btn_black_rect_2.png","3":"btn_black_rect_3.png",
                  "4":"btn_black_rect_4.png","5":"btn_black_rect_5.png","6":"btn_black_rect_6.png",
                  "7":"btn_black_rect_7.png","8":"btn_black_rect_8.png","9":"btn_black_rect_9.png",
                  "*":"btn_black_rect_asterix.png","0":"btn_black_rect_0.png","#":"btn_black_rect_#.png" }
    _keys_label4={"1":"btn_black_rect_1.png","2":"btn_black_rect_2.png","3":"btn_black_rect_3.png","4":"btn_black_rect_4.png",
                  "5":"btn_black_rect_5.png","6":"btn_black_rect_6.png","7":"btn_black_rect_7.png","8":"btn_black_rect_8.png",
                  "*":"btn_black_rect_asterix.png","9":"btn_black_rect_9.png","0":"btn_black_rect_0.png","#":"btn_black_rect_#.png" }
    keys_label=_keys_label3

    keys_im = {}
    keys_im_press = {}
    hi = {}

    def __init__(self,master,name):
        global cnf,scrmode,scrsize
        Switchwindow.__init__(self,master,name)
        self.frame.config(height=scrsize[1])
        self.hostname=hlp.readfile("/etc/hostname")
        Lockpin.hi=hlp.hostinfo();

        self.display= cnf.dml['lockpin']['display']
        self.bgimage= cnf.dml['lockpin']['background']
        self.gold_bar_img=cnf.dml['lockpin']['serial_bar']
        self.key_size_x = cnf.dml['lockpin']['keysize'][0]
        self.key_size_y = cnf.dml['lockpin']['keysize'][1]
        self.light_time = cnf.dml['lockpin']['lighttime']
        self.light_level = cnf.dml['lockpin']['lightlevel']

        if scrmode==0:
            sekf.col_no=4
            self.y_start=cnf.dml['lockpin']['ystart'][scrmode]
            self.key_size_x = cnf.dml['lockpin']['keysize'][scrmode][0]
            self.key_size_y = cnf.dml['lockpin']['keysize'][scrmode][1]
            self.keys_face=Lockpin._keys_label4
        else:
            self.col_no=3
            self.y_start=cnf.dml['lockpin']['ystart'][scrmode]
            self.key_size_x = cnf.dml['lockpin']['keysize'][scrmode][0]
            self.key_size_y = cnf.dml['lockpin']['keysize'][scrmode][1]
            self.keys_face=Lockpin._keys_label3
        self.pin=""
        self.pin_active=cnf.dml['lockpin']['pinactive']
        self.x_start = int((scrsize[0]-self.key_size_x*self.col_no) / 2)
        self.y_start = int((scrsize[1]-self.key_size_y*len(self.keys_face)/self.col_no) / 2)+self.y_start

        for f in Lockpin.keys_label:
            img = Image.open( Lockpin.images+self.keys_label[f] ).resize((self.key_size_x,self.key_size_y),resample=Image.BICUBIC)
            enhancer = ImageEnhance.Brightness(img)
            Lockpin.keys_im[ f ] = ImageTk.PhotoImage(img)
            Lockpin.keys_im_press[ f ] = ImageTk.PhotoImage( enhancer.enhance(self.light_level) )
        self.font = (cnf.dml['lockpin']['display_font'],cnf.dml['lockpin']['font_size_l'])
        self.font_s = (cnf.dml['lockpin']['font'],cnf.dml['lockpin']['font_size_s'])
        self.canvas = tk.Canvas(self.frame,width=scrsize[0],height=scrsize[1],bg="black",bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH)

        self.btn={}
        bgimage = Image.open( Lockpin.images+self.bgimage ).resize((scrsize[0],scrsize[1]),resample=Image.BICUBIC)
        self.btn['bgphoto'] = ImageTk.PhotoImage(bgimage)
        self.btn["display"] = ImageTk.PhotoImage( Image.open( Lockpin.images+self.display ).resize((self.key_size_x*self.col_no,int(self.key_size_y*0.9)),resample=Image.BICUBIC) )
        self.btn["goldbar"] = ImageTk.PhotoImage( Image.open( Lockpin.images+self.gold_bar_img ) )

        self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2), image=self.btn['bgphoto'], tag="bgphoto" )
        self.display_y_pos = self.y_start-int(self.key_size_y*0.5)
        self.canvas.create_image( (scrsize[0]/2,self.display_y_pos), image=self.btn["display"], tag="display" )
        self.canvas.create_image( (scrsize[0]/2,scrsize[1]-12), image=self.btn["goldbar"] )
        if "Hardware"  in Lockpin.hi:
            serial=Lockpin.hi["Serial"]
        else:
            serial="12345678"
        self.canvas.create_text( scrsize[0]/2,scrsize[1]-12,text=self.hostname+": No "+serial,fill=cnf.dml['lockpin']['serial_color'], justify=tk.CENTER, font=self.font_s)
        for label in Lockpin.keys_im:
            ind=list(Lockpin.keys_im).index(label)
            tag="b_"+label
            col = ind%self.col_no
            row = int(ind / self.col_no)
            position=( self.x_start+self.key_size_x/2+col*self.key_size_x, self.y_start+self.key_size_y/2+row*self.key_size_y)
            btn = self.canvas.create_image( position, image=Lockpin.keys_im[label], tag=tag )
            self.canvas.tag_bind( btn, "<Button-1>", partial( self.btn_click, tag, position ) )

    def clear(self):
        self.canvas.delete("pintext")
        self.pin=""

    def btn_click(self, tag, position, event):
        global cnf,scrsize
        label=tag.split("_",2)[1]
        self.canvas.delete(tag)
        btn=self.canvas.create_image( position, image=Lockpin.keys_im_press[label], tag=tag )
        self.press_tag=tag
        self.press_position=position
        self.master.after( self.light_time, self.btn_relise )
        if label=="#":
            if self.pin==self.pin_active:
                self.clear()
                _unlock()
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
        id = self.canvas.create_text( scrsize[0]/2,self.display_y_pos,text=_tmp,fill=cnf.dml['lockpin']['display_color'], justify=tk.CENTER, tag="pintext",font=self.font)

    def btn_relise(self):
        label=self.press_tag.split("_",2)[1]
        self.canvas.delete(self.press_tag)
        btn=self.canvas.create_image( self.press_position, image=Lockpin.keys_im[label], tag=self.press_tag )
        self.canvas.tag_bind( btn, "<Button-1>", partial( self.btn_click, self.press_tag, self.press_position ) )


class Clock(Switchwindow):
    """ clock  """
    global cnf,scrmode
    images = "images/"
    #baksnames = [ "z1b_gold_transparent.png","z1b_blue_transparent.png","z1b_green_transparent.png","z1b_red_transparent.png","z1b_transparent.png","z3b_gold_transparent.png","z3b_blue_transparent.png","z3b_green_transparent.png","z3b_red_transparent.png","z3b_purple_transparent.png","z3b_transparent.png" ]
    backs = []

    def __init__(self,master,name):
        global cnf,scrmode,scrsize
        Switchwindow.__init__(self,master,name)
        self.fbg=cnf.dml['clock']['frm_bg']
        self.bfg=cnf.dml['clock']['btn_fg']
        self.face_names={"gold":"z1b_gold_transparent.png","blue":"z1b_blue_transparent.png","green":"z1b_green_transparent.png","red":"z1b_red_transparent.png","purple":"z1b_purple_transparent.png","black":"z1b_black_transparent.png"}
        self.bgimage_names={"gold":"mesh_gold_480x320.png","blue":"mesh_blue_480x320.png","green":"mesh_green_480x320.png","red":"mesh_red_480x320.png","purple":"mesh_purple_480x320.png","black":"mesh_black_480x320.png"}
        #bgimage_name="mesh_gold_480x320.png"

        self.ind=cnf.dml['clock']['ind']
        self.ind1=cnf.dml['clock']['ind1']
        self.ind2=cnf.dml['clock']['ind2']
        self.s_color = cnf.dml['clock']['s_color']
        self.m_color = cnf.dml['clock']['m_color']
        self.h_color = cnf.dml['clock']['h_color']
        self.outline_color = cnf.dml['clock']['outline_color']
        self.arrowsize = cnf.dml['clock']['arrowsize']
        self.symbol_size = cnf.dml['clock']['symbol_size']
        self.ttf_size = cnf.dml['clock']['ttf_size']
        self.colck_y_ofset = cnf.dml['clock']['colck_y_ofset']

        self.face={}
        self.bgimage={}
        self.images = {}
        for n in self.face_names:
            self.face[n]=Image.open( Clock.images + self.face_names[n] ).resize((scrsize[1]-45,scrsize[1]-45),resample=Image.BICUBIC)
            self.bgimage[n]=Image.open( Clock.images + self.bgimage_names[n] ).resize((scrsize[0],scrsize[1]),resample=Image.BICUBIC)
        self.run_bgimage = ImageTk.PhotoImage(self.bgimage[ [*self.bgimage][self.ind2] ])
        img = Image.open( Clock.images + cnf.dml['clock']['btn_next_img'] )
        img_r = img.rotate( 180, Image.BICUBIC )
        self.images['btn_next']= ImageTk.PhotoImage( img )
        self.images['btn_back']= ImageTk.PhotoImage( img_r )

        self.fontXL = ImageFont.truetype("./fonts/tahomabd.ttf", self.ttf_size['XL'])
        self.fontL = ImageFont.truetype("./fonts/tahomabd.ttf", self.ttf_size['XL'])
        self.fontM = ImageFont.truetype("./fonts/lucon.ttf", self.ttf_size['M'])
        self.symbolsL = ImageFont.truetype("./fonts/segmdl2.ttf", self.symbol_size['L'])
        self.symbolsXL = ImageFont.truetype("./fonts/segmdl2.ttf", self.symbol_size['XL'])

        self.time=tk.StringVar()
        self.frame.config(bg=self.fbg)
        self.time.set(time.strftime('%-H:%M:%S'))

        self.canvas = tk.Canvas(self.frame,width=scrsize[0],height=scrsize[1],bg="black",bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH)
        self.drow_all()

        self.settime()

    def drow_all(self):
        self.canvas.delete("clock")
        self.canvas.delete("btn_next1")
        self.canvas.delete("btn_next2")
        self.canvas.delete("bgphoto")

        self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2-cnf.dml['topbar']['height']), image=self.run_bgimage, tag="bgphoto" )
        self.run_face=self.drowclock()
        self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2-self.colck_y_ofset), image=self.run_face, tag="clock" )
        self.canvas.create_image( (scrsize[0]-30,scrsize[1]-60), image=self.images['btn_next'], tag="btn_next1" )
        self.canvas.tag_bind( "btn_next1", "<Button-1>", self.nextface )
        self.canvas.create_image( (scrsize[0]-30,scrsize[1]-120), image=self.images['btn_next'], tag="btn_next2" )
        self.canvas.tag_bind( "btn_next2", "<Button-1>", self.nextbg )

        self.canvas.create_image( (30,scrsize[1]-60), image=self.images['btn_back'], tag="btn_back1" )
        self.canvas.tag_bind( "btn_back1", "<Button-1>", self.backface )
        self.canvas.create_image( (30,scrsize[1]-120), image=self.images['btn_back'], tag="btn_back2" )
        self.canvas.tag_bind( "btn_back2", "<Button-1>", self.backbg )



    def nextface(self,event):
        global cnf
        keys = [*self.face]
        if self.ind1 < len(self.face)-1:
            self.ind1=self.ind1+1;
        else:
            self.ind1 = 0;
        cnf.dml['clock']['ind1']=self.ind1
        cnf.save()

    def backface(self,event):
        global cnf
        keys = [*self.face]
        self.ind1=self.ind1-1;
        if self.ind1 < 0:
            self.ind1 = len(self.face)-1;
        cnf.dml['clock']['ind1']=self.ind1
        cnf.save()


    def nextbg(self,event):
        """  ???  """
        global cnf
        keys = [*self.bgimage]
        if self.ind2 < len(self.bgimage)-1:
            self.ind2=self.ind2+1
        else:
            self.ind2 = 0;
        cnf.dml['clock']['ind2']=self.ind2
        self.run_bgimage = ImageTk.PhotoImage( self.bgimage[ keys[self.ind2] ] )
        self.drow_all()
        cnf.save()

    def backbg(self,event):
        """  ???  """
        global cnf
        keys = [*self.bgimage]
        self.ind2=self.ind2-1
        if self.ind2 < 0:
            self.ind2 = len(self.bgimage)-1
        cnf.dml['clock']['ind2']=self.ind2
        self.run_bgimage = ImageTk.PhotoImage( self.bgimage[ keys[self.ind2] ] )
        self.drow_all()
        cnf.save()

    def drowclock(self):
        global scrmode,scrsize
        iconcolor = (225,180,0) #(200,200,255)
        tm = time.localtime()
        image = self.face[[*self.face][self.ind1]].copy()
        im = Image.new( "RGBA", image.size, (255,255,255,255) )
        im.paste(image)
        draw = ImageDraw.Draw(im)
        if scrmode==0:
            hands=(12,25,35)
            self.arrowsize=10
        else:
            hands=(24,50,70)
            self.arrowsize=15
        if scrmode==0:
            font=self.fontL
            symbols=self.symbolsL
            symbol_size=self.symbol_L
        else:
            font=self.fontXL
            symbols=self.symbolsXL
            symbol_size=self.symbol_size['XL']
        draw.text( (im.size[0]/2-symbol_size/2,im.size[1]/4), chr(0xE774)+u'', font=symbols, fill=iconcolor )
        temperature = hlp.getcputemp()+u"°C"
        tm_size = draw.textsize(temperature,font=font)
        draw.text( (int(im.size[0]/2-tm_size[0]/2+5), int(im.size[1]*2/3-tm_size[1]/2) ), temperature, font=font, fill=iconcolor )
        im = Image.alpha_composite( im, self.drawhands( (tm[3],tm[4],tm[5]), hands, image ) )
        return ImageTk.PhotoImage(im)



    def drawhands( self, t, r, image ):
        x = int(image.size[0]/2)
        y = int(image.size[1]/2)
        im = Image.new( "RGBA", image.size, (255,255,255,0) )
        dr = ImageDraw.Draw( im )
        dr.polygon( [(x-3,y), (x+3,y), (x+3,r[2]), (x+6,r[2]),(x,r[2]-self.arrowsize),(x-6,r[2]),(x-3,r[2])], fill=self.h_color, outline=self.outline_color )
        h = t[0] if t[0]<13 else t[0]-12
        him = im.rotate( -(h*30+t[1]*0.5), Image.BICUBIC )
        im = Image.new( "RGBA", image.size, (255,255,255,0) )
        dr = ImageDraw.Draw( im )
        dr.polygon( [(x-2,y+20), (x+2,y+20), (x+2,r[1]),(x+5,r[1]),(x,r[1]-self.arrowsize),(x-5,r[1]), (x-2,r[1])], fill = self.h_color, outline=self.outline_color )
        hmim =Image.alpha_composite( him, im.rotate( -(360*t[1])/60, Image.BICUBIC ) )
        im = Image.new( "RGBA", image.size, (255,255,255,0) )
        dr = ImageDraw.Draw( im )
        dr.line([ ( x, y+30 ), ( x, r[0]+10)], fill = self.s_color, width = 2 )
        dr.line([ ( x-3, r[0]+10 ), ( x, r[0]), ( x+3, r[0]+10 ), ( x-3, r[0]+10 )], fill = self.s_color, width = 2 )
        dr.ellipse([x-7,y-7,x+7,y+7],fill=self.s_color,outline='#777')
        return Image.alpha_composite( hmim, im.rotate( -(360*t[2])/60, Image.BICUBIC ) )


    def settime(self):
        error=False
        try:
            self.canvas.delete("clocl")
        except:
            error=True
        if not error:
            self.master.after(1000,self.settime)
            self.images["clock"]=self.drowclock()
            self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2-self.colck_y_ofset), image=self.images['clock'], tag="clock" )


class Systeminfo(Switchwindow):
    """ system info  """
    def __init__(self,master,name):
        global scrmode,scrsize,dfont
        Switchwindow.__init__(self,master,name)
        fbg = "black"
        ffg = "#ffffff"
        bfg = "darkred"
        bbg = "#ffbf00"
        monofont="DejaVu Sans Mono";
        bpady=15
        padsize=5
        self.master=master
        hi=hlp.hostinfo();
        dev=hi['dev']
        #print(hi)
        mt=int(hi['MemTotal'].split(" ",1)[0]) / 1000
        mf=int(hi['MemAvailable'].split(" ",1)[0]) / 1000
        self.frame.config(bg=fbg)
        self.info_frame = tk.Frame(self.frame,relief=tk.FLAT, bg=fbg)
        #self.frame.pack_propagate(0) # don't shrink
        self.info_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        info1 = hlp.readfile('/etc/hostname')
        if 'Hardware' in hi:
            info2=hi['model name']+", "+hi['processor']+" core\nHardware: "+hi['Hardware']+", Ser.: "+hi['Serial']+"\n"+hi['Distributor ID']+' '+hi['Release']+' '+hi['Codename']+" - "+hi['system']+"\nMemory: {:4.0f} MB total, {:4.0f} MB free".format(mt,mf)
        else:
            info2=hi['model name']+", "+hi['processor']+" core\n"+hi['Distributor ID']+' '+hi['Release']+' '+hi['Codename']+" - "+hi['system']+"\nMemory: {:4.0f} MB total, {:4.0f} MB free".format(mt,mf)
        info3="{:<6} {:<17} {}".format( "DEV:","MAC:", "IPv4:" )
        info4=""
        for d in dev:
            info4=info4+"{:<6} {:^16} {}\n".format( d[0],d[1], hlp.getip(d[0]).split("/",1)[0] )

        lbl=tk.Label(self.info_frame,text=info1,justify=tk.CENTER,anchor=tk.CENTER,font=(monofont,17),bg=fbg, fg=bbg,pady=3 )
        lbl.pack(fill=tk.X)
        lbl=tk.Label(self.info_frame,text=info2,justify=tk.CENTER,anchor=tk.CENTER, font=(monofont,dfont[scrmode]), bg=fbg, fg=ffg)
        lbl.pack(fill=tk.X)
        lbl=tk.Label(self.info_frame,text=info3,justify=tk.LEFT,anchor="nw", font=(monofont,dfont[scrmode]), bg=fbg, fg="#b0b0b0")
        lbl.pack(fill=tk.X)
        self.lbl=tk.Label(self.info_frame,text=info4,justify=tk.LEFT,anchor="nw",font=(monofont,dfont[scrmode]), bg=fbg, fg=bbg)
        self.lbl.pack(fill=tk.X)
        self.getnetworks()

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


class Ipconfig(Switchwindow):
    """ IP configuration  """
    def __init__(self,master,name):
        Switchwindow.__init__(self,master,name)
        self.drowpanel()


    def drowpanel(self):
        global scrmode,scrsize,dfont
        bfg = "black"
        bbg = "#c0c0c0"
        bpady=3

        hi=hlp.hostinfo();
        self.dev=hi['dev']
        no=0;
        ip={}
        mask={}
        self.frames=[]
        for d in self.dev:
            frm = tk.Frame(self.frame, padx=0, pady=4, borderwidth=1, relief=tk.RIDGE, width=self.width)
            frm.pack(fill=tk.X)
            self.frames.append(frm)
            dev=d[0]
            mac=d[1]
            ip[no]=tk.StringVar()
            mask[no]=tk.StringVar()
            link=self.linkstate(self)
            lbl=tk.Label(frm,text="DEV: {}, MAC: {}".format(dev,mac) )
            lbl.pack(fill=tk.X)
            allip=hlp.getallip(dev)
            if len(allip)>0:
                for _ip in allip:
                    ip[no].set(_ip.split("/",2)[0])
                    mask[no].set(_ip.split("/",2)[1])
                    frm_ip=tk.Frame(frm, padx=0, pady=1, borderwidth=1, relief=tk.FLAT, width=self.width)
                    frm_ip.pack(fill=tk.X)
                    lbl=tk.Label(frm_ip,text="IP" ).pack(side=tk.LEFT)
                    btn=tk.Button(frm_ip,textvariable=ip[no],command=partial(self.setip, ip[no]),font=(self.monofont, dfont[scrmode]),fg=self.bfg,bg=self.bbg,padx=self.bpadx,pady=self.bpady,width=15)
                    btn.pack(side=tk.LEFT)
                    lbl=tk.Label(frm_ip,text="/" ).pack(side=tk.LEFT)
                    btn=tk.Button(frm_ip,textvariable=mask[no],command=partial(self.setmask, mask[no]),font=(self.monofont, dfont[scrmode]),fg=self.bfg,bg=self.bbg,padx=self.bpadx,pady=self.bpady,width=3)
                    btn.pack(side=tk.LEFT)
                    if link[d[0]]=='UP':
                        lbl=tk.Label(frm_ip,text=link[d[0]],padx=3,fg="green").pack(side=tk.LEFT)
                        btn=tk.Button(frm_ip,text="SET",command=partial(self.ipset,d[0],ip[no],mask[no]),font=(self.monofont, dfont[scrmode]),fg="red",bg=self.bbg,padx=self.bpadx,pady=self.bpady,width=3)
                        btn.pack(side=tk.LEFT)
                        btn=tk.Button(frm_ip,text="AD",command=partial(self.ipset,d[0],ip[no],mask[no],"add"),font=(self.monofont, dfont[scrmode]),fg="red",bg=self.bbg,padx=self.bpadx,pady=self.bpady,width=3)
                        btn.pack(side=tk.LEFT)
                        btn=tk.Button(frm_ip,text="RM",command=partial(self.ipset,d[0],ip[no],mask[no],"delete"),font=(self.monofont, dfont[scrmode]),fg="red",bg=self.bbg,padx=self.bpadx,pady=self.bpady,width=3)
                        btn.pack(side=tk.LEFT)
                    else:
                        lbl=tk.Label(frm_ip,text=link[d[0]],padx=3,fg="red").pack(side=tk.LEFT)
                    no=no+1
                    ip[no]=tk.StringVar()
                    mask[no]=tk.StringVar()
            else:
                ip[no].set("")
                mask[no].set("")
                no=no+1
                ip[no]=tk.StringVar()
                mask[no]=tk.StringVar()


    def ipset(self, dev, ip, mask,mode="replace"):
        if mode=="replace":
            oldip=hlp.getip(dev).split("/")[0]
            oldmask=hlp.getip(dev).split("/")[1]
            cmd="sudo ip a del {}/{} dev {}".format( oldip, oldmask, dev )
            hlp.system_exec(cmd)
        if mode=="delete":
            cmd="sudo ip a del {}/{} dev {}".format( ip.get(), mask.get(), dev )
            hlp.system_exec(cmd)
        if mode != "delete":
            cmd="sudo ip a add {}/{} dev {}".format( ip.get(), mask.get(), dev )
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
            if parts[2].find(" state UP ")>1:
                link[parts[1]]="UP"
            else:
                link[parts[1]]="DOWN"
        return link

    def setip(self,ip):
        self.dialog=vk.Numpad(self.frame, ip.set, ip.get())

    def setmask(self,mask):
        self.dialog=vk.Numpad(self.frame, mask.set, mask.get())


def _framereplace(x,top_frame,Cframe):
    global np
    if np != None:
        if np.name() == x:
            _replace=False
        else:
            _replace=True
        np.destroy()
        if _replace:
            np=Cframe(top_frame,x)
        else:
            np=Clock(top_frame,"clock")
    else:
        np = Cframe(top_frame,x)


def test(x):
    print("test: " + x)

def _unlock(unlock=True):
    global tb_frame,panel_frame,lock_frame,lock
    if unlock:
        lock_frame.pack_forget()
        tb_frame.pack(fill=tk.X)
        panel_frame.pack(fill=tk.BOTH)
        _framereplace("clock",panel_frame,Clock)
    else:
        tb_frame.pack_forget()
        panel_frame.pack_forget()
        lock.clear()
        lock_frame.pack(fill=tk.BOTH)



cnf=Conf.Appconfig("rpipanel.ini")
np=None
window = tk.Tk()
scrsize=(window.winfo_screenwidth(),window.winfo_screenheight())
if scrsize[0]==320:
    scrmode=0
    scrsize=(320,240)
elif scrsize[0]==480:
    scrmode=1
    scrsize=(480,320)
else:
   scrmode=1
   scrsize=(480,320)
#   scrmode=0
#   scrsize=(320,240)

geometry="{}x{}+0+0".format(scrsize[0],scrsize[1])
window.overrideredirect(True)
window.geometry(geometry)
window.config(bg="black")


lock_frame=tk.Frame(window,relief=tk.FLAT,borderwidth=0,bg="black",width=scrsize[0],height=scrsize[1])
tb_frame=tk.Frame(window,relief=tk.FLAT,borderwidth=0,bg="black")
panel_frame=tk.Frame(window,relief=tk.FLAT,borderwidth=0,bg="black",height=scrsize[1])

#tb_frame.pack(fill=tk.X)
#panel_frame.pack(fill=tk.BOTH)

buttons = [ ["QUIT",partial(_framereplace,"QUIT",panel_frame,Shutdown)],
            ["IP",partial(_framereplace,"IP",panel_frame,Ipconfig)],
            ["i",partial(_framereplace,"i",panel_frame,Systeminfo)],
            ["LOK",partial(_unlock,False) ] ]

tb=Topbar(tb_frame,u"",buttons)

#np = Clock(panel_frame,"clock")
lock = Lockpin( lock_frame, "LOC" )
lock_frame.pack(fill=tk.BOTH)

window.mainloop()
