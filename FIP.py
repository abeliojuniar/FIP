###########################
# File name : FIP.py
# Description : Main program of FIP
# Author : Abelio
###########################
import tkinter
from tkinter import *

# Procedure to get required parameters from "parameter.txt"
def getVarFromFile(filename):
	import imp
	f = open(filename)
	global data
	data = imp.load_source('data', '', f)
	f.close()

# Procedure to print all parameters in "parameter.txt"
def printParam():
	global data
	print("beta = ",data.beta)
	print("gamma2 = ",data.gamma2)
	print("gamma3 = ",data.gamma3)
	print("gamma4 = ",data.gamma4)

class Window (Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master=master
		self.init_window()
	
	def init_window(self):
		self.master.title("FREIGHT INSERTION PROBLEM")
		self.pack(fill=BOTH, expand=1)
		#quitButton = Button(self,text="Quit",command=root.destroy)
		#quitButton.place(x=500, y=500)
		
		menu = Menu(self.master)
		self.master.config(menu=menu)
		
		file = Menu(menu)
		file.add_command(label='Exit',command=root.destroy)
		menu.add_cascade(label='File', menu=file)
		
		edit = Menu(menu)
		edit.add_command(label='Edit config...')
		menu.add_cascade(label='Edit', menu=edit)
	

getVarFromFile('./parameter.txt')
##printParam()
##input("\nPress <ENTER> to end program")

root = Tk()
root.geometry("600x600")
app = Window(root)
root.mainloop()