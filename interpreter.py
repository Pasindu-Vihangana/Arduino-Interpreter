import os
import threading
import time
import pickle
import tkinter

from pyfirmata import Arduino, util, Pin

from tkinter import *
from tkinter import filedialog

from functools import partial


########################################################################################################################
########################################################################################################################
def update_INPUT():
    global circuitElements
    for keys in pinConfig.keys():
        if keys.split('_')[0] == 'input':
            if circuitElements[keys].value:
                INPUT_element[keys].config(image=on)
            else:
                INPUT_element[keys].config(image=off)
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def set_INPUT(element_ID):
    global circuitElements
    # print(circuitElements[element_ID].name + ' = ' + str(circuitElements[element_ID].value))
    print(HardwarePriority[element_ID].get())
    if HardwarePriority[element_ID].get() == "HARDWARE":
        # it.start()
        try:
            print(ArduinoElements[element_ID].read())
            circuitElements[element_ID].node['pin'] = ArduinoElements[element_ID].read()
            circuitElements[element_ID].value = ArduinoElements[element_ID].read()
        finally:
            # board.exit()
            it.join(0.1)
    else:
        update_INPUT()
        if circuitElements[element_ID].value:
            circuitElements[element_ID].node['pin'] = False
            circuitElements[element_ID].value = False
        else:
            circuitElements[element_ID].node['pin'] = True
            circuitElements[element_ID].value = True

    print(circuitElements[element_ID].name + ' = ' + str(circuitElements[element_ID].value))
    refresh()
    update_INPUT()
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def runElements():
    global circuitElements
    # print("########################################################")
    for e in logicElements.keys():
        circuitElements[e].process()
        '''
        print(circuitElements[e].name)
        print(circuitElements[e].node)
        '''
    # print("########################################################")
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def update_TERMINALS():
    global circuitElements
    # print("########################################################")
    # for i in range(2):
    for wires in range(len(wiring)):
        receiver = wiring[wires][1].split('.')[0]
        receiver_T = wiring[wires][1].split('.')[1]
        sender = wiring[wires][0].split('.')[0]
        sender_T = wiring[wires][0].split('.')[1]
        # print(receiver + " @ " + receiver_T + " = " + sender + " @ " + sender_T)
        # print(str(circuitElements[receiver].out()) + " = " + str(circuitElements[sender].out()))

        # Critical # DO NOT CHANGE without AUTHORIZATION # Critical #
        circuitElements[sender].process()
        circuitElements[receiver].node[receiver_T] = circuitElements[sender].out()
        circuitElements[receiver].value = circuitElements[sender].out()
        # print(str(circuitElements[receiver].out()) + " = " + str(circuitElements[sender].out()))

    # print("########################################################")
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def update_OUTPUT():
    # print("output(s) updated")
    global circuitElements
    for keys in pinConfig.keys():
        if keys.split('_')[0] == 'output':
            # print(circuitElements[keys].node)
            ArduinoElements[keys].write(circuitElements[keys].out())
            if circuitElements[keys].out():
                OUTPUT_element[keys].config(image=on_bulb)
            else:
                OUTPUT_element[keys].config(image=off_bulb)
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def tick():
    global time1, circuitElements
    time2 = time.strftime('%H:%M:%S')
    print("clocking")
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)

    for keys in pinConfig.keys():
        if keys.split("_")[0] == "input":
            if HardwarePriority[keys].get() == "HARDWARE":
                set_INPUT(keys)

    clock.after(50, tick)
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def refresh():
    global circuitElements
    update_INPUT()
    update_TERMINALS()
    runElements()
    update_TERMINALS()
    runElements()
    update_TERMINALS()
    update_OUTPUT()
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def voidMain():
    # print('void setup()')
    # print('{')
    for keys in pinConfig.keys():
        match keys.split('_')[0]:
            case 'input':
                pinCall = 'd:' + str(pinConfig[keys].digitalAddress) + ':i'
                ArduinoElements[keys] = board.get_pin(pinCall)
                # print('pinMode(' + str(pinConfig[keys].digitalAddress) + ', INPUT);')
                # print(pinCall)
            case 'output':
                pinCall = 'd:' + str(pinConfig[keys].digitalAddress) + ':o'
                ArduinoElements[keys] = board.get_pin(pinCall)
                # print(pinCall)
                # print('pinMode(' + str(pinConfig[keys].digitalAddress) + ', OUTPUT);')
    # print('}')
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def changePriority(choice):
    global HardwarePriority, circuitElements
    print(choice)
    for keys in pinConfig.keys():
        if keys.split("_")[0] == "input":
            match HardwarePriority[keys].get():
                case 'HARDWARE':
                    # it.start()
                    try:
                        print(ArduinoElements[keys].read())
                        circuitElements[keys].node['pin'] = ArduinoElements[keys].read()
                        circuitElements[keys].value = ArduinoElements[keys].read()
                    finally:
                        # board.exit()
                        it.join(0.1)
                case 'SOFTWARE':
                    set_INPUT(keys)
    update_INPUT()
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
# Define GUI
########################################################################################################################
# Create Object
root2 = Tk()

# Set Title
root2.title('CIRCUIT SIMULATOR')

# Add Geometry
root2.geometry("640x480")
root2.columnconfigure([0, 1], minsize=300, pad=20)
root2.rowconfigure([0, 5], minsize=50, pad=20)
########################################################################################################################

########################################################################################################################
# Define Images
########################################################################################################################
on = PhotoImage(file="./images/ON.png")
off = PhotoImage(file="./images/OFF.png")
on_bulb = PhotoImage(file="./images/ON_light.png")
off_bulb = PhotoImage(file="./images/OFF_light.png")
hardware = PhotoImage(file="./images/Hardware.png")
software = PhotoImage(file="./images/Software.png")
########################################################################################################################

########################################################################################################################
# Define Variable Dicts
########################################################################################################################
INPUT_element = {}
INPUT_labels = {}
INPUT_option = {}
HardwarePriority = {}
OUTPUT_element = {}
OUTPUT_label = {}
ArduinoElements = {}
options = ['HARDWARE', 'SOFTWARE']
time1 = time.strftime('%H:%M:%S')
########################################################################################################################

########################################################################################################################
# load files from config.py
########################################################################################################################
with open("bin/boardConfig.pkl", "rb") as pinFile:
    temp = pickle.load(pinFile)
    port = temp[0]
    boardType = temp[1]
    del temp
    pinFile.close()

with open("bin/pins.pkl", "rb") as pinFile:
    temp = pickle.load(pinFile)
    pinConfig = temp
    del temp
    pinFile.close()

with open("bin/wiring.pkl", "rb") as connectionFile:
    temp = pickle.load(connectionFile)
    wiring = temp
    del temp
    connectionFile.close()

with open("bin/logicElements.pkl", "rb") as elementsFile:
    temp = pickle.load(elementsFile)
    logicElements = temp
    del temp
    elementsFile.close()
########################################################################################################################
circuitElements = pinConfig | logicElements
########################################################################################################################
########################################################################################################################

########################################################################################################################
# Define Arduino
########################################################################################################################
print("Connecting to the \"" + boardType + "\" @ " + port)
board = Arduino(port)
print('version: ' + str(board.get_firmata_version()))
print("Connected")
########################################################################################################################
########################################################################################################################

########################################################################################################################
# Initial Setup
########################################################################################################################
update_TERMINALS()
runElements()
update_TERMINALS()
runElements()
update_TERMINALS()
'''
for e in circuitElements.keys():
    print(circuitElements[e].name)
    print(circuitElements[e].node)
'''
########################################################################################################################
########################################################################################################################


########################################################################################################################
#  Create HMI
########################################################################################################################
for index, element in enumerate(pinConfig.keys()):
    match element.split('_')[0]:
        case 'input':
            match circuitElements[element].node['pin']:
                case False:
                    INPUT_element[element] = Button(
                        root2,
                        image=off,
                        bd=0,
                        command=lambda elementID=element: set_INPUT(elementID)
                    )
                case True:
                    INPUT_element[element] = Button(
                        root2,
                        image=on,
                        bd=0,
                        command=lambda elementID=element: set_INPUT(elementID)
                    )
            INPUT_element[element].grid(row=index, column=0, sticky="E")
            INPUT_labels[element] = Label(root2, text=element, font=("Helvetica", 16))
            INPUT_labels[element].grid(row=index, column=0, sticky="W", ipadx=20)

            HardwarePriority[element] = StringVar(root2)
            HardwarePriority[element].set("SOFTWARE")

            print(element)
            INPUT_option[element] = OptionMenu(
                root2,
                HardwarePriority[element],
                *options,
                command=changePriority
            )
            print(element)
            INPUT_option[element].grid(row=index, column=1)

        case 'output':
            # print(element)
            match circuitElements[element].node['pin']:
                case False:
                    OUTPUT_element[element] = Label(root2, image=off_bulb)
                case True:
                    OUTPUT_element[element] = Label(root2, image=on_bulb)
            OUTPUT_element[element].grid(row=index, column=1, sticky="E")
            OUTPUT_label[element] = Label(root2, text=element, font=("Helvetica", 16))
            OUTPUT_label[element].grid(row=index, column=1)

    clock = Label(root2, font=('times', 12, 'bold'))
    # clock.grid(row=index+1, column=0)
########################################################################################################################
########################################################################################################################
voidMain()
########################################################################################################################
########################################################################################################################
it = util.Iterator(board)
it.start()
tick()
root2.mainloop()
