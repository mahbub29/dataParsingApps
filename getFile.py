import csv

def serialSearch(num):

    serial = 'C:\\Users\\mahbub\\PycharmProjects\\BEM\\Database_output-serial_numbers.csv'
    bemNo_in = num

    with open(serial, 'r', encoding='utf8') as log:
        bemSerialcsv = csv.reader(log, delimiter=',', quotechar='"', lineterminator='\r\n')
        next(bemSerialcsv)
        for rowSerial in bemSerialcsv:
            rowSerial = [string.strip() for string in rowSerial]
            if (bemNo_in.upper() or bemNo_in.lower()) == rowSerial[0]:
                print("BEMUID " + rowSerial[2])
                return rowSerial[2]
            else:
                pass

