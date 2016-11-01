import math
global data
# Procedure to get required parameters from "parameter.txt"
def getVarFromFile(filename):
	import imp
	f = open(filename)
	global data
	data = imp.load_source('data', '', f)
	f.close()
	return data
	
# Procedure to print all parameters in "parameter.txt"
def printParam():
	global data
	print("beta = ",data.beta)
	print("gamma2 = ",data.gamma2)
	print("gamma3 = ",data.gamma3)
	print("gamma4 = ",data.gamma4)
	print(data.absK)

# calculate distance between two coordinates
# initial coordinate (x1,y1)
# destination coordinate (x2,y2)
def calculateDistance(x1,y1,x2,y2):
	return (math.sqrt(pow((x2-x1),2) + pow((y2-y1),2)))

#getVarFromFile('parameter.txt')