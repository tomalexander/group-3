from __future__ import division
from direct.showbase.DirectObject import DirectObject#for event handling
from direct.interval.IntervalGlobal import *#for compound intervals
from pandac.PandaModules import *#basic Panda modules
from direct.task import Task#for update fuctions
from direct.actor.Actor import Actor#for animated models
import sys, math
import pythonServer
import pythonClient
import carData



DasKars = carData.CarData([(0,0), (5,5), (5,0), (0,5)], -1)

def makeServer():
    DeServer = pythonServer.Network(DasKars)
    run()
def makeClient():
    DeServer = pythonClient.Client(DasKars)
    run()