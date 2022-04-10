import pickle
import os
import re

from tkinter import *
from tkinter import filedialog

import serial.tools.list_ports

import component
# from gatelogic import *


# GUI #
###################################################
configWindow = Tk()
configWindow.title('I/O CONFIG')

'''
# Add Geometry
configWindow.geometry("640x480")
configWindow.columnconfigure([0, 1], minsize=300, pad=20)
configWindow.rowconfigure([0, 5], minsize=50, pad=20)
'''
###################################################


###################################################
###################################################
def search_file():
    currdir = os.getcwd()
    file_path = filedialog.askopenfilename(parent=configWindow, initialdir=currdir, title='Please select the .pkl file')
    fname = file_path.split("/")
    return file_path, fname[-1]
###################################################
###################################################


###################################################
###################################################
def serial_ports():
    return serial.tools.list_ports.comports()


def select_PORT():
    global PORT
    PORT = StringVar(configWindow)
    try:
        PORT.set(serial_ports()[0])
    except:
        PORT.set(serial_ports("N/A"))

    PORT_label = Label(configWindow, text="COM PORT" + " : ", font=("Helvetica", 12))
    PORT_label.grid(row=0, column=2, sticky="E", ipadx=20)

    port_drop = OptionMenu(configWindow, PORT, *serial_ports())
    port_drop.grid(row=0, column=3, sticky="E")
###################################################
###################################################


###################################################
###################################################
def define_pins():
    global configWindow, INPUT_label, drop, _pins, pin_config
    count = 0

    for device in range(len(data[0])):
        if re.search('input_.+', data[0][device][1]):
            pin_config.append(IntVar(configWindow))
            pin_config[count].set(_pins[count])

            INPUT_label.append(Label(configWindow, text=data[0][device][1] + " : ", font=("Helvetica", 12)))
            INPUT_label[count].grid(row=count+1, column=0, sticky="E", ipadx=20)

            drop.append(OptionMenu(configWindow, pin_config[count], *_pins))
            drop[count].grid(row=count+1, column=1, sticky="E")

            # pin_out[IO_file[line][0]] = nano.digital[pin_config[count].get()]
            # pin_out.get(IO_file[line][0]).mode = pyfirmata.INPUT

            count += 1

        if re.search('output_.+', data[0][device][1]):
            pin_config.append(IntVar(configWindow))
            pin_config[count].set(_pins[count])

            INPUT_label.append(Label(configWindow, text=data[0][device][1] + " : ", font=("Helvetica", 12)))
            INPUT_label[count].grid(row=count+1, column=0, sticky="E", ipadx=20)

            drop.append(OptionMenu(configWindow, pin_config[count], *_pins))
            drop[count].grid(row=count+1, column=1, sticky="E")

            # pin_out[IO_file[line][0]] = nano.digital[pin_config[count].get()]
            # pin_out.get(IO_file[line][0]).mode = pyfirmata.OUTPUT

            count += 1

    select_PORT()

    button_def = Button(configWindow, text="Run Config", command=hardware_config)
    button_def.grid(row=count+1, column=3, sticky="E", ipadx=2, ipady=2, padx=10, pady=10)
###################################################
###################################################


###################################################
###################################################
def connectElements():
    for wires in range(len(data[1])):
        wiring.append(
            (
                (data[1][wires][1][0] + "." + data[1][wires][1][1]),
                (data[1][wires][1][2] + "." + data[1][wires][1][3])
            )
        )
###################################################
###################################################


###################################################
###################################################
def parametricSequence(comp, ID):
    elements = comp
    deviceID = ID
    print("Parametric Sequencing for " + deviceID)
    deviceParameters = []
    for connection in range(len(elements)):
        if elements[connection][1][0] is deviceID:
            deviceParameters.append(elements[connection][1][1])
        if elements[connection][1][2] is deviceID:
            deviceParameters.append(elements[connection][1][3])

    # print(deviceParameters)
    return deviceParameters
###################################################
###################################################


###################################################
###################################################
def hardware_config():
    count = 0

    for device in range(len(data[0])):
        if re.search('input_.+', data[0][device][1]):
            pins[data[0][device][1]] = component.D_PIN(data[0][device][1])
            pins[data[0][device][1]].digitalAddress = pin_config[count].get()
            print(pins[data[0][device][1]].name + ": "
                  + str(pins[data[0][device][1]].digitalAddress))
            # pin_out[IO_file[line][0]] = nano.digital[pin_config[count].get()]
            # pin_out.get(IO_file[line][0]).mode = pyfirmata.INPUT
            count += 1

        elif re.search('output_.+', data[0][device][1]):
            pins[data[0][device][1]] = component.D_PIN(data[0][device][1])
            pins[data[0][device][1]].digitalAddress = pin_config[count].get()
            '''
            print(pins[data[0][device][1]].name + ": "
                  + str(pins[data[0][device][1]].digitalAddress))
            '''
            # pin_out[IO_file[line][0]] = nano.digital[pin_config[count].get()]
            # pin_out.get(IO_file[line][0]).mode = pyfirmata.OUTPUT
            count += 1

        else:
            # parametricSequence(data[0][device][1])
            logicElements[data[0][device][1]] = component.deviceBuild(
                data[0][device][1],
                parametricSequence(data[1], data[0][device][1])
            )
            # print(parametricSequence(data[0][device][1]))

            print(logicElements[data[0][device][1]].node)

    COM_PORT = PORT.get().split(' ')[0]

    connectElements()

    ############################################
    #       # VARIABLES VISUALISATION #        #
    ############################################
    print(COM_PORT)

    for elements in logicElements.keys():
        # print(logicElements[elements].name)
        for nodes in logicElements[elements].node.keys():
            print(logicElements[elements].name + "." + nodes)
    
    for pin in pins.keys():
        print(pins[pin].name + "." + pins[pin].type)

    for i in range(len(wiring)):
        print(wiring[i])
    ############################################
    ############################################

    os.makedirs(os.path.dirname("bin/pins.pkl"), exist_ok=True)
    with open("bin/pins.pkl", "wb") as pinFile:
        pickle.dump(pins, pinFile)
        pinFile.close()

    os.makedirs(os.path.dirname("bin/logicElements.pkl"), exist_ok=True)
    with open("bin/logicElements.pkl", "wb") as logicElementsFile:
        pickle.dump(logicElements, logicElementsFile)
        logicElementsFile.close()

    os.makedirs(os.path.dirname("bin/wiring.pkl"), exist_ok=True)
    with open("bin/wiring.pkl", "wb") as wiringFile:
        pickle.dump(wiring, wiringFile)
        wiringFile.close()

    configWindow.destroy()
###################################################
###################################################


###################################################
###################################################
INPUT_label = []
drop = []
pin_config = []
logicElements = {}
wiring = []
pins = {}
PORT = ''

# for Arduino Uno
_pins = [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13
]

# Load Binary Schematic #
try:
    path, filename = search_file()
    with open(path, "rb") as file:
        data = pickle.load(file)
        file.close()

    '''
    for device in range(len(data[0])):
        print(data[0][device][1])

    for connections in range(len(data[1])):
        print(data[1][connections][1])
    '''

except FileNotFoundError:
    print("No file selected!")

define_pins()
configWindow.mainloop()
