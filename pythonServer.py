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

def pairsort(list):
    for i in range(len(list)):
        for k in range(len(list) - i - 1):
            if list[k][1] > list[k+1][1]:
                temp = list[k]
                list[k] = list[k+1]
                list[k+1] = temp
    return list


class Network(object):
    def __init__(self, cars, time, map, players, playername):
        self.carHitSound = base.loader.loadSfx("Sounds/CRASH2.wav")
        self.startSound = base.loader.loadSfx("Sounds/ENGINESTART.wav")
        
        self.time = time
        self.map = map
        self.players = players
        self.playername = playername
        self.playername += " (0)"
        self.playerscores = []
        self.timer = -1
        
        world_loader = w_loader()
        world_loader.load_world(map)
        
        self.textWaitObject = OnscreenText(text="Waiting for players...", style=1, fg=(1,1,1,1), pos=(0.7,-0.95), scale = .07)
        
        global spawn_locations
        
        self.carData = cars
        self.carData.spos = spawn_locations
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
        # if a new connection is made, add it to the list
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
        # every frame, read messages, and then send out updates to all clients
        selfCarDatagram = self.getCarPosDatagramFromCar(self.carData.index) # add self to list of updates
        self.myProcessDataFunction(selfCarDatagram)
        # loop through all messages recieved
        while self.cReader.dataAvailable():
            datagram=NetDatagram()  # catch the incoming data in this instance
            if self.cReader.getData(datagram):
                self.myProcessDataFunction(datagram) # handle the message
        #send out car and collision messages
        carPosDatagrams = self.getCarPosDatagrams()
        collisionDatagrams = self.getCollisionDatagrams()
        for aClient in self.activeConnections:
            for data in carPosDatagrams:
                self.cWriter.send(data, aClient)
            for data in collisionDatagrams:
                self.cWriter.send(data, aClient)
        # start game if enough players have joined
        if self.timer == -1 and self.carData.go == False and len(self.carData.carlist) >= self.players:
            startDatagram = self.startDatagram()
            for aClient in self.activeConnections:
                self.cWriter.send(startDatagram, aClient)
            self.carData.go = True
            self.textWaitObject.destroy()
            self.timer = taskdata.time
            self.startSound.play()
        # run collisions
        for pair in self.carData.collisionlist:
            if pair[0] < pair[1]:
                if pair[0] == 0:
                    self.carHitSound.play()
                collisions.collideCars(self.carData.carlist[pair[0]], self.carData.carlist[pair[1]])
        # if time is up, end game and print scores
        if self.timer >= 0 and taskdata.time > self.timer + self.time * 60:
            if self.carData.go:
                self.carData.go = False
                self.playerscores.append((self.playername, self.carData.carlist[self.carData.index].deaths))
                stopDatagram = self.stopDatagram()
                for aClient in self.activeConnections:
                    self.cWriter.send(stopDatagram, aClient)
            elif len(self.playerscores) >= len(self.carData.carlist) or (taskdata.time > self.timer + self.time * 60 + 15 and self.playerscores != []):
                self.playerscores = pairsort(self.playerscores)
                textytext = "Most Numerous Deaths:"
                for pair in self.playerscores:
                    textytext += "\n\n%s: %d"%pair
                self.textScore = OnscreenText(text=textytext, style=1, fg=(1,1,1,1), pos=(0,0.9), scale = .08)
                scoreDatagram = self.scoreDatagram()
                for aClient in self.activeConnections:
                    self.cWriter.send(scoreDatagram, aClient)
                self.playerscores = []
                
        self.carData.collisionlist = []
        self.clearCarData() #This is to prevent redundant messages from being sent
        return Task.cont
    
    def myProcessDataFunction(self, netDatagram):
        # check a message and do what it says
        myIterator = PyDatagramIterator(netDatagram)
        msgID = myIterator.getUint8()
        if msgID == PRINT_MESSAGE: # This is a debugging message
            messageToPrint = myIterator.getString()
            print messageToPrint
        elif msgID == CAR_MESSAGE: # This updates a car
            carNum = myIterator.getUint8()
            for num in self.ignore: # if the car message is out of date, ignore it
                if num == carNum:
                    break
            else: # else update the car
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
        elif msgID == NEW_PLAYER_MESSAGE: # This creates a new player
            if len(self.carData.carlist) >= self.players:
                self.cWriter.send(self.startDatagram(), netDatagram.getConnection())
            self.cWriter.send(self.mapDatagram(), netDatagram.getConnection())
            self.cWriter.send(self.addNewCar(), netDatagram.getConnection())
            self.returnAllCars(netDatagram.getConnection())
        elif msgID == COLLIDED_MESSAGE: # This verifies that a car has recieved its collision message and is now up to date
            carNum = myIterator.getUint8()
            self.ignore.remove(carNum)
        elif msgID == END_MESSAGE: # This recieves a player score
            self.playerscores.append((myIterator.getString(), myIterator.getInt32()))
            

    def myNewPyDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(PRINT_MESSAGE)
        myPyDatagram.addString("Hello, world!")
        return myPyDatagram
    
    def startDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(BEGIN_MESSAGE)
        return myPyDatagram
        
    def stopDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(END_MESSAGE)
        myPyDatagram.addInt32(-1)
        return myPyDatagram
    
    def scoreDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(END_MESSAGE)
        myPyDatagram.addInt32(len(self.playerscores))
        for pair in self.playerscores:
            myPyDatagram.addString(pair[0])
            myPyDatagram.addInt32(pair[1])
        return myPyDatagram
    
    def mapDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(MAP_MESSAGE)
        myPyDatagram.addString(self.map)
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
    
    def getCarPosDatagrams(self):
        # makes a list of datagrams for each car that updated this frame
        myDatagrams = []
        for i in range(len(self.carUpdates)):
            if self.carUpdates[i] != ():
                newDatagram = self.getCarPosDatagram(i, self.carUpdates[i])
                myDatagrams.append(newDatagram)
        return myDatagrams
    
    def getCarPosDatagram(self, num, data):
        # creates a car_message datagram from data
        newDatagram = PyDatagram()
        newDatagram.addUint8(CAR_MESSAGE)
        newDatagram.addUint8(num)
        for j in range(5):
            newDatagram.addFloat32(float(data[j]))
        for j in range(5):
            newDatagram.addBool(data[5][j])
        newDatagram.addBool(data[6])
        newDatagram.addInt32(data[7])
        return newDatagram
    
    def getCarPosDatagramFromCar(self, num):
        # creates a car_message datagram from the entry in carData (used to get new cars up to date)
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
    
    def getNewCarPosDatagram(self, num):
        # same as getCarPosDatagramFromCar, but is a player_assignment_message
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
        newDatagram.addBool(self.carData.carlist[num].lightsOn)
        newDatagram.addInt32(self.carData.carlist[num].hp)
        return newDatagram
    
    def getCollisionDatagrams(self):
        # returns a list of collision datagrams
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
        # sends a car_message for each car in carData to a new connection
        carPosDatagrams = [self.getCarPosDatagramFromCar(i) for i in range(len(self.carData.carlist))]
        for data in carPosDatagrams:
            self.cWriter.send(data, connection)
    
    def addNewCar(self):
        num = len(self.carData.carlist)
        self.carData.addCar()
        return self.getNewCarPosDatagram(num)


