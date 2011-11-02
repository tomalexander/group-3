import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.distributed.PyDatagram import PyDatagram #for packaging data
from direct.distributed.PyDatagramIterator import PyDatagramIterator #for unpacking data
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
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
    def __init__(self):
        self.carData = TempCarData()
        self.carUpdates = []
        
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
        myPyDatagram = self.myNewPyDatagram()  # build a datagram to send
        for aClient in self.activeConnections:
            self.cWriter.send(myPyDatagram, aClient)
        while self.cReader.dataAvailable():
            datagram=NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            if self.cReader.getData(datagram):
                self.myProcessDataFunction(datagram)
        carPosDatagrams = self.getCarPosDatagrams()
        collsionDatagrams = self.getCollisionDatagrams()
        for aClient in self.activeConnections:
            for data in carPosDatagrams:
                self.cWriter.send(data, aClient)
            for data in collisionDatagrams:
                self.cWriter.send(data, aClient)
        self.finalizeUpdates() #This will send the updates car positions to the game
        self.clearCarData() #This is to prevent redundant messages from being sent
        return Task.cont
    
    def myProcessDataFunction(self, netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        msgID = myIterator.getUint8()
        if msgID == PRINT_MESSAGE:
            messageToPrint = myIterator.getString()
            print messageToPrint
            print "\n"
        elif msgID == CAR_MESSAGE:
            carNum = myIterator.getUint8()
            carXpos = myIterator.getFloat32()
            carYpos = myIterator.getFloat32()
            carXvel = myIterator.getFloat32()
            carYvel = myIterator.getFloat32()
            carHeading = myIterator.getFloat32()
            carHp = myIterator.getInt32()
            self.updatePositions(carNum, (carXpos, carYpos, carXvel, carYvel, carHeading, carHp))

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
          
    def finalizeUpdates(self):
        for i in range(self.carUpdates):
            if self.carUpdates[i] != ():
                if len(self.carData.carData) > i
                    self.carData.carData[i] = self.carUpdates[i]
                else:
                    for i in range(len(self.carData.carData), i+1):
                        self.carData.carData.append(())
                    self.carData.carData[i] = self.carUpdates[i]
    
    def clearCarData(self):
        self.carUpdates = []
        self.carData.collisionData = []
    
    def getCarPosDatagrams(self):
        myDatagrams = []
        for i in range(len(self.carData.carData)):
            if self.carData.carData[i] != ():
                newDatagram = PyDatagram()
                newDatagram.addUint8(CAR_MESSAGE)
                newDatagram.addUint8(i)
                for j in range(5):
                    newDatagram.addFloat32(self.carData.carData[j])
                newDatagram.addInt32(self.carData.carData[5])
                myDatagrams.append(newDatagram)
        return myDatagrams
    
    def getCollisionDatagrams(self):
        myDatagrams = []
        for data in range(self.carData.collisionData):
            newDatagram = PyDatagram()
            newDatagram.addUint8(COLLIDED_MESSAGE)
            newDatagram.addUint8(data[0])
            newDatagram.addUint8(data[1])
            myDatagrams.append(newDatagram)
        return myDatagrams




#
print "test1"
server = Network()
run()
print "test2"