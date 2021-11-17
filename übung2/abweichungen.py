# Abweichungen vom Mittel
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
 
    # Import der Ausgeglichenen Höhen einer Messreihe
    file = open(os.path.join("data","export_nivel_2.txt"))
    data = file.readlines()
    file.close()
    for i, e in enumerate(data):
        data[i] = e.strip().split(";")

    # Erstellung der Vektoren
    a_werte = []
    for i in data:
        a_werte.append([float(i[0])])
    a_werte = np.array(a_werte)
    if(verbose):
        print(f"a_werte:\n{a_werte}\n")

    # Import der Ausgeglichenen Höhen aller Messreihen
    file = open(os.path.join("data","export_all.txt"))
    data = file.readlines()
    file.close()
    for i, e in enumerate(data):
        data[i] = e.strip().split(";")
    # Erstellung der Vektoren
    b_werte = []
    for i in data:
        b_werte.append([float(i[0])])
    b_werte = np.array(b_werte)
    if(verbose):
        print(f"b_werte:\n{b_werte}\n")

    abw = []
    for i in range(49):
        wert = b_werte[i] - a_werte[i]
        abw.append(wert)
        print(f"Abweichung:\n{wert}\n")
    abw = np.array(abw)

    # Export
    file = open(os.path.join("data","exportabw.txt"),f"w")
    for i in abw:
        i = float(i)
        file.writelines(f"{i:+.6f}\n")
    file.close()