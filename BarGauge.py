# -*- coding: UTF-8 -*-
import Tkinter as tk
import ttk
import math as Math

class BarGauge(tk.Canvas):
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
        linearr=[]
        linearr.append(self.create_line(5,5, self.width, 5))
        linearr.append(self.create_line(5, self.height, self.width, self.height))
        linearr.append(self.create_line(self.width, self.height, self.width, 5))
        linearr.append(self.create_line(5, self.height, 5, 5))
        for l in linearr:
            self.itemconfigure(l, fill= self.Color1, width=2)

        self.Bar = self.create_rectangle(5,5, 10, self.height, fill= self.Color1, outline=self.Color1)
        self.ValueText= self.create_text(.5*self.width, self.height/2, text= '10%', font=(self.Font, int(self.height*.8)), fill='White')


        #last
        self.updateGauge()

    def updateGauge(self):
        self.NormalizedValue = float(self.Value)/float(-1*self.MinValue+self.MaxValue)
        w= int((self.NormalizedValue+.03) * self.width)
        if(w> self.width):
            w=self.width
        self.coords(self.Bar,5,5,w, self.height)
        if(self.NormalizedValue>0.5):
            self.itemconfigure(self.ValueText, fill = 'black')

        else:
            self.itemconfigure(self.ValueText, fill='#fff')
        self.itemconfigure(self.ValueText, text=str(self.Value)+self.Units)

        if(self.NormalizedValue<.21):
            self.itemconfigure(self.ValueText, fill='#ff3f1e')

        #print(w)
        #print(self.NormalizedValue)



    def changeValue(self, newvalue):
        self.Value = newvalue
        if (self.Value < self.MinValue):
            self.Value = self.MinValue
        elif(self.Value > self.MaxValue):
            self.Value = self.MaxValue
        #print(self.Value)
        self.updateGauge()
    def setup(self, inivalue, minvalue, maxvalue, units, unitspacing):
        self.Value = inivalue
        self.MinValue= minvalue
        self.MaxValue = maxvalue
        self.Units= units
        self.UnitSpacing = unitspacing
        self.inidraw()

    def style(self, color1, color4, font, fontsize):
        self.Color1 = color1
        self.Color4 = color4
        self.DangerColor ='#ff3f1e'
        self.WarningColor = '#edaf07'

        self.Font = font
        self.FontSize= fontsize



'''from Tkinter import *
def up():
    #print ('up')
    g1.changeValue(g1.Value + 10)


def down():
    #print ('down')
    g1.changeValue(g1.Value - 10)


master = Tk()

g1= BarGauge(master, width=400, height=100)
g1.style("#1e74ff", "#303030", "Helvetica", 34)
g1.setup(10, 0, 100, '%',10)
g1.pack()
bup = tk.Button(text='up', command=up)
bup.pack()
bd = tk.Button(text='down', command=down)
bd.pack()
master['bg']=g1.Color4


mainloop()'''