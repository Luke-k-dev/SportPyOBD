# -*- coding: utf-8 -*-
from  SportUI import *
from  newobd import *
import Tkinter as tk
import ttk
import commands
from convert import *
import random as rand
import gc
global currentPage
currentPage=1
global UIINDEBUG
global graph
graph= None
UIINDEBUG= True ###PLEASE USE THIS
import timeit



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
t1 = css("#f47142", "#493030", "#332a23", "#303030", "Helvetica", 20)
# theme 2
t2 = css("#382", "#233", "#FFF", "#FFF", "Helvetica", 20)
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
    Temp = "Temp"
    Percent="%"
    Distance = "Dist"
    Pressure = "KPA"
    NM= "NewtonMeters"
    Count = 'count'
    Ratio='Ratio'
    Airflow='G/S'

    def __init__(self, value, uibar, uitext, typeofunit, minvalue):
        self.TypeOfUnit = typeofunit
        ###FOR TEMP###
        v= value
        if(typeofunit== PIDDATA.Temp):
            if(Settings.F):
                self.value = CtoF(value)
                self.uibar = uibar
                self.uitxt = uitext
                self.units = " F"
                self.minvalue = CtoF(minvalue)
            else:
                self.value = value
                self.uibar = uibar
                self.uitxt= uitext
                self.units = " C"
                self.minvalue= minvalue
        elif typeofunit == PIDDATA.Percent:
            self.value = value
            self.uibar = uibar
            self.uitxt = uitext
            self.units = " %"
            self.minvalue = minvalue
        elif typeofunit ==PIDDATA.Count:
            self.value = value
            self.uibar = uibar
            self.uitxt = uitext
            self.units = " Ct."
            self.minvalue = minvalue
        elif(typeofunit== PIDDATA.Distance):
            if(Settings.Miles):
                self.value = KmtoM(value)
                self.uibar = uibar
                self.uitxt = uitext
                self.units = " Miles"
                self.minvalue = KmtoM(minvalue)
            else:
                self.value = value
                self.uibar = uibar
                self.uitxt= uitext
                self.units = " Km"
                self.minvalue= minvalue
        #Catch units not yet made
        try:
            self.changeValue(v)
        except:
            print("ERROR UNIT NOT IMPLEMENTED IN PIDDATA CLASS, ALSO CHACK CHANGE VALUE METHOD AFTER PLZZZZ")
            raise NotImplementedError
    def changeValue(self, newvalue):
        unitsupported = False
        if(self.TypeOfUnit ==PIDDATA.Temp):
            unitsupported = True
            if(Settings.F):
                self.value = CtoF(newvalue)
            else:
                self.value= newvalue
        elif(self.TypeOfUnit ==PIDDATA.Percent or self.TypeOfUnit ==PIDDATA.Count):
            unitsupported = True
            self.value= newvalue



        ###we always do these
        if(unitsupported != True):
            print("ERROR UNIT NOT IMPLEMENTED IN PIDDATA changeValue(newvalue) method")
            raise NotImplementedError
        self.uibar['value'] = int(self.value)+abs(int(self.minvalue))
        self.uitxt['text'] = str(self.value)+" "+str(self.units)


global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, MAF, IntakeAirTemp,OilTemp, FuelRate, AirIntakeTemp, ThrottlePos

#UI VARS

#LOAD STATIC VALUES FROM FILE


oilcmd= commands.getPID("FRS_OIL_TEMP")
coolantcmd=commands.getPID("COOLANT_TEMP")
engineloadcmd=commands.getPID("ENGINE_LOAD")
throttlecmd=commands.getPID("THROTTLE_POS")

###UPDATE DATA FUNCTIONS
def updateUIData():
    ###STORE ALL PID IN ARRAY FOR EASIER UPDATING WITH FOR LOOP
    ###ALSO REDUCE DELAY FOR COM to .09 this will allow fast comunication and no overload and backup on obd que
    global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, MAF, IntakeAirTemp, OilTemp, FuelRate, AirIntakeTemp, ThrottlePos

    ###CHECK PAGE BY PAGE FOR UPDATES B/C UPDATING ALL AT ONCE IS BAD AF
    if(UIINDEBUG):
        return
    if currentPage == 1:
        ThrottlePos.changeValue(int(com.query(throttlecmd)))
        AbsoluteEngineLoad.changeValue(int(com.query(engineloadcmd)))
        CoolantTemp.changeValue(int(com.query(coolantcmd)))
        OilTemp.changeValue(int(com.query(oilcmd)))
    if currentPage ==2:
        pass
    if currentPage ==3:
        pass



    #print (com(commands.getPID("SPEED")))
    #print('updating data')
    checkforpopup()
    #root.after(5000, updateUIData)

def checkforpopup():
    ###this will be called right after the ui updates data perhaps even in the same frame
    #Pedal Dance Here
    pass
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

        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self, bg = ui.activeTheme.color4)
        frame.pack(side="top", fill="both", expand=True)
        #create the display here
        title = tk.Label(frame, text='Overview', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                         font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1.5),'bold'))
        title.grid(column=0, row=0, sticky=tk.NW, pady=0)
        DisplayPos = 1
        #0105 ENGINE COOLANT TEMP USE THIS TO DETECT PEDAL DANCE @ 174F
        coolanttitle = tk.Label(frame, text='Coolant Temp: ')
        coolanttitle.grid(column=0, row=DisplayPos, sticky=tk.NE, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)
        coolantbar = ttk.Progressbar(frame, orient="horizontal", length=500, mode="determinate")
        coolantbar['maximum'] = 300
        coolantbar['value'] = 40
        coolanttxt = tk.Label(frame, text='0 DEG C')
        coolanttxt.grid(column=2, row=DisplayPos, sticky=tk.NW, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)
        coolantbar.grid(column=1, row=DisplayPos, sticky=tk.NS, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)

        DisplayPos=2
        #0106 FUEL TRIM %


        DisplayPos=3
        #0110 MAF SENSOR FOR AIR FLOW

        DisplayPos=4
        #0143 ABSOLUTE ENGINE LOAD
        engineabstitle = tk.Label(frame, text='Engine Load: ')
        engineabstitle.grid(column=0, row=DisplayPos, sticky=tk.NE, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)
        engineabsbar = ttk.Progressbar(frame, orient="horizontal", length=500, mode="determinate")
        engineabsbar['maximum'] = 25700
        engineabsbar['value'] = 200
        engineabstxt = tk.Label(frame, text='0%')
        engineabstxt.grid(column=2, row=DisplayPos, sticky=tk.NW, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)
        engineabsbar.grid(column=1, row=DisplayPos, sticky=tk.NS, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)

        DisplayPos=5
        #015C ENGINE OIL TEMP
        oiltitle = tk.Label(frame, text='Oil Temp: ')
        oiltitle.grid(column=0, row=DisplayPos, sticky=tk.NE, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)
        oilbar = ttk.Progressbar(frame, orient="horizontal", length=500, mode="determinate")
        oilbar['maximum'] = 300
        oilbar['value'] = 10
        oiltxt = tk.Label(frame, text='0 DEG C')
        oiltxt.grid(column=2, row=DisplayPos, sticky=tk.NW, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)
        oilbar.grid(column=1, row=DisplayPos, sticky=tk.NS, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)

        DisplayPos=6
        #015E ENGINE FUEL RATE LITERS/HR

        DisplayPos=7
        #0162 ENGINE TQ

        DisplayPos=8
        #0168 INTAKE AIR TEMP

        DisplayPos=9
        #throttle pos PID: 0111
        throtletitle = tk.Label(frame, text='Throttle Pos: ')
        throtletitle.grid(column =0, row=DisplayPos, sticky= tk.NE, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)
        throtlebar = ttk.Progressbar(frame, orient="horizontal", length=500, mode="determinate")
        throtlebar['maximum'] = 100
        throtlebar['value'] = 10
        throtletxt= tk.Label(frame, text='0%')
        throtletxt.grid(column = 2, row =DisplayPos, sticky=tk.NW, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)
        throtlebar.grid(column = 1, row=DisplayPos, sticky= tk.NS, padx= ui.activeTheme.padx, pady=ui.activeTheme.pady)


        ###ADDSPACE ON LAST ROW AND COL
        spacecol = tk.Label(frame, text='', bg=ui.activeTheme.color4, fg = ui.activeTheme.color1, font =(ui.activeTheme.font, ui.activeTheme.fontsize))
        spacecol.grid(column = 99, row = 0, padx = 400)
        spacerow = tk.Label(frame, text='', bg=ui.activeTheme.color4, fg = ui.activeTheme.color1, font =(ui.activeTheme.font, ui.activeTheme.fontsize))
        spacerow.grid(column=0, row=99, pady=400)

        ###LAST THING IS CREATE PID OBJS

        global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, MAF, IntakeAirTemp, OilTemp, FuelRate, AirIntakeTemp, ThrottlePos
        ThrottlePos = PIDDATA(0, throtlebar, throtletxt, PIDDATA.Percent,0)
        AbsoluteEngineLoad = PIDDATA(0, engineabsbar, engineabstxt, PIDDATA.Percent,0)
        CoolantTemp = PIDDATA(0, coolantbar, coolanttxt, PIDDATA.Temp,-40)
        OilTemp = PIDDATA(0, oilbar, oiltxt, PIDDATA.Temp,-40)

        ###ALSO ADD ALL TO ARRS AND CALL stylize
        regtxtarr = [throtletitle, coolanttitle, engineabstitle, oiltitle, oiltxt, coolanttxt, engineabstxt, throtletxt]
        stylizeui(regtxtarr, 'pagetext')

        progressbars =[oilbar,coolantbar,engineabsbar,throtlebar]
        stylizeui(progressbars, 'progressbar')

        
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
         title.grid(column=0, row=0, sticky=tk.NW, pady=0)
         rownum=1

         #rpm graph on the right
         graph= RevGraph(frame, height=340, width=610, bg= ui.activeTheme.color4, bd=0, relief='ridge', highlightthickness=0)
         graph.grid(column=2, row=rownum)


         # bhp = MAF x 1.25


###create rpm and TQ graph
class RevGraph(tk.Canvas):
    #340 by 600

    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args,**kwargs)
        self.rpmcolor = 'red'
        self.tqcolor = 'yellow'
        self.timescale=50 #50px =1 second
        self.graphwidth=600
        self.graphheight =300
        self.points=[]
        self.lines=[]
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
            y1=int(300-int(float(self.points[ct].RPMvalue)/28.0))
            x2=int(self.graphwidth- (calcvar+1)*self.timescale)
            y2=int(300-int(float(self.points[ctt].RPMvalue)/28.0))
            ###OLD CODE HERE###
            #self.lines.append(self.create_line(x1,y1,x2,y2))

            ###OBJ POOL###
            self.coords(self.lines[ct], x1, y1, x2, y2)


            #tqline

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
            self.itemconfig(g, fill=ui.activeTheme.color3)
            # border Lines here
        borders = []
        # x1, y1, x2, y2
        borders.append(self.create_line(0, 0, 0, 300))
        borders.append(self.create_line(600, 0, 600, 300))
        borders.append(self.create_line(0, 300, 600, 300))
        borders.append(self.create_line(0, 0, 600, 0))
        for b in borders:
            self.itemconfig(b, fill=ui.activeTheme.color1)

        self.create_text(30,14, text='RPM', fill=self.rpmcolor, justify=tk.RIGHT, font=(ui.activeTheme.font, int(ui.activeTheme.fontsize*.8)))
        self.create_text(70, 14, text='TQ', fill=self.tqcolor, justify=tk.RIGHT, font=(ui.activeTheme.font, int(ui.activeTheme.fontsize*.8)))
        self.create_text(305,330, text='Time Since Last Update', fill= ui.activeTheme.color1, font=(ui.activeTheme.font, ui.activeTheme.fontsize))
        ###create line obj pool
        x= 15 #lines length
        while x > -1:
            self.lines.append(self.create_line(0,0,0,0))
            x-=1

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
        self.newdatapt(rand.randint(600,8000), rand.randint(0, 65000))
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
    def __init__(self, rpmvalue, tqvalue):
        self.Time = 0
        self.RPMvalue= rpmvalue
        self.TQvalue= tqvalue
    def passtime(self):
        self.Time = self.Time+1




class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self, bg=ui.activeTheme.color4)
        frame.pack(side="top", fill="both", expand=True)
        title = tk.Label(frame, text='Fuel View', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                         font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1.5), 'bold'))
        title.grid(column=0, row=0, sticky=tk.NW, pady=0)

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

class popup(tk.Frame):

    def __init__(self, *args, **kwargs):
        global ui
        tk.Frame.__init__(self, *args, **kwargs)
        self.config(bg=ui.activeTheme.color4)
        self.pdancetxt='TRACK MODE\nREADY\n'+u"\u26A0"
        self.coldwarning = 'ENGINE\nCOLD\n' + u"\u26A0"
        self.txt = tk.Label(self, text="", bg=ui.activeTheme.color4, fg= ui.activeTheme.alertcolor, font= (ui.activeTheme.fontsize,90))
        self.txt.pack()
    def show(self, displayset):
        if displayset=='PEDAL':
            self.txt['text'] = self.pdancetxt
        elif displayset =='ENGINECOLD':
            self.txt['text'] = self.coldwarning
        elif displayset == "OILTEMP":
            pass
        elif displayset=='BCK':
            ###THIS IS FOR UI BCK FORMATING
            self.txt['text']= 'test'

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
        popupwindow = popup(self)
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
        carvin = tk.Label(buttonframe, text ='[JF1ZCAC12D1607662]')
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
        popupwindow.grid(column=1, row =1, in_=container, sticky = tk.NSEW)

        
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
    root.after(1000,startupdate)


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
