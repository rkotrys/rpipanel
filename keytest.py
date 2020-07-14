#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys,os,math,time
import tkinter as tk
import datetime as dt
from functools import partial
import threading
import subprocess as proc
import RPi.GPIO as GPIO

KEY1_PIN = 18  #pin 12
KEY2_PIN = 32  #pin 16
KEY3_PIN = 24  #pin 18

GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

class Kbd:
    buttons = { 'k1':0, 'k2':0, 'k3':0 }
    keyid =   {'k1':KEY1_PIN,'k2':KEY2_PIN,'k3':KEY3_PIN }
    handler = { 'k1':0, 'k2':0, 'k3':0 }

    def __init__(self):
        for k in self.handler.keys():
            self.handler[k] = self.keyhandle;
        self.x = threading.Thread( name='keydrv', target=self.keydrv, args=(0.1,), daemon=True)
        self.x.start()

    def keydrv( self, period ):
        while 1:
            self.read()
            time.sleep(period)

    def keyhandle( self, name, state ):
        print( u'{} is {}'.format( name, state ) )

    def sethanddle( self, name, handle ):
        self.handler[name] = handle

    def key(self,name):
        Kbd.read(self)
        return Kbd.buttons[name]

    def read(self):
        for k in Kbd.buttons.keys():
            if GPIO.input(Kbd.keyid[k]): # button is released
                if Kbd.buttons[k] == 1:
                    Kbd.buttons[k] = 0
                    if callable(Kbd.handler[k]):
                        Kbd.handler[k](k,'UP')
            else: # button is pressed:
                if Kbd.buttons[k] == 0:
                    Kbd.buttons[k] = 1;
                    if callable(Kbd.handler[k]):
                        Kbd.handler[k](k,'Down')



