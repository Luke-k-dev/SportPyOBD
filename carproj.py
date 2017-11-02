





#PLEASE DONT EVER RUN THIS. IT IS LEGACY CODE I REWROTE





from obd import *
from OBDSIM import *
#global vars here
#---------------------
obd.logger.setLevel(obd.logging.DEBUG) 
loopct = 0
speed =0
rpm =0
oiltemp = 0
intakepressue =0
hascar = True

connect = obd.OBD("/dev/ttyUSB0")
connect.baudrate = 115200
print(elm327.ECU)

spdcmd = obd.commands.SPEED

spdresponse = connect.query(spdcmd)

if spdresponse.value == None:
    print('error no connection found however the speed could be anything')
    hascar = False

if spdresponse.value != None:
    print(spdresponse.value)
    hascar = True

#UI STARTS HERE
from Tkinter import *
import ttk

#theme is at end after root is created
#create a pallete class to store colors
class ColorPallet():
    bck="#232323"
    h1 ="#97e81e"
    h2 ="#232323"
    bck2 ="#e0e0e0"
    h3 =""
    p =""

class CSS():
    font1 = ("Sans", 45)
    fonttop = ("Sans", 60)
    datajustify = "left"
    
    
    
class Application(Frame):
    
    def updatecar(self):
        global hascar
        global loopct
        global speed
        global rpm
        global oiltemp
        global intakepressue
        speed =-1
        rpm = 400
        oiltemp = -1
        if hascar:
            #run obd get commands here
            speed = connect.query(spdcmd)
            rpm = connect.query(obd.commands.RPM)
            oiltmep = connect.query(obd.commands.OIL_TEMP)

        if hascar!= True:
            connect = obd.OBD()
            #setthem to random values
            speed = sim.getdataframe('SPEED')
            rpm = sim.getdataframe("RPM")
            oiltemp = sim.getdataframe("OIL_TEMP")

        self.RPMbar['value'] = rpm
        self.RPMout['text'] = str(rpm)
        #self.speedo['text'] = "Speed:"+str(speed)+"\nRPM: "+str(rpm)+"\nOIL: "+str(oiltemp)+ '\nDATA UPDATE NUMBER: '+str(loopct)
        root.after(500, self.updatecar)

    def createStatWidgets(self):
        self.toptxt =Label(self, font = CSS.fonttop, justify='left')
        self.toptxt['text']='Scion FR-S'
        #padding and colspan is here
        self.toptxt.grid(column=0, row=0, columnspan =3, pady=(0,30), sticky=W)
        self.toptxt['bg'] = ColorPallet.bck2
        self.toptxt['fg'] = ColorPallet.h2

        #rpm
        self.RPM = Label(self, font = CSS.font1, justify='left')
        self.RPM['text'] = 'RPM: '
        self.RPM.grid(column =0, row=1,sticky=NE )
        self.RPM['bg'] = ColorPallet.bck
        self.RPM['fg'] = ColorPallet.h1
        #bar
        self.RPMbar = ttk.Progressbar(self, style="RPM.Horizontal.TProgressbar",orient="horizontal", length=500, mode="determinate")
        self.RPMbar.grid(column =1, row=1)
        self.RPMbar["maximum"] = 9000
        self.RPMbar['value'] = 100
        
        #readout
        self.RPMout = Label(self, font = CSS.font1, justify='left')
        self.RPMout['text'] = '700'
        self.RPMout.grid(column =2, row=1,sticky=NW )
        self.RPMout['bg'] = ColorPallet.bck
        self.RPMout['fg'] = ColorPallet.h1
        

        #OIL temp
        self.oiltemp = Label(self, font = CSS.font1, justify=CSS.datajustify)
        self.oiltemp['text'] = 'OIL TEMP: '
        self.oiltemp.grid(column =0, row=2,sticky=NE)
        self.oiltemp['bg'] = ColorPallet.bck
        self.oiltemp['fg'] = ColorPallet.h1
        #readout
        self.oiltempout = Label(self, font = CSS.font1, justify='left')
        self.oiltempout['text'] = '00'
        self.oiltempout.grid(column =2, row=2,sticky=NW)
        self.oiltempout['bg'] = ColorPallet.bck
        self.oiltempout['fg'] = ColorPallet.h1
        
        
        #intake pressure
        self.inpressure = Label(self, font = CSS.font1,justify=CSS.datajustify )
        self.inpressure['text'] = 'INTK PRESSURE: '
        self.inpressure.grid(column =0, row=3,sticky=NE)
        self.inpressure['bg'] = ColorPallet.bck
        self.inpressure['fg'] = ColorPallet.h1
        #readout
        self.inpressureout = Label(self, font = CSS.font1, justify='left')
        self.inpressureout['text'] = '00.0'
        self.inpressureout.grid(column =2, row=3,sticky=NW)
        self.inpressureout['bg'] = ColorPallet.bck
        self.inpressureout['fg'] = ColorPallet.h1



        #SPACER FOR BTM
        #self.spacer = Label(self, font = CSS.font1,justify=CSS.datajustify )
        #self.spacer['text'] = '                                                                          '
        #self.spacer.grid(column =1, row=100,sticky=NW)
        #self.spacer['bg'] = ColorPallet.bck
        #self.spacer['fg'] = ColorPallet.h1
        
        #lets put this last
        self.QUIT = Button(self, highlightthickness = 0, bd = 0)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT['bg']=ColorPallet.bck
        self.QUIT["command"] =  self.closeout

        self.QUIT.grid(column =0, row=21)

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

    
        


class SIMCTRL(Frame):

    def gas(self):
            sim.pressgass(5)

    def mgas(self):
            sim.pressgass(-5)
            
    def createWidgets(self):
        self.DATAOUT = Label(self)
        self.DATAOUT['text'] = 'SIM DATA HERE'
        self.DATAOUT.pack({'side':'top'})
        self.SPD = Label(self)
        self.SPD['text'] = 'SPEED: 0'
        self.SPD.pack({'side':'top'})

        self.OIL = Label(self)
        self.OIL['text'] = 'OIL_TEMP: 0'
        self.OIL.pack({'side':'top'})

        self.RPM = Label(self)
        self.RPM['text'] = 'RPM: 0'
        self.RPM.pack({'side':'top'})

        

        self.GAS = Button(self)
        self.GAS['text'] = "[GAS]"
        self.GAS['fg'] = 'yellow'
        self.GAS['command'] = self.gas
        self.GAS.pack({"side":'left'})

        self.MGAS = Button(self)
        self.MGAS['text'] = "[REMOVE GAS]"
        self.MGAS['fg'] = 'yellow'
        self.MGAS['command'] = self.mgas
        self.MGAS.pack({"side":'left'})

        

        
        #lets put this last
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] = root2.destroy

        self.QUIT.pack({"side": "bottom"})
    

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.gas()
        self.createWidgets()
        






sim = OBDIIsim()


root = Tk()
#switch theme
style = ttk.Style()
style.theme_use('default')

style.configure("RPM.Horizontal.TProgressbar",thickness=48, background=ColorPallet.h1, fieldbackground='black')

root.attributes("-fullscreen", True)
root.configure(background=ColorPallet.bck)
root2=Tk() #remove anyhting here with a 2 to disable the sim
app = Application(master=root)
app2 = SIMCTRL(master=root2)
app.configure(background=ColorPallet.bck)
app.mainloop()
#we do not need this b/c quit button
try:
    root.destroy()
except:
    print("root has already been destroyed.")
