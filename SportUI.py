#THis is the ui class for the project here any ui mods can be made
import  io as io
#UI HOLDER CLASS


class UI():
    themeOne = None
    themeTwo = None
    themeThree = None
    activetheme= None
    def __init__(self, css1, css2, css3):

        print("UI THEMES:")
        print (css1)
        print (css2)
        print (css3)

        self.themeOne = css1
        self.themeTwo = css2
        self.themeThree = css3
        self.activeTheme= css1

    def changetheme(self, css):
        self.activeTheme = css


class settings():
    def __init__(self):
        ###just load from defult data and read files
        self.PedalDancePopUp = True
        self.ShowTurbo = False
        self.BHPValue = 171
        self.ZT60 = 6.3

        print("SETTINGS LOADING NOW")
        self.readsettingdata()

    def str_to_bool(self, s):
        ss = s
        if ss.__contains__('T'):
            return True
        elif ss.__contains__("F"):
            return False
        else:
            print ("PROBLEM WITH:" + str(s))
            raise ValueError  # evil ValueError that doesn't tell you what the wrong value was

    def removeLineEnding(self, strtouse):
        strtouse = strtouse[:2]
        print (strtouse)
        return strtouse


    def readsettingdata(self):
        try:
            print("read file....")
            file = open('settings.txt', 'r')
            data = file.readlines()
            line=data[1]
            self.PedalDancePopUp = self.str_to_bool(line[line.find('=')+1:])
            print("Pedal Dance Pop Up: " + str(self.PedalDancePopUp))
            line = data[2]
            self.ShowTurbo = self.str_to_bool(line[line.find('=')+1:])
            print("Show Turbo: " + str(self.PedalDancePopUp))
            line = data[3]
            self.BHPValue = int(line[line.find('=') + 1:])
            print("BHP: " + str(self.BHPValue))
            line = data[4]
            self.ZT60 = float(line[line.find('=') + 1:])
            print("BHP: " + str(self.ZT60))
            line = data[5]
            self.F = self.str_to_bool(line[line.find('=') + 1:])
            print("Temp in F: " + str(self.F))
            line= data[6]
            self.Miles = self.str_to_bool(line[line.find('=') + 1:])
            print("Dist in Miles: " + str(self.Miles))
            line = data[7]
            self.PSI = self.str_to_bool(line[line.find('=') + 1:])
            print("Boost in PSI: " + str(self.PSI))



        except:
            print("ERROR In settings.txt CHECK FILE FORMAT.")
        file.close()

    def getStringFromBool(self, booleanvalue):
        if(booleanvalue):
            return "T"
        return "F"
    def saveSettings(self):
        file = open('settings.txt', 'w')
        file.close()
        file = open('settings.txt', 'w')
        datatowrite = "THIS IS SETTING DATA NO SPACES AND CASE SENSITIVE [SAVED]\n"
        datatowrite +="PedalDancePopUp="+self.getStringFromBool(self.PedalDancePopUp)+'\n'
        datatowrite += "ShowTurbo=" + self.getStringFromBool(self.ShowTurbo) + '\n'
        datatowrite += "BHPValue=" + str(self.BHPValue) + '\n'
        datatowrite += "ZT60=" + str(self.ZT60) + '\n'
        file.write(datatowrite)
        file.close()


#css class
class css():
    color1 = ''
    color2 = ''
    color3 = ''
    color4 = ''
    font = ''
    fontsize = 0
    localdatablock = None
    def __init__(self, c1, c2, c3, c4, font, fontsize):
        self.color1 = c1
        self.color2 = c2
        self.color3 = c3
        self.color4 = c4
        self.unlitColor ='#232323'
        self.alertcolor = 'yellow'
        self.font = font
        self.fontsize = fontsize
        self.padx = 5
        self.pady = 10
    def __str__(self):
        return "COLORS: " +self.color1 + ' '+self.color2 + ' '+self.color3 + ' '+self.color4 + ' FONT:' + self.font +" FONT-SIZE: " + str(self.fontsize)




###EXAMPLE TEST FOR UI CLASS###
testui = False
if(testui):
    t1 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "16")
    t2 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "17")
    t3 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "18")



    ui = UI(t1,t2,t3)


