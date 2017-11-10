# -*- coding: utf-8 -*-
from  SportUI import *
from  newobd import *
import Tkinter as tk
import ttk
import commands
global currentPage
currentPage=1
global UIINDEBUG
UIINDEBUG= True



###SET UP OBD CONNECTION###
com = None
if osx:
    # ports may be different depending on drivers and device
    com = OBDcom('/dev/tty.usbserial-113010881974', 115200, '6')
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
    def __init__(self, value, uibar, uitext, units):
        self.value = value
        self.uibar = uibar
        self.uitxt= uitext
        self.units = units
    def changeValue(self, newvalue):
        self.value = newvalue
        self.uibar['value'] = self.value
        self.uitxt['text'] = str(self.value)+str(self.units)


global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, MAF, IntakeAirTemp,OilTemp, FuelRate, AirIntakeTemp, ThrottlePos

#UI VARS

#LOAD STATIC VALUES FROM FILE



###UPDATE DATA FUNCTIONS
def updateUIData():
    ###STORE ALL PID IN ARRAY FOR EASIER UPDATING WITH FOR LOOP
    ###ALSO REDUCE DELAY FOR COM to .09 this will allow fast comunication and no overload and backup on obd que
    global CoolantTemp, AbsoluteEngineLoad, BHP, FuelTrim, MAF, IntakeAirTemp, OilTemp, FuelRate, AirIntakeTemp, ThrottlePos

    ###CHECK PAGE BY PAGE FOR UPDATES B/C UPDATING ALL AT ONCE IS BAD AF
    if(UIINDEBUG):
        return
    if currentPage == 1:
        ThrottlePos.changeValue(com.query(commands.getPID("THROTTLE_POS")))
        AbsoluteEngineLoad.changeValue(com.query(commands.getPID("ENGINE_LOAD")))
        CoolantTemp.changeValue(com.query(commands.getPID("COOLANT_TEMP")))
    if currentPage ==2:
        pass
    if currentPage ==3:
        pass



    #print (com(commands.getPID("SPEED")))
    #print('updating data')
    checkforpopup()
    root.after(5000, updateUIData)

def checkforpopup():
    ###this will be called once every second
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
        coolantbar['value'] = 50
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
        ThrottlePos = PIDDATA(0, throtlebar, throtletxt, "%")
        AbsoluteEngineLoad = PIDDATA(0, engineabsbar, engineabstxt, "%")
        CoolantTemp = PIDDATA(0, coolantbar, coolanttxt, 'DEG C')
        OilTemp = PIDDATA(0, oilbar, oiltxt, 'DEG C')

        ###ALSO ADD ALL TO ARRS AND CALL stylize
        regtxtarr = [throtletitle, coolanttitle, engineabstitle, oiltitle, oiltxt, coolanttxt, engineabstxt, throtletxt]
        stylizeui(regtxtarr, 'pagetext')

        progressbars =[oilbar,coolantbar,engineabsbar,throtlebar]
        stylizeui(progressbars, 'progressbar')

        
class Page2(Page):
    def __init__(self, *args, **kwargs):
         global ui
         Page.__init__(self, *args, **kwargs)
         frame = tk.Frame(self, bg = ui.activeTheme.color4)
         frame.pack(side="top", fill="both", expand=True)
         #create the display here
         title = tk.Label(frame, text='Race View', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                          font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1.5), 'bold'))
         title.grid(column=0, row=0, sticky=tk.NW, pady=0)
         #0162 ENGINE TQ

         #0110 MAF SENSOR FOR AIR FLOW

         #0143 ABSOLUTE ENGINE LOAD

         #0105 ENGINE COOLANT TEMP USE THIS TO DETECT PEDAL DANCE @ 174F this is in C

         #015C ENGINE OIL TEMP

         #0168 INTAKE AIR TEMP

         # bhp = MAF x 1.25
         ###ADDSPACE ON LAST ROW AND COL
         spacecol = tk.Label(frame, text='', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                             font=(ui.activeTheme.font, ui.activeTheme.fontsize))
         spacecol.grid(column=99, row=0, padx=400)
         spacerow = tk.Label(frame, text='', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                             font=(ui.activeTheme.font, ui.activeTheme.fontsize))
         spacerow.grid(column=0, row=99, pady=400)

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
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)
        frame.config(bg=ui.activeTheme.color4)
        title = tk.Label(frame, text='Settings', bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                         font=(ui.activeTheme.font, int(ui.activeTheme.fontsize * 1.5), 'bold'))
        title.grid(row=0, column=0, pady=0, sticky= tk.NW)

        ###PEDAL DANCE CTRL HERE###
        showpedaltxt=tk.Label(frame, text='Show Track Pop-Up:', bg =ui.activeTheme.color4, fg=ui.activeTheme.color1, font= (ui.activeTheme.font, int(ui.activeTheme.fontsize)))
        showpedaltxt.grid(column=0, row=1, sticky=tk.E)
        showpedalbtn= toggle(frame)
        showpedalbtn.grid(column = 2, row=1, sticky= tk.NW)
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



        ###CALIBRATE BUTTONS HERE###
        ZT60title = tk.Label(frame, text= "Zero to 60: ",bg=ui.activeTheme.color4, fg=ui.activeTheme.color1, font=(ui.activeTheme.font, int(ui.activeTheme.fontsize)))
        ZT60title.grid(column=0, row =4, sticky = tk.NE)
        ZT60value = tk.Label(frame, text="6.31", bg=ui.activeTheme.color4, fg=ui.activeTheme.color1,
                             font=(ui.activeTheme.font, int(ui.activeTheme.fontsize)))
        ZT60value.grid(column=1, row=4, sticky=tk.NW)
        #ZT60cal = tk.button()




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

def reloadui():
    global main, root
    root.destroy()
    root = tk.Tk()
    main =MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x480")
    updateUIData()
    main.loadsettings()
    root.mainloop()

main.pack(side="top", fill="both", expand=True)
root.wm_geometry("800x480")
updateUIData()
root.mainloop()


# root = Tk()
# switch theme
# style = ttk.Style()
# style.theme_use('default')

# style.configure("RPM.Horizontal.TProgressbar", thickness=48, background=ui.themeOne.color2, fieldbackground='black')

# root.attributes("-fullscreen", True) for full screen displau
# root.configure(background=ui.themeOne.color4)
# root2 = Tk()  # remove anyhting here with a 2 to disable the sim
# app = Application(master=root)

# app.configure() #background=ui.themeOne.color4 as param
# app.mainloop()
