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
	freightPickUp=[]
	startTime=[]
	finishTime=[]
	beta=None
	gamma2=None
	gamma3=None
	gamma4=None
	def __init__(self):
		self.taxiNo=None
		self.initialRoute=[]
		self.distanceRoute=[]
		self.V=[]
		self.Vpo=[]
		self.Vpd=[]
		self.pickUpTime=[]
		self.timeWindow=[]
		self.actualArrival=[]
		self.distOrDes=[]

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
def distForm(coord0,coord1):
	return mat.sqrt(pow((coord1[0]-coord0[0]),2) + pow((coord1[1]-coord0[1]),2))

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
	K[0].beta=int(column[1][1])
	K[0].gamma2=int(column[2][1])
	K[0].gamma3=int(column[3][1])
	K[0].gamma4=int(column[4][1])
	K[0].startTime=column[1][7].split(':')
	K[0].finishTime=column[2][7].split(':')

	for i in range(8,len(column)):
		if(column[i][0]=='Start Route'):
			foundCar=foundCar+1
			K[foundCar].taxiNo = foundCar+1
		elif(column[i][0]=='Passenger'):
			K[foundCar].Vpo.append([float(column[i][1]),float(column[i][2])])
			K[foundCar].Vpd.append([float(column[i][3]),float(column[i][4])])
		elif(column[i][0]=='Freight'):
			K[foundCar].Vfo.append([float(column[i][1]),float(column[i][2])])
			K[foundCar].Vfd.append([float(column[i][3]),float(column[i][4])])
			K[foundCar].freightPickUp.append(0)
			
	for i in range(len(K)):	
		K[i].pickUpTime=[timeFormat() for j in range(len(K[i].Vpo))]
		K[i].timeWindow=[timeFormat() for j in range(len(K[i].Vpo))]
		K[i].actualArrival=[timeFormat() for j in range(len(K[i].Vpo))]	
		for j in range(len(K[i].Vpo)):
			K[i].pickUpTime[j].hour=int(K[0].startTime[0])
			K[i].pickUpTime[j].minute=int(K[0].startTime[1])
	calculateDistanceBetween(K)
	
def calculateDistanceBetween(K):
	for i in range(len(K)):
		#print('--')
		for j in range(len(K[i].Vpo)):
			K[i].distOrDes.append(distForm(K[i].Vpo[j],K[i].Vpd[j]))
			
def plotInitialRoute(K):
	for i in range(len(K)):
		for j in range(len(K[i].Vpo)):
			K[i].initialRoute.append([K[i].Vpo[j][0],K[i].Vpo[j][1]])
			K[i].initialRoute.append([K[i].Vpd[j][0],K[i].Vpd[j][1]])
	for h in range(len(K)):
		line, = plt.plot([K[h].initialRoute[i][0] for i in range(len(K[h].initialRoute))],[K[h].initialRoute[i][1] for i in range(len(K[h].initialRoute))],'g-')
		oriPas, = plt.plot([K[h].initialRoute[i][0] for i in range(0,len(K[h].initialRoute),2)],[K[h].initialRoute[i][1] for i in range(0,len(K[h].initialRoute),2)],'bo')
		desPas, = plt.plot([K[h].initialRoute[i][0] for i in range(1,len(K[h].initialRoute),2)],[K[h].initialRoute[i][1] for i in range(1,len(K[h].initialRoute),2)],'ro')

def FIP(K):
	reroute=[0 for i in range(len(K))]
	for h in range(len(K)):
		reroute[h]=[[0 for i in range(len(K[h].Vfo))] for j in range(len(K[h].initialRoute))]
	for h in range(len(K)):
		for i in range(0,len(K[h].initialRoute),1):
			if(i+1<len(K[h].initialRoute)):
				K[h].distanceRoute.append(distForm(K[h].initialRoute[i],K[h].initialRoute[i+1]))
			for j in range(len(K[h].Vfo)):
				reroute[h][i][j]=[distForm(K[h].initialRoute[i],K[h].Vfo[j])]
				reroute[h][i][j].append(distForm(K[h].initialRoute[i],K[h].Vfd[j]))
				#print(i,';',len(K[h].initialRoute))
				if((i+1)<len(K[h].initialRoute)):
					reroute[h][i+1][j]=[distForm(K[h].initialRoute[i+1],K[h].Vfo[j])]
					reroute[h][i+1][j].append(distForm(K[h].initialRoute[i+1],K[h].Vfd[j]))
					#print(reroute[h][i+1][j][0])
					if(reroute[h][i][j][0]+reroute[h][i+1][j][0]<=K[h].distanceRoute[i]*2):
						print('pickup',h,';',i,';',j)
						for k in range(i+1,len(K[h].initialRoute)):
							#print(reroute[h][k][j
							if(k+1<len(K[h].initialRoute)):
								#if(reroute[h][k][j][1]+reroute[h][k+1][j][1]<=K[h].distanceRoute[k]*2):
								print('deliver',h,';',k,';',j)
							#print('--')
			#print(reroute[h][i])


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
	
readCSV('./data_small2.csv')
fig, ax = plt.subplots()
plt.axis([-25,25,-25,25])
setVariable(column)
#print([int(column[1][7].split(':')[0]),int(column[1][7].split(':')[1])])
#print(column[2][7])
calculateDistanceBetween(K)
plotInitialRoute(K)
plotFreight(K)
FIP(K)
#plotPas()
plt.axis([-25,25,-25,25])
plt.grid(True)
plt.show()
