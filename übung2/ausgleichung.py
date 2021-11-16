# Ausgleichung
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
    
    # Import der x-Vektor Punktbeschreibung
    file = open(os.path.join("data","punktnummern.txt"))
    data = file.readlines()
    file.close()
    for i, e in enumerate(data):
        data[i] = e.strip()
    
    # Aufstellen des x-Vektors
    x_vektor = []
    for i in data:
        x_vektor.append([i])
    x_vektor = np.array(x_vektor)
    if(verbose):
        print(f"x_vektor:\n{x_vektor}\n")
    
    # Import der Messwerte des Höhennetzes
    file = open(os.path.join("data","messungen.txt"))
    data = file.readlines()
    file.close()
    for i, e in enumerate(data):
        data[i] = e.strip().split(";")

    # Aufstellen des Beobachtungsvektors
    l_vektor = []
    for i in data:
        l_vektor.append([float(i[0])])
    l_vektor = np.array(l_vektor)
    if(verbose):
        print(f"l_vektor:\n{l_vektor}\n")

    # Aufstellen der A-Matrix
    a_matrix = np.zeros([len(l_vektor), len(x_vektor)])
    for i, e in enumerate(data):
        a_matrix[i][int(e[1])] = 1
        if(int(e[2]) != -1):
            a_matrix[i][int(e[2])] = -1
    if(verbose):
        print(f"a_matrix:\n{a_matrix}\n")

    # Berechnung der Redundanz
    redundanz = len(l_vektor)-len(x_vektor)
    if(verbose):
        print(f"redundanz:\n{redundanz}\n")

    x_vektor_berechnet = np.linalg.inv(np.transpose(a_matrix)@a_matrix)@np.transpose(a_matrix)@l_vektor
    if(verbose):
        print(f"x_vektor_berechnet:\n{x_vektor_berechnet}\n")
