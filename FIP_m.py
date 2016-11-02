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
	Vfo=[]
	Vfd=[]
	startTime=[]
	finishTime=[]
	def __init__(self):
		self.start=None
		self.V=[]
		self.Vpo=[]
		self.Vpd=[]
		self.pickUpTime=[]
		self.timeWindow=[]
		self.actualArrival=[]

class timeFormat(object):
	def __init__(self):
		self.hour=None
		self.minute=None
	def returnTime(self):
		if(self.minute<10):
			return str(self.hour)+':0'+str(self.minute)
		else:
			return str(self.hour)+':'+str(self.minute)
	def addTime(self,t):
		if((mat.modf(t)[1]+self.hour)>=24):
			self.hour=int(mat.modf(t)[1])+int(self.hour)-24
		else:
			self.hour=int(mat.modf(t)[1])+int(self.hour)
		if((mat.modf(t)[0]*60+self.minute)>=60):
			self.hour=self.hour+1
			self.minute=int(round(mat.modf(t)[0]*60)+self.minute-60)
		else:
			self.minute=int(round(mat.modf(t)[0]*60)+self.minute)
	
# Calculate distance formula
def distForm(x1,y1,x2,y2):
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
	
	K[0].startTime=column[1][7].split(':')
	K[0].finishTime=column[2][7].split(':')
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

#def calculateDistance(K):
		
	
#def calculateTimeWindow(K):

			
def plotInitialRoute(K):
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
	#line1, = plt.plot(routeX[1],routeY[1],'m-')
	oriPas, = plt.plot(orX,orY,'bo')
	desPas, = plt.plot(desX,desY,'ro')
	start, = plt.plot(startX,startY,'ko')

def plotFreight(K):
	Vfo_x=[]
	Vfo_y=[]
	Vfd_x=[]
	Vfd_y=[]
	for i in range(len(K[0].Vfo)):
		Vfo_x.append(K[0].Vfo[i][0])
		Vfo_y.append(K[0].Vfo[i][1])
		Vfd_x.append(K[0].Vfd[i][0])
		Vfd_y.append(K[0].Vfd[i][1])
	oriFre, = plt.plot(Vfo_x,Vfo_y,'bv')
	desFre, = plt.plot(Vfd_x,Vfd_y,'rv')
	
readCSV('./data_small.csv')
fig, ax = plt.subplots()
plt.axis([-25,25,-25,25])
setVariable(column)
print([int(column[1][7].split(':')[0]),int(column[1][7].split(':')[1])])
print(column[2][7])
plotInitialRoute(K)
plotFreight(K)
#plotPas()
plt.axis([-25,25,-25,25])
plt.grid(True)
plt.show()
