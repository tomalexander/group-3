import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.distributed.PyDatagram import PyDatagram #for packaging data
from direct.distributed.PyDatagramIterator import PyDatagramIterator #for unpacking data
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
from direct.gui.OnscreenText import OnscreenText
from w_loader import w_loader
from w_loader import spawn_locations
import collisions
import sys, math, random

PRINT_MESSAGE = 1
CAR_MESSAGE = 2
COLLIDED_MESSAGE = 3
NEW_PLAYER_MESSAGE = 4
PLAYER_ASSIGNMENT_MESSAGE = 5
BEGIN_MESSAGE = 6
END_MESSAGE = 7
MAP_MESSAGE = 8


#Client connects to a game that is running a server
class Client(object):
    def __init__(self, cars, ip_address, playername):
        self.carHitSound = base.loader.loadSfx("Sounds/CRASH2.wav")
        self.startSound = base.loader.loadSfx("Sounds/ENGINESTART.wav")
        
        self.playername = playername
        
        self.carData = cars
        self.carData.index = -1
        
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        self.textWaitObject = OnscreenText(text="Waiting for players...", style=1, fg=(1,1,1,1), pos=(0.7,-0.95), scale = .07)
        
        self.port_address=9099  # same for client and server
         
         # a valid server URL. You can also use a DNS name
         # if the server has one, such as "localhost" or "panda3d.org"
        self.ip_address=ip_address
         
         # how long until we give up trying to reach the server?
        self.timeout_in_miliseconds=3000  # 3 seconds
        # make the connection
        self.myConnection = self.cManager.openTCPClientConnection(self.ip_address, self.port_address, self.timeout_in_miliseconds)
        if self.myConnection:
            self.cReader.addConnection(self.myConnection)  # receive messages from server
        else:
            print "No connection found!"
            sys.exit()
        # let the server know that a new car has joined the game
        self.cWriter.send(self.newPlayerMessage(), self.myConnection)
        taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
    
    def tskReaderPolling(self, taskdata):
        # sends/recieves data every frame
        self.updates = [() for i in self.carData.carlist]
        while self.cReader.dataAvailable():
            datagram=NetDatagram()  # catch the incoming data in this instance
            if self.cReader.getData(datagram):
                self.myProcessDataFunction(datagram) # handle the incoming data
        myCarDatagram = self.getPosDatagram()
        if myCarDatagram != None:
            self.cWriter.send(myCarDatagram, self.myConnection) # send the server your updated information
        return Task.cont
    
    def myProcessDataFunction(self, netDatagram):
        # check a message and do what it says
        myIterator = PyDatagramIterator(netDatagram)
        msgID = myIterator.getUint8()
        if msgID == PRINT_MESSAGE: # This is a debugging message
            messageToPrint = myIterator.getString()
            print messageToPrint
        elif msgID == PLAYER_ASSIGNMENT_MESSAGE: # This assigns the player to a car
            playerNum = myIterator.getUint8()
            self.carData.index = playerNum
            self.playername += " (%d)"%playerNum
            carXpos = myIterator.getFloat32()
            carYpos = myIterator.getFloat32()
            carXvel = myIterator.getFloat32()
            carYvel = myIterator.getFloat32()
            carHeading = myIterator.getFloat32()
            carInput = []
            for i in range(5):
                carInput.append(myIterator.getBool())
            carLights = myIterator.getBool()
            carHp = myIterator.getInt32()
            self.updatePositions(playerNum, (carXpos, carYpos, carXvel, carYvel, carHeading, carInput, carLights, carHp))
        elif msgID == CAR_MESSAGE: # This updates a car
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
                carLights = myIterator.getBool()
                carHp = myIterator.getInt32()
                self.updatePositions(carNum, (carXpos, carYpos, carXvel, carYvel, carHeading, carInput, carLights, carHp))
        elif msgID == COLLIDED_MESSAGE: # This runs car-car collisions
            collisionFrom = myIterator.getUint8()
            if collisionFrom == self.carData.index:
                self.carHitSound.play()
                self.doCarCollision(myIterator.getUint8())
                self.cWriter.send(self.verifyCollisionMessage(), self.myConnection)
        elif msgID == MAP_MESSAGE: # This sets the map
            map = myIterator.getString()
            print map
            world_loader = w_loader()
            world_loader.load_world(map)
            global spawn_locations
            self.carData.spos = spawn_locations
        elif msgID == BEGIN_MESSAGE: # This starts the game
            self.carData.go = True
            self.textWaitObject.destroy()
            self.startSound.play()
        elif msgID == END_MESSAGE: # This ends the game, and then displays the score on the second receipt
            self.carData.go = False
            num = myIterator.getInt32()
            if num == -1:
                scoreDatagram = self.scoreDatagram()
                self.cWriter.send(scoreDatagram, self.myConnection)
            else:
                textytext = "Most Numerous Deaths:"
                for i in range(num):
                    textytext += "\n\n%s: %d"%(myIterator.getString(), myIterator.getInt32())
                self.textScore = OnscreenText(text=textytext, style=1, fg=(1,1,1,1), pos=(0,0.9), scale = .08)
            
            
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
    
    def scoreDatagram(self):
        # Send the player's score
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(END_MESSAGE)
        myPyDatagram.addString(self.playername)
        myPyDatagram.addInt32(self.carData.carlist[self.carData.index].deaths)
        return myPyDatagram
    
    def verifyCollisionMessage(self):
        # Send an acknowledgement of the collision
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(COLLIDED_MESSAGE)
        myPyDatagram.addUint8(self.carData.index)
        return myPyDatagram
    
    def updatePositions(self, carNum, data):
        # set a car's properites, create it if it doesn't exist
        if len(self.carData.carlist) > carNum:
            self.carData.carlist[carNum].model.setPos(data[0], data[1], 0)
            self.carData.carlist[carNum].vel.setXY(data[2], data[3])
            self.carData.carlist[carNum].model.setH(data[4])
            self.carData.carlist[carNum].input = data[5]
            self.carData.carlist[carNum].setHeadlights(data[6])
            self.carData.carlist[carNum].hp = data[7]
        else:
            for i in range(len(self.carData.carlist), carNum+1):
                self.carData.addCar()
            self.carData.carlist[carNum].model.setPos(data[0], data[1], 0)
            self.carData.carlist[carNum].vel.setXY(data[2], data[3])
            self.carData.carlist[carNum].model.setH(data[4])
            self.carData.carlist[carNum].input = data[5]
            self.carData.carlist[carNum].setHeadlights(data[6])
            self.carData.carlist[carNum].hp = data[7]
    
    def getPosDatagram(self):
        # send player car data
        num = self.carData.index
        if num < 0:
            return None
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
        newDatagram.addBool(self.carData.carlist[num].lightsOn)
        newDatagram.addInt32(self.carData.carlist[num].hp)
        return newDatagram
    
    def doCarCollision(self, otherCarNum):
        collisions.collideCars(self.carData.carlist[self.carData.index], self.carData.carlist[otherCarNum])
