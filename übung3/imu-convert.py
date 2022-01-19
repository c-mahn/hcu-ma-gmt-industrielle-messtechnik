# Parsen und konvertieren von IMU-Daten
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
    
    # Select active lines
    data_split = []
    for i, e in enumerate(data):
        if(e[0] != "#"):
            data_split.append(e.strip().split(" "))

    # Select only marked lines
    raw_markers = []
    for i in data_split:
        if(i[0] != "0000"):
            raw_markers.append(i)

    # Convert lines in float-lists
    markers = []
    for i, e in enumerate(raw_markers):
        markers.append([])
        for j in e:
            if(j != ""):  # Skip empty strings
                markers[i].append(float(j))

    # Convert units
    for i, e in enumerate(markers):
        if(len(e) == 12):
            markers[i][0] = int(e[0]) # marker-id to integer
            markers[i][1] = e[1]
            markers[i][2] = e[2] /180*np.pi  # convert °/s to rad/s
            markers[i][3] = e[3] /180*np.pi  # convert °/s to rad/s
            markers[i][4] = e[4] /180*np.pi  # convert °/s to rad/s
            markers[i][5] = e[5]
            markers[i][6] = e[6]
            markers[i][7] = e[7]
            markers[i][8] = e[8] /180*np.pi  # convert ° to s
            markers[i][9] = e[9] /180*np.pi  # convert ° to s
            markers[i][10] = e[10] /180*np.pi  # convert ° to s
            markers[i][11] = e[11] -273.15  # convert °K to °C

    # Export
    file = open(os.path.join("data","imu_data_converted.txt"),f"w")
    for i in markers:
        for j in i:
            file.writelines(f"{j}; ")
        file.writelines(f"\b\b\n")
    file.close()
