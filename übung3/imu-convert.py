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
        data[i] = e.strip().split(" ")



    # Export
    file = open(os.path.join("data","imu_data_converted.txt"),f"w")
    for i in 5:
        file.writelines(f"hello\n")
    file.close()
