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
        self.pickUpWindow = []
        self.dropWindow = []
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
        self.pickUpWindow = []
        self.dropWindow = []
        self.actualPickUp = TIMEFORMAT()
        self.actualDrop = TIMEFORMAT()
        self.pickUpToPoint=[]
        self.dropToPoint=[]
        self.pickUpCost=[]
        self.dropCost=[]
        self.pickTimeCost=[]
        self.dropTimeCost=[]
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
            K[foundRoute].initialRoute.passenger[foundPas].pickUpWindow.append(int(column[i][5].split(':')[0])*60+int(column[i][5].split(':')[1]))
            K[foundRoute].initialRoute.passenger[foundPas].pickUpWindow.append(int(column[i][6].split(':')[0])*60+int(column[i][6].split(':')[1]))
            K[foundRoute].initialRoute.passenger[foundPas].dropWindow.append(int(column[i][7].split(':')[0])*60+int(column[i][7].split(':')[1]))
            K[foundRoute].initialRoute.passenger[foundPas].dropWindow.append(int(column[i][8].split(':')[0])*60+int(column[i][8].split(':')[1]))
        elif (column[i][0] == 'Freight'):
            FrList.addFreight()
            FrList.list[-1].addPickUpCoordinate(float(column[i][1]), float(column[i][2]))
            FrList.list[-1].addDropCoordinate(float(column[i][3]), float(column[i][4]))
            FrList.list[-1].pickUpWindow.append(int(column[i][5].split(':')[0]) * 60 + int(column[i][5].split(':')[1]))
            FrList.list[-1].pickUpWindow.append(int(column[i][6].split(':')[0]) * 60 + int(column[i][6].split(':')[1]))
            FrList.list[-1].dropWindow.append(int(column[i][7].split(':')[0]) * 60 + int(column[i][7].split(':')[1]))
            FrList.list[-1].dropWindow.append(int(column[i][8].split(':')[0]) * 60 + int(column[i][8].split(':')[1]))

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
        list.pickUpCost=[[] for i in range(totalRoute)]
        list.dropCost=[[] for i in range(totalRoute)]
        list.pickTimeCost=[[] for i in range(totalRoute)]
        list.dropTimeCost=[[] for i in range(totalRoute)]
    for freight in FrList.list:
        for i in range(totalRoute):
            for points in K[i].initialRoute.points:
                freight.pickUpToPoint[i].append(distForm(freight.pickUpCoordinate.coord,points.coord))
                freight.dropToPoint[i].append(distForm(freight.dropCoordinate.coord,points.coord))
            for j in range(len(K[i].initialRoute.points)):
                if(j<len(K[i].initialRoute.points)-1):
                    freight.pickUpCost[i].append(freight.pickUpToPoint[i][j]+freight.pickUpToPoint[i][j+1]-K[i].initialRoute.distanceBetween[j])
                    freight.dropCost[i].append(freight.dropToPoint[i][j]+freight.dropToPoint[i][j+1]-K[i].initialRoute.distanceBetween[j])
                    freight.pickTimeCost[i].append((freight.pickUpToPoint[i][j]+freight.pickUpToPoint[i][j+1])/(K[i].initialRoute.distanceBetween[j]))
                    freight.dropTimeCost[i].append((freight.dropToPoint[i][j]+freight.dropToPoint[i][j+1])/(K[i].initialRoute.distanceBetween[j]))
                else:
                    freight.pickUpCost[i].append(freight.pickUpToPoint[i][j])
                    freight.dropCost[i].append(freight.dropToPoint[i][j])
                    freight.pickTimeCost[i].append(0)
                    freight.dropTimeCost[i].append(0)

def calculateDistanceBetween():
    for i in range(totalRoute):
        K[i].initialRoute.calculateDistanceBetween()

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

def listAllPossibleRoute():
    allPossibleRoute=[]
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
                        # for app in possibleRoute:
                        #     print(app)
        print('--')
        allPossibleRoute.append(possibleRoute[:-1])
    allPossibleRoute=(list(itertools.product(*allPossibleRoute)))
    return allPossibleRoute

def isRouteValid(route):
    res=[]
    for foo in route:
        for bar in foo:
            if(bar[0]=='B'):
                res.append(int(bar[1:]))
    if(len(res)==len(list(set(res)))):
        return 1
    else:
        return 0

def generateValidRoutes(allPossibleRoute):
    valid=[]
    for route in allPossibleRoute:
        valid.append(isRouteValid(route))
    return (list(itertools.compress(allPossibleRoute,valid)))

def checkTimingWindow(route):
    for routeNo in range(len(route)):
        prev = 'A0'
        strt = int(startTime[0])*60 + int(startTime[1])
        timePoint=[strt]
        count=-1
        for input in route[routeNo]:
            count+=1
            if(input[0]=='P' and prev[0]=='P'):
                distance=K[routeNo].initialRoute.distanceBetween[int(prev[1:])]
            elif(input[0]=='B' and prev[0]=='P'):
                distance=FrList.list[int(input[1:])].pickUpToPoint[routeNo][int(prev[1:])]
            elif(input[0]=='P' and prev[0]=='B'):
                distance=FrList.list[int(prev[1:])].pickUpToPoint[routeNo][int(input[1:])]
            elif(input[0]=='D' and prev[0]=='P'):
                distance=FrList.list[int(input[1:])].dropToPoint[routeNo][int(prev[1:])]
            elif(input[0]=='P' and prev[0]=='D'):
                distance=FrList.list[int(prev[1:])].dropToPoint[routeNo][int(input[1:])]
            if(count!=0):
                timePoint.append(mat.floor(distance*60/Vavg) + timePoint[-1])
                if(input[0]=='P'):
                    if(int(input[1:])%2==0):
                        earlyPickUp = K[routeNo].initialRoute.passenger[mat.floor(int(input[1:]) / 2)].pickUpWindow[0]
                        latePickUp = K[routeNo].initialRoute.passenger[mat.floor(int(input[1:]) / 2)].pickUpWindow[1]
                        # print('pu',timePoint[-1],earlyPickUp,latePickUp)
                        if(not(timePoint[-1]>=earlyPickUp and timePoint[-1]<=latePickUp)):
                            return 0
                            # print(input, 'not meet')
                        # else:
                        #     print(input,'meet')
                    elif(int(input[1:])%2==1):
                        earlyDrop = K[routeNo].initialRoute.passenger[mat.floor(int(input[1:]) / 2)].dropWindow[0]
                        lateDrop = K[routeNo].initialRoute.passenger[mat.floor(int(input[1:]) / 2)].dropWindow[1]
                        # print('d',timePoint[-1], earlyDrop, lateDrop)
                        if (not(timePoint[-1] >= earlyDrop and timePoint[-1] <= lateDrop)):
                            return 0
                            # print(input, 'not meet')
                        # else:
                        #     print(input, 'meet')
                elif(input[0]=='B'):
                    earlyPickUp = FrList.list[int(input[1:])].pickUpWindow[0]
                    latePickUp = FrList.list[int(input[1:])].pickUpWindow[1]
                    if (not(timePoint[-1] >= earlyPickUp and timePoint[-1] <= latePickUp)):
                        return 0
                        # print(input, 'not meet')
                    # else:
                    #     print(input, 'meet')
                elif (input[0] == 'D'):
                    earlyDrop = FrList.list[int(input[1:])].dropWindow[0]
                    lateDrop = FrList.list[int(input[1:])].dropWindow[1]
                    if (not(timePoint[-1] >= earlyDrop and timePoint[-1] <= lateDrop)):
                        return 0
                        # print(input, 'not meet')
                    # else:
                    #     print(input, 'meet')
            prev = input
    return 1

def printTimePoint (route):
    for routeNo in range(len(route)):
        prev = 'A0'
        strt = int(startTime[0])*60 + int(startTime[1])
        timePoint=[strt]
        count=-1
        for input in route[routeNo]:
            count+=1
            if(input[0]=='P' and prev[0]=='P'):
                distance=K[routeNo].initialRoute.distanceBetween[int(prev[1:])]
            elif(input[0]=='B' and prev[0]=='P'):
                distance=FrList.list[int(input[1:])].pickUpToPoint[routeNo][int(prev[1:])]
            elif(input[0]=='P' and prev[0]=='B'):
                distance=FrList.list[int(prev[1:])].pickUpToPoint[routeNo][int(input[1:])]
            elif(input[0]=='D' and prev[0]=='P'):
                distance=FrList.list[int(input[1:])].dropToPoint[routeNo][int(prev[1:])]
            elif(input[0]=='P' and prev[0]=='D'):
                distance=FrList.list[int(prev[1:])].dropToPoint[routeNo][int(input[1:])]
            if(count!=0):
                timePoint.append(mat.floor(distance*60/Vavg) + timePoint[-1])
                print(input,mat.floor(timePoint[-1]/60),':',timePoint[-1]%60)
            else:
                print('POINT 0')
            prev = input

def checkAllTimingWindow(allRoute):
    buffer=[]
    newRoute=[]
    for route in allRoute:
        if (checkTimingWindow(route)):
            newRoute.append(route)
    return newRoute

def calculateProfit(route):
    #State : 0=START, 1=Freight doesnt exist, 2=Freight exist
    sumProfit=0
    for routeNo in range(len(route)):
        state = 0
        prev = None
        freightPicked=None
        rerouteCost = 0
        distanceToDrop = 0
        timeCost = 0
        # timePoint=[]
        for input in route[routeNo]:
            if(state==0):
                if(input[0]=='P'):
                    state=1
                    prev=input
                else:
                    print('route invalid')
            elif (state == 1):
                if (input[0] == 'B'):
                    state = 2
                    freightPicked = int(input[1:])
                    rerouteCost += FrList.list[int(input[1:])].pickUpCost[routeNo][int(prev[1:])]
                    # timePoint.append(FrList.list[int(input[1:])].pickUpToPoint[routeNo][int(prev[1:])])
                    if (prev[0] == 'P' and int(prev[1:]) % 2 == 0):
                        timeCost += FrList.list[int(input[1:])].pickTimeCost[routeNo][int(prev[1:])] - 1
                    prev = input
                else:
                    prev = input
            elif(state==2):
                if(input[0]=='D'):
                    state=1
                    rerouteCost += FrList.list[freightPicked].dropCost[routeNo][int(prev[1:])]
                    distanceToDrop += FrList.list[freightPicked].dropToPoint[routeNo][int(prev[1:])]
                    if (prev[0] == 'P' and int(prev[1:])% 2 == 0):
                        timeCost += FrList.list[freightPicked].dropTimeCost[routeNo][int(prev[1:])] - 1
                    sumProfit+=beta+gamma2*distanceToDrop-gamma3*rerouteCost-gamma4*timeCost
                    rerouteCost=0
                    distanceToDrop=0
                    timeCost=0
                    prev = input
                else:
                    if(prev[0]=='B'):
                        distanceToDrop+=FrList.list[freightPicked].pickUpToPoint[routeNo][int(input[1:])]
                    elif(prev[0]=='P'):
                        distanceToDrop+=K[routeNo].initialRoute.distanceBetween[int(prev[1:])]
                    prev = input
    return sumProfit

def getMaxProfit(allValidRoute):
    max=0
    count=-1
    for validRoute in allValidRoute:
        count+=1
        profit=calculateProfit(validRoute)
        if(profit>max):
            max=profit
            index=count
    return max,allValidRoute[index]

def getRouteCoordinate(route):
    newRoute=[[] for i in range(len(route))]
    for routeNo in range(len(route)):
        count = -1
        for point in route[routeNo]:
            count+=1
            if(point[0]=='P'):
                newRoute[routeNo].append(K[routeNo].initialRoute.points[int(point[1:])])
            elif(point[0]=='B'):
                newRoute[routeNo].append(FrList.list[int(point[1:])].pickUpCoordinate)
            elif(point[0]=='D'):
                newRoute[routeNo].append(FrList.list[int(point[1:])].dropCoordinate)
    return newRoute

def plotMaxRoute(route):
    for r in route:
        # print(r)
        # print(r[0])
        maxline, = plt.plot([r[j].x for j in range(len(r))], [r[j].y for j in range(len(r))], 'y--')

readCSV('./data_small2.csv')
readParameter()
K = [CAR() for i in range(totalRoute)]
FrList = FREIGHTLIST()
assignPassenger()
fig, ax = plt.subplots()
plt.axis([-25,25,-25,25])
plotInitialRoute()
plotFreight()
calculateDistanceBetween()
calculateFreightToPoint()
allPossibleRoute=listAllPossibleRoute()
allValidRoute=generateValidRoutes(allPossibleRoute)
checkTimingRoute = checkAllTimingWindow(allValidRoute)
maxProfit,maxRoute=getMaxProfit(checkTimingRoute)
# print(maxRoute)
printTimePoint(maxRoute)
print('MAXIMUM PROFIT = ',maxProfit)
print('MAXIMUM ROUTE = ',maxRoute)
maxRoute=getRouteCoordinate(maxRoute)
plotMaxRoute(maxRoute)
plt.show()
