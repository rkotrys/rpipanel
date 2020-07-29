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


class Clock(panel.Switchpanel):
    """ clock  frame: create frame on 'master' create canvas, drow and initialize clock face and buttons """
    backs = []

    def __init__(self,app,master,name):
        panel.Switchpanel.__init__(self,app,master,name)
        dml=self.app.dml
        srcmode=self.app.scrmode
        scrsize=self.app.scrsize
        #
        self.fbg=dml['clock']['frm_bg']
        self.bfg=dml['clock']['btn_fg']
        self.face_names=dml['clock']['face_names']
        self.bgimage_names=dml['global']['bgimage_names']
        self.s_color = dml["clock"]["colors"]["s_hand"]
        self.m_color = dml["clock"]["colors"]["m_hand"]
        self.h_color = dml["clock"]["colors"]["h_hand"]
        self.outline_color = dml["clock"]["colors"]["outline_hand"]
        self.arrowsize = dml['clock']['arrowsize']
        self.symbol_size = dml['clock']['symbol_size']
        self.ttf_size = dml['clock']['ttf_size']
        self.colck_y_ofset = dml['clock']['colck_y_ofset']
        #
        self.face={}
        self.bgimage={}
        self.images = {}
        for n in self.face_names:
            self.face[n]=Image.open( dml["global"]["images"] + self.face_names[n] ).resize((scrsize[1]-45,scrsize[1]-45),resample=Image.BICUBIC)
            self.bgimage[n]=ImageTk.PhotoImage(Image.open( dml["global"]["images"] + self.bgimage_names[n] ).resize((scrsize[0],scrsize[1]),resample=Image.BICUBIC))
        #self.run_bg = ImageTk.PhotoImage(self.bgimage[dml["global"]["theme"]])
        # buttons
        img = Image.open( dml["global"]["images"] + dml['clock']['btn_next_img'] )
        img_r = img.rotate( 180, Image.BICUBIC )

        self.images['btn_next']= self.btn_img_make(0xF0D2, self.bfg, size=(50,50))
        self.images['btn_color']= self.btn_img_make(0xE2B1, self.bfg, size=(50,50))


        self.images['btn_gog']= self.btn_img_make(0xE115, self.bfg, size=(dml["clock"]["btn_size"],dml["clock"]["btn_size"]) )

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

        self.animation = self.settime

    def drow_all(self):
        """ prepare and drow all images on the canvas """
        dml=self.app.dml
        scrmode=self.app.scrmode
        scrsize=self.app.scrsize

        # delete old images from canvas
        self.canvas.delete("clock")
        self.canvas.delete("bgphoto")
        self.canvas.delete("btn_next")
        self.canvas.delete("btn_color")

        # clock prepare and drow face
        self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2), image=self.bgimage[dml["global"]["theme"]], tag="bgphoto" )
        self.run_face=self.drowclock()
        self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2-self.colck_y_ofset), image=self.run_face, tag="clock" )

        # buttons prepare, set callbacks and drow
        self.btn= { "next": self.btn_img_make( 0xF0D2, dml["global"]["theme_btn_colors"][dml["global"]["theme"]], dml["global"]["theme_btn"][dml["global"]["theme"]] ),
                    "shutdown": self.btn_img_make( 0xE7E8, dml["global"]["theme_btn_colors"][dml["global"]["theme"]], dml["global"]["theme_btn"][dml["global"]["theme"]] ) }

        self.canvas.create_image( (scrsize[0]-25,scrsize[1]-25), image=self.btn["next"], tag=("btn","btn_next") )
        self.canvas.tag_bind( "btn_next", "<Button-1>", partial(self.app.inst.frame_replace, "Conf") )

        self.canvas.create_image( (25,scrsize[1]-25), image=self.btn["shutdown"], tag=("btn","btn_shutdown") )
        self.canvas.tag_bind( "btn_shutdown", "<Button-1>", partial(self.app.inst.frame_replace, "Shutdown") )

    def drowclock(self):
        dml=self.app.dml
        scrmode=self.app.scrmode
        scrsize=self.app.scrsize
        #
        iconcolor = dml["clock"]["colors"]["icon"]
        termcolor = dml["clock"]["colors"]["term"]
        tm = time.localtime()
        image = self.face[dml["global"]["theme"]].copy()
        im = Image.new( "RGBA", image.size, (255,255,255,255) )
        im.paste(image)
        draw = ImageDraw.Draw(im)
        hands=( dml['clock']['hands_size'][scrmode]['s'], dml['clock']['hands_size'][scrmode]['m'], dml['clock']['hands_size'][scrmode]['h'])
        self.arrowsize=dml['clock']['arrowsize'][scrmode]
        # face anotations
        if scrmode==0:
            font=self.fontL
            symbols=self.symbolsL
            symbol_size=self.symbol_size['L']
        else:
            font=self.fontXL
            symbols=self.symbolsXL
            symbol_size=self.symbol_size['XL']
        draw.text( (im.size[0]/2-symbol_size/2,im.size[1]/4), chr(0xE774)+u'', font=symbols, fill=iconcolor )
        temperature = hlp.getcputemp()+u"°C"
        tm_size = draw.textsize(temperature,font=font)
        draw.text( (int(im.size[0]/2-tm_size[0]/2+5), int(im.size[1]*2/3-tm_size[1]/2) ), temperature, font=font, fill=termcolor )
        im = Image.alpha_composite( im, self.drawhands( (tm[3],tm[4],tm[5]), hands, image ) )
        return ImageTk.PhotoImage(im)



    def drawhands( self, t, r, image ):
        dml=self.app.dml
        #
        x = int(image.size[0]/2)
        y = int(image.size[1]/2)
        im = Image.new( "RGBA", image.size, (255,255,255,0) )
        dr = ImageDraw.Draw( im )
        # H
        dr.polygon( [(x-3,y), (x+3,y), (x+3,r[2]), (x+6,r[2]),(x,r[2]-self.arrowsize),(x-6,r[2]),(x-3,r[2])], fill=self.h_color, outline=self.outline_color )
        h = t[0] if t[0]<13 else t[0]-12
        him = im.rotate( -(h*30+t[1]*0.5), Image.BICUBIC )
        # M
        im = Image.new( "RGBA", image.size, (255,255,255,0) )
        dr = ImageDraw.Draw( im )
        dr.polygon( [(x-2,y+20), (x+2,y+20), (x+2,r[1]),(x+5,r[1]),(x,r[1]-self.arrowsize),(x-5,r[1]), (x-2,r[1])], fill = self.h_color, outline=self.outline_color )
        hmim =Image.alpha_composite( him, im.rotate( -(360*t[1])/60, Image.BICUBIC ) )
        # S
        im = Image.new( "RGBA", image.size, (255,255,255,0) )
        dr = ImageDraw.Draw( im )
        dr.line([ ( x, y+30 ), ( x, r[0]+10)], fill = self.s_color, width = 3 )
        dr.line([ ( x-4, r[0]+10 ), ( x, r[0]), ( x+3, r[0]+10 ), ( x-3, r[0]+10 )], fill = self.s_color, width = 2 )
        dr.ellipse([x-8,y-8,x+8,y+8],fill=self.s_color,outline='#777')
        return Image.alpha_composite( hmim, im.rotate( -(360*t[2])/60, Image.BICUBIC ) )


    def settime(self):
        scrmode=self.app.scrmode
        scrsize=self.app.scrsize
        self.images["clock"]=self.drowclock()
        self.canvas.delete("clock")
        self.canvas.create_image( (scrsize[0]/2,scrsize[1]/2-self.colck_y_ofset), image=self.images['clock'], tag="clock" )

    def show(self):
        self.frame.pack(fill=tk.X)
        self.drow_all()
        self.run=True
        self.run_animation()

    def photo_make(self, label, size=20, bg="#ffffffff", fg="#00000000" ):
        dml=self.app.dml
        scrmode=self.app.scrmode
        scrsize=self.app.scrsize
        #
        im = Image.new( "RGBA", (size,size), bg )
        font =  ImageFont.truetype( dml["global"]["fonts"]+"segmdl2.ttf", size-2 )
        label_str = chr(label)+u""
        draw = ImageDraw.Draw(im)
        draw.text( (1,1), text=label_str, font=font,fill=fg )
        im.save("test.png","PNG")
        return ImageTk.PhotoImage(im)


    def btn_img_make(self, label, fg, fname="btn_gold_black_50.png", size=(50,50)):
        dml=self.app.dml
        scrmode=self.app.scrmode
        scrsize=self.app.scrsize
        #
        img_bg = Image.open( dml["global"]["images"] + fname )
        font_size = 28
        if img_bg.size!=size:
            img_bg = img_bg.resize(size,resample=Image.BICUBIC)
        font =  ImageFont.truetype( dml["global"]["fonts"]+"segmdl2.ttf", font_size )
        label_str = chr(label)+u""
        draw = ImageDraw.Draw(img_bg)
        label_size = draw.textsize(label_str,font=font)
        t_place = ( int((img_bg.size[0]-label_size[0])/2), int((img_bg.size[0]-label_size[0])/2) )
        draw.text( t_place, text=label_str, font=font, fill=fg )
        return ImageTk.PhotoImage(img_bg)

