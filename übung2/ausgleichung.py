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

verbose = False  # Shows more debugging information


# Functions
# -----------------------------------------------------------------------------


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    
    # Aufstellen des x-Vektors
    x_vektor = np.array([["h2"],
                         ["h3"],
                         ["h4"],
                         ["h6"]])

    # Aufstellen des Beobachtungsvektors
    l_vektor = np.array([[h_12],
                         [h_23],
                         [h_34],
                         [h_45],
                         [h_15]])
    if(verbose):
        print(f"l_vektor:\n{l_vektor}\n")

    # Aufstellen der A-Matrix
    a_matrix = np.zeros([len(l_vektor), len(x_vektor)])
    a_matrix[0][0] = 1
    a_matrix[1][0] = -1
    a_matrix[1][1] = 1
    a_matrix[2][1] = -1
    a_matrix[2][2] = 1
    a_matrix[3][2] = -1
    a_matrix[3][3] = 1
    a_matrix[4][3] = 1
    if(verbose):
        print(f"a_matrix:\n{a_matrix}\n")
    
    
    