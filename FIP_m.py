###########################
# File name : FIP.py
# Description : Main program of FIP
# Author : Abelio
###########################
import math as mat
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons

# K = set of cars
class setCar(object):
	def __init__(self):
		self.start=None
		self.V=[]
		self.Vpo=[]
		self.Vpd=[]
		self.Vfo=[]

# Calculate distance
def calculateDistance(x1,y1,x2,y2):
	return mat.sqrt(pow((x2-x1),2) + pow((y2-y1),2))
	
def readCSV(filename):
	import csv
	global column
	column=[]
	with open(filename) as f:
		reader = csv.reader(f)
		for row in reader:
			column.extend(row)
		for i in range(0,len(column)):
			column[i]=column[i].split(';')

def setVariable(column):
	# Vpo = passenger origins
	# Vpd = passenger destinations 
	# Vfo = freight origins
	# Vfd = freight destinations
	global K,Vpo,Vpd,Vfo,Vfd
	K=[setCar() for i in range(int(column[2][4]))]
	foundCar=-1
	Vpo=[];Vpd=[];Vfo=[];Vfd=[]
	for i in range(8,len(column)):
		if(column[i][0]=='Car'):
			foundCar=foundCar+1
			K[foundCar].start = [float(column[i][1]),float(column[i][2])]
		elif(column[i][0]=='Passenger'):
			K[foundCar].Vpo.append([float(column[i][1]),float(column[i][2])])
			K[foundCar].Vpd.append([float(column[i][3]),float(column[i][4])])
		elif(column[i][0]=='Freight'):
			K[foundCar].Vfo.append([float(column[i][1]),float(column[i][2])])
			K[foundCar].Vfd.append([float(column[i][3]),float(column[i][4])])
			
def plotInitialRoute(K):
	print(K[0].start[1])
	routeX=[0 for i in range(len(K))]
	routeY=[0 for i in range(len(K))]
	orX=[]
	orY=[]
	desX=[]
	desY=[]
	startX=[]
	startY=[]
	for i in range(len(K)):
		routeX[i]=[K[i].start[0]]
		routeY[i]=[K[i].start[1]]
		startX.append(K[i].start[0])
		startY.append(K[i].start[1])
		for j in range(len(K[i].Vpo)):
			routeX[i].append(K[i].Vpo[j][0])
			routeY[i].append(K[i].Vpo[j][1])
			routeX[i].append(K[i].Vpd[j][0])
			routeY[i].append(K[i].Vpd[j][1])
			orX.append(K[i].Vpo[j][0])
			orY.append(K[i].Vpo[j][1])
			desX.append(K[i].Vpd[j][0])
			desY.append(K[i].Vpd[j][1])
	#ppo, = plt.plot(xpo,ypo,'ro--')
	line0, = plt.plot(routeX[0],routeY[0],'g-')
	line1, = plt.plot(routeX[1],routeY[1],'m-')
	line0, = plt.plot(orX,orY,'bo')
	line1, = plt.plot(desX,desY,'ro')
	start = plt.plot(startX,startY,'ko')
	
readCSV('./data.csv')
fig, ax = plt.subplots()
plt.axis([-25,25,-25,25])
setVariable(column)
#print(K[0].Vpo)
#print(K[1].Vpo)
plotInitialRoute(K)
#plotPas()
plt.axis([-25,25,-25,25])
plt.grid(True)
plt.show()
