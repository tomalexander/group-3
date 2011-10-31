import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

PRINT_MESSAGE = 1

"""
A simple echo server
"""
"""
import socket

host = ''
port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
while 1:
    client, address = s.accept()
    data = client.recv(size)
    if data:
        client.send(data)
    client.close()  """

#
class Network(object):
    def __init__(self):
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
        return Task.cont
    
    def myProcessDataFunction(self, netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        msgID = myIterator.getUint8()
        if msgID == PRINT_MESSAGE:
            messageToPrint = myIterator.getString()
            print messageToPrint
            print "\n"

    def myNewPyDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(PRINT_MESSAGE)
        myPyDatagram.addString("Hello, world!")
        return myPyDatagram




#
print "test1"
server = Network()
run()
print "test2"

"""
cManager = QueuedConnectionManager()
cListener = QueuedConnectionListener(self.cManager, 0)
cReader = QueuedConnectionReader(self.cManager, 0)
cWriter = ConnectionWriter(self.cManager,0)
 
activeConnections=[] # We'll want to keep track of these later

port_address=9099 #No-other TCP/IP services are using this port
backlog=1000 #If we ignore 1,000 connection attempts, something is wrong!
tcpSocket = cManager.openTCPServerRendezvous(port_address,backlog)
 
cListener.addConnection(tcpSocket)

taskMgr.add(tskListenerPolling,"Poll the connection listener",-39)
taskMgr.add(tskReaderPolling,"Poll the connection reader",-40)

def tskListenerPolling(taskdata):
    if cListener.newConnectionAvailable():
     
        rendezvous = PointerToConnection()
        netAddress = NetAddress()
        newConnection = PointerToConnection()
     
        if cListener.getNewConnection(rendezvous,netAddress,newConnection):
            newConnection = newConnection.p()
            activeConnections.append(newConnection) # Remember connection
            cReader.addConnection(newConnection)     # Begin reading connection
    return Task.cont

def tskReaderPolling(taskdata):
    if cReader.dataAvailable():
        datagram=NetDatagram()  # catch the incoming data in this instance
        # Check the return value; if we were threaded, someone else could have
        # snagged this data before we did
        if cReader.getData(datagram):
            myProcessDataFunction(datagram)
    return Task.cont

def myProcessDataFunction(netDatagram):
    myIterator = PyDatagramIterator(netDatagram)
    msgID = myIterator.getUint8()
    if msgID == PRINT_MESSAGE:
        messageToPrint = myIterator.getString()
        print messageToPrint
"""