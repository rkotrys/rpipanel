#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys,os
import tkinter as tk
import datetime as dt
import time
from functools import partial
import helper as hlp
import Vkeypad as vk
from PIL import Image,ImageDraw,ImageFont,ImageColor,ImageFilter,ImageTk
import subprocess as proc
import threading

#scrmode=0 # 320x240
scrmode=1 # 480x320
scrtype=["320x240-0-0","480x320+0+0"]
dfont=[11,12]

class Topbar:
    """ simple top bar with buttons  """
    def __init__(self,master,label_text,buttons):
        global scrsize,dfont,scrmode
        self.master=master
        maxwidth=scrsize[0]
        maxheight=scrsize[1]
        barh=24
        bfgr="black"
        bbgr="#707070"
        fgr= "#ffbf00"
        bgr="darkblue"
        font=("DejaVu Sans Mono", dfont[scrmode])
        self.label=tk.StringVar()
        self.label.set(label_text)
        self.temperature=tk.StringVar()
        self.time=tk.StringVar()

        self.frame = tk.Frame(master,relief=tk.FLAT,borderwidth=1,bg=bgr,height=barh)
        self.frame.pack_propagate(0) # don't shrink
        self.frame.pack(fill=tk.X)

        lbl_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=bgr,width=maxwidth-150)
        lbl_frame.pack_propagate(0) # don't shrink
        lbl_frame.pack(fill=tk.Y, side=tk.LEFT)
        lbl=tk.Label(lbl_frame,textvariable=self.time,anchor="w",justify=tk.LEFT,font=font,bg=bgr,fg=fgr)
        lbl.pack(side=tk.LEFT,padx=2)
        lbl=tk.Label(lbl_frame,textvariable=self.temperature,anchor="w",justify=tk.LEFT,font=font,bg=bgr,fg=fgr)
        lbl.pack(side=tk.LEFT,padx=2)
        lbl=tk.Label(lbl_frame,textvariable=self.label,anchor="w",justify=tk.LEFT,font=font,bg=bgr,fg=fgr)
        lbl.pack(side=tk.LEFT,padx=2)

        btn_frame=tk.Frame(self.frame,relief=tk.FLAT,borderwidth=0,bg=bgr)
        btn_frame.pack(fill=tk.Y, side=tk.RIGHT)
        for b in buttons:
            btn=tk.Button(btn_frame,text=b[0],command=b[1],relief=tk.RAISED,font=font,fg=fgr,bg=bbgr,highlightbackground=bbgr,padx=3,pady=0,bd=1,width=4)
            btn.pack(fill=tk.Y, side=tk.RIGHT)
        self.settime()
        self.settemperature()

    def settime(self):
        self.time.set(time.strftime('%-H:%M:%S'))
        self.master.after(1000,self.settime)

    def settemperature(self):
        self.temperature.set(hlp.getcputemp()+u"°C")
        #self.temperature.set(u"51°C")
        self.master.after(1000,self.settemperature)

class Switchwindow:
    """ virtual class  """
    def __init__(self,master,name):
        global scrsize
        self.master=master
        self.window_name=name
        self.width=scrsize[0]
        self.height=scrsize[1]
        self.ffg="black"
        self.fbg="#c0c0c0"
        self.bfg="black"
        self.bbg="#c0c0c0"
        self.bpadx=2
        self.bpady=2
        self.monofont="DejaVu Sans Mono"
        self.frame = tk.Frame(master,relief=tk.FLAT, bg=self.fbg, width=self.width, height=self.height-24 )
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
        Switchwindow.__init__(self,master,name)
        fbg = "black"
        ffg = "#ffffff"
        bfg = "darkred"
        bbg = "#ffbf00"
        bpady=15
        font=("DejaVu Sans Mono", 14)
        padsize=5
        #self.master=master

        #self.frame = tk.Frame(master,relief=tk.FLAT,borderwidth=2,width=300,bg=fbg)
        #self.frame.pack_propagate(0) # don't shrink
        #self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        #self.frame.config(bg="#808080")
        self.frame.config(bg=bfg)

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

    def destroy(self):
        self.frame.destroy()

class Clock(Switchwindow):
    """ clock  """
    global scrmode
    images = "images/"
    baksnames = [ "t1b.png","t3blue_250.png","t3coper_250.png","t3gold_250.png","t3green_250.png","t4b_250.png","t4b_gold_250.png" ]
    baksnames320 = [ "z1b.bmp","z2b.bmp","z3b.bmp","z4.bmp","z6.bmp"]
    backs = []

    def __init__(self,master,name):
        Switchwindow.__init__(self,master,name)
        self.fbg="black"
        self.bfg="#ff8000"

        self.ind=3
        self.s_color = (255,0,0,255)
        self.m_color = (255,190,0,255)
        self.h_color = (255,190,0,255)
        self.outline_color = (255,170,0,255)
        self.arrowsize = 15
        if scrmode==0:
            Clock.baksnames = Clock.baksnames320
        for n in range(0,len(Clock.baksnames)):
            Clock.backs.append( Image.open( Clock.images + Clock.baksnames[n] ) )
        self.font = ImageFont.truetype("./fonts/tahomabd.ttf", 16)
        self.font12 = ImageFont.truetype("./fonts/lucon.ttf", 12)
        self.symbols = ImageFont.truetype("./fonts/segmdl2.ttf", 16)

        self.time=tk.StringVar()
        self.frame.config(bg=self.fbg)
        self.time.set(time.strftime('%-H:%M:%S'))
        self.time_frame = tk.Frame(self.frame,relief=tk.FLAT, bg=self.fbg)
        self.time_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.photo=self.drowclock(self.ind)
        #self.lbl=tk.Label(self.time_frame,textvariable=self.time,justify=tk.CENTER,anchor=tk.CENTER,font=(self.monofont,45),bg=self.fbg, fg=self.bfg,pady=3 )
        self.lbl=tk.Label(self.time_frame,image=self.photo,justify=tk.CENTER,anchor=tk.CENTER,font=(self.monofont,45),bg=self.fbg, fg=self.bfg,pady=3 )
        self.lbl.pack()
        self.btn=tk.Button(self.frame,text=' > ', command=self.nextface ,bg="gold", font=("DejaVu Sans Mono", 14),fg=self.fbg,borderwidth=0,relief=tk.FLAT,padx=0,pady=0)
        self.btn.place(relx=0.9, rely=0.9, anchor=tk.CENTER)
        self.settime()

    def nextface(self):
        if self.ind < len(Clock.baksnames)-1:
            self.ind=self.ind+1;
        else:
            self.ind = 0;

    def drowclock(self,ind):
        global scrmode,scrsize
        iconcolor = (225,180,0) #(200,200,255)
        tm = time.localtime()
        image = Clock.backs[ind].copy()
        im = Image.new( "RGBA", image.size, (255,255,255,255) )
        im.paste(image)
        draw = ImageDraw.Draw(im)
        if scrmode==0:
            hands=(12,25,35)
            self.arrowsize=10
        else:
            hands=(24,50,70)
            self.arrowsize=15
        draw.text( (im.size[0]/2-8,im.size[0]/4), chr(0xE774)+u'', font=self.symbols, fill=iconcolor )
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
        dr.polygon( [(x-2,y), (x+2,y), (x+2,r[1]),(x+5,r[1]),(x,r[1]-self.arrowsize),(x-5,r[1]), (x-2,r[1])], fill = self.h_color, outline=self.outline_color )
        hmim =Image.alpha_composite( him, im.rotate( -(360*t[1])/60, Image.BICUBIC ) )
        im = Image.new( "RGBA", image.size, (255,255,255,0) )
        dr = ImageDraw.Draw( im )
        dr.line([ ( x, y+20 ), ( x, r[0]+10)], fill = self.s_color, width = 2 )
        dr.line([ ( x-3, r[0]+10 ), ( x, r[0]), ( x+3, r[0]+10 ), ( x-3, r[0]+10 )], fill = self.s_color, width = 2 )
        dr.ellipse([x-7,y-7,x+7,y+7],fill=self.s_color,outline='#777')
        return Image.alpha_composite( hmim, im.rotate( -(360*t[2])/60, Image.BICUBIC ) )


    def settime(self):
        self.photo=self.drowclock(self.ind)
        self.lbl.config(image=self.photo)
        #self.time.set(time.strftime('%-H:%M:%S'))
        self.master.after(1000,self.settime)


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
        self.lbl.config(text=info)
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
    #scrmode=0
    #scrsize=(320,240)
window.overrideredirect(True)
window.geometry(scrtype[scrmode])
window.config(bg="black")
#window.geometry("480x320+0+0")


tb_frame=tk.Frame(window,relief=tk.FLAT,borderwidth=0,bg="black")
panel_frame=tk.Frame(window,relief=tk.FLAT,borderwidth=0,bg="black",height=scrsize[1])
tb_frame.pack(fill=tk.X)
panel_frame.pack(fill=tk.BOTH)

buttons = [ ["QUIT",partial(_framereplace,"QUIT",panel_frame,Shutdown)],
            ["IP",partial(_framereplace,"IP",panel_frame,Ipconfig)],
            ["i",partial(_framereplace,"i",panel_frame,Systeminfo)] ]

tb=Topbar(tb_frame,u"",buttons)
np = Clock(panel_frame,"clock")

window.mainloop()
