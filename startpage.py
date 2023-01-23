import tkinter as tk
import os
from tkinter import font


HEADING_FONT= ("Times New Roman", 30)
NORMAL_FONT = ("Times New Roman", 20)
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        print("StartPage")
        from IOTThings import IOTThings
        from Recipes import Recipe
        tk.Frame.__init__(self, parent)
        headingText = tk.Label(self, text="Start Page", font=HEADING_FONT)
        headingText.place(x = 315, y = 10)

        ThingsButton = tk.Button(self, text="Things",
                            command=lambda: controller.show_frame(IOTThings))
        ThingsButton.pack()
        ThingsButton.place(x=170, y=75, height=90,width=180)
        ThingsButton['font'] = NORMAL_FONT
        
        servicesButton = tk.Button(self, text="Services",
                            command=lambda:os.system("python services.py"))
        servicesButton.pack()
        servicesButton.place(x=430,y=75,height=90,width=180)
        servicesButton['font'] = NORMAL_FONT
        
        relationshipButton = tk.Button(self, text="Relationship",
                            command=lambda:os.system("python Relationship.py"))
        relationshipButton.pack()
        relationshipButton.place(x=170, y=205, height = 90, width=180)
        relationshipButton['font'] = NORMAL_FONT

        recipeButton = tk.Button(self, text="Recipe",
                            command=lambda: controller.show_frame(Recipe))
        recipeButton.pack()
        recipeButton.place(x=430, y=205, height=90, width=180)
        recipeButton['font'] = NORMAL_FONT

        appsButton = tk.Button(self, text="Apps",
                             command=lambda:os.system("python Application.py"))
        appsButton.pack()
        appsButton.place(x=300, y = 335, height = 90, width=180)
        appsButton['font'] = NORMAL_FONT

        quitButton = tk.Button(self, text="Quit",
                            command=self.quit)
        quitButton.pack()
        quitButton.place(x=170, y=460, height=40, width = 440)
        quitButton['font'] = NORMAL_FONT
