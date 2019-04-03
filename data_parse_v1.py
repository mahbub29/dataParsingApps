import tkinter as tk
from getFile import serialSearch
import json
import csv
import glob
import pickle
import gzip
import time


b = tk.Button
e = tk.Entry
l = tk.Label

row = 0

class data_parsing_app(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("BEM Analysis Tool")
        self.grid()

        l(self.master, text="BEM Number : ").grid(row=0, column=0, sticky="W")

        self.entry_bem = e(self.master)
        self.entry_bem.grid(row=0, column=1, sticky="W")

        b(self.master, text="Quit", command=master.quit)\
            .grid(row=2, column=0, sticky="EW")

        submit = b(self.master, text="Get Records", command=self.show_entry_fields)\
            .grid(row=2, column=1, sticky="EW")



    def show_entry_fields(self):
        global num
        if len(self.entry_bem.get()) == 0:
            print("No BEM number entered. Please enter a BEM number.")
            l(self.master, text="No BEM number entered.")\
                .grid(row=3, column=0, columnspan=3, sticky="W")
            l(self.master, text="Please enter a BEM number.") \
                .grid(row=4, column=0, columnspan=3, sticky="W")
        else:
            num = self.entry_bem.get()
            print(num)
            print("Finding BEM UID for BEM %s..." % num)
            bemUID = serialSearch(num)
            # print("BEM Number: %s" % (e1.get()))
            self.entry_bem.delete(0, 'end')
            self.bem_search(bemUID)
        #return bemUID


    def bem_search(self, bemUID):

        global bemGraphFile

        bemGraphFile = 0

        path = 'C:\\Users\\mahbub\\PycharmProjects\\*\\*\\*\\*.csv'

        print("Please wait...")

        for file in glob.glob(path):
            csvFile = open(file, "r")
            csvFileArray = []
            csvRead = csv.reader(csvFile, delimiter=",", quotechar='"', lineterminator="\r\n")
            for row in csvRead:
                csvFileArray.append(row)
            if row[1] == "datagramReceived":
                jString = json.loads(row[2])
                if (jString["bemUID"].upper() or jString["bemUID"].lower()) == bemUID:
                    bemFound = str(jString["bemUID"])
                    # print("Found it! " + bemFound)
                    # print(file)
                    self.options_win()
                    bemGraphFile = file

        print("Raw BEM data attained.")
        print("...")
        time.sleep(3)

        self.pickle_time()

        print("PROCESS COMPLETE\n\n----------------\n\n")


    def options_win(self):

        window2 = tk.Toplevel(self)
        window2.title("BEM Analysis Options")

        l(window2, text="Select an option :")\
            .grid(row=0, column=0, columnspan=3, sticky="W")

        button1 = b(window2, text="Decode Time/Date", command=self.date_vs_decodetime)
        button1.grid(row=1, column=0, sticky="EW")
        button1.config(width=20, height=2)

        button2 = b(window2, text="Decode Time/Decode Date", command=self.decode_vs_decodetime)
        button2.grid(row=1, column=1, sticky="EW")
        button2.config(width=20, height=2)

        button3 = b(window2, text="Current/Date", command=self.current_vs_date)
        button3.grid(row=2, column=0, sticky="EW")
        button3.config(width=20, height=2)

        button4 = b(window2, text="Voltage/Date", command=self.voltage_vs_date)
        button4.grid(row=2, column=1, sticky="EW")
        button4.config(width=20, height=2)

        button5 = b(window2, text="Voltage/Current", command=self.voltage_vs_current)
        button5.grid(row=3, column=0, sticky="EW")
        button5.config(width=20, height=2)

        button6 = b(window2, text="Voltage/Charge", command=self.voltage_vs_charge)
        button6.grid(row=3, column=1, sticky="EW")
        button6.config(width=20, height=2)

        button7 = b(window2, text="Voltage/Energy", command=self.voltage_vs_energy)
        button7.grid(row=4, column=0, sticky="EW")
        button7.config(width=20, height=2)


    def get_file(self, picklePath, rw):
        with open(picklePath, "r") as csvFile:
            datareader = csv.reader(csvFile)
            global count
            count = 0
            for row in datareader:
                yield row[rw]
                count += 1
            csvFile.close()


    def get_data(self, picklePath, rw):
        for row in self.get_file(picklePath, rw):
            yield row


    def save_Gzipped_pickle(self, obj, filename, protocol=-1):
        with gzip.open(filename, 'w') as f:
            pickle.dump(obj, f, protocol)


    def load_Gzipped_pickle(self, file_name):
        with gzip.open(file_name, 'rb') as f:
            loaded_object = pickle.load(f)
            return loaded_object


    def pickle_time(self):
        global picklePath

        import dateutil.parser as dtp

        date = []
        decode = []
        seqNum = []
        voltage = []
        temperature = []
        amp_seconds = []
        enIn = []
        enOut = []

        #####  INDIVIDUAL CELLS  #####

        vc1 = []
        vc2 = []
        vc3 = []
        vc4 = []
        vc5 = []
        vc6 = []
        vc7 = []
        vc8 = []
        vc9 = []
        vc10 = []
        vc11 = []
        vc12 = []

        bcc1 = []
        bcc2 = []
        bcc3 = []
        bcc4 = []
        bcc5 = []
        bcc6 = []
        bcc7 = []
        bcc8 = []
        bcc9 = []
        bcc10 = []
        bcc11 = []
        bcc12 = []

        tc1 = []
        tc2 = []
        tc3 = []
        tc4 = []
        tc5 = []
        tc6 = []
        tc7 = []
        tc8 = []
        tc9 = []
        tc10 = []
        tc11 = []
        tc12 = []

        ###############################

        picklePath = bemGraphFile

        global bem_rec_dir
        bem_rec_dir = ("C:\\Users\\mahbub\\PycharmProjects\\BEM_records\\BEM_" + num)

        import os

        if not os.path.exists(bem_rec_dir):
            print("There is no BEM record directory for BEM " + num + ". Please wait whilst a directory is made...")

            os.makedirs(bem_rec_dir)

            print("Converting JSON strings files to FILE files...")

        for row in self.get_data(picklePath, 2):

            if (count % 10000) == 0:
                print(str(count) + " entries loaded")

            try:
                var = json.loads(row)
                date.append(dtp.parse(var['date']))
                decode.append(dtp.parse(var['dateDecoded']))
                seqNum.append(int(var['sequenceNumber']))
                voltage.append(int(var['bemVoltageAve']))
                temperature.append(int(var['temperature']))
                amp_seconds.append(int(var['bemAmpSeconds']))
                enIn.append(int(var['bemEnergyIn']))
                enOut.append(int(var['bemEnergyOut']))

                vc1.append(var['cells'][1]['cellVoltage'])
                vc2.append(var['cells'][1]['cellVoltage'])
                vc3.append(var['cells'][2]['cellVoltage'])
                vc4.append(var['cells'][3]['cellVoltage'])
                vc5.append(var['cells'][4]['cellVoltage'])
                vc6.append(var['cells'][5]['cellVoltage'])
                vc7.append(var['cells'][6]['cellVoltage'])
                vc8.append(var['cells'][7]['cellVoltage'])
                vc9.append(var['cells'][8]['cellVoltage'])
                vc10.append(var['cells'][9]['cellVoltage'])
                vc11.append(var['cells'][10]['cellVoltage'])
                vc12.append(var['cells'][11]['cellVoltage'])

                bcc1.append(var['cells'][0]['balanceCurrent'])
                bcc2.append(var['cells'][1]['balanceCurrent'])
                bcc3.append(var['cells'][2]['balanceCurrent'])
                bcc4.append(var['cells'][3]['balanceCurrent'])
                bcc5.append(var['cells'][4]['balanceCurrent'])
                bcc6.append(var['cells'][5]['balanceCurrent'])
                bcc7.append(var['cells'][6]['balanceCurrent'])
                bcc8.append(var['cells'][7]['balanceCurrent'])
                bcc9.append(var['cells'][8]['balanceCurrent'])
                bcc10.append(var['cells'][9]['balanceCurrent'])
                bcc11.append(var['cells'][10]['balanceCurrent'])
                bcc12.append(var['cells'][11]['balanceCurrent'])

                tc1.append(var['cells'][0]['temperature'])
                tc2.append(var['cells'][1]['temperature'])
                tc3.append(var['cells'][2]['temperature'])
                tc4.append(var['cells'][3]['temperature'])
                tc5.append(var['cells'][4]['temperature'])
                tc6.append(var['cells'][5]['temperature'])
                tc7.append(var['cells'][6]['temperature'])
                tc8.append(var['cells'][7]['temperature'])
                tc9.append(var['cells'][8]['temperature'])
                tc10.append(var['cells'][9]['temperature'])
                tc11.append(var['cells'][10]['temperature'])
                tc12.append(var['cells'][11]['temperature'])

            except IndexError:
                pass
        #
        # print("temperature " + str(len(temperature)))
        # print("enOut " + str(len(enOut)))
        # print("vc6 " + str(len(vc6)))
        # print("vc10 " + str(len(vc10)))
        # print("bcc4 " + str(len(bcc4)))
        # print("bcc8 " + str(len(bcc8)))
        # print("tc1 " + str(len(tc1)))
        # print("tc11 " + str(len(tc11)))

        if not os.path.exists(bem_rec_dir + "\\date.file"):
            print("No date.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(date, (bem_rec_dir + "\\date.file"))
            print("date.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\decode.file"):
            print("No decode.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(decode, (bem_rec_dir + "\\decode.file"))
            print("decode.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\seqNum.file"):
            print("No seqNum.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(seqNum, (bem_rec_dir + "\\seqNum.file"))
            print("seqNum.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\voltage.file"):
            print("No voltage.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(voltage, (bem_rec_dir + "\\voltage.file"))
            print("voltage.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\temperature.file"):
            print("No temperature.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(temperature, (bem_rec_dir + "\\temperature.file"))
            print("temperature.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\amp_seconds.file"):
            print("No amp_seconds.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(amp_seconds, (bem_rec_dir + "\\amp_seconds.file"))
            print("amp_seconds.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\enIn.file"):
            print("No enIn.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(enIn, (bem_rec_dir + "\\enIn.file"))
            print("enIn.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\enOut.file"):
            print("No enOut.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(enOut, (bem_rec_dir + "\\enOut.file"))
            print("enOut.file --- save complete.")
        else:
            pass
        
        #################################################################################

        if len(vc1) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_1.file"):
                print("No volt_1.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc1, (bem_rec_dir + "\\volt_1.file"))
                print("volt_1.file --- save complete.")
            else:
                pass
        else:
            pass
        
        if len(vc2) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_2.file"):
                print("No volt_2.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc2, (bem_rec_dir + "\\volt_2.file"))
                print("volt_2.file --- save complete.")
            else:
                pass
        if len(vc3) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_3.file"):
                print("No volt_3.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc3, (bem_rec_dir + "\\volt_3.file"))
                print("volt_3.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc4) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_4.file"):
                print("No volt_4.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc1, (bem_rec_dir + "\\volt_4.file"))
                print("volt_1.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc5) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_5.file"):
                print("No volt_5.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc5, (bem_rec_dir + "\\volt_5.file"))
                print("volt_5.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc6) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_6.file"):
                print("No volt_6.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc6, (bem_rec_dir + "\\volt_6.file"))
                print("volt_6.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc7) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_7.file"):
                print("No volt_7.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc7, (bem_rec_dir + "\\volt_7.file"))
                print("volt_7.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc8) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_8.file"):
                print("No volt_8.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc8, (bem_rec_dir + "\\volt_8.file"))
                print("volt_8.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc9) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_9.file"):
                print("No volt_9.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc9, (bem_rec_dir + "\\volt_9.file"))
                print("volt_9.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc10) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_10.file"):
                print("No volt_10.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc10, (bem_rec_dir + "\\volt_10.file"))
                print("volt_10.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc11) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_11.file"):
                print("No volt_11.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc11, (bem_rec_dir + "\\volt_11.file"))
                print("volt_11.file --- save complete.")
            else:
                pass
        else:
            pass

        if len(vc12) > 0:
            if not os.path.exists(bem_rec_dir + "\\volt_12.file"):
                print("No volt_12.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(vc12, (bem_rec_dir + "\\volt_12.file"))
                print("volt_12.file --- save complete.")
            else:
                pass
        else:
            pass

        # self.save_Gzipped_pickle(vc2, (bem_rec_dir + "\\vc2.file"))
        # self.save_Gzipped_pickle(vc3, (bem_rec_dir + "\\vc3.file"))
        # self.save_Gzipped_pickle(vc4, (bem_rec_dir + "\\vc4.file"))
        # self.save_Gzipped_pickle(vc5, (bem_rec_dir + "\\vc5.file"))
        # self.save_Gzipped_pickle(vc6, (bem_rec_dir + "\\vc6.file"))
        # self.save_Gzipped_pickle(vc7, (bem_rec_dir + "\\vc7.file"))
        # self.save_Gzipped_pickle(vc8, (bem_rec_dir + "\\vc8.file"))
        # self.save_Gzipped_pickle(vc9, (bem_rec_dir + "\\vc9.file"))
        # self.save_Gzipped_pickle(vc10, (bem_rec_dir + "\\vc10.file"))
        # self.save_Gzipped_pickle(vc11, (bem_rec_dir + "\\vc11.file"))
        # self.save_Gzipped_pickle(vc12, (bem_rec_dir + "\\vc12.file"))
        # print("------------ saves complete.")
        ##########################################################################



        if not os.path.exists(bem_rec_dir + "\\bal_cur_1.file"):
            print("No bal_cur_1.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc1, (bem_rec_dir + "\\bal_cur_1.file"))
            print("bal_cur_1.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_2.file"):
            print("No bal_cur_2.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc2, (bem_rec_dir + "\\bal_cur_2.file"))
            print("bal_cur_2.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_3.file"):
            print("No bal_cur_3.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc3, (bem_rec_dir + "\\bal_cur_3.file"))
            print("bal_cur_3.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_4.file"):
            print("No bal_cur_4.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc4, (bem_rec_dir + "\\bal_cur_4.file"))
            print("bal_cur_4.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_5.file"):
            print("No bal_cur_5.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc5, (bem_rec_dir + "\\bal_cur_5.file"))
            print("bal_cur_5.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_6.file"):
            print("No bal_cur_6.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc6, (bem_rec_dir + "\\bal_cur_6.file"))
            print("bal_cur_6.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_7.file"):
            print("No bal_cur_7.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc7, (bem_rec_dir + "\\bal_cur_7.file"))
            print("bal_cur_7.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_8.file"):
            print("No bal_cur_8.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc8, (bem_rec_dir + "\\bal_cur_8.file"))
            print("bal_cur_8.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_9.file"):
            print("No bal_cur_9.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc9, (bem_rec_dir + "\\bal_cur_9.file"))
            print("bal_cur_9.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_10.file"):
            print("No bal_cur_10.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc10, (bem_rec_dir + "\\bal_cur_10.file"))
            print("bal_cur_10.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_11.file"):
            print("No bal_cur_11.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc11, (bem_rec_dir + "\\bal_cur_11.file"))
            print("bal_cur_11.file --- save complete.")
        else:
            pass

        if not os.path.exists(bem_rec_dir + "\\bal_cur_12.file"):
            print("No bal_cur_12.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(bcc12, (bem_rec_dir + "\\bal_cur_12.file"))
            print("bal_cur_12.file --- save complete.")
        else:
            pass

        # print("Creating individual Cell Balancing Current FILE files...")
        # self.save_Gzipped_pickle(bcc1, (bem_rec_dir + "\\bcc1.file"))
        # self.save_Gzipped_pickle(bcc2, (bem_rec_dir + "\\bcc2.file"))
        # self.save_Gzipped_pickle(bcc3, (bem_rec_dir + "\\bcc3.file"))
        # self.save_Gzipped_pickle(bcc4, (bem_rec_dir + "\\bcc4.file"))
        # self.save_Gzipped_pickle(bcc5, (bem_rec_dir + "\\bcc5.file"))
        # self.save_Gzipped_pickle(bcc6, (bem_rec_dir + "\\bcc6.file"))
        # self.save_Gzipped_pickle(bcc7, (bem_rec_dir + "\\bcc7.file"))
        # self.save_Gzipped_pickle(bcc8, (bem_rec_dir + "\\bcc8.file"))
        # self.save_Gzipped_pickle(bcc9, (bem_rec_dir + "\\bcc9.file"))
        # self.save_Gzipped_pickle(bcc10, (bem_rec_dir + "\\bcc10.file"))
        # self.save_Gzipped_pickle(bcc11, (bem_rec_dir + "\\bcc11.file"))
        # self.save_Gzipped_pickle(bcc12, (bem_rec_dir + "\\bcc12.file"))
        # print("------------ saves complete.")
        ##########################################################################


        if not os.path.exists(bem_rec_dir + "\\temp_1.file"):
            print("No temp_1.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc1, (bem_rec_dir + "\\temp_1.file"))
            print("temp_1.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_2.file"):
            print("No temp_2.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc2, (bem_rec_dir + "\\temp_2.file"))
            print("temp_2.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_3.file"):
            print("No temp_3.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc3, (bem_rec_dir + "\\temp_3.file"))
            print("temp_3.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_4.file"):
            print("No temp_4.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc4, (bem_rec_dir + "\\temp_4.file"))
            print("temp_4.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_5.file"):
            print("No temp_5.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc5, (bem_rec_dir + "\\temp_5.file"))
            print("temp_5.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_6.file"):
            print("No temp_6.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc6, (bem_rec_dir + "\\temp_6.file"))
            print("temp_6.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_7.file"):
            print("No temp_7.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc7, (bem_rec_dir + "\\temp_7.file"))
            print("temp_7.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_8.file"):
            print("No temp_8.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc8, (bem_rec_dir + "\\temp_8.file"))
            print("temp_8.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_9.file"):
            print("No temp_9.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc9, (bem_rec_dir + "\\temp_9.file"))
            print("temp_9.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_10.file"):
            print("No temp_10.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc10, (bem_rec_dir + "\\temp_10.file"))
            print("temp_10.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_11.file"):
            print("No temp_11.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc11, (bem_rec_dir + "\\temp_11.file"))
            print("temp_11.file --- save complete.")
        else:
            pass
        
        if not os.path.exists(bem_rec_dir + "\\temp_12.file"):
            print("No temp_12.file detected for BEM_" + num + ".")
            self.save_Gzipped_pickle(tc12, (bem_rec_dir + "\\temp_12.file"))
            print("temp_12.file --- save complete.")
        else:
            pass

        # print("Creating individual Cell Temperature FILE files... ")
        # self.save_Gzipped_pickle(tc1, (bem_rec_dir + "\\tc1.file"))
        # self.save_Gzipped_pickle(tc2, (bem_rec_dir + "\\tc2.file"))
        # self.save_Gzipped_pickle(tc3, (bem_rec_dir + "\\tc3.file"))
        # self.save_Gzipped_pickle(tc4, (bem_rec_dir + "\\tc4.file"))
        # self.save_Gzipped_pickle(tc5, (bem_rec_dir + "\\tc5.file"))
        # self.save_Gzipped_pickle(tc6, (bem_rec_dir + "\\tc6.file"))
        # self.save_Gzipped_pickle(tc7, (bem_rec_dir + "\\tc7.file"))
        # self.save_Gzipped_pickle(tc8, (bem_rec_dir + "\\tc8.file"))
        # self.save_Gzipped_pickle(tc9, (bem_rec_dir + "\\tc9.file"))
        # self.save_Gzipped_pickle(tc10, (bem_rec_dir + "\\tc10.file"))
        # self.save_Gzipped_pickle(tc11, (bem_rec_dir + "\\tc11.file"))
        # self.save_Gzipped_pickle(tc12, (bem_rec_dir + "\\tc12.file"))
        # print("------------ saves complete.")
        ##########################################################################


            print("Directory for BEM " + num + " complete. Please select an option below.")


    ##########   P   L   O   T   S   ##########

    def date_vs_decodetime(self):
        print("Unzipping BEM Record FILE files...")

        d_date = []

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        decode = (self.load_Gzipped_pickle(bem_rec_dir + "\\decode.file"))
        print("decode.file --- unzip complete.")

        print("Total number of entries is " + str(len(date)))

        for x in range(len(date)):
            d_date.append(((decode[x] - date[x]).total_seconds()) / 3600)
            # print(d_date)
        print("decode times calculated.")

        import matplotlib.pyplot as plt

        #### DECODE_TIME/DATE  #####
        fig1 = plt.figure(1)
        plt.plot(date, d_date, '.')
        ax1 = fig1.add_subplot(111)
        ax1.set_title('DECODE TIMES')
        ax1.set_xlabel('DATE')
        ax1.set_ylabel('DECODE TIME, hrs')
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def decode_vs_decodetime(self):
        print("Unzipping BEM Record FILE files...")

        d_date = []

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        decode = (self.load_Gzipped_pickle(bem_rec_dir + "\\decode.file"))
        print("decode.file --- unzip complete.")

        for x in range(len(date)):
            d_date.append(((decode[x] - date[x]).total_seconds()) / 3600)
            # print(d_date)
        print("decode times calculated.")

        import matplotlib.pyplot as plt

        #####  DECODE_TIME/DECODE  #####
        fig2 = plt.figure(2)
        plt.plot(decode, d_date)
        ax2 = fig2.add_subplot(111)
        ax2.set_title('DECODE TIMES')
        ax2.set_xlabel('DATE DECODED')
        ax2.set_ylabel('DECODE TIME, hrs')
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def current_vs_date(self):
        print("Unzipping BEM Record FILE files...")

        current = []

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        amp_seconds = (self.load_Gzipped_pickle(bem_rec_dir + "\\amp_seconds.file"))
        print("amp_seconds.file --- unzip complete.")

        for x in range(len(date)):
            dd = (date[x] - date[x - 1]).total_seconds()
            # print(d_date, " and ", date[x], " and ", date[x - 1])
            if dd > 0:
                damp_seconds = amp_seconds[x] - amp_seconds[x - 1]
                current.append(int(damp_seconds / dd))

            else:
                current.append(0)

        print("current calculated.")

        import matplotlib.pyplot as plt

        ##### CURRENT/DATE  #####
        fig3 = plt.figure(3)
        plt.plot(date, current)
        ax3 = fig3.add_subplot(111)
        ax3.set_title('CURRENT')
        ax3.set_xlabel('DATE')
        ax3.set_ylabel('CURRENT')
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def voltage_vs_date(self):
        print("Unzipping BEM Record FILE files...")

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        voltage = (self.load_Gzipped_pickle(bem_rec_dir + "\\voltage.file"))
        print("voltage.file --- unzip complete.")

        import matplotlib.pyplot as plt

        #####  VOLTAGE/DATE  #####
        fig5 = plt.figure(5)
        plt.plot(date, voltage)
        ax5 = fig5.add_subplot(111)
        ax5.set_title('VOLTAGE/DATE')
        ax5.set_xlabel('DATE')
        ax5.set_ylabel('VOLTAGE')
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def voltage_vs_current(self):
        print("Unzipping BEM Record FILE files...")

        current = []

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        voltage = (self.load_Gzipped_pickle(bem_rec_dir + "\\voltage.file"))
        print("voltage.file --- unzip complete.")

        amp_seconds = (self.load_Gzipped_pickle(bem_rec_dir + "\\amp_seconds.file"))
        print("amp_seconds.file --- unzip complete.")

        for x in range(len(date)):
            dd = (date[x] - date[x - 1]).total_seconds()
            # print(d_date, " and ", date[x], " and ", date[x - 1])
            if dd > 0:
                damp_seconds = amp_seconds[x] - amp_seconds[x - 1]
                current.append(int(damp_seconds / dd))

            else:
                current.append(0)

        import matplotlib.pyplot as plt

        #####  VOLTAGE/CURRENT  #####
        fig4 = plt.figure(4)
        plt.plot(current, voltage)
        ax4 = fig4.add_subplot(111)
        ax4.set_title('VOLTAGE/CURRENT')
        ax4.set_xlabel('CURRENT')
        ax4.set_ylabel('VOLTAGE')
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def voltage_vs_charge(self):
        print("Unzipping BEM Record FILE files...")

        charge = []

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        voltage = (self.load_Gzipped_pickle(bem_rec_dir + "\\voltage.file"))
        print("voltage.file --- unzip complete.")

        amp_seconds = (self.load_Gzipped_pickle(bem_rec_dir + "\\amp_seconds.file"))
        print("amp_seconds.file --- unzip complete.")

        for x in range(len(date)):
            dd = (date[x] - date[x - 1]).total_seconds()
            # print(d_date, " and ", date[x], " and ", date[x - 1])
            if dd > 0:
                damp_seconds = amp_seconds[x] - amp_seconds[x - 1]
                charge.append(int((damp_seconds / dd) / dd))

            else:
                charge.append(0)

        import matplotlib.pyplot as plt

        #####  VOLTAGE/CURRENT  #####
        fig5 = plt.figure(5)
        plt.plot(charge, voltage)
        ax5 = fig5.add_subplot(111)
        ax5.set_title('VOLTAGE/CHARGE')
        ax5.set_xlabel('CHARGE')
        ax5.set_ylabel('VOLTAGE')
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def voltage_vs_energy(self):
        print("Unzipping BEM Record FILE files...")

        voltage = (self.load_Gzipped_pickle(bem_rec_dir + "\\voltage.file"))
        print("voltage.file --- unzip complete.")

        enIn = (self.load_Gzipped_pickle(bem_rec_dir + "\\enIn.file"))
        print("enIn.file --- unzip complete.")

        enOut = (self.load_Gzipped_pickle(bem_rec_dir + "\\enOut.file"))
        print("enOut.file --- unzip complete.")

        import matplotlib.pyplot as plt

        #####  VOLTAGE/ENERGY  #####
        fig6 = plt.figure(6)
        plt.plot(enOut, voltage, '.', enIn, voltage, '.')
        ax6 = fig6.add_subplot(111)
        ax6.set_title('VOLTAGE/ENERGY')
        ax6.set_xlabel('ENERGY')
        ax6.set_ylabel('VOLTAGE')
        plt.grid(True)
        time.sleep(2)
        print("Writing graph...")
        plt.show()


root = tk.Tk()
app = data_parsing_app(root)
root.mainloop()