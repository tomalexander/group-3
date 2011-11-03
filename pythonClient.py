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
        self.playerNum = -1



class Client(object):
    def __init__(self, cars):
        self.carData = cars
        
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        
        self.port_address=9099  # same for client and server
         
         # a valid server URL. You can also use a DNS name
         # if the server has one, such as "localhost" or "panda3d.org"
        self.ip_address="localhost"
         
         # how long until we give up trying to reach the server?
        self.timeout_in_miliseconds=3000  # 3 seconds
         
        self.myConnection = self.cManager.openTCPClientConnection(self.ip_address, self.port_address, self.timeout_in_miliseconds)
        if self.myConnection:
            self.cReader.addConnection(self.myConnection)  # receive messages from server
        
        self.cWriter.send(self.newPlayerMessage(), self.myConnection)
        taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
    
    def tskReaderPolling(self, taskdata):
        while self.cReader.dataAvailable():
            datagram=NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            
            if self.cReader.getData(datagram):
                self.myProcessDataFunction(datagram)
        return Task.cont
    
    def myProcessDataFunction(self, netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        msgID = myIterator.getUint8()
        if msgID == PRINT_MESSAGE:
            messageToPrint = myIterator.getString()
            print messageToPrint
        elif msgID == PLAYER_ASSIGNMENT_MESSAGE:
            playerNum = myIterator.getUint8()
            self.carData.index = playerNum
        elif msgID == CAR_MESSAGE:
            carNum = myIterator.getUint8()
            if carNum != self.carData.index:
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
            
            
    def myNewPyDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(PRINT_MESSAGE)
        myPyDatagram.addString("Hello, world!")
        return myPyDatagram
    
    def newPlayerMessage(self):
        # Send a request to join the game
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(NEW_PLAYER_MESSAGE)
        return myPyDatagram
    
    def updatePositions(self, carNum, data):
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


"""
print "test1"
client = Client()
run()
print "test2"
"""