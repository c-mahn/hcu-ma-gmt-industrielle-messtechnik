# Schwingungsanalyse
# #############################################################################

# This python script prepares the data for the main python script for
# calculation of the frequencies of the occilations.

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
# import re
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
    print("Runnung schwingungsanalyse_prepare_data.py...")

    # Import der Messwerte von "Schwingungsanalyse_50Hz_PtoP_0.1.txt"
    file = open(os.path.join("data","Schwingungsanalyse_50Hz_PtoP_0.1.txt"))
    data = file.readlines()
    file.close()
    data.pop(0)
    for i, e in enumerate(data):
        data[i] = e.strip().split(",")
        temp = []
        for j, f in enumerate(data[i]):
            if(j == 0):
                temp.append(int(f))
            else:
                temp.append(float(f))
        data[i] = temp

    # Export der konvertierten Messwerte von "Schwingungsanalyse_50Hz_PtoP_0.1.txt"
    file = open(os.path.join("data","totalstation_data_converted.txt"),f"w")
    for i in totalstation_data:
        for j, e in enumerate(i):
            if(j == 0):
                file.writelines(f"{e}")
            else:
                file.writelines(f"; {e}")
        file.writelines(f"\n")
    file.close()
