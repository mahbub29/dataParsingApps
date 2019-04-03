from tkinter import *
from getFile import serialSearch
import json
import csv


def show_entry_fields():
    print("Finding BEM UID for BEM %s..." % (e1.get()))
    global num
    num = (e1.get())
    bemUID = serialSearch(num)

    #print("BEM Number: %s" % (e1.get()))
    e1.delete(0,END)
    return bemUID

def bem_search(bemUID):
    try:
        path = 'C:\\Users\\mahbub\\PycharmProjects\\*\\*\\*\\*.csv'

        for file in glob.glob(path):
            with open(file, 'r') as log:
                csvreader = csv.reader(log, delimiter=',', quotechar='"', lineterminator='\r\n')
                if ("datagramReceived" in row[1]):
                    var = json.loads(row[2])
                    if (var["bemUID"] == bemUID):
                        return file

    except FileNotFoundError:
        print("No such file entries exist for BEM " + num)

def pickle():


def current_plot():
    current  = []
    date = []
    with open(bem_search(), 'r') as log:
        csvreader = csv.reader(log, delimiter=',', quotechar='2', lineterminator='\r\n')


def window1():
    master = Tk()

    Label(master, text="BEM Number:").grid(row=0)

    e1 = Entry(master)

    e1.grid(row=0, column=1)

    Button(master, text='Quit', command=master.quit)\
        .grid(row=2, column=0, sticky=EW, pady=4)
    Button(master, text='Get Records', command=show_entry_fields)\
        .grid(row=2, column=1, sticky=EW, pady=4)

    mainloop()
    return master

def window2(master):
    master.destroy()
    graphOptions = Tk()

    Button(graphOptions, text='BEM Restart plot', command=)\
        .grid(row=0, column=0, sticky=EW, pady=4)
    Button(graphOptions, text='BEM Current/Date', command=)\
        .grid(row=1, column=0, sticky=EW, pady=4)
    Button(graphOptions, text='BEM Voltage/Date', command=)\
        .grid(row=1, column=0, sticky=EW, pady=4)
    Button(graphOptions, text='BEM Decode Time/Date', command=)\
        .grid(row=1, column=0, sticky=EW, pady=4)
    Button(graphOptions, text='BEM Date Decoded/Date', command=)\
        .grid(row=1, column=0, sticky=EW, pady=4)

window1()