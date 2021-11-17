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
    file = open(os.path.join("data","nivel_2.txt"))
    data = file.readlines()
    file.close()
    for i, e in enumerate(data):
        data[i] = e.strip().split(";")

    # Erstellung der Vektoren
    x_werte = []
    for i in data:
        x_werte.append([float(i[0])])
    x_werte = np.array(x_werte)
    if(verbose):
        print(f"x_werte:\n{x_werte}\n")
    
    y_werte = []
    for i in data:
        y_werte.append([float(i[1])])
    y_werte = np.array(y_werte)
    if(verbose):
        print(f"y_werte:\n{y_werte}\n")
    
    # Berechnung der Höhenunterschiede
    deltah_vektor = []
    for i in range(49):
        if i % 7 == 6:
            continue
        else:
            wert = np.sin(x_werte[i]/1000)*0.15
            deltah_vektor.append([float(wert)])

    for i in range(49):
        if i % 7 == 6:
            continue
        else:
            wert = np.sin(y_werte[i]/1000)*0.15
            deltah_vektor.append([float(wert)])
    deltah_vektor = np.array(deltah_vektor)
    if(verbose):
        print(f"h_vektor:\n{deltah_vektor}\n")

    # Export
    file = open(os.path.join("data","exportneig.txt"),f"w")
    for i in deltah_vektor:
        i = float(i[0])
        file.writelines(f"{i:+.8f}\n")
    file.close()
