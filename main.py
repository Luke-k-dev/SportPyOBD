# -*- coding: utf-8 -*-
from  SportUI import *
from  newobd import *
import Tkinter as tk
import ttk
global currentPage
currentPage=1
###SET UP OBD CONNECTION###
com = None
if osx:
    # ports may be different depending on drivers and device
    com = OBDcom('/dev/tty.usbserial-113010881974', 115200, '1')
else:

    com = OBDcom('/dev/ttyUSB0', 115200, None)

###NOW LOAD IN UI DATA###
# THEMES ARE HERE COLOR COLOR COLOR COLOR FONT SIZE
#FONT COLOR 1, FONT COLOR 2, PROGRESS BAR COLOR, backgourd color
# theme 1
t1 = css("#f47142", "#493030", "#332a23", "#303030", "Helvetica", 20)
# theme 2
t2 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", 16)
# theme 3
t3 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", 16)


ui = UI(t1, t2, t3)
global buttonNavList
buttonNavList=None
###UI CLASS HERE

class Page(tk.Frame):
    global buttonNavList
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
        global buttonNavList
        x=4
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
    global throtlebar
    def updatedata(self):
        global throtlebar
        throtlebar['value'] = 50
    
    def __init__(self, *args, **kwargs):
        global throtlebar
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self, bg = ui.activeTheme.color4)
        frame.pack(side="top", fill="both", expand=True)
        #create the display here

        #0105 ENGINE COOLANT TEMP USE THIS TO DETECT PEDAL DANCE @ 174F

        #bhp = MAF x 1.25

        #0106 FUEL TRIM %
        
        #0110 MAF SENSOR FOR AIR FLOW

        #0143 ABSOLUTE ENGINE LOAD

        #015C ENGINE OIL TEMP

        #015E ENGINE FUEL RATE LITERS/HR

        #0162 ENGINE TQ

        #0168 INTAKE AIR TEMP

        #throttle pos PID: 0111
        throtletitle = tk.Label(frame, text='Throtle Pos: ', bg=ui.activeTheme.color4, fg = ui.activeTheme.color1, font =(ui.activeTheme.font, ui.activeTheme.fontsize))
        throtletitle.grid(column =0, row=2, sticky= tk.NE)
        throtlebar = ttk.Progressbar(frame, orient="horizontal", length=500, mode="determinate")
        throtlebar['maximum'] = 100
        throtlebar['value'] = 10
        throtlebar.grid(column = 1, row=2, sticky= tk.NS)
        self.updatedata()
        
class Page2(Page):
    def __init__(self, *args, **kwargs):
         Page.__init__(self, *args, **kwargs)
         frame = tk.Frame(self, bg = ui.activeTheme.color4)
         frame.pack(side="top", fill="both", expand=True)
         #create the display here

         #0162 ENGINE TQ

         #0110 MAF SENSOR FOR AIR FLOW

         #BHP (STATIC VALUE)

         #0143 ABSOLUTE ENGINE LOAD

         #0105 ENGINE COOLANT TEMP USE THIS TO DETECT PEDAL DANCE @ 174F this is in C

         #015C ENGINE OIL TEMP

         #0168 INTAKE AIR TEMP


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)
        title = tk.Label(frame, text='test3')
        title.grid(column=0, row=0)


class PageSettings(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)
        title = tk.Label(frame, text='test4')
        title.grid(column=0, row=0)


class MainView(tk.Frame):

    def __init__(self, *args, **kwargs):
        global buttonNavList
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

        
        ###PACK THE BUTTONS FOR THE NAV###
        b4.pack(side='right')
        b3.pack(side="right")
        b2.pack(side="right")
        b1.pack(side="right")

        
        
        
        ###OPEN PAGE ONE###
        p1.show()



root = tk.Tk()

main = MainView(root)
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("800x480")

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
