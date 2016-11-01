###########################
# File name : FIP.py
# Description : Main program of FIP
# Author : Abelio
###########################
import tkinter
from defproc import *
from tkinter import * 
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys

class Window (Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master=master
		self.init_window()
		self.createWidgets()
	
	def init_window(self):
		self.master.title("FREIGHT INSERTION PROBLEM")
		self.pack(fill=BOTH, expand=1)
		
		menu = Menu(self.master)
		self.master.config(menu=menu)
		
		file = Menu(menu)
		file.add_command(label='Exit',command=root.destroy)
		menu.add_cascade(label='File', menu=file)
		
		edit = Menu(menu)
		edit.add_command(label='Edit config...')
		menu.add_cascade(label='Edit', menu=edit)
		
		self.createWidgets()
		self.quitButton = Button(master=root,text="Quit",command=root.destroy)
		self.quitButton.place(x=550, y=550)
	
	def createWidgets(self):
		# fig=plt.figure(figsize=(8,8))
		# ax=fig.add_axes([0.1,0.1,0.8,0.9],polar=False)
		# canvas=FigureCanvasTkAgg(fig,master=root)
		# canvas.get_tk_widget().grid(row=0,column=1)
		# canvas.show()
		fig, ax = plt.subplots()
		#plt.subplots_adjust(left=0.25, bottom=0.25)
		plt.axis([-25, 25, -25, 25])
		#self.plotbutton=Button(master=root, text="plot", command=lambda: self.showPlot())
		#self.plotbutton.grid(row=0,column=0)
		#plt.plot([4,3,2,3,4])
		#plt.ylabel('some numbers')
		plt.show()
	
	#def showPlot(self):


	

##printParam()
##input("\nPress <ENTER> to end program")
root = Tk()
#root.geometry("400x400")
app = Window(root)
#root.mainloop()
