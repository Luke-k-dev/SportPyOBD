# -*- coding: UTF-8 -*-
import Tkinter as tk
import ttk
import math as Math

class FuelTrimGauge(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.width = int(self['width'])-5
        self.height = int(self['height'])-5
        self.Value=0
        self.NormalizedValue=0.00 #between 0 and1
        self.MinValue=0
        self.MaxValue=100


    def inidraw(self):
        self['bg'] = self.Color4
        self['highlightthickness'] = 0
        self['relief'] = 'ridge'
        linearr = []
        ct = int(float(self.width) / 21.0)-6
        hgt= int(self.height*.25)
        while ct < self.width:
            linearr.append(self.create_line(ct, 5, ct, hgt+5))
            linearr.append(self.create_line(ct, self.height, ct, self.height-hgt))
            ct += int(float(self.width) / 21.0)
        for l in linearr:
            self.itemconfigure(l, fill=self.Color1, width=1)
        linearr=[]
        linearr.append(self.create_line(5,5, self.width, 5))
        linearr.append(self.create_line(5, self.height, self.width, self.height))
        linearr.append(self.create_line(self.width, self.height, self.width, 5))
        linearr.append(self.create_line(5, self.height, 5, 5))
        for l in linearr:
            self.itemconfigure(l, fill= self.Color1, width=2)


        self.Bar = self.create_rectangle(self.width/2,5, self.width/2, self.height, fill= self.Color1, outline=self.Color1)
        self.ValueText= self.create_text(.2*self.width, self.height/2+3, text= '+10%', font=(self.Font, int(self.height*.55)), fill=self.Color1)


        #last
        #self.updateGauge()

    def updateGauge(self):
        self.NormalizedValue = float(float(self.Value)/200.0)
        w= int((self.NormalizedValue+.5) * self.width)
        #print(w)
        #print(self.NormalizedValue)
        if(self.NormalizedValue> 0):
            self.coords(self.ValueText, .2 * self.width, self.height / 2 + 3)

        else:
            self.coords(self.ValueText,.8*self.width, self.height/2+3 )
        #print(w)
        #print(self.NormalizedValue)
        self.coords(self.Bar, self.width/2, 5, w, self.height)
        self.itemconfigure(self.ValueText, text= str(self.Value) + self.Units)


    def changeValue(self, newvalue):
        self.Value = newvalue
        if (self.Value < self.MinValue):
            self.Value = self.MinValue
        elif(self.Value > self.MaxValue):
            self.Value = self.MaxValue
        #print(self.Value)
        self.updateGauge()
    def setup(self, inivalue, minvalue, maxvalue, units):
        self.Value = inivalue
        self.MinValue= minvalue
        self.MaxValue = maxvalue
        self.Units= units
        self.UnitSpacing = 10
        self.inidraw()

    def style(self, color1, color4, font, fontsize):
        self.Color1 = color1
        self.Color4 = color4
        self.DangerColor ='#ff3f1e'
        self.WarningColor = '#edaf07'

        self.Font = font
        self.FontSize= fontsize

'''
from Tkinter import *
def up():
    #print ('up')
    g1.changeValue(g1.Value + 10)


def down():
    #print ('down')
    g1.changeValue(g1.Value - 10)


master = Tk()

g1= BarGauge(master, width=400, height=100)
g1.style("#1e74ff", "#303030", "Helvetica", 34)
g1.setup(10, -100, 100, '%')
g1.pack()
bup = tk.Button(text='up', command=up)
bup.pack()
bd = tk.Button(text='down', command=down)
bd.pack()
master['bg']=g1.Color4

mainloop()'''