# Umrechnen von mrad in m
# #############################################################################

# Authors:
# Joshua Wolf
# Silas Teske
# Lasse Zeh
# Christopher Mahn

# #############################################################################

# Import of Libraries
# -----------------------------------------------------------------------------

# import math as m
# import string as st
# import random as r
import numpy as np
import os


# -----------------------------------------------------------------------------
# Debugging-Settings

verbose = True  # Shows more debugging information


# Functions
# -----------------------------------------------------------------------------


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
 
    # Import der Messwerte des Neigungssensors
    file = open(os.path.join("data","imu_data.txt"))
    data = file.readlines()
    file.close()
    for i, e in enumerate(data):
        if(e[0] != "#"):
            data[i] = e.strip().split(" ")

    # Convert strings to numbers
    markers = []
    for i in data:
        if(i[0] != "0000"):
            markers.append(i)

    # Export
    file = open(os.path.join("data","imu_data_converted.txt"),f"w")
    for i in markers:
        file.writelines(f"i\n")
    file.close()
