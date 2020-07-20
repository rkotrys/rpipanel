#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#

import sys,os
from PIL import Image
import tkinter as tk
from functools import partial



class Keypad:
    def __init__(self,master,callback,entrytext="abcd"):
        font=("DejaVu Sans Mono", 11);
        maxkeys=13
        bpad=4
        fbg="black"
        self.command=callback
        self.frame = tk.Frame(master=master,relief=tk.FLAT,borderwidth=0,bg=fbg,padx=1,pady=1)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        frm_entry = tk.Frame(master=self.frame,relief=tk.RAISED,borderwidth=0,bg="black")
        frm_entry.pack(fill=tk.X,side=tk.TOP)
        self.entry = tk.Entry(frm_entry,width=30,font=font)
        if entrytext is not None:
            self.entry.insert(0,entrytext);
        self.entry.pack(fill=tk.X,side=tk.TOP)
        self.keymode=1
        self.frm_keys = self._keylines(self.frame,self.keymode,True)

    def _keylines(self,master,mode=1,start=True):
        fbg="black"
        font=("DejaVu Sans Mono", 11);
        bpad=4
        kl1=['q','w','e','r','t','y','u','i','o','p','[',']']
        kl2=['a','s','d','f','g','h','j','k','l',':','"','|']
        kl3=['z','x','c','v','b','b','n','m',',','.','/','?']
        kl1a=['Q','W','E','R','T','Y','U','I','O','P','[',']']
        kl2a=['A','S','D','F','G','H','J','K','L',':','"','|']
        kl3a=['Z','X','C','V','B','N','M',',',',','.','/','?']
        kl1b=['1','2','3','4','5','6','7','8','9','0','-','=']
        kl2b=['~','`','@','#','$','%','^','&','*','(',')','_']
        kl3b=['!','{','}',';',',','\'',',','.','?','/',' ',' ']
        kl4=['Shft',' ','<-bs','Entr',' Clr',' Esc']
        if mode == 1:
            keys = [kl1,kl2,kl3]
        elif mode == 2:
            keys = [kl1a,kl2a,kl3a]
        elif mode == 3:
            keys = [kl1b,kl2b,kl3b]

        if not start:
            self.frm_keys.destroy()
        self.frm_keys=tk.Frame(master=master,relief=tk.FLAT,borderwidth=0,bg=fbg)
        self.frm_keys.pack(fill=tk.X,side=tk.TOP)
        r=0
        for kl in keys:
            c=0
            for x in kl:
                frm=tk.Frame(master=self.frm_keys,relief=tk.FLAT,borderwidth=1,width=20,height=20,bg=fbg)
                frm.grid(row=r,column=c,padx=0,pady=0)
                key=tk.Button(master=frm,font=font,padx=bpad,pady=0,text=x,command=partial(self.pressnum, x) )
                key.pack(fill=tk.X)
                c=c+1
            r=r+1
        kl=kl4;
        c=0
        for x in kl:
            frm=tk.Frame(master=self.frm_keys,relief=tk.FLAT,borderwidth=1,width=40,height=20,bg=fbg)
            frm.grid(row=r,column=c,columnspan=2,padx=0,pady=0)
            if x==' ':
                _x='    '
            else:
                _x=x
            key=tk.Button(master=frm,font=font,padx=bpad,pady=2,text=_x,command=partial(self.pressnum, x ))
            key.pack(fill=tk.X)
            c=c+2
        return self.frm_keys

    def pressnum(self,n):
        if n=="enter":
            quit()
        elif n=="<-bs":
            self.entry.delete( len(self.entry.get())-1 )
        elif n==' Esc':
            self.frame.destroy()
        elif n==' Clr':
            self.entry.delete(0,len(self.entry.get()))
        elif n=='Entr':
            self.command(self.entry.get())
            self.frame.destroy()
        elif n=='Shft':
            if self.keymode==1:
                self.keymode=2
            elif self.keymode==2:
                self.keymode=3
            else:
                self.keymode=1

            self.frm_keys = self._keylines(self.frame,self.keymode,False)
        else:
            self.entry.insert( len(self.entry.get()),n )

    def destroy(self):
        self.frame.destroy()

class Numpad:
    """ simple numeric keypad widget in top window  """
    def __init__(self,master,callback,entrytext="1234"):
        self.command=callback
        btn_size=32
        btn_sizex=42
        fg_entry="black"
        bg_entry="white"
        fg_key="black"
        bg_key="#dddddd"
        bg_frame="#606060"
        pad=1

        self.font=("DejaVu Sans Mono", 12);
        k=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','x',' ','.','/','<','CL','OK','X']
        maxnumitems=5
        #self.top=tk.Toplevel()
        #self.top.title("Numpad test")
        #self.top.overrideredirect(True)
        #self.top.focus_set()
        self.master=master
        self.frame = tk.Frame(master=self.master,relief=tk.FLAT,borderwidth=2,bg=bg_frame)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame.focus_set()
        self.entry=tk.Entry(self.frame,width=21,font=self.font,bg=bg_entry,fg=fg_entry)
        self.entry.insert(0,entrytext)
        self.entry.grid(row=0,column=0,columnspan=5,pady=2,padx=2)
        i=0
        for n in k:
            nrow=int(i/maxnumitems)+1
            if n=="OK":
                frm_bt=tk.Frame(self.frame,borderwidth=0,relief=tk.FLAT,height=btn_size,width=btn_sizex*2,bg=bg_frame,highlightthickness=0)
                frm_bt.pack_propagate(0) # don't shrink
                frm_bt.grid(row=nrow,column=i%maxnumitems,padx=pad,pady=pad,columnspan=2)
                i=i+1
            elif n=="X":
                frm_bt=tk.Frame(self.frame,borderwidth=0,relief=tk.FLAT,height=btn_size,width=btn_sizex,bg=bg_frame,highlightthickness=0)
                frm_bt.pack_propagate(0) # don't shrink
                frm_bt.grid(row=nrow,column=i%maxnumitems,padx=pad,pady=pad)
            elif n=="CL":
                frm_bt=tk.Frame(self.frame,borderwidth=0,relief=tk.FLAT,height=btn_size,width=btn_sizex,bg=bg_frame,highlightthickness=0)
                frm_bt.pack_propagate(0) # don't shrink
                frm_bt.grid(row=nrow,column=i%maxnumitems,padx=pad,pady=pad)
            else:
                frm_bt=tk.Frame(self.frame,borderwidth=0,relief=tk.FLAT,height=btn_size,width=btn_sizex,bg=bg_frame,highlightthickness=0)
                frm_bt.pack_propagate(0) # don't shrink
                frm_bt.grid(row=nrow,column=i%maxnumitems,padx=pad,pady=pad)

            bt=tk.Button(frm_bt,text=n,command=partial(self.kpres, n),font=self.font,fg=fg_key,bg=bg_key,highlightthickness=0)
            bt.pack(fill=tk.X)
            i=i+1
        #self.top.geometry("+40+40")

    def kpres(self,n):
        if n=="OK":
            self.command(self.entry.get())
            self.frame.destroy()
        elif n=="<":
            self.entry.delete(len(self.entry.get())-1)
        elif n=='CL':
            self.entry.delete(0, tk.END)
        elif n=='X':
            self.frame.destroy()
        else:
            self.entry.insert(len(self.entry.get()),n)

    def destroy(self):
        self.frame.destroy()



#def character_range(char1, char2):
#    for char in range(ord(char1), ord(char2)+1):
#        yield (char)

#-----------------------------------------------
# forr test
#-----------------------------------------------
#
# test callback function
#
#def test(x):
#    print("test: " + x)

# window setup
#
#window = tk.Tk()
#window.overrideredirect(True)
#window.geometry("320x240+0+0")
#window.config(bg="black")
#item = keypad(window,test,"abcd")
#item = numpad(window,test,"1234")
#window.mainloop()

# - end test -
