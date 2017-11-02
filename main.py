from  SportUI import *
from  newobd import  *
from  tkinter import *
import  ttk

###SET UP OBD CONNECTION###
com = None
if osx:
    #ports may be different depending on drivers and device
    com = OBDcom('/dev/tty.usbserial-113010881974', 115200, '1')
else:

    com =OBDcom('/dev/ttyUSB0', 115200, None)

###NOW LOAD IN UI DATA###
#THEMES ARE HERE COLOR COLOR COLOR COLOR FONT SIZE
#theme 1
t1 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", 16)
#theme 2
t2 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", 16)
#theme 3
t3 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", 16)
#data block
#TAB LAYOUTS HERE THESE ARE PID CODES
tab1 = ['010C', '010F', '0167', '010B', '0004']
tab2 = ['0100', '0100', '0100', '0100', '0100']
tab3 = ['0100', '0100', '0100', '0100', '0100']
grid= datablock(tab1, tab2, tab3)
ui = UI(t1, t2, t3, grid)

###UI CLASS HERE
class Application(Frame):
    def updatecar(self):
        global hascar
        global loopct
        global speed
        global rpm
        global oiltemp
        global intakepressue
        speed = -1
        rpm = 400
        oiltemp = -1


        self.RPMbar['value'] = rpm
        self.RPMout['text'] = str(rpm)
        # self.speedo['text'] = "Speed:"+str(speed)+"\nRPM: "+str(rpm)+"\nOIL: "+str(oiltemp)+ '\nDATA UPDATE NUMBER: '+str(loopct)
        root.after(500, self.updatecar)

    def createStatWidgets(self):
        self.toptxt = Label(self, justify='left')
        self.toptxt['text'] = 'Scion FR-S'
        # padding and colspan is here
        self.toptxt.grid(column=0, row=0, columnspan=3, pady=(0, 30), sticky=W)
        #self.toptxt['bg'] = ColorPallet.bck2
        #self.toptxt['fg'] = ColorPallet.h2

        # rpm
        self.RPM = Label(self, justify='left')
        self.RPM['text'] = 'RPM: '
        self.RPM.grid(column=0, row=1, sticky=NE)
        #self.RPM['bg'] = ColorPallet.bck
        #self.RPM['fg'] = ColorPallet.h1
        # bar
        self.RPMbar = ttk.Progressbar(self, style="RPM.Horizontal.TProgressbar", orient="horizontal", length=500,
                                      mode="determinate")
        self.RPMbar.grid(column=1, row=1)
        self.RPMbar["maximum"] = 9000
        self.RPMbar['value'] = 100

        # readout
        self.RPMout = Label(self, justify='left')
        self.RPMout['text'] = '700'
        self.RPMout.grid(column=2, row=1, sticky=NW)
        #self.RPMout['bg'] = ColorPallet.bck
        #self.RPMout['fg'] = ColorPallet.h1

        # OIL temp
        self.oiltemp = Label(self)
        self.oiltemp['text'] = 'OIL TEMP: '
        self.oiltemp.grid(column=0, row=2, sticky=NE)
        #self.oiltemp['bg'] = ColorPallet.bck
        #self.oiltemp['fg'] = ColorPallet.h1
        # readout
        self.oiltempout = Label(self, justify='left')
        self.oiltempout['text'] = '00'
        self.oiltempout.grid(column=2, row=2, sticky=NW)
        #self.oiltempout['bg'] = ColorPallet.bck
        #self.oiltempout['fg'] = ColorPallet.h1

        # intake pressure
        self.inpressure = Label(self)
        self.inpressure['text'] = 'INTK PRESSURE: '
        self.inpressure.grid(column=0, row=3, sticky=NE)
        #self.inpressure['bg'] = ColorPallet.bck
        #self.inpressure['fg'] = ColorPallet.h1
        # readout
        self.inpressureout = Label(self, justify='left')
        self.inpressureout['text'] = '00.0'
        self.inpressureout.grid(column=2, row=3, sticky=NW)
        #self.inpressureout['bg'] = ColorPallet.bck
        #self.inpressureout['fg'] = ColorPallet.h1

        # SPACER FOR BTM
        # self.spacer = Label(self, font = CSS.font1,justify=CSS.datajustify )
        # self.spacer['text'] = '                                                                          '
        # self.spacer.grid(column =1, row=100,sticky=NW)
        # self.spacer['bg'] = ColorPallet.bck
        # self.spacer['fg'] = ColorPallet.h1

        # lets put this last
        self.QUIT = Button(self, highlightthickness=0, bd=0)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        #self.QUIT['bg'] = ColorPallet.bck
        self.QUIT["command"] = self.closeout

        self.QUIT.grid(column=0, row=21)

    def closeout(self):
        try:
            root2.destroy()
        except:
            print("SIM IS GONE")

        root.destroy()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createStatWidgets()
        self.updatecar()


root = Tk()
# switch theme
style = ttk.Style()
style.theme_use('default')

#style.configure("RPM.Horizontal.TProgressbar", thickness=48, background=ui.themeOne.color2, fieldbackground='black')

root.attributes("-fullscreen", True)
#root.configure(background=ui.themeOne.color4)
root2 = Tk()  # remove anyhting here with a 2 to disable the sim
app = Application(master=root)

app.configure() #background=ui.themeOne.color4 as param
app.mainloop()







