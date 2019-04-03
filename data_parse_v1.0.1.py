import json
import csv
import glob
import pickle
import gzip
import time
import dateutil.parser as dtp

bemNo = input("Search BEM number: ")

def search_bem():
    serialSearch = "C:\\Users\\mahbub\\PycharmProjects\\BEM\\Database_output-serial_numbers.csv"

    with open(serialSearch, "r", encoding="utf8") as database:
        csv_db = csv.reader(database, delimiter=",", quotechar='"', lineterminator="\r\n")
        next(csv_db)
        for row in csv_db:
            row = [string.strip() for string in row]
            if bemNo == row[0]:
                bemUID = row[2]
                print(bemUID)
                return bemUID

path = "C:\\Users\\mahbub\\PycharmProjects\\BEM\\bemLogs\\*.csv"

# csvFileArray = []

date = []
direction = []
x = []

for file in glob.glob(path):
    with open(file, "r", encoding="utf8") as bemLog:
        csv_log = csv.reader(bemLog, delimiter=",", quotechar='"', lineterminator="\r\n")
        for row in csv_log:
            if row[1] == "bucketStart":
                next(csv_log)
                if row[0] == search_bem():
                    var = json.loads(row[5])

                    date.append(dtp.parse(var["eventCaptureTime"]))
                    direction.append(var["direction"])

                    if direction == "rising":
                        x = 1
                    elif direction == "falling":
                        x = -1
                    else:
                        x = 0

            else:
                print("No event log found for BEM " + bemNo)
                break



