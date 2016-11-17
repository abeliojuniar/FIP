import math as mat
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
import itertools

class TIMEFORMAT(object):
    def __init__(self):
        self.hour = None
        self.minute = None
        self.time = [self.hour, self.minute]

    def __repr__(self):
        return (self.time)

    def returnTime(self):
        if (self.minute < 10):
            return str(self.hour) + ':0' + str(self.minute)
        else:
            return str(self.hour) + ':' + str(self.minute)

    def addTime(self, t):
        if ((mat.modf(t)[1] + self.hour) >= 24):
            self.hour = int(mat.modf(t)[1]) + int(self.hour) - 24
        else:
            self.hour = int(mat.modf(t)[1]) + int(self.hour)
        if ((mat.modf(t)[0] * 60 + self.minute) >= 60):
            self.hour = self.hour + 1
            self.minute = int(round(mat.modf(t)[0] * 60) + self.minute - 60)
        else:
            self.minute = int(round(mat.modf(t)[0] * 60) + self.minute)


class COORDINATE(object):
    def __init__(self, x, y):
        self.coord = [x, y]
        self.x = x
        self.y = y

    def __repr__(self):
        return repr(self.coord)


class PASSENGER(object):
    def __init__(self):
        self.pickUpCoordinate = COORDINATE(None, None)
        self.dropCoordinate = COORDINATE(None, None)
        self.pickUpWindow = TIMEFORMAT()
        self.dropWindow = TIMEFORMAT()
        self.actualPickUp = TIMEFORMAT()
        self.actualDrop = TIMEFORMAT()

    def addPickUpCoordinate(self, x, y):
        self.pickUpCoordinate = COORDINATE(x, y)

    def addDropCoordinate(self, x, y):
        self.dropCoordinate = COORDINATE(x, y)



class FREIGHT(object):
    def __init__(self):
        self.pickUpCoordinate = COORDINATE(None, None)
        self.dropCoordinate = COORDINATE(None, None)
        self.pickUpWindow = TIMEFORMAT()
        self.dropWindow = TIMEFORMAT()
        self.actualPickUp = TIMEFORMAT()
        self.actualDrop = TIMEFORMAT()
        self.pickUpToPoint=[]
        self.dropToPoint=[]
        self.isPickedUp = 0

    def addPickUpCoordinate(self, x, y):
        self.pickUpCoordinate = COORDINATE(x, y)

    def addDropCoordinate(self, x, y):
        self.dropCoordinate = COORDINATE(x, y)


class FREIGHTLIST(object):
    def __init__(self):
        self.list = FREIGHT()

    def addFreight(self):
        if(isinstance(self.list,list)):
            self.list.append(FREIGHT())
        else:
            self.list=[FREIGHT()]

    def __repr__(self):
        return repr(self.list)


class ROUTE(object):
    def __init__(self):
        self.points = COORDINATE(None,None)
        self.passenger = PASSENGER()
        self.freight = FREIGHT()
        self.distanceBetween = []

    def addPoint(self, x, y):
        if(isinstance(self.points,list)):
            self.points.append(COORDINATE(x, y))
        else:
            self.points=[COORDINATE(x, y)]

    def addPassenger(self):
        if(isinstance(self.passenger,list)):
            self.passenger.append(PASSENGER())
        else:
            self.passenger=[PASSENGER()]

    def addFreight(self):
        if(isinstance(self.freight,list)):
            self.freight.append(FREIGHT())
        else:
            self.freight=[FREIGHT()]

    def calculateDistanceBetween(self):
        for i in range(len(self.points)-1):
            self.distanceBetween.append(distForm(self.points[i].coord,self.points[i+1].coord))

class CAR(object):
    freight = FREIGHT()

    def __init__(self):
        self.initialRoute = ROUTE()
        self.FIPRoute = ROUTE()
        self.possibleRoute = ROUTE()
        self.totalPassenger = 0
        self.isLoaded = 0
    def addPossibleRoute():
        if(isinstance(self.possibleRoute,list)):
            self.possibleRoute.append(ROUTE())
        else:
            self.possibleRoute=[ROUTE()]


def readCSV(filename):
    import csv
    global column
    column = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            column.extend(row)
        for i in range(0, len(column)):
            column[i] = column[i].split(';')


def readParameter():
    global beta, gamma2, gamma3, gamma4
    global totalRoute, totalPassenger, totalFreight, Vavg
    global startTime, finishTime
    beta = int(column[1][1])
    gamma2 = int(column[2][1])
    gamma3 = int(column[3][1])
    gamma4 = int(column[4][1])
    startTime = column[1][7].split(':')
    finishTime = column[2][7].split(':')
    totalRoute = int(column[2][4])
    totalPassenger = int(column[3][4])
    totalFreight = int(column[4][4])
    Vavg = int(column[1][4])


def assignPassenger():
    foundRoute = -1
    for i in range(8, len(column)):
        if (column[i][0] == 'Start Route'):
            foundRoute = foundRoute + 1
            foundPas = -1
        elif (column[i][0] == 'Passenger'):
            foundPas+=1
            K[foundRoute].initialRoute.addPassenger()
            K[foundRoute].initialRoute.addPoint(float(column[i][1]), float(column[i][2]))
            K[foundRoute].initialRoute.addPoint(float(column[i][3]), float(column[i][4]))
            K[foundRoute].initialRoute.passenger[foundPas].addPickUpCoordinate(float(column[i][1]), float(column[i][2]))
            K[foundRoute].initialRoute.passenger[foundPas].addDropCoordinate(float(column[i][3]), float(column[i][4]))
            K[foundRoute].totalPassenger=foundPas+1
        elif (column[i][0] == 'Freight'):
            FrList.addFreight()
            FrList.list[-1].addPickUpCoordinate(float(column[i][1]), float(column[i][2]))
            FrList.list[-1].addDropCoordinate(float(column[i][3]), float(column[i][4]))

def plotInitialRoute():
    for i in range(totalRoute):
        #for j in range(len(K[i].initialRoute.points)):
        #    print(K[i].initialRoute.points[j])
        line,=plt.plot([K[i].initialRoute.points[j].x for j in range(len(K[i].initialRoute.points))],\
                       [K[i].initialRoute.points[j].y for j in range(len(K[i].initialRoute.points))],'g-')
        oriPas,=plt.plot([K[i].initialRoute.points[j].x for j in range(0,len(K[i].initialRoute.points),2)],\
                         [K[i].initialRoute.points[j].y for j in range(0,len(K[i].initialRoute.points),2)],'bo')
        oriPas, = plt.plot([K[i].initialRoute.points[j].x for j in range(1, len(K[i].initialRoute.points),2)], \
                           [K[i].initialRoute.points[j].y for j in range(1, len(K[i].initialRoute.points),2)], 'ro')

def plotFreight():
    oriFre,=plt.plot([FrList.list[i].pickUpCoordinate.x for i in range(totalFreight)], \
                     [FrList.list[i].pickUpCoordinate.y for i in range(totalFreight)],'bv')
    desFre, = plt.plot([FrList.list[i].dropCoordinate.x for i in range(totalFreight)], \
                       [FrList.list[i].dropCoordinate.y for i in range(totalFreight)], 'rv')

def distForm(coord0,coord1):
    return mat.sqrt(pow((coord1[0] - coord0[0]), 2) + pow((coord1[1] - coord0[1]), 2))

def calculateFreightToPoint():
    #print(FrList.list[0].pickUpCoordinate)
    for list in FrList.list:
        list.pickUpToPoint=[[] for i in range(totalRoute)]
        list.dropToPoint=[[] for i in range(totalRoute)]
    for freight in FrList.list:
        for i in range(totalRoute):
            for points in K[i].initialRoute.points:
                freight.pickUpToPoint[i].append(distForm(freight.pickUpCoordinate.coord,points.coord))
                freight.dropToPoint[i].append(distForm(freight.dropCoordinate.coord,points.coord))

def calculateDistanceBetween():
    for i in range(totalRoute):
        K[i].initialRoute.calculateDistanceBetween()
        #print(list(itertools.permutations([1,2,3])))

def listAllPossiblePickUp(routeNo, point):
    possibility=[]
    i=-1
    for freight in FrList.list:
        i+=1
        Btemp = 'B'+str(i)
        if(point<len(K[routeNo].initialRoute.points)-1):
            reroutePickUp=freight.pickUpToPoint[routeNo][point]+freight.pickUpToPoint[routeNo][point+1]
            if (reroutePickUp<2*K[routeNo].initialRoute.distanceBetween[point]):
                possibility.append(i)
                #possibility.append(Btemp)
                #possibility.append(freight.pickUpCoordinate)
    return possibility

def listAllPossibleDrop(routeNo, point):
    possibility=[]
    i=-1
    for freight in FrList.list:
        i+=1
        if(point<len(K[routeNo].initialRoute.points)-1):
            rerouteDrop=freight.dropToPoint[routeNo][point]+freight.dropToPoint[routeNo][point+1]
            if (rerouteDrop < 2*K[routeNo].initialRoute.distanceBetween[point]):
                possibility.append(i)
                #possibility.append(freight.dropCoordinate)
    return possibility

def findDropPoint(routeNo, currentPoint, FreightList):
    result=[]
    for i in FreightList:
        #temp = [i]
        temp = ["B"+str(i)]
        dropPoint = []
        freight=FrList.list[i]
        for point in range(currentPoint+1, len(K[routeNo].initialRoute.points)):
            if (point < len(K[routeNo].initialRoute.points) - 1):
                rerouteDrop = freight.dropToPoint[routeNo][point] + freight.dropToPoint[routeNo][point + 1]
                if (rerouteDrop < 2 * K[routeNo].initialRoute.distanceBetween[point]):
                    #dropPoint.append(point)
                    dropPoint.append('E'+str(point))
            else:
                #dropPoint.append(point)
                dropPoint.append('E' + str(point))
        result.append(list(itertools.product(temp,dropPoint)))
        #print(dropPoint)
    return result

def isDropPossible(routeNo, point, pickUpPoint):
    possibility=False
    if(point<len(K[routeNo].initialRoute.points)-1):
        for freight in FrList.list:
            if (freight.pickUpCoordinate==pickUpPoint):
                dropPoint = freight.dropCoordinate
                rerouteDrop = freight.dropToPoint[routeNo][point]+freight.dropToPoint[routeNo][point+1]
                if(rerouteDrop<2*K[routeNo].initialRoute.distanceBetween[point]):
                    possibility=True
    else:
        possibility=True
    return possibility

def product(List1,List2):
    temp=list(itertools.repeat(List1,len(List2)))
    for i in range(len(List2)):
        if (i==0):
            List1.append(i)
        else:
            List1.append(temp)
            List1[-1].append(i)
    print(List1)
    return List1

def listAllPossiblePickUpDrop():
    possiblePickUp=[]
    possibleDrop=[]
    for i in range(totalRoute):
        possibleRoute=[]
        print('route: ',i)
        Rtemp='R'+str(i)
        for j in range(len(K[i].initialRoute.points)-1):
            Ptemp = 'P'+str(j)
            if (possibleRoute==[]):
                possibleRoute.append(tuple([Ptemp]))
            print('  point: ', j)
            pickUpList = listAllPossiblePickUp(i,j)
            if (pickUpList!=[]):
                findDP = findDropPoint(i,j,pickUpList)
                print('   PICKUP : ',pickUpList)
                a = []
                for route in possibleRoute:
                    if(route[-1][0]=='P'):
                        a.append(1)
                    else:
                        a.append(0)
                temp = tuple(itertools.compress(possibleRoute,a))
                for frNo in findDP:
                    prod=list(itertools.product(temp,frNo))
                    for res in prod:
                        result=tuple(itertools.chain.from_iterable(res))
                        possibleRoute=possibleRoute[:-1]+[result]+possibleRoute[-1:]
            count = -1
            for app in possibleRoute:
                count+=1
                temp=tuple(['P'+str(j+1)])
                if(app[-1][0]!='E'):
                    possibleRoute[count]=app+temp
                else:
                    idx = int(app[-1][1:])
                    if(j+1<idx):
                        possibleRoute[count]=app[:-1]+temp+app[-1:]
                    else:
                        # last=app[-1]
                        bar=list(app)
                        bar.reverse()
                        for foo in bar:
                            if (foo[0] == 'B'):
                                last = (foo[1:])
                                break
                        possibleRoute[count]=app[0:-1]+temp+tuple(['D'+last])
            for app in possibleRoute:
                print(app)
        print('--')
readCSV('./data_small2.csv')
readParameter()
K = [CAR() for i in range(totalRoute)]
FrList = FREIGHTLIST()
assignPassenger()
fig, ax = plt.subplots()
plt.axis([-25,25,-25,25])
plotInitialRoute()
plotFreight()
calculateFreightToPoint()
calculateDistanceBetween()
listAllPossiblePickUpDrop()
plt.show()
