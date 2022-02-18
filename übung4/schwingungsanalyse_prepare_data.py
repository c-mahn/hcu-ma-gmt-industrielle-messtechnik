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

def convert_data(input_filename, output_filename, Hz):
    """
    This function converts files formating for later use.

    Args:
        input_filename ([string]): [Defines the filename the data is in]
        output_filename ([string]): [Defines the filename for saving the data]
        Hz ([int]): [describes the datarate, by with the first line will be
                    calculated]
    """
    
    # Import der Messwerte
    file = open(os.path.join("data", input_filename))
    data = file.readlines()
    file.close()
    data.pop(0)
    for i, e in enumerate(data):
        if(verbose):
            print(f"[{i+1}/{len(data)}] Import", end="\r")
        if(e[0] != "/"):
            data[i] = e.strip().split(",")
            temp = []
            for j, f in enumerate(data[i]):
                if(j == 0):
                    temp.append(int(f)/int(Hz))  # Berechnung der Timestamps
                else:
                    temp.append(float(f))
            data[i] = temp

    # Export der konvertierten Messwerte
    file = open(os.path.join("data", output_filename),f"w")
    for i, e in enumerate(data):
        if(verbose):
            print(f"[{i+1}/{len(data)}] Export", end="\r")
        for j, f in enumerate(e):
            if(j == 0):
                file.writelines(f"{f}")
            else:
                file.writelines(f"; {f}")
        file.writelines(f"\n")
    file.close()
    if(verbose):
        print(f"[{i+1}/{len(data)}] Done  ")


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    print("Running schwingungsanalyse_prepare_data.py...")
    
    convert_data("Schwingungsanalyse_50Hz_PtoP_0.1.txt", "Schwingungsanalyse_01.txt", 50)
    convert_data("Schwingungsanalyse_100Hz_PtoP_0.1.txt", "Schwingungsanalyse_02.txt", 100)
    convert_data("Schwingungsanalyse_100Hz_PtoP_0.5.txt", "Schwingungsanalyse_03.txt", 100)
    convert_data("Schwingungsanalyse_100Hz_PtoP_1.0.txt", "Schwingungsanalyse_04.txt", 100)
    # convert_data("Schwingungsanalyse_Cloud_PtoP-0.5_LtoL-0.5.txt", "Schwingungsanalyse_05.txt", 1)
    # convert_data("Schwingungsanalyse_Cloud_PtoP-2.0_LtoL-2.0.txt", "Schwingungsanalyse_06.txt", 1)
    # convert_data("Schwingungsanalyse_Cloud_PtoP-5.0_LtoL-5.0.txt", "Schwingungsanalyse_07.txt", 1)
