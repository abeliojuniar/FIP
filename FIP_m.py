###########################
# File name : FIP.py
# Description : Main program of FIP
# Author : Abelio
###########################
import tkinter
from defproc import *
#from tkinter import * 
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt
import sys

#n = input('Jumlah barang = ')
#m = input('Jumlah penumpang = ')
#absK = input('Jumlah mobil yang beroperasi = ')

fig, ax = plt.subplots()
t = np.arange(0.0, 1.0, 0.001)
a0 = 5
f0 = 3
s = a0*np.sin(2*np.pi*f0*t)
l, = plt.plot([15, 22, 0], [-21, 21, 0], lw=2, color='red')

plt.axis([-25,25,-25,25])

axcolor = 'lightgoldenrodyellow'
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax,'Plot', color=axcolor, hovercolor='0.975')


param=getVarFromFile('parameter.txt')
getVarFromFile('position.txt')
print(param.absK)
print(param.gamma2)
#printParam()

#print(data.beta)


plt.show()
