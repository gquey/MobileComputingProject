import tkinter as tk
from initialization import Initialization
from startpage import StartPage
from IOTThings import IOTThings
from Recipes import Recipe

LARGE_FONT= ("Times New Roman", 14)

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        print("1")
        tk.Tk.__init__(self, *args, **kwargs)
        f=open('thing.csv','w')
        f.close()
        f=open('service.csv','w')
        f.close()
        f=open('finalize_app.txt','w')
        f.close()
        self.geometry('%dx%d' % (800, 500))
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #start with StartPage
        #self.show_frame(StartPage)
        self.show_frame(Initialization)

    #show new frame
    def show_frame(self, cont):
        for F in (Initialization, StartPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()

app = Main()
app.mainloop()