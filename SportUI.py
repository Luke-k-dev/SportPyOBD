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


