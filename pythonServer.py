import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.distributed.PyDatagram import PyDatagram #for packaging data
from direct.distributed.PyDatagramIterator import PyDatagramIterator #for unpacking data
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import collisions
import sys, math, random

PRINT_MESSAGE = 1
CAR_MESSAGE = 2
COLLIDED_MESSAGE = 3
NEW_PLAYER_MESSAGE = 4
PLAYER_ASSIGNMENT_MESSAGE = 5


#
class TempCarData(object):
    def __init__(self):
        self.collisionData = []
        self.carData = []
        self.playerNum = 0

class Network(object):
    def __init__(self, cars):
        self.carData = cars
        self.carData.addCar()
        self.carData.index = 0
        self.carUpdates = [() for c in self.carData.carlist]
        self.ignore = []
        
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        self.activeConnections = []
        
        self.port_address = 9099 #No-other TCP/IP services are using this port
        self.backlog = 1000 #If we ignore 1,000 connection attempts, something is wrong!
        self.tcpSocket = self.cManager.openTCPServerRendezvous(self.port_address, self.backlog)
        
        self.cListener.addConnection(self.tcpSocket)
        
        taskMgr.add(self.tskListenerPolling,"Poll the connection listener",-39)
        taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)

    def tskListenerPolling(self, taskdata):
        if self.cListener.newConnectionAvailable():
         
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
         
            if self.cListener.getNewConnection(rendezvous,netAddress,newConnection):
                newConnection = newConnection.p()
                self.activeConnections.append(newConnection) # Remember connection
                self.cReader.addConnection(newConnection)     # Begin reading connection
        return Task.cont
    
    def tskReaderPolling(self, taskdata):
        selfCarDatagram = self.getCarPosDatagramFromCar(self.carData.index)
        self.myProcessDataFunction(selfCarDatagram)
        while self.cReader.dataAvailable():
            datagram=NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            if self.cReader.getData(datagram):
                self.myProcessDataFunction(datagram)
        carPosDatagrams = self.getCarPosDatagrams()
        collisionDatagrams = self.getCollisionDatagrams()
        for aClient in self.activeConnections:
            for data in carPosDatagrams:
                self.cWriter.send(data, aClient)
            for data in collisionDatagrams:
                self.cWriter.send(data, aClient)
        for pair in self.carData.collisionlist:
            if pair[0] < pair[1]:
                collisions.collideCars(self.carData.carlist[pair[0]], self.carData.carlist[pair[1]])
        self.carData.collisionlist = []
        self.clearCarData() #This is to prevent redundant messages from being sent
        return Task.cont
    
    def myProcessDataFunction(self, netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        msgID = myIterator.getUint8()
        if msgID == PRINT_MESSAGE:
            messageToPrint = myIterator.getString()
            print messageToPrint
        elif msgID == CAR_MESSAGE:
            carNum = myIterator.getUint8()
            for num in self.ignore:
                if num == carNum:
                    break
            else:
                carXpos = myIterator.getFloat32()
                carYpos = myIterator.getFloat32()
                carXvel = myIterator.getFloat32()
                carYvel = myIterator.getFloat32()
                carHeading = myIterator.getFloat32()
                carInput = []
                for i in range(5):
                    carInput.append(myIterator.getBool())
                carHp = myIterator.getInt32()
                self.updatePositions(carNum, (carXpos, carYpos, carXvel, carYvel, carHeading, carInput, carHp))
        elif msgID == NEW_PLAYER_MESSAGE:
            self.cWriter.send(self.addNewCar(), netDatagram.getConnection())
            self.returnAllCars(netDatagram.getConnection())
        elif msgID == COLLIDED_MESSAGE:
            print "Verified Collision"
            carNum = myIterator.getUint8()
            self.ignore.remove(carNum)
            

    def myNewPyDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(PRINT_MESSAGE)
        myPyDatagram.addString("Hello, world!")
        return myPyDatagram
    
    def updatePositions(self, carNum, data):
        if len(self.carUpdates) > carNum:
            self.carUpdates[carNum] = data
        else:
            for i in range(len(self.carUpdates),carNum+1):
                self.carUpdates.append(())
            self.carUpdates[carNum] = data
        if len(self.carData.carlist) > carNum:
            if carNum != self.carData.index:
                self.carData.carlist[carNum].model.setPos(data[0], data[1], 0)
                self.carData.carlist[carNum].vel.setXY(data[2], data[3])
                self.carData.carlist[carNum].model.setH(data[4])
                self.carData.carlist[carNum].input = data[5]
                self.carData.carlist[carNum].hp = data[6]
        else:
            for i in range(len(self.carData.carlist), carNum+1):
                self.carData.addCar()
            self.carData.carlist[carNum].model.setPos(data[0], data[1], 0)
            self.carData.carlist[carNum].vel.setXY(data[2], data[3])
            self.carData.carlist[carNum].model.setH(data[4])
            self.carData.carlist[carNum].input = data[5]
            self.carData.carlist[carNum].hp = data[6]
            
          
    def finalizeUpdates(self): #currently unused
        for i in range(len(self.carUpdates)):
            if self.carUpdates[i] != ():
                if len(self.carData.carData) > i:
                    self.carData.carlist[i].model.setPos(self.carUpdates[i][0], self.carUpdates[i][1], 0)
                    self.carData.carlist[i].vel.setXY(self.carUpdates[i][2], self.carUpdates[i][3])
                else:
                    for j in range(len(self.carData.carData), i+1):
                        self.carData.carData.append(())
                    self.carData.carData[i] = self.carUpdates[i]
    
    def clearCarData(self):
        self.carUpdates = [() for c in self.carData.carlist]
        self.collisionData = []
    
    def getCarPosDatagrams(self):
        myDatagrams = []
        for i in range(len(self.carUpdates)):
            if self.carUpdates[i] != ():
                newDatagram = self.getCarPosDatagram(i, self.carUpdates[i])
                myDatagrams.append(newDatagram)
        return myDatagrams
    
    def getCarPosDatagram(self, num, data):
        newDatagram = PyDatagram()
        newDatagram.addUint8(CAR_MESSAGE)
        newDatagram.addUint8(num)
        for j in range(5):
            newDatagram.addFloat32(float(data[j]))
        for j in range(5):
            newDatagram.addBool(data[5][j])
        newDatagram.addInt32(data[6])
        return newDatagram
    
    def getCarPosDatagramFromCar(self, num):
        newDatagram = PyDatagram()
        newDatagram.addUint8(CAR_MESSAGE)
        newDatagram.addUint8(num)
        newDatagram.addFloat32(self.carData.carlist[num].model.getX())
        newDatagram.addFloat32(self.carData.carlist[num].model.getY())
        vel = self.carData.carlist[num].vel.getXY()
        newDatagram.addFloat32(vel[0])
        newDatagram.addFloat32(vel[1])
        newDatagram.addFloat32(self.carData.carlist[num].model.getH())
        for j in range(5):
            newDatagram.addBool(self.carData.carlist[num].input[j])
        newDatagram.addInt32(self.carData.carlist[num].hp)
        return newDatagram
    
    def getNewCarPosDatagram(self, num):
        newDatagram = PyDatagram()
        newDatagram.addUint8(PLAYER_ASSIGNMENT_MESSAGE)
        newDatagram.addUint8(num)
        newDatagram.addFloat32(self.carData.carlist[num].model.getX())
        newDatagram.addFloat32(self.carData.carlist[num].model.getY())
        vel = self.carData.carlist[num].vel.getXY()
        newDatagram.addFloat32(vel[0])
        newDatagram.addFloat32(vel[1])
        newDatagram.addFloat32(self.carData.carlist[num].model.getH())
        for j in range(5):
            newDatagram.addBool(self.carData.carlist[num].input[j])
        newDatagram.addInt32(self.carData.carlist[num].hp)
        return newDatagram
    
    def getCollisionDatagrams(self):
        myDatagrams = []
        for data in self.carData.collisionlist:
            newDatagram = PyDatagram()
            newDatagram.addUint8(COLLIDED_MESSAGE)
            newDatagram.addUint8(data[0])
            newDatagram.addUint8(data[1])
            myDatagrams.append(newDatagram)
            if data[0] != 0:
                self.ignore.append(data[0])
        return myDatagrams
    
    def returnAllCars(self, connection):
        carPosDatagrams = [self.getCarPosDatagramFromCar(i) for i in range(len(self.carData.carlist))]
        for data in carPosDatagrams:
            self.cWriter.send(data, connection)
    
    def addNewCar(self):
        num = len(self.carData.carlist)
        self.carData.addCar()
        return self.getNewCarPosDatagram(num)




"""
print "test1"
server = Network()
run()
print "test2"
"""