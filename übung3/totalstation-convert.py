# Parsen und konvertieren von Tachymeter-Daten
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

verbose = False  # Shows more debugging information


# Functions
# -----------------------------------------------------------------------------


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    print("Running totalstation-convert.py...")

    # Import der Messwerte des Tachymeters
    file = open(os.path.join("data","totalstation_data.txt"))
    totalstation_data = file.readlines()
    file.close()
    totalstation_data.pop(0)
    for i, e in enumerate(totalstation_data):
        totalstation_data[i] = e.strip().split(";")
        temp = []
        for j, f in enumerate(totalstation_data[i]):
            if(j == 0 or j == 2):
                temp.append(int(f))
            elif(j != 1):
                temp.append(float(f))
            else:
                temp.append(f)
        totalstation_data[i] = temp

    for i, e in enumerate(totalstation_data):
        totalstation_data[i][3] = e[3] /200*np.pi
        totalstation_data[i][4] = e[4] /200*np.pi

    # Export
    file = open(os.path.join("data","totalstation_data_converted.txt"),f"w")
    for i in totalstation_data:
        for j, e in enumerate(i):
            if(j == 0):
                file.writelines(f"{e}")
            else:
                file.writelines(f"; {e}")
        file.writelines(f"\n")
    file.close()
