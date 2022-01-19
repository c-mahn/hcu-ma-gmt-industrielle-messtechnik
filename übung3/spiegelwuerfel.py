# Überprürfung der Rechtwinkligkeit
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
    file = open(os.path.join("data","imu_data_converted.txt"))
    imu_data = file.readlines()
    file.close()
    for i, e in enumerate(imu_data):
        imu_data[i] = e.strip().split(";")
        temp = []
        for j in imu_data[i]:
            temp.append(float(j))
        imu_data[i] = temp

    # Import der Messwerte des Tachymeters
    file = open(os.path.join("data","messwerte_ts60.csv"))
    totalstation_data = file.readlines()
    file.close()
    totalstation_data.pop(0)
    for i, e in enumerate(totalstation_data):
        totalstation_data[i] = e.strip().split(";")
        temp = []
        for j, f in enumerate(totalstation_data[i]):
            if(j != 1):
                temp.append(float(f))
            else:
                temp.append(f)
        totalstation_data[i] = temp

    for i in imu_data:
        print(f"{i[8]}, {i[9]}, {i[10]}")