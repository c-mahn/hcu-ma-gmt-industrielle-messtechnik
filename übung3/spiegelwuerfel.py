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
    file = open(os.path.join("data","totalstation_data_converted.txt"))
    totalstation_data = file.readlines()
    file.close()
    for i, e in enumerate(totalstation_data):
        totalstation_data[i] = e.strip().split(";")
        temp = []
        for j, f in enumerate(totalstation_data[i]):
            if(j != 1):
                temp.append(float(f))
            else:
                temp.append(f)
        totalstation_data[i] = temp

    # Berechnung der Orientierung der IMU
    pos1IMU = []
    pos1IMU.append(np.average([imu_data[0][8], imu_data[1][8], imu_data[2][8]]))
    pos1IMU.append(np.average([imu_data[0][9], imu_data[1][9], imu_data[2][9]]))
    pos1IMU.append(np.average([imu_data[0][10], imu_data[1][10], imu_data[2][10]]))

    pos2IMU = []
    pos2IMU.append(np.average([imu_data[7][8], imu_data[8][8], imu_data[9][8]]))
    pos2IMU.append(np.average([imu_data[7][9], imu_data[8][9], imu_data[9][9]]))
    pos2IMU.append(np.average([imu_data[7][10], imu_data[8][10], imu_data[9][10]]))

    meas_imu1 = []
    meas_imu1.append(np.average([totalstation_data[1][3],totalstation_data[3][3],totalstation_data[5][3]]))
    meas_imu1.append(np.average([totalstation_data[1][4],totalstation_data[3][4],totalstation_data[5][4]]))

    meas_imu2 = []
    meas_imu2.append(np.average([totalstation_data[7][3],totalstation_data[9][3],totalstation_data[11][3]]))
    meas_imu2.append(np.average([totalstation_data[7][4],totalstation_data[9][4],totalstation_data[1][4]]))





    pos1totalstation = []

    print(pos1IMU, pos2IMU, meas_imu1, meas_imu2)