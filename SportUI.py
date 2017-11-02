#THis is the ui class for the project here any ui mods can be made

#UI HOLDER CLASS
class UI():
    themeOne = None
    themeTwo = None
    themeThree = None
    db = None
    def __init__(self, css1, css2, css3, datab):


        print (css1)
        print (css2)
        print (css3)
        db = datab



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

class datablock():
    #data per page 5 so only 5 pieces of info will be displayed
    # setup commands for every page
    #simply add the PID code for every piece of data you want
    #PID table can be found here https://en.wikipedia.org/wiki/OBD-II_PIDs#Mode_01
    tabOne = ['010C', '010F', '0167', '010B', '04']

    tabTwo = ['0100', '0100', '0100', '0100', '0100']

    tabThree = ['0100', '0100', '0100', '0100', '0100']
    def __init__(self, tabone, tabtwo, tabthree):
        print('data block ready.')
        self.tabOne = tabone
        self.tabTwo = tabtwo
        self.tabThree = tabthree

    #defult display
    #rpm, intake air temperature, coolenttemp, intake pressure, engine load

    #END OF LAYOUTS



###EXAMPLE TEST FOR UI CLASS###
testui = False
if(testui):
    t1 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "16")
    t2 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "17")
    t3 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", "18")
    tab1 = ['010C', '010F', '0167', '010B', '0004']
    tab2 = ['0100', '0100', '0100', '0100', '0100']
    tab3 = ['0100', '0100', '0100', '0100', '0100']
    d = datablock(tab1,tab2,tab3)

    ui = UI(t1,t2,t3, d)


