# Standardabweichungen
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
 
    # Import der Ausgeglichenen Höhen
    file = open(os.path.join("data","export_dini.txt"))
    data = file.readlines()
    file.close()
    for i, e in enumerate(data):
        data[i] = e.strip().split(";")

    # 
    a_werte = []
    for i in data:
        a_werte.append([float(i[0])])
    a_werte = np.array(a_werte)
    if(verbose):
        print(f"a_werte:\n{a_werte}\n")

    # Import der Ausgeglichenen Höhen All
    file = open(os.path.join("data","export_all.txt"))
    data = file.readlines()
    file.close()
    for i, e in enumerate(data):
        data[i] = e.strip().split(";")
    # 
    b_werte = []
    for i in data:
        b_werte.append([float(i[0])])
    b_werte = np.array(b_werte)
    if(verbose):
        print(f"b_werte:\n{b_werte}\n")

    abw = []
    for i in range(49):
        wert = b_werte[i] - a_werte[i]
        abw.append(float(i))
        print(f"Abweichung:\n{wert}\n")
    