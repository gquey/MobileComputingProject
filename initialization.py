import tkinter as tk
from tkinter import ttk
import time
import tkinter.messagebox
import os
import queue
import struct
import socket
import threading
import select
from startpage import StartPage

thing = 0
ip_array = []
name = ''
flag = False
count = 1

class Initialization(tk.Frame):
    def __init__(self, parent, controller):
        global thing
        global ip_array

        tk.Frame.__init__(self, parent)
        self.queue = queue.Queue()
        ip_array = ''
        label = tk.Label(self, text="Enter the VSS Name: ")
        label.place(x=10, y=10)
        self.nameName=tk.Entry(self, relief=tk.RIDGE)
        self.nameName.place(x=130, y=10, width=300, height=20)

        label2 = tk.Label(self, text="Enter the total number of Things: ")
        label2.place(x=10, y=50)
        self.thingName = tk.Entry(self, relief=tk.RIDGE)
        self.thingName.place(x= 200, y=50, height = 20, width = 30)

        self.label3 = tk.Label(self, text="Please click on the start button when you have correctly inputted all the information!")
        self.label3.place(x=150, y=100)
        self.progress = ttk.Progressbar(self, orient='horizontal', length=450, mode='determinate')
        self.button = tk.Button(self, text="START", command = lambda : self.start(controller))
        self.button.place(x=380, y=200)
        self.progress.place(x=150, y=150)

    def start(self, controller):
        global thing
        global count
        global ip_array
        global name
        global flag
        good = True
        things = []
        name = self.nameName.get()
        thing = self.thingName.get()
        if good:
            count = int(thing)
            thing = int(thing)
            self.button.config(state="disabled")
            self.thd = User(self.queue)
            self.multiple()

            self.label3['text'] = "Collecting VSS data - this may take a minute"
            self.button['command'] = lambda : controller.show_frame(StartPage)

    def multiple(self):
        self.checkup()
        self.button.config(state = "active")
        if flag:
            self.label3['text'] = "Incorrect input"
            self.label3['text'] = "log out"
            self.button['command'] = lambda:Initialization.quit(self)

    def checkup(self):
        global count
        while self.queue.qsize():
            tweet = self.queue.get(0)
            self.progress['value'] += 100 / count

class User(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        global thing, ip_array, name, flag
        global num

        thing_array = {}
        ip_array = {}
        indicies = {}

        o = set()

        tweet = [''] * thing
        servicesArray = [[]]
        relationshipArray = [[]]
        count = 0
        for j in range(thing - 1):
            servicesArray += [[]]
            relationshipArray += [[]]

        print("tweet: ", tweet)
        print("servicesArray: ", servicesArray)
        print("relationshipArray", relationshipArray)

        multicast_group = '232.1.1.1'
        server_address = ('', 8080)

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(server_address)

        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:

            sock.setblocking(0)

            selectArray = select.select([sock], [], [], 40)
            if selectArray[0]:
                data, server = sock.recvfrom(4096)
            else:
                flag = 1
                tk.messagebox.showinfo('Error', 'Application timed out')
                break
            vss = "\"Space ID\" : \"" + name + "\""
            strng = data.decode("utf-8")
            if vss not in strng:
                continue
            datadict = data.decode("utf-8").replace("\"waitingTime_Seconds\"", "waitingTime_Seconds")
            datadict = datadict.replace("'", "_")
            datadict = datadict.replace("\"", "'")
            datadict = eval(datadict)

            thing = datadict['Thing ID']
            tweetType = datadict['Tweet Type']

            if thing not in thing_array and count == thing:
                continue

            if datadict not in tweet:
                if thing not in o and count < thing:
                    o.add(thing)
                    thing_array[thing] = count
                    ip_array[thing] = count
                    tweet[count] = datadict
                    print(o)
                    index = thing_array[thing]
                    print("new thing: ", thing, index)
                    print("first:" + str(tweet))
                    count += 1
                    print("count: ", count)
                else:
                    index = thing_array[thing]
                    print("existed thing, index", thing, index)

                print(thing, index, tweetType)

                if tweetType == 'Service':
                    servicesArray[index].append(datadict['Name'])
                    print("datadict['Name'] ", datadict['Name'])
                    print("servicesArray ", servicesArray)
                elif tweetType == 'Relationship':
                    rs = [datadict['Name'], datadict['Type'], datadict['FS name'], datadict['SS name']]
                    relationshipArray[index].append(rs)
                    print(relationshipArray)
                elif tweetType == "Identity_Language":
                    ip_array[thing] = datadict['IP']
                    indicies[thing] = index
            else:
                print("pop: " + str(thing_array))
                thing_array.pop(thing)
                print("pop: " + str(thing_array))
                self.queue.put(count)
                if not thing_array:
                    break

        sock.close()
        print("")
        print("Reception done!\n")
        print("o: ", o)
        print("ip_array: ", ip_array)
        print("indicies: ", indicies)
        print("servicesArray: ", servicesArray)
        print("relationshipArray", relationshipArray)

        o = list(o)
        file = open('thing.csv', 'w')
        for thing_array in ip_array:
            file.write(thing_array + ',' + ip_array[thing_array] + '\n')
        file.close()

        file = open('service.csv', 'w')
        for i in range(len(servicesArray)):
            for j in indicies:
                if indicies[j] == i:
                    thing = j
                    break
            for service_name in servicesArray[i]:
                file.write(service_name + ',' + thing + '\n')
        file.close()

        file = open('relationship.csv', 'w')
        file.write("Name,Type,Service1,Service2" + '\n')
        for thing in relationshipArray:
            if thing:
                for r in thing:
                    file.write(
                        r[0] + ',' + r[1] + ',' + r[2] + ',' + r[3] + '\n')
        file.close()


        






