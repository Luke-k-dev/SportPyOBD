#THis is the ui class for the project here any ui mods can be made
import  io as io
#UI HOLDER CLASS


class UI():
    themeOne = None
    themeTwo = None
    themeThree = None
    activetheme= None
    def __init__(self, css1, css2, css3):


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
            print("Pedal Dance Pop Up: "+ str(self.PedalDancePopUp))
            line = data[2]
            self.ShowTurbo = self.str_to_bool(line[line.find('=')+1:])
            print("Show Turbo: " + str(self.PedalDancePopUp))

        except:
            print("ERROR In settings.txt CHECK FILE FORMAT.")


    def writesettingdata(self, var, varkey):
        file = open('settings.txt', 'w')

        pass

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
        self.font = font
        self.fontsize = fontsize
    def __str__(self):
        return "COLORS: " +self.color1 + ' '+self.color2 + ' '+self.color3 + ' '+self.color4 + ' FONT:' + self.font +" FONT-SIZE: " + str(self.fontsize)




###EXAMPLE TEST FOR UI CLASS###
testui = False
if(testui):
    t1 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "16")
    t2 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "17")
    t3 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "18")
    tab1 = ['010C', '010F', '0167', '010B', '0004']
    tab2 = ['0100', '0100', '0100', '0100', '0100']
    tab3 = ['0100', '0100', '0100', '0100', '0100']


    ui = UI(t1,t2,t3, d)


