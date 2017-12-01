# -*- coding: utf-8 -*-
from  SportUI import *
from  newobd import *
import Tkinter as tk
import ttk
from BarGauge import BarGauge
import commands
from convert import *
import random as rand
from Gauge import Gauge

global currentPage
currentPage=1
global carvin
global UIINDEBUG
global graph
global coldlight, TrackReady, HeatWarning, CWarning
graph= None
UIINDEBUG= True ###PLEASE USE THIS
import timeit

global COMERROR
COMERROR=False


###SET UP OBD CONNECTION###
com = None
if osx:
    # ports may be different depending on drivers and device
    com = OBDcom('/dev/tty.usbserial-00002014', 115200, '6')
else:

    com = OBDcom('/dev/ttyUSB0', 115200, '6') ###POROTCAL 6 FOR 2013 FRS

###READ EG SETTINGS ETC
global Settings
Settings = settings()


###NOW LOAD IN UI DATA###
# THEMES ARE HERE COLOR COLOR COLOR COLOR FONT SIZE
#FONT COLOR 1, FONT COLOR 2, PROGRESS BAR COLOR, backgourd color
# theme 1
t1 = css("#ef2d2d", '#493030', "#332a23", "#303030", "Helvetica", 20)
# theme 2
t2 = css("#1e74ff", "#493030", "#332a23", "#303030", "Helvetica", 20)
# theme 3
t3 = css("#283334", "#343334", "#333344", "#FF333F", "Helvetica", 20)


ui = UI(t1, t2, t3)
global buttonNavList
buttonNavList=None

###MAJOR BREAK THROUGH NEW STYLE SYSTEM###
###simply pass an array of object of the same type and a string iding there style
#then inside this function add an if statement relating there id to the style you want
#b00m
def stylizeui(uiarr, styleid):
    if(styleid == "pagetext"):
        for obj in uiarr:
            obj.config(bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                                 font=(ui.activeTheme.font, ui.activeTheme.fontsize))
    if(styleid=='progressbar'):
        for obj in uiarr:
            print('should style progress bar see styleui()')
            #obj.config()#some code to style progress bar here
    if styleid == 'button':
        for obj in uiarr:
            pass
            #obj.config()#stylize the buttons here


#################################
#GLOBAL VARS HERE
#################################
#OBD VALUES
class PIDDATA():
    '''Temp = "Temp"
    Percent="%"
    Distance = "Dist"
    Pressure = "KPA"
    NM= "NewtonMeters"
    Count = 'count'
    Ratio='Ratio'
    Airflow='G/S'
    '''

    def __init__(self, gauge):
        self.GAUGE = gauge
        self.Value= gauge.Value
    def changeValue(self, newvalue):
        self.GAUGE.changeValue(newvalue)
        self.Value= newvalue


global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, MAF, IntakeAirTemp,OilTemp, FuelRate, AirIntakeTemp, ThrottlePos, MAFORBOOST

#UI VARS

#LOAD STATIC VALUES FROM FILE

MAFcmd=commands.getPID('MAF')
oilcmd= commands.getPID("FRS_OIL_TEMP")
coolantcmd=commands.getPID("COOLANT_TEMP")
engineloadcmd=commands.getPID("ENGINE_LOAD")
throttlecmd=commands.getPID("THROTTLE_POS")
rpmcmd=commands.getPID("RPM")
tqcmd=commands.getPID("THROTTLE_POS")
###UPDATE DATA FUNCTIONS
global firstpass
firstpass= True
def updateUIData():
    ###STORE ALL PID IN ARRAY FOR EASIER UPDATING WITH FOR LOOP
    ###ALSO REDUCE DELAY FOR COM to .09 this will allow fast comunication and no overload and backup on obd que
    global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, MAF, IntakeAirTemp, OilTemp, FuelRate, AirIntakeTemp, ThrottlePos, MAFORBOOST
    global firstpass
    ###CHECK PAGE BY PAGE FOR UPDATES B/C UPDATING ALL AT ONCE IS BAD AF
    if(UIINDEBUG):
        checkforstatus()
        return
    if(firstpass):
        firstpass=False
        carvin['text']= "["+str(com.query(commands.getPID("VIN")))+']'

    if currentPage == 1:
        MAFORBOOST.changeValue(int(com.query(MAFcmd)))
        AbsoluteEngineLoad.changeValue(int(com.query(engineloadcmd)))
        CoolantTemp.changeValue(CtoF(int(com.query(coolantcmd))))
        OilTemp.changeValue(CtoF(int(com.query(oilcmd))))
    if currentPage ==2:
        hp=200.00 #horsepower of engine
        localrpm=int(com.query(rpmcmd))
        localtq= int(((float(localrpm) *  5252)/hp))
        graph.newdatapt(localrpm,localtq)
    if currentPage ==3:
        pass



    #print (com(commands.getPID("SPEED")))
    #print('updating data')
    checkforstatus()
    #root.after(5000, updateUIData)

def checkforstatus():

    if(CoolantTemp.Value < 120):
        #popup snowflake
        coldlight.SetStatus(True)
    else:
        coldlight.SetStatus(False)

    if (CoolantTemp.Value >173):
        # popup snowflake
        TrackReady.SetStatus(True)
    else:
        TrackReady.SetStatus(False)
    if (CoolantTemp.Value >240 or OilTemp.Value > 265):
        # popup snowflake
        HeatWarning.SetStatus(True)
    else:
        HeatWarning.SetStatus(False)
    if(COMERROR):
        CWarning.SetStatus(True)
    else:
        CWarning.SetStatus(False)
###UI CLASS HERE

class Page(tk.Frame):
    global buttonNavList
    global currentPage
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
        global currentPage
        global buttonNavList
        ###set active page for data update functions
        currentPage = int(self.id[1:])
        print (currentPage)

        if buttonNavList !=None:
            for btn in buttonNavList:
                btn['bg'] = ui.activeTheme.color3
                if self.id == "p1" and btn.id=='b1':
                    btn['bg']=ui.activeTheme.color2
                if self.id == "p2" and btn.id=='b2':
                    btn['bg']=ui.activeTheme.color2
                if self.id == "p3" and btn.id=='b3':
                    btn['bg']=ui.activeTheme.color2
                if self.id == "p4" and btn.id=='b4':
                    btn['bg']=ui.activeTheme.color2
                

class Page1(Page):


    def __init__(self, *args, **kwargs):
        global ui
        stylearr=[]
        gaugesticky= tk.NS
        gaugepadx=0
        gaugepady=0
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self, bg = ui.activeTheme.color4)
        frame.pack(side="top", fill="both", expand=True)
        #create the display here
        title = tk.Label(frame, text='Overview', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                         font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1.5),'bold'))
        title.grid(column=0, row=0, columnspan=3, sticky=tk.NW, pady=0)
        #spacer
        tk.Label(frame, text='',pady=0, bg=ui.activeTheme.color4).grid(column=0, row=1)

        DisplayPos = 0
        #0105 ENGINE COOLANT TEMP USE THIS TO DETECT PEDAL DANCE @ 174F
        t=tk.Label(frame, text='Coolant Temp', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                 font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .9)))
        t.grid(column=DisplayPos, row=2)
        coolantg = Gauge(frame,width=200, height=200)
        coolantg.grid(column=DisplayPos, row=3, sticky = gaugesticky, pady= gaugepady, padx=gaugepadx)
        coolantg.setup(32,-10,250,'°F', 15)
        stylearr.append(coolantg)

        DisplayPos=1
        # 015C ENGINE OIL TEMP
        t = tk.Label(frame, text='Oil Temp', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                     font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .9)))
        t.grid(column=DisplayPos, row=2)
        oilg = Gauge(frame, width=200, height=200)
        oilg.grid(column=DisplayPos, row=3, sticky=gaugesticky, pady=gaugepady, padx=gaugepadx)
        oilg.setup(32, -10, 280, '°F', 10)
        stylearr.append(oilg)



        DisplayPos=2
        #0104 ABSOLUTE ENGINE LOAD
        t = tk.Label(frame, text='Absolute Load', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                     font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .9)))
        t.grid(column=DisplayPos, row=2)
        abslg = Gauge(frame, width=200, height=200)
        abslg.grid(column=DisplayPos, row=3, sticky=gaugesticky, pady=gaugepady, padx=gaugepadx)
        abslg.setup(0, 0, 100, '%', 20)
        stylearr.append(abslg)

        #0110 MAF SENSOR FOR AIR FLOW

        DisplayPos=3
        t = tk.Label(frame, text='Air Flow', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                     font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .9)))
        t.grid(column=DisplayPos, row=2)
        aflowg = Gauge(frame, width=200, height=200)
        aflowg.grid(column=DisplayPos, row=3, sticky=gaugesticky, pady=gaugepady, padx=gaugepadx)
        aflowg.setup(0, 0, 655, 'g/s', 75)
        stylearr.append(aflowg)

        ###NOW we do status lights
        global coldlight, TrackReady, HeatWarning, CWarning
        statpady= 20
        coldlight= statusWarning(frame,'blue',ui.activeTheme.unlitColor, False, '❄')
        coldlight.grid(column=0, row=4,pady=statpady)
        TrackReady = statusWarning(frame, '#02ce1d', ui.activeTheme.unlitColor, False, '∞')
        TrackReady.grid(column=1, row=4, pady=statpady)
        HeatWarning = statusWarning(frame, '#ff5900', ui.activeTheme.unlitColor, False, 'HOT')
        HeatWarning.grid(column=2, row=4, pady=statpady)
        CWarning = statusWarning(frame, 'red', ui.activeTheme.unlitColor, False, '!!!')
        CWarning.grid(column=3, row=4, pady=statpady)



        ###ADDSPACE ON LAST ROW AND COL

        ###LAST THING IS CREATE PID OBJS

        global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, IntakeAirTemp, OilTemp, FuelRate, AirIntakeTemp, ThrottlePos, MAFORBOOST
        #ThrottlePos = PIDDATA(0, throtlebar, throtletxt, PIDDATA.Percent,0)
        #AbsoluteEngineLoad = PIDDATA(0, engineabsbar, engineabstxt, PIDDATA.Percent,0)
        CoolantTemp = PIDDATA(coolantg)
        OilTemp = PIDDATA(oilg)
        AbsoluteEngineLoad= PIDDATA(abslg)
        MAFORBOOST = PIDDATA(aflowg)

        ###ALSO ADD ALL TO ARRS AND CALL stylize
        #regtxtarr = [throtletitle, coolanttitle, engineabstitle, oiltitle, oiltxt, coolanttxt, engineabstxt, throtletxt]
        #stylizeui(regtxtarr, 'pagetext')

        #progressbars =[oilbar,coolantbar,engineabsbar,throtlebar]
        #stylizeui(progressbars, 'progressbar')


        for s in stylearr:
            s.style(ui.activeTheme.color1,ui.activeTheme.color4, ui.activeTheme.font, ui.activeTheme.fontsize)
            s.inidraw()

class statusWarning(tk.Label):
    def __init__(self, parrent, litcolor, unlitcolor, boollitornot, symbol):
        tk.Label.__init__(self,parrent, fg= litcolor, bg=ui.activeTheme.color4, font=(ui.activeTheme.font, int(ui.activeTheme.fontsize*3)), text=symbol)
        self.lit= boollitornot
        self.litColor=litcolor
        self.unlitColor = unlitcolor
        self.check()
    def SetStatus(self, bool):
        self.lit = bool
        self.check()
    def check(self):
        if(self.lit):
            self['fg']= self.litColor
        else:
            self['fg']= self.unlitColor



        
class Page2(Page):
    def __init__(self, *args, **kwargs):
         global graph
         global ui
         global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, MAF, IntakeAirTemp, OilTemp, FuelRate, AirIntakeTemp, ThrottlePos
         Page.__init__(self, *args, **kwargs)
         frame = tk.Frame(self, bg = ui.activeTheme.color4)
         frame.pack(side="top", fill="both", expand=True)
         #create the display here
         title = tk.Label(frame, text='Race View', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                          font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1.5), 'bold'))
         title.grid(column=0, row=0, sticky=tk.NW, pady=0, columnspan=3)
         rownum=1

         #rpm graph on the right
         graph= RevGraph(frame, height=340, width=610, bg= ui.activeTheme.color4, bd=0, relief='ridge', highlightthickness=0)
         graph.grid(column=2, row=rownum, rowspan=5)

         #tiny gauges here
         tinygarr=[]
         gaugepady=0
         gaugepadx=20
         gaugesticky=tk.NS
         #oil
         t = tk.Label(frame, text='Oil Temp', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                      font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .9)))
         t.grid(column=0, row=1)
         oilg = Gauge(frame, width=150, height=150)
         oilg.grid(column=0, row=2, pady=gaugepady, padx=gaugepadx, sticky= gaugesticky)
         oilg.setup(32, -10, 280, '°F', 10)
         tinygarr.append(oilg)
         #MAF
         t = tk.Label(frame, text='MAF', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                      font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .9)))
         t.grid(column=0, row=3)
         mafg = Gauge(frame, width=150, height=150)
         mafg.grid(column=0, row=4, pady=gaugepady, padx=gaugepadx, sticky=gaugesticky)
         mafg.setup(0, 0, 655, 'g/s', 75)
         tinygarr.append(mafg)
         for s in tinygarr:
             s.style(ui.activeTheme.color1, ui.activeTheme.color4, ui.activeTheme.font, ui.activeTheme.fontsize)
             s.inidraw()


###create rpm and TQ graph
class RevGraph(tk.Canvas):
    #340 by 600

    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args,**kwargs)
        self.rpmcolor = ui.activeTheme.color1
        self.spdcolor = '#ef9a2d'
        self.gridcolor='#232323'
        self.timescale=50 #50px =1 second
        self.graphwidth=600
        self.graphheight =300
        self.points=[]
        self.lines=[]#for rpm
        self.speedlines=[]##for tq
        self.drawlabels()
        self.points.append(datapt(0,0))

    def ElapseTime(self):
        for s in self.points:
            s.passtime()
    #newpt also passes time

    #iniator function
    def newdatapt(self, rpm, tq):
        self.points.append(datapt(rpm, tq))
        self.drawgraph()

    #main graph function others just assist
    def drawgraph(self):
        self.cleargraph()
        self.ElapseTime()
        ct=len(self.points)-1
        while ct > -1:
            #######rpm line
            #we go from high to low high is at far side
            #rpm from 1 to 8000
            calcvar= len(self.points)- ct
            ctt= ct-1
            if ctt<0:
                ctt=0

            x1=int(self.graphwidth- calcvar*self.timescale)
            y1=int(300-int(float(self.points[ct].RPMvalue)/30.0))
            x2=int(self.graphwidth- (calcvar+1)*self.timescale)
            y2=int(300-int(float(self.points[ctt].RPMvalue)/30.0))
            ###OLD CODE HERE###
            #self.lines.append(self.create_line(x1,y1,x2,y2))

            ###OBJ POOL###
            self.coords(self.lines[ct], x1, y1, x2, y2)



            #spdline
            x1 = int(self.graphwidth - calcvar * self.timescale)
            y1 = int(300 - int(float(self.points[ct].Speedvalue) *1.5))
            x2 = int(self.graphwidth - (calcvar + 1) * self.timescale)
            y2 = int(300 - int(float(self.points[ctt].Speedvalue) *1.5))
            ###OLD CODE HERE###
            # self.lines.append(self.create_line(x1,y1,x2,y2))

            ###OBJ POOL###
            self.coords(self.speedlines[ct], x1, y1, x2, y2)
            ct-=1
            #print('ct: '+str(ct))


    def drawlabels(self):
        # grid lines here
        grid = []
        gridspacing = 50
        xpos = gridspacing
        ypos = gridspacing
        # horizontal lines
        while (ypos < 300):
            grid.append(self.create_line(0, ypos, 600, ypos))
            ypos = ypos + gridspacing
        # vertical lines
        while (xpos < 600):
            grid.append(self.create_line(xpos, 0, xpos, 300))
            xpos = xpos + gridspacing
        for g in grid:
            self.itemconfig(g, fill=self.gridcolor)
            # border Lines here
        ###create line obj pool
        x = 15  # lines length
        while x > -1:
            self.lines.append(self.create_line(0, 0, 0, 0))
            x -= 1
        for l in self.lines:
            self.itemconfigure(l,fill=self.rpmcolor)
        x = 15  # lines length
        while x > -1:
            self.speedlines.append(self.create_line(0, 0, 0, 0))
            x -= 1
        for l in self.speedlines:
            self.itemconfigure(l,fill=self.spdcolor)

        borders = []
        # x1, y1, x2, y2
        borders.append(self.create_line(0, 0, 0, 300))
        borders.append(self.create_line(600, 0, 600, 300))
        borders.append(self.create_line(0, 300, 600, 300))
        borders.append(self.create_line(0, 0, 600, 0))
        for b in borders:
            self.itemconfig(b, fill=ui.activeTheme.color1)

        self.create_text(30,14, text='RPM', fill=self.rpmcolor, justify=tk.RIGHT, font=(ui.activeTheme.font, int(ui.activeTheme.fontsize*.8)))
        self.create_text(self.graphwidth-60, 14, text='Speed (MPH)', fill=self.spdcolor, justify=tk.RIGHT, font=(ui.activeTheme.font, int(ui.activeTheme.fontsize*.8)))
        self.create_text(305,330, text='Time (1 Second)', fill= ui.activeTheme.color1, font=(ui.activeTheme.font, ui.activeTheme.fontsize))
        #use for loop to create the labels
        #rpm here
        ypos=gridspacing
        rpmct=7500
        while (ypos < 300):
            self.create_text(30,ypos, text=str(rpmct), fill=self.rpmcolor)
            rpmct-=1500
            ypos = ypos + gridspacing
        self.create_text(30, 290, text=str(0), fill=self.rpmcolor)
        # spd here
        ypos = gridspacing
        spdct = 120
        while (ypos < 300):
            self.create_text(self.graphwidth-30, ypos, text=str(spdct), fill=self.spdcolor)
            spdct -= 24
            ypos = ypos + gridspacing
        self.create_text(self.graphwidth - 30, 290, text=str(0), fill=self.spdcolor)



    def cleargraph(self):
        #for s in self.lines:
        #    self.delete(s)
        #self.lines =[]
        #find out what points to delete
        numtokeep= int(float(self.graphwidth)/float(self.timescale))+1
        if(numtokeep < len(self.points)):
            sent= len(self.points)
            x=sent-numtokeep-1
            newarr=[]
            #print('cut array down')
            while x <sent:
                newarr.append(self.points[x])
                x+=1
            self.points=newarr




    def debuggraph(self):
        self.newdatapt(rand.randint(600,8000), rand.randint(0, 160))
        '''print("Graph debug\n---------")
        print("self.lines size: "+str(self.lines.__sizeof__())+' bytes')
        print("self.points size: " + str(self.points.__sizeof__()) + ' bytes')
        #calc abg id
        x=0
        for l in self.lines:
            x+=l
        x= x/len(self.lines)
        print('avg line id: ' +str(x))'''





class datapt():
    def __init__(self, rpmvalue, spdvalue):
        self.Time = 0
        self.RPMvalue= rpmvalue
        self.Speedvalue= spdvalue
    def passtime(self):
        self.Time = self.Time+1




class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self, bg=ui.activeTheme.color4)
        frame.pack(side="top", fill="both", expand=True)
        title = tk.Label(frame, text='Fuel View', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                         font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1.5), 'bold'))
        title.grid(column=0, row=0, sticky=tk.NW, pady=0, columnspan=4)

        #FUEL LEVEL REMAINING
        t= tk.Label(frame, text='Fuel Level', fg = ui.activeTheme.color1, bg=ui.activeTheme.color4,font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .8)) )
        t.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=17)
        fuelgauge= BarGauge(frame, width=400, height=90)
        fuelgauge.grid(column=0, row=2, columnspan=3, padx=15)
        fuelgauge.style(ui.activeTheme.color1, ui.activeTheme.color4, "Helvetica", 34)
        fuelgauge.setup(86, 0, 100, '%', 10)

        ##vert spacer
        spacer1=tk.Label(frame, text='                         ', bg= ui.activeTheme.color4)
        spacer1.grid(row=2, column=4)

        #miles to empty 330 * fuel remaing
        fuelrtitle = tk.Label(frame, text='Range', fg = ui.activeTheme.color1, bg=ui.activeTheme.color4,font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .8)) )
        fuelrtitle.grid(row=1, column=5, sticky=tk.W)
        RangeValue = tk.Label(frame, text='227', fg = ui.activeTheme.color1, bg=ui.activeTheme.color4,font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 4)))
        RangeValue.grid(row=2, column=5, sticky=tk.SW)
        RangeLabel= tk.Label(frame, text='Miles', fg = ui.activeTheme.color1, bg=ui.activeTheme.color4,font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1)))
        RangeLabel.grid(row=2, column=6, sticky= tk.SW, pady=13)
        #throtle position %
        fuelrtitle = tk.Label(frame, text='Throtle Position', fg=ui.activeTheme.color1, bg=ui.activeTheme.color4,
                              font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .8)))
        fuelrtitle.grid(row=3, column=0, columnspan=3, sticky=tk.W)

        #Fuel Rate


        ###ADDSPACE ON LAST ROW AND COL
        spacecol = tk.Label(frame, text='', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                            font=(ui.activeTheme.font, ui.activeTheme.fontsize))
        spacecol.grid(column=99, row=0, padx=400)
        spacerow = tk.Label(frame, text='', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                            font=(ui.activeTheme.font, ui.activeTheme.fontsize))
        spacerow.grid(column=0, row=99, pady=400)



class PageSettings(Page):
    def __init__(self, *args, **kwargs):
        global ui
        rownum=0
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)
        frame.config(bg=ui.activeTheme.color4)
        title = tk.Label(frame, text='Settings', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                         font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1.5), 'bold'))
        title.grid(row=rownum, column=0, pady=0, sticky= tk.NW)

        #do row nums to add temp support in settings
        
        ###PEDAL DANCE CTRL HERE###
        rownum=1
        showpedaltxt=tk.Label(frame, text='Show Track Pop-Up:', bg =ui.activeTheme.color4, fg=ui.activeTheme.color1, font= (ui.activeTheme.font, int(ui.activeTheme.fontsize)))
        showpedaltxt.grid(column=0, row=rownum, sticky=tk.E)
        showpedalbtn= toggle(frame)
        showpedalbtn.grid(column = 2, row=rownum, sticky= tk.NW)
        showpedalbtn.load('PedalDancePopUp')

        ###PEDAL DANCE CTRL HERE###
        showpedaltxt = tk.Label(frame, text='Show Turbo Info:', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                                font=(ui.activeTheme.font, int(ui.activeTheme.fontsize)))
        showpedaltxt.grid(column=0, row=2, sticky=tk.E)
        showpedalbtn = toggle(frame)
        showpedalbtn.grid(column=2, row=2, sticky=tk.NW)
        showpedalbtn.load('ShowTurbo')

        ###THEME BUTTONS HERE
        themetitle = tk.Label(frame, text='Theme:',bg=ui.activeTheme.color4, fg=ui.activeTheme.color1, font=(ui.activeTheme.font, int(ui.activeTheme.fontsize)))
        themetitle.grid(column=0, row=3, sticky= tk.E)
        ###THEME SELECT BUTTONS WILL USE COL 1 LIKE THE SPACER
        nxt = themeclicker(frame)
        nxt.load(1)
        nxt.grid(column=1, row=3, sticky=tk.NE, padx= 90)

        themeid = themeLabel(frame)
        themeid.grid(column =1, row=3, sticky = tk.NS)

        prev = themeclicker(frame)
        prev.load(-1)
        prev.grid(column=1, row=3, sticky=tk.NW, padx=90)


        divider= tk.Label(frame, text='Stats:', background = ui.activeTheme.color4, fg=ui.activeTheme.color1,font=(ui.activeTheme.font, int(ui.activeTheme.fontsize *1.35)))
        divider.grid(column=0, row=4, pady=25)
        ###STATS HERE###
        #0 to 60
        ZT60title = tk.Label(frame, text= "Zero to 60: ",bg=ui.activeTheme.color4, fg=ui.activeTheme.color1, font=(ui.activeTheme.font, int(ui.activeTheme.fontsize)))
        ZT60title.grid(column=0, row =5, sticky = tk.NE)
        ZT60value = tk.Label(frame, text="6.31", bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                             font=(ui.activeTheme.font, int(ui.activeTheme.fontsize)))
        ZT60value.grid(column=1, row=5, sticky=tk.NW)
        ZT60cal = tk.Button(frame, text='0-60 Pull')#need styling
        ZT60cal.grid(column=2, row =5)

        #hp

        #ODO

        #TQ

        ###SPACE COL 1###
        spacer = tk.Label(frame, text=" ", bg=ui.activeTheme.color4)
        spacer.grid(column=1, row=0,padx=250)

        ###ADDSPACE ON LAST ROW AND COL
        spacecol = tk.Label(frame, text='', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                            font=(ui.activeTheme.font, ui.activeTheme.fontsize))
        spacecol.grid(column=99, row=0, padx=400)
        spacerow = tk.Label(frame, text='', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                            font=(ui.activeTheme.font, ui.activeTheme.fontsize))
        spacerow.grid(column=0, row=99, pady=400)

class themeLabel(tk.Label):
    global ui
    themeList = [ui.themeOne, ui.themeTwo, ui.themeThree]
    def findtheme(self):
        global themeList
        ct=0
        for t in themeList:
            if(t.color1 == ui.activeTheme.color1 and t.color2 == ui.activeTheme.color2 and t.color3 == ui.activeTheme.color3):
                print('theme id = '+str(ct))
                return ct
            if(ct>2):
                return 2
            ct= ct+1

    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)
        t = self.findtheme() +1
        txt= 'Theme '+ str(t)
        self.configure( text=txt, bg =ui.activeTheme.color4, fg=ui.activeTheme.color1, font= (ui.activeTheme.font, int(ui.activeTheme.fontsize)))

class themeclicker(tk.Button):
    global ui
    global themeList
    themeList = [ui.themeOne, ui.themeTwo, ui.themeThree]
    ###NEVER PASS STYLES WHEN CREATING OBJECT INSTACE MODIFY THISS CLASS DIRECTLY OR DUPLICATE AND MODIFY
    def __init__(self, *args, **kwargs):
        global ui
        tk.Button.__init__(self, *args, **kwargs)
        self['command'] = self.clickit
        ###STYLES LOADED IN HERE IN CLASS INIT
        self.ThemeID= 0
        self.configure(borderwidth=0, highlightthickness=0, fg=ui.activeTheme.color1, pady=10,
                       font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * .5), 'bold'), width=12)


    def findtheme(self):
        global themeList
        ct=0
        for t in themeList:
            if(t.color1 == ui.activeTheme.color1 and t.color2 == ui.activeTheme.color2 and t.color3 == ui.activeTheme.color3):
                print('theme id = '+str(ct))
                return ct
            if(ct>2):
                return 2
            ct= ct+1


    def clickit(self):
        global themeList
        if(self.mode):
            ###ADD TO THEME COUNT
            ltheme= self.findtheme()
            if(ltheme< 2):
                ltheme=ltheme+1
                ui.changetheme(themeList[ltheme])
                print (ui.activeTheme)
                reloadui()
            else:
                print("NO MORE THEMES")


        else:
            ###SUBTRACT
            ltheme = self.findtheme()
            if (ltheme > 0):
                ltheme = ltheme - 1
                ui.changetheme(themeList[ltheme])
                print (ui.activeTheme)
                reloadui()
            else:
                print("NO MORE THEMES")


    def load(self, intposormin):
        if(intposormin > 0):
            self.mode=True
            self['text'] ="Next"
        else:
            self.mode = False
            self['text'] ="Prev"

class toggle(tk.Button):
    global Settings
    global ui
    ###NEVER PASS STYLES WHEN CREATING OBJECT INSTACE MODIFY THISS CLASS DIRECTLY OR DUPLICATE AND MODIFY
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self['command']= self.clickit
        ###STYLES LOADED IN HERE IN CLASS INIT
        self.configure(borderwidth = 0, highlightthickness=0, fg= ui.activeTheme.color1, pady=10, font = (ui.activeTheme.font, int(ui.activeTheme.fontsize* .5), 'bold'), width=12)
        self.enabled= False
        self['text'] = 'OFF'
    def clickit(self):
        if(self.enabled):
            self.enabled=False
            self['text']='OFF'
        else:
            self.enabled = True
            self['text'] = 'ON'
        #print (str(self.enabled))

    def seton(self):
        self.enabled=True
        self['text'] = 'ON'

    def setoff(self):
        self.enabled=False
        self['text'] = 'OFF'
    def load(self, settingkey):
        if settingkey=="PedalDancePopUp":
            if(Settings.PedalDancePopUp):
                self.seton()
            else:
                self.setoff()
        ###REPEAT STRUCTURE FOR OTHER TOGGLES
        if settingkey=="ShowTurbo":
            if(Settings.ShowTurbo):
                self.seton()
            else:
                self.setoff()
        ###REPEAT STRUCTURE FOR OTHER TOGGLES


class MainView(tk.Frame):
    global p4
    def loadsettings(self):
        global p4
        p4.show()

    def __init__(self, *args, **kwargs):
        global p4
        global ui
        global buttonNavList
        global  popupwindow
        ###SOME INI SETUP CODE###
        tk.Frame.__init__(self, *args, **kwargs)



        
        
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = PageSettings(self)

        p1.id='p1'
        p2.id='p2'
        p3.id='p3'
        p4.id='p4'
        buttonframe = tk.Frame(self)

        container = tk.Frame(self)
        container.config(bg=ui.activeTheme.color4)
        
        
        buttonframe.pack(fill="x", expand=False, side='top')
        buttonframe.config(bg=ui.activeTheme.color4)
        
        ###CREATE DIVIDERBAR###
        txt='‾‾‾‾‾'
        for i in range(1,15):
            txt+=txt
        labeldiv = tk.Label(text=txt,font =(ui.activeTheme.font, ui.activeTheme.fontsize), bg=ui.activeTheme.color4, fg=ui.activeTheme.color1 )
        labeldiv.pack(fill="x", expand=False, after= buttonframe)
        
        container.pack(fill="both", expand=True, side='bottom')
        ###CAR TITLE AND VIN###

        ###ADD CAR VIN AND LOGIC HERE###
        ###DONT FORGET THE DATA HERE IS TEMP DATA###
        cartitle = tk.Label(buttonframe, text='FR-S ')
        cartitle.pack(side='left')
        cartitle.config(fg=ui.activeTheme.color1, bg= ui.activeTheme.color4, font = (ui.activeTheme.font, int(ui.activeTheme.fontsize*1.4)))
        global carvin
        carvin = tk.Label(buttonframe, text ='[VIN HERE]')
        carvin.config(fg=ui.activeTheme.color1, bg= ui.activeTheme.color4, font = (ui.activeTheme.font, int(ui.activeTheme.fontsize*0.9)))
        carvin.pack(side = 'left')
        

        ###NAV BUTTONS
        
        b1 = tk.Button(buttonframe, text="Overview")
        b1.configure(command = p1.show)
        b2 = tk.Button(buttonframe, text="Race View")
        b2.configure(command= p2.show)
        b3 = tk.Button(buttonframe, text="Fuel View")
        b3.configure(command=p3.show)
        b4 = tk.Button(buttonframe, text="Settings")
        b4.configure(command=p4.show)
        ###asign nav list and id###
        b1.id='b1'
        b2.id='b2'
        b3.id='b3'
        b4.id='b4'
        buttonNavList = {b1,b2,b3,b4}
        ###ADD SHARED BTN ATTR###
        for btn in buttonNavList:
            btn.configure(borderwidth = 0, highlightthickness=0, fg= ui.activeTheme.color1, pady=10, font = (ui.activeTheme.font, int(ui.activeTheme.fontsize* .5), 'bold'))
        
        ###PACE ALL PAGES IN SAME GRID CELL TO HAVE PAGE EFFECT
        p1.grid(column = 1, row=1, in_ = container, sticky=tk.NW)
        p2.grid(column=1, row=1, in_=container, sticky=tk.NW)
        p3.grid(column=1, row=1, in_=container, sticky=tk.NW)
        p4.grid(column=1, row=1, in_=container, sticky=tk.NW)


        
        ###PACK THE BUTTONS FOR THE NAV###
        b4.pack(side='right')
        b3.pack(side="right")
        b2.pack(side="right")
        b1.pack(side="right")

        
        

        ###OPEN PAGE ONE###
        p1.show()


        ###DEBUGPOPUP###




global main, root
root = tk.Tk()

main = MainView(root)
'''global oldtime
oldtime =7'''
def startupdate():
    '''global oldtime
    initime= timeit.default_timer()'''
    updateUIData()
    if(UIINDEBUG):
        graph.debuggraph()
    #time=timeit.default_timer()-initime
    #print (time)
    #####HERE is what we know, the graph function creates to many instances of lines over time
    #therfor we must either recycle lines using obj pooling or regin the canvas ()revGrapg after a certain amount of seconds
    '''if(oldtime +.000005> time):
        pass
    else:
        if(oldtime +.000009 < time):
            print("######WARING VERY SLOW#######")
        print ('slower')
    oldtime = time'''
    root.after(1000, startupdate)


def reloadui():
    global main, root
    root.destroy()
    root = tk.Tk()
    main =MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x480")
    ####start update methods####

    startupdate()
    main.loadsettings()
    root.mainloop()

####start update methods####
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("800x480")
startupdate()
root.mainloop()



# root = Tk()
# switch theme
# style = ttk.Style()
# style.theme_use('default')

# style.configure("RPM.Horizontal.TProgressbar", thickness=48, background=ui.themeOne.color2, fieldbackground='black')

# root.attributes("-fullscreen", True) for full screen display
# root.configure(background=ui.themeOne.color4)
# root2 = Tk()  # remove anyhting here with a 2 to disable the sim
# app = Application(master=root)

# app.configure() #background=ui.themeOne.color4 as param
# app.mainloop()
