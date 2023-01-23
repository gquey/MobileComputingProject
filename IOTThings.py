from tkinter import *
import tkinter.ttk as ttk
import csv

LARGE_FONT = ("Times New Roman", 12)

class IOTThings(Frame):
    def __init__(self, parent, controller):
        from startpage import StartPage
        Frame.__init__(self, parent)

        #set title of columns
        self.dataCols = ('Thing Name','Thing IP')
        self.tree = ttk.Treeview(self, columns=self.dataCols, height = 5)
        self.tree.grid(row=0, column=0, sticky=NSEW)

        # Setup column heading
        self.tree.heading('#0', text='Thing Name')
        self.tree.heading('#1', text='Thing IP')
        
        style = ttk.Style(self)
        style.configure('Treeview', rowheight=80)
    
    
        with open('thing.csv','r') as csvfile:
            csv_reader = csv.csv_reader(csvfile)
            thing_rows= [row for row in csv_reader]
        for thing_item in range(len(thing_rows)):
            self.tree.insert('', 'end', value=(thing_rows[thing_item][0], thing_rows[thing_item][1]))


        #add back button
        button1 = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.place(x=650, y=400)
