import json
import csv
import pickle
import gzip
import time

num = str(401)

bemDataFile = "C:\\Users\\mahbub\\PycharmProjects\\BEM\\8-401\\8.401.csv"


def save_Gzipped_pickle(obj, filename, protocol=-1):
    with gzip.open(filename, 'w') as f:
        pickle.dump(obj, f, protocol)


def load_Gzipped_pickle(file_name):
    with gzip.open(file_name, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object

def pickle_time():
    global picklePath

    import dateutil.parser as dtp
    import os

    count = 0

    date = []
    decode = []
    voltage = []
    temperature = []
    amp_seconds = []
    enIn = []
    enOut = []

    ###############################

    picklePath = bemDataFile

    global bem_rec_dir
    bem_rec_dir = ("C:\\Users\\mahbub\\PycharmProjects\\401_sample_data\\BEM_" + num)

    if not os.path.exists(bem_rec_dir):
        print("There is no BEM record directory for BEM " + num + ". Please wait whilst a directory is made...")

        os.makedirs(bem_rec_dir)

        print("Converting JSON strings files to FILE files...")

    for row in picklePath:

        if (count % 10000) == 0:
            print(str(count) + " entries loaded")

        # if count == 1000:
        #     break

        var = json.loads(row)
        date.append(dtp.parse(var['date']))
        decode.append(dtp.parse(var['dateDecoded']))
        voltage.append(int(var['bemVoltageAve']))
        temperature.append(int(var['temperature']))
        amp_seconds.append(int(var['bemAmpSeconds']))
        enIn.append(int(var['bemEnergyIn']))
        enOut.append(int(var['bemEnergyOut']))

    if not os.path.exists(bem_rec_dir + "\\date.file"):
        print("No date.file detected for BEM_" + num + ".")
        save_Gzipped_pickle(date, (bem_rec_dir + "\\date.file"))
        print("date.file --- save complete.")
    else:
        pass

    if not os.path.exists(bem_rec_dir + "\\decode.file"):
        print("No decode.file detected for BEM_" + num + ".")
        save_Gzipped_pickle(decode, (bem_rec_dir + "\\decode.file"))
        print("decode.file --- save complete.")
    else:
        pass

    if not os.path.exists(bem_rec_dir + "\\voltage.file"):
        print("No voltage.file detected for BEM_" + num + ".")
        save_Gzipped_pickle(voltage, (bem_rec_dir + "\\voltage.file"))
        print("voltage.file --- save complete.")
    else:
        pass

    if not os.path.exists(bem_rec_dir + "\\temperature.file"):
        print("No temperature.file detected for BEM_" + num + ".")
        save_Gzipped_pickle(temperature, (bem_rec_dir + "\\temperature.file"))
        print("temperature.file --- save complete.")
    else:
        pass

    if not os.path.exists(bem_rec_dir + "\\amp_seconds.file"):
        print("No amp_seconds.file detected for BEM_" + num + ".")
        save_Gzipped_pickle(amp_seconds, (bem_rec_dir + "\\amp_seconds.file"))
        print("amp_seconds.file --- save complete.")
    else:
        pass

    if not os.path.exists(bem_rec_dir + "\\enIn.file"):
        print("No enIn.file detected for BEM_" + num + ".")
        save_Gzipped_pickle(enIn, (bem_rec_dir + "\\enIn.file"))
        print("enIn.file --- save complete.")
    else:
        pass

    if not os.path.exists(bem_rec_dir + "\\enOut.file"):
        print("No enOut.file detected for BEM_" + num + ".")
        save_Gzipped_pickle(enOut, (bem_rec_dir + "\\enOut.file"))
        print("enOut.file --- save complete.")
    else:
        pass

    ##########################################################################

def bem_in_out():
    import matplotlib.pyplot as plt

    print("Unzipping BEM Record files...")

    date = (load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
    print("date.file --- unzip complete.")

    enIn = (load_Gzipped_pickle(bem_rec_dir + "\\enIn.file"))
    print("enIn.file --- unzip complete.")

    enOut = (load_Gzipped_pickle(bem_rec_dir + "\\enOut.file"))
    print("enOut.file --- unzip complete.")

    fig = plt.figure(1)
    plt.plot(date, enIn, date, enOut)
    ax = fig.add_subplot(111)
    ax.set_title("ENERGY IN/OUT")
    ax.set_xlabel("DATE")
    ax.set_ylabel("ENERGY IN/OUT")
    plt.grid(True)
    print("Writing graph...")
    time.sleep(2)
    plt.show()


with open(bemDataFile) as csvFile:
    filereader = csv.reader(csvFile, delimiter=',', quotechar='"', lineterminator='\r\n')
    for row in filereader:
        print("running pickle_time...")

        pickle_time()

bem_in_out()
