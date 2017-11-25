# -*- coding: UTF-8 -*-
import Tkinter as tk
import ttk
import math as Math

class Gauge(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args,**kwargs)
        self.hyp = float(float(self['width']) - 20) / 2.0


    def style(self,style, color1, color4, font, fontsize):
        self.Style= style #style is for gauge design
        self.Color1 = color1
        self.Color4 = color4
        self.DangerColor ='#ff3f1e'
        self.WarningColor = '#edaf07'

        self.Font = font
        self.FontSize= fontsize

    def changeValue(self, newvalue):
        self.Value = newvalue
        if (self.Value < self.MinValue):
            self.Value = self.MinValue
        elif(self.Value > self.MaxValue):
            self.Value = self.MaxValue
        self.updatePOD()


    def setup(self, inivalue, minvalue, maxvalue, units, unitspacing):
        self.Value = inivalue
        self.MinValue= minvalue
        self.MaxValue = maxvalue
        self.Units= units
        self.UnitSpacing = unitspacing

    def inidraw(self):
        self['bg']=self.Color4
        self['bd']=0
        self['highlightthickness'] = 0
        self['relief'] = 'ridge'

        #print(self['width'])
        gpod = self.create_oval(10,10, int(self['width'])-10, int(self['height'])-10, outline= self.Color1, width=2)

        ###create the lines on the circle###
        lengthofdash = .15
        widthofdash= 2 #in pix
        temp = self.Value
        self.Value =self.MinValue
        while self.Value <= self.MaxValue:
            self.create_line(self.getxunscalled() * self.hyp * (1-lengthofdash) +int(self['width'])/2,
                             self.getyunscalled() * self.hyp * (1-lengthofdash)+int(self['height'])/2,
                             self.getxunscalled() * self.hyp * (1) +int(self['width'])/2,
                             self.getyunscalled() * self.hyp * (1)+int(self['height'])/2,
                             fill=self.Color1,
                             width= widthofdash)
            self.Value += self.UnitSpacing
        self.Value = temp
        self.ValueText = self.create_text(int(self['width'])/2, int(self['height'])/2+40, text='test', fill=self.Color1, font=(self.Font,self.FontSize,'bold'))
        self.pointer= self.create_line(int(self['width'])/2, int(self['height'])/2, 10, (int(self['height'])/2), fill=self.Color1)
        # create tiny ball at center
        radius = 7
        self.create_oval(int(self['width']) / 2 + radius, int(self['height']) / 2 + radius,
                         int(self['width']) / 2 - radius, int(self['height']) / 2 - radius,
                         fill=self.Color4,
                         outline=self.Color1)
        self.updatePOD()

    def updatePOD(self):
        self.coords(self.pointer, self.getx()+int(self['width'])/2, self.gety()+ int(self['height'])/2, int(self['width'])/2, int(self['height'])/2 )
        tempcolor = self.Color1
        if(float(self.Value)/float(self.MaxValue)>.75):
            tempcolor = self.WarningColor
        if (float(self.Value) / float(self.MaxValue) > .9):
            tempcolor = self.DangerColor
        self.itemconfigure(self.ValueText, text=str(self.Value) +" "+self.Units, fill = tempcolor)

    def getx(self):
        r = self.computeRAD()

        xout = Math.cos(r)*self.hyp
        #print('X value='+str(xout))
        return xout

    def getxunscalled(self):
        r = self.computeRAD()
        xout = Math.cos(r)
        # print('X value='+str(xout))
        return xout
    def getyunscalled(self):
        r = self.computeRAD()
        yout = Math.sin(r)
        # print('X value='+str(xout))
        return yout

    def gety(self):
        r = self.computeRAD()
        #print(Math.sin(r))
        yout = Math.sin(r) * self.hyp
        #print('Y value=' + str(yout))
        return yout



    def computeRAD(self):
        normvalue = (float(self.Value)+ (-1*self.MinValue))/float(-1*self.MinValue + self.MaxValue)
        #1 is at the end 0 at begining
        #print ('ini: '+str(normvalue))
        normvalue *= (2*Math.pi)
        #print (normvalue)
        normvalue += 5
        normvalue = normvalue/1.7
        #print (normvalue)

        return normvalue



'''#just comment this out when done refining
from Tkinter import *
def up():
    #print ('up')
    g1.changeValue(g1.Value + 10)


def down():
    #print ('down')
    g1.changeValue(g1.Value - 10)


master = Tk()
master['bg']='black'
g1= Gauge(master, width=200, height=200)
g1.style(0, 10, "#1e74ff", "#493030", "#332a23", "#303030", "Helvetica", 34)
g1.setup(10, -10, 150, '°C')
g1.pack()
bup = tk.Button(text='up', command=up)
bup.pack()
bd = tk.Button(text='down', command=down)
bd.pack()


mainloop()'''