from  SportUI import *
from  newobd import *
import tkinter as tk
import ttk

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
t1 = css("#FFF", "#FFF", "#FFF", "#3a3a3a", "Helvetica", 16)
# theme 2
t2 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", 16)
# theme 3
t3 = css("#FFF", "#FFF", "#FFF", "#FFF", "Helvetica", 16)
# data block
# TAB LAYOUTS HERE THESE ARE PID CODES

ui = UI(t1, t2, t3)


###UI CLASS HERE

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)
        #create the display here

        #throttle pos 0111
        throtletitle = tk.Label(frame, text='Throtle Pos: ')
        throtletitle.grid(column =0, row=0, sticky= tk.NE)
        throtlebar = ttk.Progressbar(frame, orient="horizontal", length=500, mode="determinate")
        throtlebar['maximum'] = 100
        throtlebar['value'] = 0
        throtlebar.grid(column = 1, row=0, sticky= tk.NE)


        #torque





class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tk.Frame(self)
        frame.pack(side="top", fill="both", expand=True)
        title = tk.Label(frame, text='test1')
        title.grid(column=0, row=0, sticky= tk.NE)


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
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = PageSettings(self)

        buttonframe = tk.Frame(self)

        container = tk.Frame(self)

        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        cartitle = tk.Label(buttonframe, text='FRS')
        cartitle.pack(side='left')


        b1 = tk.Button(buttonframe, text="Overview", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Race View", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Fuel View", command=p3.lift)
        b4 = tk.Button(buttonframe, text="Settings", command=p4.lift)

        p1.grid(column = 1, row=1, in_ = container)
        p2.grid(column=1, row=1, in_=container)
        p3.grid(column=1, row=1, in_=container)
        p4.grid(column=1, row=1, in_=container)


        cartitle.pack(side='left')
        b4.pack(side='right')
        b3.pack(side="right")
        b2.pack(side="right")
        b1.pack(side="right")


        p1.show()



root = tk.Tk()
style = ttk.Style()
style.theme_use('classic')
root.configure(background =ui.activeTheme.color4)
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
