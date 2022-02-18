# Schwingungsanalyse
# #############################################################################

# This python script calculates the frequency of the occilation.

# Parts of this python script come from the following github-repository made by
# Christopher Mahn:
# https://github.com/c-mahn/test-sensor-data-analysis

# Authors:
# Joshua Wolf
# Silas Teske
# Lasse Zeh
# Christopher Mahn

# #############################################################################

# Import of Libraries
# -----------------------------------------------------------------------------

# import string as st
# import random as r
# import re
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import math as m
import sys
import os
from scipy.fft import fft, fftfreq
from scipy import signal


# -----------------------------------------------------------------------------
# Settings

verbose = True  # Shows more debugging information
fix_steigung = False  # Disregards permanent sensor changes
show_graphs = False  # If disabled, the Plots will not be shown.


# Functions
# -----------------------------------------------------------------------------

def run_analysis(input_file):
        
    if(verbose):
        print(14*"-", "BEGIN OF CALCULATION", 14*"-")
    
    # Einlesen der Daten
    if(verbose):
        print(f'[{1}/{3}] Einlesen von "{input_file}"', end="\r")
    with open(os.path.join("data", input_file), "r") as f:
        data = f.readlines()
    
    # Datenbereinigung
    if(verbose):
        print(f'[{2}/{3}] Einlesen von "{input_file}"', end="\r")
    for i, e in enumerate(data):
        data[i] = e.split(";")
        for j, e in enumerate(data[i]):
            data[i][j] = float(e.strip())

    # Umwandeln in Datenreihen
    if(verbose):
        print(f'[{3}/{3}] Einlesen von "{input_file}"', end="\r")
    datenreihen = [[], [], [], []]
    for i in data:
        datenreihen[0].append(i[0])
        datenreihen[1].append(i[1])
        datenreihen[2].append(i[2])
        datenreihen[3].append(i[3])
    datenreihen_ohne_zeit = datenreihen[1:4]
    if(verbose):
        print("")
    if(show_graphs):
        plot_xyzt(datenreihen_ohne_zeit, datenreihen[0], f'Messreihe "{input_file}"')
    
    # Berechnung der linearen Regression von Sensor 1
    x = np.array(datenreihen[0])
    y = np.array(datenreihen[1])
    steigung_1 = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    offset_1 = (np.sum(y) - steigung_1 *np.sum(x)) / len(x)
    if(verbose):
        print(f'[X] Trend: ({steigung_1:.10f})x + ({offset_1:+.6f})')
    
    # Berechnung der linearen Regression von Sensor 2
    x = np.array(datenreihen[0])
    y = np.array(datenreihen[2])
    steigung_2 = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    offset_2 = (np.sum(y) - steigung_2 *np.sum(x)) / len(x)
    if(verbose):
        print(f'[Y] Trend: ({steigung_2:.10f})x + ({offset_2:+.6f})')
    
    # Berechnung der linearen Regression von Sensor 3
    x = np.array(datenreihen[0])
    y = np.array(datenreihen[3])
    steigung_3 = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    offset_3 = (np.sum(y) - steigung_3 *np.sum(x)) / len(x)
    if(verbose):
        print(f'[Z] Trend: ({steigung_3:.10f})x + ({offset_3:+.6f})')

    # Erstellung Lineare Regression zum Plotten (Plot-Punkte)
    linearisierung = [[], [], []]
    for i in datenreihen[0]:
        linearisierung[0].append(i*steigung_1+offset_1)
        linearisierung[1].append(i*steigung_2+offset_2)
        linearisierung[2].append(i*steigung_3+offset_3)
    # Plot der linearen Regression
    if(show_graphs):
        plot_werte_t([datenreihen[1], linearisierung[0]], datenreihen[0], ["X", "Linearisierung"])
        plot_werte_t([datenreihen[2], linearisierung[1]], datenreihen[0], ["Y", "Linearisierung"])
        plot_werte_t([datenreihen[3], linearisierung[2]], datenreihen[0], ["Z", "Linearisierung"])

    # Wenn Steigung nicht bereinigt werden soll
    if(fix_steigung):
        steigung_1 = 0
        steigung_2 = 0
        steigung_3 = 0

    # Bereinigung des Trends aller Sensorreihen
    datenreihen_ohne_trend = [[], [], []]
    if(verbose):
        print(f"[{1}/{len(datenreihen_ohne_trend)}] Trendbereinigung", end="\r")
    for i, e in enumerate(datenreihen[1]):
        datenreihen_ohne_trend[0].append(e - (steigung_1*(datenreihen[0][i])+offset_1))
    if(verbose):
        print(f"[{2}/{len(datenreihen_ohne_trend)}] Trendbereinigung", end="\r")
    for i, e in enumerate(datenreihen[2]):
        datenreihen_ohne_trend[1].append(e - (steigung_2*(datenreihen[0][i])+offset_2))
    if(verbose):
        print(f"[{3}/{len(datenreihen_ohne_trend)}] Trendbereinigung", end="\r")
    for i, e in enumerate(datenreihen[3]):
        datenreihen_ohne_trend[2].append(e - (steigung_3*(datenreihen[0][i])+offset_3))
    if(verbose):
        print("")
    # Plot der vom Trend bereinigten Sensorreihen
    if(show_graphs):
        plot_xyzt(datenreihen_ohne_trend, datenreihen[0], f'Messreihe "{input_file}" (ohne Trend)')

    # Low-Pass-Filterung der Sensorreihen
    low_pass_strength = 3
    datenreihen_low_pass = []
    for i, e in enumerate(datenreihen_ohne_trend):
        if(verbose):
            print(f"[{i+1}/{len(datenreihen_ohne_trend)}] Low-Pass-Filterung (Strength {low_pass_strength})", end="\r")
        datenreihen_low_pass.append(low_pass_filter(e, low_pass_strength))
    if(verbose):
        print("")
    # Plot der low-pass Sensorreihen
    if(show_graphs):
        plot_xyzt(datenreihen_low_pass, datenreihen[0], f'Messreihe "{input_file}" (mit Low-Pass-Filter)')

    # Hoch-Pass-Filterung der Sensorreihen
    datenreihen_hoch_pass = [[], [], []]
    if(verbose):
        print(f"[{1}/{len(datenreihen_hoch_pass)}] Hoch-Pass-Filterung", end="\r")
    for i, e in enumerate(datenreihen_low_pass[0]):
        datenreihen_hoch_pass[0].append(datenreihen_ohne_trend[0][i] - e)
    if(verbose):
        print(f"[{2}/{len(datenreihen_hoch_pass)}] Hoch-Pass-Filterung", end="\r")
    for i, e in enumerate(datenreihen_low_pass[1]):
        datenreihen_hoch_pass[1].append(datenreihen_ohne_trend[1][i] - e)
    if(verbose):
        print(f"[{3}/{len(datenreihen_hoch_pass)}] Hoch-Pass-Filterung", end="\r")
    for i, e in enumerate(datenreihen_low_pass[2]):
        datenreihen_hoch_pass[2].append(datenreihen_ohne_trend[2][i] - e)
    if(verbose):
        print("")
    # Plot der hoch-pass Sensorreihen
    if(show_graphs):
        plot_xyzt(datenreihen_hoch_pass, datenreihen[0], f'Messreihe "{input_file}" (mit Hoch-Pass-Filter)')

    # Fourier-Transformation

    # Weitere Informationen:
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html
    sample_frequenz = datenreihen[0][2] - datenreihen[0][1]
    N = len(datenreihen[0])*2
    if(verbose):
        print(f"[{1}/{len(datenreihen_ohne_trend)}] Fast-Fourier-Transformation", end="\r")
    yf_1 = fft(datenreihen_low_pass[0])
    xf_1 = fftfreq(len(datenreihen_low_pass[0]), 1/sample_frequenz)
    if(verbose):
        print(f"[{2}/{len(datenreihen_ohne_trend)}] Fast-Fourier-Transformation", end="\r")
    yf_2 = fft(datenreihen_low_pass[1])
    xf_2 = fftfreq(len(datenreihen_low_pass[1]), 1/sample_frequenz)
    if(verbose):
        print(f"[{3}/{len(datenreihen_ohne_trend)}] Fast-Fourier-Transformation", end="\r")
    yf_3 = fft(datenreihen_low_pass[2])
    xf_3 = fftfreq(len(datenreihen_low_pass[2]), 1/sample_frequenz)
    if(verbose):
        print("")
    # Plot der Fourier-Transformation
    if(show_graphs):
        plt.plot(xf_1, 2.0/N * np.abs(yf_1[0:N//2]))
        # plt.xlim(0, 0.0001)
        plt.grid()
        plt.xlabel("Frequenz [s/Sample]")
        plt.ylabel("Amplitude [1]")
        plt.title("Fast-Fourier-Transformation (X-Achse)")
        plt.tight_layout()
        plt.show()

        plt.plot(xf_2, 2.0/N * np.abs(yf_2[0:N//2]))
        # plt.xlim(0, 0.0001)
        plt.grid()
        plt.xlabel("Frequenz [s/Sample]")
        plt.ylabel("Amplitude [1]")
        plt.title("Fast-Fourier-Transformation (Y-Achse)")
        plt.tight_layout()
        plt.show()

        plt.plot(xf_3, 2.0/N * np.abs(yf_3[0:N//2]))
        # plt.xlim(0, 0.0001)
        plt.grid()
        plt.xlabel("Frequenz [s/Sample]")
        plt.ylabel("Amplitude [1]")
        plt.title("Fast-Fourier-Transformation (Z-Achse)")
        plt.tight_layout()
        plt.show()
        
    if(verbose):
        print(15*"-", "END OF CALCULATION", 15*"-")


def plot_werte(datenreihen, name=["Messwerte"]):
    """
    Diese Funktion nimmt Datenreihen und plottet diese in ein Diagramm.
    """
    for i, datenreihe in enumerate(datenreihen):
        zeit = range(len(datenreihe))
        plt.plot(zeit, datenreihe)
    plt.legend(name)
    plt.grid()
    plt.xlabel("")
    plt.ylabel("")
    plt.title(name[0])
    plt.show()


def plot_werte_t(datenreihen, zeit, name=["Messwerte"]):
    """
    Diese Funktion plottet Werte an eine Zeitachse.

    Args:
        datenreihen ([type]): Datenreihen zum Plotten
        zeit ([type]): Eine Liste mit der Angabe der Zeitintervalle.
        name (list, optional): Angaben zur Beschriftung. Defaults to ["Messwerte"].
    """
    for i, datenreihe in enumerate(datenreihen):
        plt.plot(zeit, datenreihe)
    plt.legend(name)
    plt.grid()
    plt.xlabel("Zeit [s]")
    plt.ylabel("Koordinate [mm]")
    plt.title(name[0])
    plt.tight_layout()
    plt.show()


def plot_xyzt(datenreihen, zeit, name="Messwerte"):
    """
    Diese Funktion nimmt genau drei Datenreihen und plottet diese in ein Diagramm.

    Args:
        datenreihen ([list]): Drei Datenreihen zum Plotten.
        zeit ([list]): Eine Liste mit der Angabe der Zeitintervalle.
        name (list, optional): Dies ist der Titel. Defaults to "Messwerte".
    """
    for i, datenreihe in enumerate(datenreihen):
        plt.plot(zeit, datenreihe)
    plt.legend(["x", "y", "z"])
    plt.grid()
    plt.xlabel("Zeit [s]")
    plt.ylabel("Koordinate [mm]")
    plt.title(name)
    plt.tight_layout()
    plt.show()


def plot_xy(datenreihen, name=["Messwerte"]):
    """
    Diese Funktion nimmt je zwei Datenreihen und plottet diese in Abhängigkeit
    zueinander in ein Diagramm.
    """
    for i, datenreihe in enumerate(datenreihen):
        plt.plot(datenreihe[0], datenreihe[1])
    plt.legend(name)
    plt.grid()
    plt.xlabel("Y")
    plt.ylabel("X")
    plt.title(name[0])
    plt.show()


def fill_nan(A):
    '''
    interpolate to fill nan values
    '''
    inds = np.arange(A.shape[0])
    good = np.where(np.isfinite(A))
    f = interpolate.interp1d(inds[good], A[good],bounds_error=False)
    B = np.where(np.isfinite(A),A,f(inds))
    return B


def low_pass_filter(datenreihe, filterungsgrad):
    """
    Diese Funktion macht einen vereinfachten Low-Pass-Filter, indem die letzten
    x Sensorwerte gemittelt werden.
    """
    ausgabe = []
    for i, e in enumerate(datenreihe):
        divisor = filterungsgrad
        summe = 0
        for j in range(filterungsgrad):
            ji = i-j
            if(ji < 0):  # Wenn Wert ausserhalb der Datenreihe, ändern des Divisors
                divisor = divisor - 1
            else:
                summe = summe + float(datenreihe[ji])
        temp = summe/divisor
        ausgabe.append(temp)
    return(ausgabe)


def cross_correlation(x_red, y_red):
        Nx = len(x_red)
        if Nx != len(y_red):
            raise ValueError('x and y must be equal length')
        c = np.correlate(x_red, y_red, mode=2)
        c /= np.sqrt(np.dot(x_red, x_red) * np.dot(y_red, y_red))
        maxlags = Nx - 1
        if maxlags >= Nx or maxlags < 1:
            raise ValueError('maglags must be None or strictly '
                             'positive < %d' % Nx)
        lags = np.arange(-maxlags, maxlags + 1)
        c = c[Nx - 1 - maxlags:Nx + maxlags]
        return lags, c


# Classes
# -----------------------------------------------------------------------------


# Beginning of the Programm
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    print("Running schwingungsanalyse_main.py...")
    
    for i in range(4):
        i += 1
        run_analysis(f"Schwingungsanalyse_{i:02d}.txt")
