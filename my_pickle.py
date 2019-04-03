import csv
import json
import pickle
import gzip
import dateutil.parser as dtp
import os.path

date = []
decode = []
d_date = []
seqNum = []
voltage = []
temperature = []
amp_seconds = []
enIn = []
enOut = []
restart = []
dateReceived = []
dateReal = []
xR = []

# tPath = file

def get_file(tPath_l,rw):
    with open(tPath_l, "r") as csvFile:
        datareader = csv.reader(csvFile)
        global count
        count = 0
        for row in datareader:
             yield row[rw]
             count += 1
        csvFile.close()

def get_data(tPath_l,rw):
    for row in get_file(tPath_l,rw):
        yield row

def pickle_voltage(var):
    if (os.path.exists('C:\\Users\\mahbub\\PycharmProjects\\graphGUI\\pickled\\voltage.file') == False):
        for row in get_data(tPath,2):
            if (count % 1000) == 0:
                print(count)


