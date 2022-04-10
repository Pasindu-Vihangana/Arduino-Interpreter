import pickle
import re

from tkinter import *
from tkinter import filedialog

from functools import partial


# GUI #
########################################################################################################################
# Create Object
root2 = Tk()

# Set Title
root2.title('CIRCUIT EMULATOR')

# Add Geometry
root2.geometry("640x480")
root2.columnconfigure([0, 1], minsize=300, pad=20)
root2.rowconfigure([0, 5], minsize=50, pad=20)
########################################################################################################################

########################################################################################################################
# Define Images
on = PhotoImage(file="./images/ON.png")
off = PhotoImage(file="./images/OFF.png")
on_bulb = PhotoImage(file="./images/ON_light.png")
off_bulb = PhotoImage(file="./images/OFF_light.png")
########################################################################################################################

INPUT_element = {}
INPUT_labels = {}
OUTPUT_element = {}
OUTPUT_label = {}

########################################################################################################################
########################################################################################################################
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

circuitElements = pinConfig | logicElements
print(circuitElements)
print(wiring)


########################################################################################################################
########################################################################################################################
def runElements():
    global circuitElements
    print("########################################################")
    for e in circuitElements.keys():
        circuitElements[e].process()
        print(circuitElements[e].name)
        print(circuitElements[e].node)
    print("########################################################")
########################################################################################################################
########################################################################################################################


########################################################################################################################
#   #  CREATE ELEMENTS  #   #
########################################################################################################################
for index, element in enumerate(pinConfig.keys()):
    match element.split('_')[0]:
        case 'input':
            # print(element)
            match circuitElements[element].node['pin']:
                case False:
                    INPUT_element[element] = Button(
                        root2,
                        image=off,
                        bd=0,
                        command=lambda elementID=element: update_INPUT(elementID)
                    )
                case True:
                    INPUT_element[element] = Button(
                        root2,
                        image=on,
                        bd=0,
                        command=lambda elementID=element: update_INPUT(elementID)
                    )
            INPUT_element[element].grid(row=index, column=0, sticky="E")
            INPUT_labels[element] = Label(root2, text=element, font=("Helvetica", 16))
            INPUT_labels[element].grid(row=index, column=0, sticky="W", ipadx=20)

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
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def update_INPUT(element_ID):
    global circuitElements
    if circuitElements[element_ID].value:
        INPUT_element[element_ID].config(image=off)
        circuitElements[element_ID].node['pin'] = False
        circuitElements[element_ID].value = False
    else:
        INPUT_element[element_ID].config(image=on)
        circuitElements[element_ID].node['pin'] = True
        circuitElements[element_ID].value = True

    clock()


########################################################################################################################
########################################################################################################################
def clock():
    global circuitElements
    update_TERMINALS()
    runElements()
    update_TERMINALS()
    runElements()
    for e in circuitElements.keys():
        print(circuitElements[e].name)
        print(circuitElements[e].node)
    update_OUTPUT()

########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def update_TERMINALS():
    global circuitElements
    print("########################################################")
    for i in range(2):
        for wires in range(len(wiring)):
            receiver = wiring[wires][1].split('.')[0]
            receiver_T = wiring[wires][1].split('.')[1]
            sender = wiring[wires][0].split('.')[0]
            print(receiver + " @ " + receiver_T + " = " + sender)

            # Critical # DO NOT CHANGE without AUTHORIZATION # Critical #
            circuitElements[receiver].node.update({receiver_T: circuitElements[sender].out()})
            circuitElements[receiver].value = circuitElements[sender].out()

        print("########################################################")
########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
def update_OUTPUT():
    # print("output(s) updated")
    global circuitElements
    for keys in pinConfig.keys():
        if keys.split('_')[0] == 'output':
            print(circuitElements[keys].node)
            match circuitElements[keys].out():
                case False:
                    OUTPUT_element[keys].config(image=off_bulb)
                case True:
                    OUTPUT_element[keys].config(image=on_bulb)
########################################################################################################################
########################################################################################################################


root2.mainloop()
