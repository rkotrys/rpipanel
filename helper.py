#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, io, subprocess
from pathlib import Path

def readfile(filename):
    if os.path.isfile(filename):
        with open(filename,'r') as file:
            data = file.readline().strip().replace('\n','')
    else:
        data=False

    return data

def system_exec(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip().split('\n')

def hostinfo():
    model = {}
    with open('/proc/cpuinfo','r') as file:
        for line in file:
           data = line.strip().replace('\n','').split(':',2)
           if  len(data)==2:
               key=data[0].strip()
               value=data[1].strip()
               if not key in model:
                   model[key] = data[1].strip()
               elif key=="processor":
                   model[key] = "{}".format( int(model[key])+1 )
               if key=="Serial":
                   model[key]=model[key][8:]
        model['processor']="{}".format( int(model['processor'])+1 )

    with open('/proc/meminfo','r') as file:
        for line in file:
           data = line.strip().replace('\n','').split(':',2)
           if  len(data)==2:
               key=data[0].strip()
               value=data[1].strip()
               if not key in model:
                   model[key] = data[1].strip()

    with open('/proc/version','r') as file:
        data = file.readline().strip().split(' ', 4)
        model['system'] = data[0] + ' ' + data[2]

    dev = []
    p=Path('/sys/class/net/');
    for x in p.iterdir():
        if x.is_dir():
            l = str(x).split('/')
            if l[4]=='lo': continue
            with open(str(x)+'/address','r') as file:
                data = file.readline().strip().replace('\n','')

        dev.append( ( l[4], data ) )

    model['dev']=dev
    for line in system_exec('lsb_release -irc'):
        data = line.split(':',2)
        model[data[0].strip()]=data[1].strip()

    return  model

def getcputemp():
    temperature='/sys/class/thermal/thermal_zone0/temp'
    if os.path.isfile(temperature):
        t=float(readfile('/sys/class/thermal/thermal_zone0/temp'))
        t = t / 1000.0
    else:
        t=0.0
    return "{:4.1f}".format(t)

def getip(dev):
    w=system_exec("ip -4 a l {}".format(dev) )
    if len(w)<3:
        return ""
    w=w[1].strip().split(" ",2)
    return w[1]

def getallip(dev):
    w=system_exec("ip -4 a l {}".format(dev) )
    if len(w)<3:
        return ""
    iplist=[]
    for l in w:
        if l.find("inet")>1:
            iplist.append(l.strip().split(" ",2)[1])
        else:
            continue
    return iplist

def getmmcinfo():
    w=system_exec("blkid -t TYPE=ext4 -o export")
    r={}
    for l in w:
        _it=l.strip().split("=",2)
        r[_it[0]] = _it[1]
    w=system_exec("df -kH --type=ext4 --output=size,avail")
    _tmp=w[1].strip()
    r['size']=_tmp.split(" ")[0]
    r['free']=_tmp[len(r['size']):].strip()
    return r

class RingBuffer:
    def __init__(self,items):
        self.data = items

    def __str__(self):
        r="[ "
        for n in self.data:
            r = r + "{} ".format(n)
        return r + "]"

    def get(self):
        return self.data[0]

    def next(self):
        self.data.append(self.data.pop(0))
        return self.data[0]

    def add(self,item):
        self.data.append(item)

    def remove(self,item=None):
        if item != None:
            try:
                self.data.remove(item)
            except ValueError:
                pass
        else:
            self.data.pop()

