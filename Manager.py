import collections
from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter import filedialog
from tkinter import messagebox
import os
import csv
from itertools import islice
import socket
import shutil
import time
import datetime
import pandas as pd
import threading

dev_mode = False
log = collections.defaultdict(list)

class ApplicationManager(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Manager in non-development mode")

        self.flag = True

        self.menu = Menu(self)
        self['menu']=self.menu
        self.menu.add_command(label = 'View different mode', command = self.alterMode)
        self.b_activate = ttk.Button(self, text="Activate Thing", command=self.activateThing)
        self.b_activate.pack(expand=1)
        self.b_status = ttk.Button(self, text="Check Status", command=self.checkStatus)
        self.b_status.pack(expand=1)

    def alterMode(self):
        global dev_mode
        if not dev_mode:
            dev_mode = True
            self.title("Manager in development mode")
        else:
            dev_mode = False
            self.title("Manager not in development mode")

    def activateThing(self):
        activation = Toplevel()
        activation.title("Activate Thing")
        activation.geometry('500x200')

        file = open('./Application.csv')
        lines = csv.reader(file)
        array = []
        for line in islice(lines, 1, None):
            array.append(line[0])
        activationList = Listbox(activation, width=50)
        for x in array:
            activationList.insert("end", x)
        activationList.pack()
        file.close()

        def RunApp():
            app_array = []
            i = activationList.get(activationList.curselection())
            app_file = open('./Application.csv')
            second_file = csv.reader(app_file)
            for y in islice(second_file, 1, None):
                if y[0] == i:
                    path = y[1]
                    break
            app_file.close()
            for z in open(path, 'r'):
                app_array += [z.split(',')[0]]
            stat = pd.read_csv('./ApplicationStatus.csv')
            stat.loc[stat['Name'] == i, 'ApplicationStatus'] = 'is running'
            stat.loc[stat['Name'] == i, 'Date'] = time.strftime('%Y-%m-%d')
            stat.loc[stat['Name'] == i, 'Time'] = time.strftime('%H:%M:%S')
            stat.to_csv('./ApplicationStatus.csv', index=False)
            self.manual = 0
            for s in app_array:
                if not self.flag:
                    stat2 = pd.read_csv('./ApplicationStatus.csv')
                    stat2.loc[stat2['Name'] == i, 'ApplicationStatus'] = 'not active'
                    stat2.loc[stat2['Name'] == i, 'Done'] = time.strftime('%H:%M:%S')
                    stat2.to_csv('./ApplicationStatus.csv', index=False)
                    self.flag = True
                    self.manual = 1
                    break
                else:
                    self.send_tweet(s)
                    log[i].append(str(s) + " is running")
                    time.sleep(20)
                    self.manual = 2
            log[i].append(str(i) + " stopped running")
            if self.manual == 2:
                stat3 = pd.read_csv('./ApplicationStatus.csv')
                stat3.loc[stat3['Name'] == i, 'ApplicationStatus'] = 'complete'
                stat3.loc[stat3['Name'] == i, 'Done'] = time.strftime('%H:%M:%S')
                stat3.to_csv('./ApplicationStatus.csv', index=False)

        Button(activation, text="Start app", command=lambda: threading.Thread(target=RunApp()).start()).pack()

    def checkStatus(self):
        status = Toplevel()
        status.title("check status")
        status.geometry('300x100')

        def undergo():
            file = open('./ApplicationStatus.csv')
            file2 = csv.reader(file)
            count = 1

            def logging(k, j):
                if k == "is running":
                    def output(c=None):
                        if c is not None:
                            if c <= 1000:
                                outputText = str(log[j][-1]) + "\n"
                                secondText.insert('end', outputText)
                                c += 1
                                toplevel.after(5432, lambda: output(count))
                        else:
                            output(1)

                    toplevel = Toplevel(status)
                    secondText = scrolledtext.ScrolledText(toplevel, width=40, height=25)
                    secondText.grid(column=0, row=1, sticky='nsew')
                    secondText.config(background='light grey', foreground='black', font='arial 20 bold', wrap='word',
                                 relief='sunken', bd=5)
                    toplevel.after(1, lambda: output())
                    toplevel.focus_set()
                    toplevel.grab_set()
                else:
                    pass

            for i in islice(file2, 1, None):
                if i[1] == 'is running':
                    Button(status, text=i[0], command=lambda: logging(i[1], i[0])).place(x=30, y=count * 50)
                    Label(status, text='status: ' + i[1]).place(x=120, y=count * 50)
                    Label(status, text='start time: ' + i[2] + ' ' + i[3]).place(x=220, y=count * 50)
                    count = count + 1
                elif i[4] != '':
                    now = time.strftime('%H:%M:%S')
                    curr = datetime.datetime.strptime(now, '%H:%M:%S')
                    arrest = datetime.datetime.strptime(i[4], '%H:%M:%S')
                    gap = curr - arrest
                    if gap.seconds < 0 or gap.seconds >= 300:
                        Button(status, text=i[0], command=lambda: logging(i[1], i[0])).place(x=30, y=count * 50)
                        Label(status, text='status: deleted').place(x=120, y=count * 50)
                    else:
                        Button(status, text=i[0], command=lambda: logging(i[1], i[0])).place(x=30, y=count * 50)
                        Label(status, text='status: ' + i[1]).place(x=120, y=count * 50)
                        Label(status, text='start time: ' + i[2] + ' ' + i[3]).place(x=220, y=count * 50)
                        count = count + 1
            file.close()

            def arrestMethod():
                stop = Toplevel()
                stop.title("Stop")
                stop.geometry('300x200')

                file = open('./ApplicationStatus.csv')
                lines = csv.reader(file)
                array = []
                for line in islice(lines, 1, None):
                    if line[1] == 'is running':
                        array.append(line[0])
                outputList = Listbox(stop, width=50)
                for x in array:
                    outputList.insert("end", x)
                outputList.pack()
                file.close()

                def greenLight():
                    j = outputList.get(outputList.curselection())
                    self.flag = False
                    stat = pd.read_csv('./ApplicationStatus.csv')
                    stat.loc[stat['Name'] == j, 'ApplicationStatus'] = 'inactive'
                    stat.loc[stat['Name'] == j, 'Stop'] = time.strftime('%H:%M:%S')
                    stat.to_csv('./ApplicationStatus.csv', index=False)

                    Button(stop, text="okay", command=lambda: greenLight()).pack()

                Button(status, text="Stop process", command=lambda: arrestMethod()).place(x=285, y=10)
                status.after(20000, undergo)
            undergo()

    def sendOutput(self, subID):
        with open("ApplicationService.csv", 'r') as file:
            interpret = csv.reader(file)
            lines = [row for row in interpret]

        for line in lines:
            if line[0] == subID:
                output = "{ \"Message Type\" : \"Service \",\"Thing_ID\" : \"" + line[
                    1] + "\",\"Space_ID\" : \"FinalProject\",\"Name of service\" : \"" + line[
                            0] + "\",\"Input\" : \"()\" }"
                prod_id = line[1]
                break

        with open("ApplicationThing.csv", 'r') as file:
            interpret = csv.reader(file)
            lines = [row for row in interpret]

        for line in lines:
            if line[0] == prod_id:
                i = line[1]
                break

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((i, 6668))
        sock.send(output.encode())
        sock.close()

def goBack():
    root.destroy()
    os.system("python Application.py")

root = ApplicationManager()
root.geometry('300x300')
root.protocol("WM_DELETE_WINDOW", goBack)
root.mainloop()