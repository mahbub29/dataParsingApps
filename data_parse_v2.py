import tkinter as tk
from getFile import serialSearch
import json
import csv
import glob
import pickle
import gzip
import time
import matplotlib.pyplot as plt

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

        b(self.master, text="Quit", command=master.quit) \
            .grid(row=2, column=0, sticky="EW")

        submit = b(self.master, text="Get Records", command=self.show_entry_fields) \
            .grid(row=2, column=1, sticky="EW")

    def show_entry_fields(self):
        global num

        if len(self.entry_bem.get()) == 0:
            print("No BEM number entered. Please enter a BEM number.")
            l(self.master, text="No BEM number entered.") \
                .grid(row=3, column=0, columnspan=3, sticky="W")
            l(self.master, text="Please enter a BEM number.") \
                .grid(row=4, column=0, columnspan=3, sticky="W")
        else:
            num = self.entry_bem.get()
            print(num)
            print("Finding BEM UID for BEM %s..." % num)
            bemUID = serialSearch(num)
            if serialSearch(num):
                # print("BEM Number: %s" % (e1.get()))
                self.entry_bem.delete(0, 'end')
                self.bem_search(bemUID)
            else:
                print("No existing BEM UID found for BEM " + num)
                print("Check that you have entered the BEM number correctly or enter a different BEM number.")
                l(self.master, text="No existing BEM UID found for " + num) \
                    .grid(row=3, column=0, columnspan=3, sticky="W")
                l(self.master, text="Check that you have entered the BEM number") \
                    .grid(row=4, column=0, columnspan=3, sticky="W")
                l(self.master, text="correctly or enter a different BEM number.") \
                    .grid(row=5, column=0, columnspan=3, sticky="W")
                pass

    def bem_search(self, bemUID):

        global bemGraphFile
        global numCell

        numCell = 0

        bemGraphFile = 0

        path = 'C:\\Users\\mahbub\\PycharmProjects\\*\\*\\*\\*.csv'

        print("\nSearching for Raw BEM data. Please wait...\n")

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
                    numCell = int(jString["numberOfCells"])
                    # print("number of Cells " + str(numCell))
                    self.options_win()
                    bemGraphFile = file
                    print("Raw BEM data retrieved.")
                    print("...")
                    time.sleep(3)
                    self.pickle_time()
                    break
                else:
                    pass
            elif row[1] != "datagramReceived":
                print("No raw BEM data exists for BEM " + num)
                break
            else:
                pass

        print("\n\n------------------------------------------------------------------\n\n"
              "                         PROCESS COMPLETE"
              "\n\n------------------------------------------------------------------\n\n")


    def options_win(self):

        window2 = tk.Toplevel(self)
        window2.title("BEM Analysis Options")

        l(window2, text="Select an option :") \
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

        button8 = b(window2, text="Charge/Date", command=self.charge_vs_date)
        button8.grid(row=4, column=1, sticky="EW")
        button8.config(width=20, height=2)

        button10 = b(window2, text="Individual Cell Voltages", command=self.individual_volts)
        button10.grid(row=5, column=0, sticky="EW")
        button10.config(width=20, height=2)

        button9 = b(window2, text="State of Charge Analysis", command=self.charge_analysis)
        button9.grid(row=6, column=0, columnspan=2, sticky="EW")
        button9.config(width=40, height=3)


    def charge_analysis(self):

        window3 = tk.Toplevel(self)
        window3.title("State of Charge Analysis")

        button1 = b(window3, text="Discharge over Time", command=self.discharge_vs_date)
        button1.grid(row=0, column=0, sticky="EW")
        button1.config(width=30, height=2)

        button2 = b(window3, text="Charge Map", command=self.ask_increment)
        button2.grid(row=1, column=0, sticky="EW")
        button2.config(width=30, height=2)

        button3 = b(window3, text="Peak Charges", command=self.peak_charge)
        button3.grid(row=2, column=0, sticky="EW")
        button3.config(width=30, height=2)

        button4 = b(window3, text="Trough Charges", command=self.trough_charge)
        button4.grid(row=3, column=0, sticky="EW")
        button4.config(width=30, height=2)

        button5 = b(window3, text="State of Charge", command=self.midway)
        button5.grid(row=4, column=0, sticky="EW")
        button5.config(width=30, height=2)

        button6 = b(window3, text="Minimums", command=self.minimums)
        button6.grid(row=5, column=0, sticky="EW")
        button6.config(width=30, height=2)


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
        charge = []
        enIn = []
        enOut = []

        # #####  INDIVIDUAL CELLS  #####
        #
        # vc0 = []
        # vc1 = []
        # vc2 = []
        # vc3 = []
        # vc4 = []
        # vc5 = []
        # vc6 = []
        # vc7 = []
        # vc8 = []
        # vc9 = []
        # vc10 = []
        # vc11 = []
        #
        # bcc1 = []
        # bcc2 = []
        # bcc3 = []
        # bcc4 = []
        # bcc5 = []
        # bcc6 = []
        # bcc7 = []
        # bcc8 = []
        # bcc9 = []
        # bcc10 = []
        # bcc11 = []
        # bcc12 = []
        #
        # tc1 = []
        # tc2 = []
        # tc3 = []
        # tc4 = []
        # tc5 = []
        # tc6 = []
        # tc7 = []
        # tc8 = []
        # tc9 = []
        # tc10 = []
        # tc11 = []
        # tc12 = []

        allCellVolt = []
        allCellBal = []
        allCellTemp = []

        ###############################

        picklePath = bemGraphFile

        global bem_rec_dir
        bem_rec_dir = ("C:\\Users\\mahbub\\PycharmProjects\\BEM_records\\BEM_" + num)

        import os

        if not (os.path.exists(bem_rec_dir + "\\date.file") \
                and os.path.exists(bem_rec_dir + "\\decode.file") \
                and os.path.exists(bem_rec_dir + "\\seqNum.file") \
                and os.path.exists(bem_rec_dir + "\\voltage.file") \
                and os.path.exists(bem_rec_dir + "\\temperature.file") \
                and os.path.exists(bem_rec_dir + "\\charge.file") \
                and os.path.exists(bem_rec_dir + "\\enIn.file") \
                and os.path.exists(bem_rec_dir + "\\enOut.file") \
                and os.path.exists(bem_rec_dir + "\\allCellVolt.file") \
                and os.path.exists(bem_rec_dir + "\\allCellBal.file") \
                and os.path.exists(bem_rec_dir + "\\allCellTemp.file")):

            if not os.path.exists(bem_rec_dir):
                print("There is no BEM record directory for BEM " + num + ". Please wait whilst a directory is made...")

                os.makedirs(bem_rec_dir)

                print("Converting JSON strings files to FILE files...")

            for row in self.get_data(picklePath, 2):

                if (count % 10000) == 0:
                    print(str(count) + " entries loaded")

                # if count == 1000:
                #     break

                try:
                    var = json.loads(row)
                    date.append(dtp.parse(var['date']))
                    decode.append(dtp.parse(var['dateDecoded']))
                    seqNum.append(int(var['sequenceNumber']))
                    voltage.append(int(var['bemVoltageAve']))
                    temperature.append(int(var['temperature']))
                    charge.append(int(var['bemAmpSeconds']))
                    enIn.append(int(var['bemEnergyIn']))
                    enOut.append(int(var['bemEnergyOut']))

                    tmpCellVolt = []
                    tmpCellBal = []
                    tmpCellTemp = []


                    if numCell > 0:
                        # print(numCell)
                        for i in range(0, numCell):

                            tmpCellVolt.append(var['cells'][i]['cellVoltage'])
                            allCellVolt.append(tmpCellVolt)

                            tmpCellBal.append(var['cells'][i]['balanceCurrent'])
                            allCellBal.append(tmpCellBal)

                            tmpCellTemp.append(var['cells'][i]['temperature'])
                            allCellTemp.append(tmpCellTemp)

                            # tempCellVolt.append(var['cells'][i]['cellVoltage'])
                            # allCellVolt.append(tempCellVolt[i])

                            # dictCellVolt["vc{0}".format(i)] = var['cells'][i]['cellVoltage']
                            # dictCellBal["bcc{0}".format(i)] = var['cells'][i]['balanceCurrent']
                            # dictCellTemp["tc{0}".format(i)] = var['cells'][i]['temperature']

                            # print("tempCellVolt" + str(tempCellVolt))
                            # print("allCellVolt" + str(allCellVolt))

                        # print(dictCellBal)
                        # print(dictCellTemp)

                    # vc1.append(var['cells'][1]['cellVoltage'])
                    # vc2.append(var['cells'][1]['cellVoltage'])
                    # vc3.append(var['cells'][2]['cellVoltage'])
                    # vc4.append(var['cells'][3]['cellVoltage'])
                    # vc5.append(var['cells'][4]['cellVoltage'])
                    # vc6.append(var['cells'][5]['cellVoltage'])
                    # vc7.append(var['cells'][6]['cellVoltage'])
                    # vc8.append(var['cells'][7]['cellVoltage'])
                    # vc9.append(var['cells'][8]['cellVoltage'])
                    # vc10.append(var['cells'][9]['cellVoltage'])
                    # vc11.append(var['cells'][10]['cellVoltage'])
                    # vc12.append(var['cells'][11]['cellVoltage'])
                    #
                    # bcc1.append(var['cells'][0]['balanceCurrent'])
                    # bcc2.append(var['cells'][1]['balanceCurrent'])
                    # bcc3.append(var['cells'][2]['balanceCurrent'])
                    # bcc4.append(var['cells'][3]['balanceCurrent'])
                    # bcc5.append(var['cells'][4]['balanceCurrent'])
                    # bcc6.append(var['cells'][5]['balanceCurrent'])
                    # bcc7.append(var['cells'][6]['balanceCurrent'])
                    # bcc8.append(var['cells'][7]['balanceCurrent'])
                    # bcc9.append(var['cells'][8]['balanceCurrent'])
                    # bcc10.append(var['cells'][9]['balanceCurrent'])
                    # bcc11.append(var['cells'][10]['balanceCurrent'])
                    # bcc12.append(var['cells'][11]['balanceCurrent'])
                    #
                    # tc1.append(var['cells'][0]['temperature'])
                    # tc2.append(var['cells'][1]['temperature'])
                    # tc3.append(var['cells'][2]['temperature'])
                    # tc4.append(var['cells'][3]['temperature'])
                    # tc5.append(var['cells'][4]['temperature'])
                    # tc6.append(var['cells'][5]['temperature'])
                    # tc7.append(var['cells'][6]['temperature'])
                    # tc8.append(var['cells'][7]['temperature'])
                    # tc9.append(var['cells'][8]['temperature'])
                    # tc10.append(var['cells'][9]['temperature'])
                    # tc11.append(var['cells'][10]['temperature'])
                    # tc12.append(var['cells'][11]['temperature'])

                except IndexError:
                    pass

            time.sleep(3)
            print("\n---------------------------------------\nTotal number of entries --- "\
                  + str(count) + "\n---------------------------------------\n")
            time.sleep(3)


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

            if not os.path.exists(bem_rec_dir + "\\charge.file"):
                print("No charge.file detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(charge, (bem_rec_dir + "\\charge.file"))
                print("charge.file --- save complete.")
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

            ##############  INDIVIDUAL CELL READINGS   ##############

            if not os.path.exists(bem_rec_dir + "\\allCellVolt.file"):
                print("No allCellVolt.file  detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(allCellVolt, (bem_rec_dir + "\\allCellVolt.file"))
                print("allCellVolt.file --- save complete.")
            else:
                pass

            if not os.path.exists(bem_rec_dir + "\\allCellBal.file"):
                print("No allCellBal.file  detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(allCellBal, (bem_rec_dir + "\\allCellBal.file"))
                print("allCellBal.file --- save complete.")
            else:
                pass

            if not os.path.exists(bem_rec_dir + "\\allCellTemp.file"):
                print("No allCellTemp.file  detected for BEM_" + num + ".")
                self.save_Gzipped_pickle(allCellTemp, (bem_rec_dir + "\\allCellTemp.file"))
                print("allCellTemp.file --- save complete.")
            else:
                pass
            #################################################################################

            # if len(vc1) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_1.file"):
            #         print("No volt_1.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc1, (bem_rec_dir + "\\volt_1.file"))
            #         print("volt_1.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc2) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_2.file"):
            #         print("No volt_2.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc2, (bem_rec_dir + "\\volt_2.file"))
            #         print("volt_2.file --- save complete.")
            #     else:
            #         pass
            # if len(vc3) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_3.file"):
            #         print("No volt_3.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc3, (bem_rec_dir + "\\volt_3.file"))
            #         print("volt_3.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc4) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_4.file"):
            #         print("No volt_4.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc1, (bem_rec_dir + "\\volt_4.file"))
            #         print("volt_1.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc5) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_5.file"):
            #         print("No volt_5.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc5, (bem_rec_dir + "\\volt_5.file"))
            #         print("volt_5.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc6) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_6.file"):
            #         print("No volt_6.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc6, (bem_rec_dir + "\\volt_6.file"))
            #         print("volt_6.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc7) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_7.file"):
            #         print("No volt_7.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc7, (bem_rec_dir + "\\volt_7.file"))
            #         print("volt_7.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc8) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_8.file"):
            #         print("No volt_8.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc8, (bem_rec_dir + "\\volt_8.file"))
            #         print("volt_8.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc9) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_9.file"):
            #         print("No volt_9.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc9, (bem_rec_dir + "\\volt_9.file"))
            #         print("volt_9.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc10) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_10.file"):
            #         print("No volt_10.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc10, (bem_rec_dir + "\\volt_10.file"))
            #         print("volt_10.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc11) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_11.file"):
            #         print("No volt_11.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc11, (bem_rec_dir + "\\volt_11.file"))
            #         print("volt_11.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass
            #
            # if len(vc12) > 0:
            #     if not os.path.exists(bem_rec_dir + "\\volt_12.file"):
            #         print("No volt_12.file detected for BEM_" + num + ".")
            #         self.save_Gzipped_pickle(vc12, (bem_rec_dir + "\\volt_12.file"))
            #         print("volt_12.file --- save complete.")
            #     else:
            #         pass
            # else:
            #     pass

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

            # if not os.path.exists(bem_rec_dir + "\\bal_cur_1.file"):
            #     print("No bal_cur_1.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc1, (bem_rec_dir + "\\bal_cur_1.file"))
            #     print("bal_cur_1.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_2.file"):
            #     print("No bal_cur_2.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc2, (bem_rec_dir + "\\bal_cur_2.file"))
            #     print("bal_cur_2.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_3.file"):
            #     print("No bal_cur_3.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc3, (bem_rec_dir + "\\bal_cur_3.file"))
            #     print("bal_cur_3.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_4.file"):
            #     print("No bal_cur_4.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc4, (bem_rec_dir + "\\bal_cur_4.file"))
            #     print("bal_cur_4.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_5.file"):
            #     print("No bal_cur_5.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc5, (bem_rec_dir + "\\bal_cur_5.file"))
            #     print("bal_cur_5.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_6.file"):
            #     print("No bal_cur_6.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc6, (bem_rec_dir + "\\bal_cur_6.file"))
            #     print("bal_cur_6.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_7.file"):
            #     print("No bal_cur_7.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc7, (bem_rec_dir + "\\bal_cur_7.file"))
            #     print("bal_cur_7.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_8.file"):
            #     print("No bal_cur_8.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc8, (bem_rec_dir + "\\bal_cur_8.file"))
            #     print("bal_cur_8.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_9.file"):
            #     print("No bal_cur_9.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc9, (bem_rec_dir + "\\bal_cur_9.file"))
            #     print("bal_cur_9.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_10.file"):
            #     print("No bal_cur_10.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc10, (bem_rec_dir + "\\bal_cur_10.file"))
            #     print("bal_cur_10.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_11.file"):
            #     print("No bal_cur_11.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc11, (bem_rec_dir + "\\bal_cur_11.file"))
            #     print("bal_cur_11.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\bal_cur_12.file"):
            #     print("No bal_cur_12.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(bcc12, (bem_rec_dir + "\\bal_cur_12.file"))
            #     print("bal_cur_12.file --- save complete.")
            # else:
            #     pass

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

            # if not os.path.exists(bem_rec_dir + "\\temp_1.file"):
            #     print("No temp_1.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc1, (bem_rec_dir + "\\temp_1.file"))
            #     print("temp_1.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_2.file"):
            #     print("No temp_2.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc2, (bem_rec_dir + "\\temp_2.file"))
            #     print("temp_2.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_3.file"):
            #     print("No temp_3.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc3, (bem_rec_dir + "\\temp_3.file"))
            #     print("temp_3.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_4.file"):
            #     print("No temp_4.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc4, (bem_rec_dir + "\\temp_4.file"))
            #     print("temp_4.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_5.file"):
            #     print("No temp_5.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc5, (bem_rec_dir + "\\temp_5.file"))
            #     print("temp_5.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_6.file"):
            #     print("No temp_6.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc6, (bem_rec_dir + "\\temp_6.file"))
            #     print("temp_6.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_7.file"):
            #     print("No temp_7.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc7, (bem_rec_dir + "\\temp_7.file"))
            #     print("temp_7.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_8.file"):
            #     print("No temp_8.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc8, (bem_rec_dir + "\\temp_8.file"))
            #     print("temp_8.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_9.file"):
            #     print("No temp_9.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc9, (bem_rec_dir + "\\temp_9.file"))
            #     print("temp_9.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_10.file"):
            #     print("No temp_10.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc10, (bem_rec_dir + "\\temp_10.file"))
            #     print("temp_10.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_11.file"):
            #     print("No temp_11.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc11, (bem_rec_dir + "\\temp_11.file"))
            #     print("temp_11.file --- save complete.")
            # else:
            #     pass
            #
            # if not os.path.exists(bem_rec_dir + "\\temp_12.file"):
            #     print("No temp_12.file detected for BEM_" + num + ".")
            #     self.save_Gzipped_pickle(tc12, (bem_rec_dir + "\\temp_12.file"))
            #     print("temp_12.file --- save complete.")
            # else:
            #     pass

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
        else:
            pass

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

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        for x in range(len(date)):
            dd = (date[x] - date[x - 1]).total_seconds()
            # print(d_date, " and ", date[x], " and ", date[x - 1])
            if dd > 0:
                dcharge = charge[x] - charge[x - 1]
                current.append(int(dcharge / dd))

            else:
                current.append(0)

        print("current calculated.")

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

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        for x in range(len(date)):
            dd = (date[x] - date[x - 1]).total_seconds()
            # print(d_date, " and ", date[x], " and ", date[x - 1])
            if dd > 0:
                dCharge = charge[x] - charge[x - 1]
                current.append(int(dCharge / dd))

            else:
                current.append(0)

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

        voltage = (self.load_Gzipped_pickle(bem_rec_dir + "\\voltage.file"))
        print("voltage.file --- unzip complete.")

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

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

        #####  VOLTAGE/ENERGY  #####
        fig6 = plt.figure(6)
        plt.plot(enOut, voltage, enIn, voltage)
        ax6 = fig6.add_subplot(111)
        ax6.set_title('VOLTAGE/ENERGY')
        ax6.set_xlabel('ENERGY')
        ax6.set_ylabel('VOLTAGE')
        plt.grid(True)
        time.sleep(2)
        print("Writing graph...")
        plt.show()


    def charge_vs_date(self):

        import numpy

        print("Unzipping BEM Record FILE files...")

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        # allCellVolt = (self.load_Gzipped_pickle(bem_rec_dir + "\\allCellVolt.file"))
        # print("allCellVolt.file --- unzip complete.")

        chargeArray = numpy.array(charge)
        Ah = chargeArray/3600

        fig = plt.figure(7)
        plt.plot(date, Ah, ".")
        ax = fig.add_subplot(111)
        ax.set_title("CHARGE/DATE")
        ax.set_xlabel("DATE")
        ax.set_ylabel("Ah")
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()

    def individual_volts(self):
        print("Unzipping BEM Record FILE files...")

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        allCellVolt = (self.load_Gzipped_pickle(bem_rec_dir + "\\allCellVolt.file"))
        print("allCellVolt.file --- unzip complete.")

        try:
            fig = plt.figure(8)
            plt.plot(date*numCell, allCellVolt)
            ax = fig.add_subplot(111)
            ax.set_title("INDIVIDUAL CELL VOLTAGES")
            ax.set_xlabel("DATE")
            ax.set_ylabel("CELL VOLTAGE")
            plt.grid(True)
            print("Writing graph...")
            time.sleep(2)
            plt.show()
        except MemoryError:
            print("Unable to display graph for Individaul Cell Voltages, due to a MemoryError!")

    def discharge_vs_date(self):
        import numpy as np
        from datetime import datetime, timedelta
        import matplotlib.dates as mdates

        print("Unzipping BEM Record FILE files...")

        dates_list = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        # date_start = dates_list[0]
        # date_end = dates_list[-1] + timedelta(3 * 365 / 12)

        date = mdates.date2num(dates_list)

        dischargeArray = np.array(charge)
        Ah = dischargeArray / -3600

        z = np.polyfit(date, Ah, 1)
        p = np.poly1d(z)

        # print("________________________")
        # print(Ah[0])
        # print(Ah[109])
        # print(Ah[22605])
        # print("________________________")

        fig = plt.figure(9)
        plt.plot(date, Ah, ".", markersize=1, color="blue")
        plt.plot(dates_list, p(date), "--r", linewidth=1)
        ax = fig.add_subplot(111)
        ax.set_title("DISCHARGE/DATE")
        ax.set_xlabel("DATE")
        ax.set_ylabel("Ah")
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()

    def ask_increment(self):
        global increment_window

        increment_window = tk.Toplevel(self)
        increment_window.title("Set Ah Boundary")

        l(increment_window, text="(Optional) Enter desired +/-Ah boundary (default = +/-0.015 Ah).")\
            .grid(row=0, column=0, columnspan=3, sticky="W")

        l(increment_window, text="(+/-Ah value must be 0 <= +/-Ah <= 20)")\
            .grid(row=1, column=0, columnspan=3, sticky="W")

        global incQuery

        incQuery = e(increment_window)
        incQuery.grid(row=2, column=0, columnspan=3, sticky="EW")

        quitButton = b(increment_window, text="Back", command=increment_window.destroy)
        quitButton.grid(row=3, column=0, sticky="EW")

        contButton = b(increment_window, text="Continue", command=self.ask_inc_get)
        contButton.grid(row=3, column=1, columnspan=3, sticky="EW")

    def ask_inc_get(self):
        global increment

        if len(incQuery.get()) == 0:
            increment = 0.015
            increment_window.destroy()
            self.charge_map(increment)
        else:
            getQuery = int(float(incQuery.get()))
            if getQuery > 20:
                print("+/-Ah too high. Please type a smaller +/-Ah value. Default value is +/-0.015 Ah.")
                l(increment_window, \
                  text="+/-Ah too high. Please type a smaller +/-Ah value. Default value is +/-0.015 Ah.")\
                    .grid(row=4, column=0, columnspan=3, sticky="W")
                increment = 0.015
                pass
            elif getQuery < 0:
                print("+/-Ah cannot be a negative value. Default value is +/-0.015 Ah.")
                l(increment_window, \
                  text="+/-Ah cannot be a negative value. Default value is +/-0.015 Ah.") \
                    .grid(row=5, column=0, columnspan=3, sticky="W")
                increment = 0.015
                pass
            else:
                increment = getQuery
                increment_window.destroy()
                self.charge_map(increment)


    def charge_map(self, increment):
        import numpy

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        state = []
        state.append(int(0))

        dischargeArray = numpy.array(charge)
        Ah = dischargeArray / -3600

        for i in range(0, len(date)-1):

            if Ah[i+1] > (Ah[i] + int(increment)):
                state.append(int(1))
            elif Ah[i+1] < (Ah[i] - int(increment)):
                state.append(int(-1))
            else:
                state.append(int(0))

        state = numpy.array(state)

        fig = plt.figure(10)
        plt.plot(date, state, linewidth=0.5)
        ax = fig.add_subplot(111)
        ax.set_title("CHARGE MAP")
        ax.set_xlabel("DATE")
        ax.set_ylabel("CHAREGE(+1) OR DISHCHARGE(-1)")
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def peak_charge(self):
        import numpy

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        peakC = []
        peakDates = []
        indexPeak = []

        dischargeArray = numpy.array(charge)
        Ah = dischargeArray / -3600

        maxAh = Ah[0]

        for i in range(0, len(charge)):
            if Ah[i] > maxAh:
                peakC.append(Ah[i])
                peakDates.append(date[i])
                indexPeak.append(i)
                maxAh = Ah[i]
            else:
                pass

        print(str(len(peakDates)) + " peaks " + str(indexPeak))

        csvfile = "C:\\Users\\mahbub\\PycharmProjects\\BEM_csv\\peak_charge\\" + num + "peaks.csv"

        try:
            with open(csvfile, "w", newline="") as peaksFile:
                writer = csv.writer(peaksFile)
                writer.writerows(zip(peakDates, peakC))
        except PermissionError:
            print("\nThe CSV file you are trying to write to is open. Please close this file so that it can be rewritten.\n")

        fig = plt.figure(11)
        plt.plot(peakDates, peakC, color="red", linewidth=1)
        plt.plot(peakDates, peakC, "*", markersize=0.5, color="black")
        ax = fig.add_subplot(111)
        ax.set_title("PEAK CHARGES")
        ax.set_xlabel("DATE")
        ax.set_ylabel("PEAK CHARGES")
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def trough_charge(self):
        import numpy

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        troughC = []
        troughDates = []
        indexTrough = []

        dischargeArray = numpy.array(charge)
        Ah = dischargeArray / -3600

        minAh = Ah[len(charge)-1]

        for i in range(len(charge)-1, 0, -1):
            if Ah[i] < minAh:
                troughC.append(Ah[i])
                troughDates.append(date[i])
                indexTrough.append(i)
                minAh = Ah[i]
            else:
                pass

        # print(troughC)
        # print(len(troughC))
        # print(len(troughDates))
        print(str(len(troughDates)) + " troughs " + str(indexTrough))

        fig = plt.figure(11)
        plt.plot(troughDates, troughC, color="blue", linewidth=1)
        plt.plot(troughDates, troughC,"*", markersize=0.5, color="black")
        ax = fig.add_subplot(111)
        ax.set_title("TROUGH CHARGES")
        ax.set_xlabel("DATE")
        ax.set_ylabel("TROUGH CHARGES")
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def midway(self):
        import numpy

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        peakC = []
        peakDates = []
        indexPeak = []

        troughC = []
        troughDates = []
        indexTrough = []

        dischargeArray = numpy.array(charge)
        Ah = dischargeArray / -3600

        maxAh = Ah[0]
        minAh = Ah[len(charge) - 1]

        for i in range(0, len(charge)):
            if Ah[i] > maxAh:
                peakC.append(Ah[i])
                peakDates.append(date[i])
                indexPeak.append(i)
                maxAh = Ah[i]
            else:
                pass

        for i in range(len(charge)-1, 0, -1):
            if Ah[i] < minAh:
                troughC.append(Ah[i])
                troughDates.append(date[i])
                indexTrough.append(i)
                minAh = Ah[i]
            else:
                pass

        newIndexPeak = []
        newIndexTrough = []

        for i in range(len(indexTrough)-1, 0, -1):
            newIndexTrough.append(indexTrough[i])

        print(len(newIndexTrough))
        print(newIndexTrough)

        for i in range(len(indexPeak)-len(newIndexTrough), len(indexPeak)):
            newIndexPeak.append(indexPeak[i])

        print(len(newIndexPeak))
        print(newIndexPeak)

        # diff = 0
        #
        # if len(newIndexPeak) <= len(newIndexTrough):
        #     for c in range(0, len(newIndexTrough)):
        #         for i in range(0, len(indexPeak)):
        #             if (indexPeak[i] != newIndexTrough[c] + diff or indexPeak[i] != newIndexTrough[c] - diff) and diff <= 250:
        #                 diff += 1
        #             if indexPeak[i] == indexTrough[c] + diff or indexPeak[i] == indexTrough[c] - diff:
        #                 print("A " + str(i))
        #                 print("B " + str(indexPeak[i]))
        #                 newIndexPeak.append(indexPeak[i])
        #                 diff = 0
        #             elif indexPeak[i] == indexTrough[c] + diff and indexPeak[i] == indexTrough[c] - diff:
        #                 diff = 0
        #                 continue
        #             elif diff > 250:
        #                 diff = 0
        #                 continue
        #             else:
        #                 diff = 0
        #                 pass
        # else:
        #     pass


        # print("C " + str(newIndexPeak))
        # print("D " + str(newIndexTrough))

        # peak_trough_diff = [peakC[i] for i in newIndexPeak]
        # print(len(newIndexPeak))
        # print(newIndexPeak)
        #
        # print(len(peakC))

        print(len(peakC))

        peak_trough_diff = []
        peak_trough_dates = []

        for i in range(0, len(newIndexPeak)):
            peak_trough_diff.append(Ah[newIndexPeak[i]] - Ah[newIndexTrough[i]])
            peak_trough_dates.append(date[newIndexPeak[i]])

        print(peak_trough_diff)

        fig = plt.figure(11)
        plt.plot(peak_trough_dates, peak_trough_diff, "g--", linewidth=1)
        ax = fig.add_subplot(111)
        ax.set_title("SoC")
        ax.set_xlabel("DATE")
        ax.set_ylabel("CHARGE")
        plt.grid(True)
        print("Writing graph...")
        time.sleep(2)
        plt.show()


    def minimums(self):
        import numpy

        date = (self.load_Gzipped_pickle(bem_rec_dir + "\\date.file"))
        print("date.file --- unzip complete.")

        charge = (self.load_Gzipped_pickle(bem_rec_dir + "\\charge.file"))
        print("charge.file --- unzip complete.")

        dischargeArray = numpy.array(charge)
        Ah = dischargeArray / -3600

        peakC = []
        peakDates = []
        indexPeak = []

        dischargeArray = numpy.array(charge)
        Ah = dischargeArray / -3600

        maxAh = Ah[0]
        minAh = Ah[len(charge) - 1]

        for i in range(0, len(charge)):
            if Ah[i] > maxAh:
                peakC.append(Ah[i])
                peakDates.append(date[i])
                indexPeak.append(i)
                maxAh = Ah[i]
            else:
                pass

        # for i in range(0, len(Ah)):
        #     if Ah[i] < Ah[i+1] and Ah[i] < Ah[i+2] and Ah[i] < Ah[i+3] and Ah[i] < Ah[i+4] and Ah[i] < Ah[i+5] and Ah[i] < Ah[i+6] and Ah[i] < Ah[i+7] and Ah[i] < Ah[i+8] and Ah[i] < Ah[i+9] and Ah[i] < Ah[i+10]\
        #             and Ah[i] < Ah[i-1] and Ah[i] < Ah[i-2] and Ah[i] < Ah[i-3] and Ah[i] < Ah[i-4] and Ah[i] < Ah[i-5] and Ah[i] < Ah[i-6] and Ah[i] < Ah[i-7] and Ah[i] < Ah[i-8] and Ah[i] < Ah[i-9] and Ah[i] < Ah[i-10]:
        #

        # minimums = []
        # minDates = []
        #
        # for i in range(2, len(charge)-3):
        #     if Ah[i] < Ah[i+1] and Ah[i] < Ah[i+2] and Ah[i] < Ah[i+3] and Ah[i] < Ah[i+4] and Ah[i] < Ah[i+5] and Ah[i] < Ah[i+6] and Ah[i] < Ah[i+7] and Ah[i] < Ah[i+8] and Ah[i] < Ah[i+9] and Ah[i] < Ah[i+10]\
        #             and Ah[i] < Ah[i-1] and Ah[i] < Ah[i-2] and Ah[i] < Ah[i-3] and Ah[i] < Ah[i-4] and Ah[i] < Ah[i-5] and Ah[i] < Ah[i-6] and Ah[i] < Ah[i-7] and Ah[i] < Ah[i-8] and Ah[i] < Ah[i-9] and Ah[i] < Ah[i-10]:
        #         minimums.append(Ah[i])
        #         minDates.append(date[i])
        #     else:
        #         pass
        #
        # fig = plt.figure(11)
        # plt.plot(minDates, minimums, color="green", linewidth=1)
        # plt.plot(minDates, minimums, ".", color="black", markersize=0.5)
        # ax = fig.add_subplot(111)
        # ax.set_title("MINIMUMS")
        # ax.set_xlabel("DATE")
        # ax.set_ylabel("CHARGE")
        # plt.grid(True)
        # print("Writing graph...")
        # time.sleep(2)
        # plt.show()


root = tk.Tk()
app = data_parsing_app(root)
root.mainloop()