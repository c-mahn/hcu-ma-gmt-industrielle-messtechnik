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

verbose = False  # Shows more debugging information
fix_steigung = True # Disregards permanent sensor changes


# Functions
# -----------------------------------------------------------------------------

def run_analysis(input_file):
    

    # Einlesen der Daten
    print(f"[{1}/{1}] Einlesen der Daten...", end="\r")
    with open(os.path.join("data", input_file), "r") as f:
        data = f.readlines()
    print("")
    
    # Datenbereinigung
    print(f"[{1}/{1}] Datenbereinigung...", end="\r")
    for i, e in enumerate(data):
        data[i] = e.split(";")
        for j, e in enumerate(data[i]):
            data[i][j] = float(e.strip())
    print("")

    # Umwandeln in Datenreihen
    print(f"[{1}/{1}] Datenkonvertierung...", end="\r")
    datenreihen = [[], [], [], []]
    for i in data:
        datenreihen[0].append(i[0])
        datenreihen[1].append(i[1])
        datenreihen[2].append(i[2])
        datenreihen[3].append(i[3])
    datenreihen_ohne_zeit = datenreihen[1:4]
    print("")
    plot_werte(datenreihen_ohne_zeit, ["Sensor 1", "Sensor 2", "Sensor 3"])
    
    # Berechnung der linearen Regression von Sensor 1
    x = np.array(datenreihen[0])
    y = np.array(datenreihen[1])
    steigung_1 = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    offset_1 = (np.sum(y) - steigung_1 *np.sum(x)) / len(x)
    print(f'[Sensor 1] Trend: ({steigung_1:.10f})x + ({offset_1:+.6f})')
    
    # Berechnung der linearen Regression von Sensor 2
    x = np.array(datenreihen[0])
    y = np.array(datenreihen[2])
    steigung_2 = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    offset_2 = (np.sum(y) - steigung_2 *np.sum(x)) / len(x)
    print(f'[Sensor 2] Trend: ({steigung_2:.10f})x + ({offset_2:+.6f})')
    
    # Berechnung der linearen Regression von Sensor 3
    x = np.array(datenreihen[0])
    y = np.array(datenreihen[3])
    steigung_3 = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    offset_3 = (np.sum(y) - steigung_3 *np.sum(x)) / len(x)
    print(f'[Sensor 2] Trend: ({steigung_3:.10f})x + ({offset_3:+.6f})')

    # Erstellung Lineare Regression zum Plotten (Plot-Punkte)
    linearisierung = [[], [], []]
    for i in datenreihen[0]:
        linearisierung[0].append(i*steigung_1+offset_1)
        linearisierung[1].append(i*steigung_2+offset_2)
        linearisierung[2].append(i*steigung_3+offset_3)
    # Plot der linearen Regression
    plot_werte([datenreihen[1], linearisierung[0]], ["Sensor 1", "Linearisierung"])
    plot_werte([datenreihen[2], linearisierung[1]], ["Sensor 2", "Linearisierung"])
    plot_werte([datenreihen[3], linearisierung[2]], ["Sensor 3", "Linearisierung"])

    # Wenn Steigung nicht bereinigt werden soll
    if(fix_steigung):
        steigung_1 = 0
        steigung_2 = 0
        steigung_3 = 0

    # Bereinigung des Trends aller Sensorreihen
    datenreihen_ohne_trend = [[], [], []]
    print(f"[{1}/{len(datenreihen_ohne_trend)}] Bereinigung des Trends...", end="\r")
    for i, e in enumerate(datenreihen[1]):
        datenreihen_ohne_trend[0].append(e - (steigung_1*(datenreihen[0][i])+offset_1))
    print(f"[{2}/{len(datenreihen_ohne_trend)}] Bereinigung des Trends...", end="\r")
    for i, e in enumerate(datenreihen[2]):
        datenreihen_ohne_trend[1].append(e - (steigung_2*(datenreihen[0][i])+offset_2))
    print(f"[{3}/{len(datenreihen_ohne_trend)}] Bereinigung des Trends...", end="\r")
    for i, e in enumerate(datenreihen[3]):
        datenreihen_ohne_trend[2].append(e - (steigung_3*(datenreihen[0][i])+offset_3))
    print("")
    # Plot der vom Trend bereinigten Sensorreihen
    plot_werte(datenreihen_ohne_trend, ["Sensor 1 (ohne Trend)", "Sensor 2 (ohne Trend)", "Sensor 3 (ohne Trend)"])

    # Low-Pass-Filterung der Sensorreihen
    low_pass_strength = 500
    datenreihen_low_pass = []
    for i, e in enumerate(datenreihen_ohne_trend):
        print(f"[{i+1}/{len(datenreihen_ohne_trend)}] Low-Pass-Filterung (Strength {low_pass_strength})...", end="\r")
        datenreihen_low_pass.append(low_pass_filter(e, low_pass_strength))
    print("")
    # Plot der low-pass Sensorreihen
    plot_werte(datenreihen_low_pass, ["Sensor 1 (mit Low-Pass-Filter)", "Sensor 2 (mit Low-Pass-Filter)", "Sensor 3 (mit Low-Pass-Filter)"])

    # Hoch-Pass-Filterung der Sensorreihen
    datenreihen_hoch_pass = [[], [], []]
    print(f"[{1}/{len(datenreihen_hoch_pass)}] Hoch-Pass-Filterung...", end="\r")
    for i, e in enumerate(datenreihen_low_pass[0]):
        datenreihen_hoch_pass[0].append(datenreihen_ohne_trend[0][i] - e)
    print(f"[{2}/{len(datenreihen_hoch_pass)}] Hoch-Pass-Filterung...", end="\r")
    for i, e in enumerate(datenreihen_low_pass[1]):
        datenreihen_hoch_pass[1].append(datenreihen_ohne_trend[1][i] - e)
    print(f"[{3}/{len(datenreihen_hoch_pass)}] Hoch-Pass-Filterung...", end="\r")
    for i, e in enumerate(datenreihen_low_pass[2]):
        datenreihen_hoch_pass[2].append(datenreihen_ohne_trend[2][i] - e)
    print("")
    # Plot der hoch-pass Sensorreihen
    plot_werte(datenreihen_hoch_pass, ["Sensor 1 (mit Hoch-Pass-Filter)", "Sensor 2 (mit Hoch-Pass-Filter)", "Sensor 3 (mit Hoch-Pass-Filter)"])

    # Fourier-Transformation

    # Weitere Informationen:
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html
    sample_frequenz = 1/10
    N = 36286*2
    print(f"[{1}/{len(datenreihen_ohne_trend)}] Fast-Fourier-Transformation...", end="\r")
    yf_1 = fft(datenreihen_low_pass[0])
    xf_1 = fftfreq(len(datenreihen_low_pass[0]), 1/sample_frequenz)
    print(f"[{2}/{len(datenreihen_ohne_trend)}] Fast-Fourier-Transformation...", end="\r")
    yf_2 = fft(datenreihen_low_pass[1])
    xf_2 = fftfreq(len(datenreihen_low_pass[1]), 1/sample_frequenz)
    print(f"[{3}/{len(datenreihen_ohne_trend)}] Fast-Fourier-Transformation...", end="\r")
    yf_3 = fft(datenreihen_low_pass[2])
    xf_3 = fftfreq(len(datenreihen_low_pass[2]), 1/sample_frequenz)
    print("")
    # Plot der Fourier-Transformation
    plt.plot(xf_1, 2.0/N * np.abs(yf_1[0:N//2]))
    plt.xlim(0, 0.0001)
    plt.grid()
    plt.show()

    plt.plot(xf_2, 2.0/N * np.abs(yf_2[0:N//2]))
    plt.xlim(0, 0.0001)
    plt.grid()
    plt.show()

    plt.plot(xf_3, 2.0/N * np.abs(yf_3[0:N//2]))
    plt.xlim(0, 0.0001)
    plt.grid()
    plt.show()


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
