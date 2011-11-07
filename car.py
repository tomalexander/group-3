from __future__ import division
from velocity import Velocity
from pandac.PandaModules import *#basic Panda modules
from direct.showbase.DirectObject import DirectObject#for event handling
from direct.actor.Actor import Actor#for animated models
import sys, os, math

class Car():
    """This is a car."""
    def __init__ (self, x=0, y=0, h=0):
        #mydir = os.path.abspath(sys.path[0])
        #mydir = Filename.fromOsSpecific(mydir).getFullpath()
        #self.model = loader.loadModel(mydir + "/models/newcar.egg")
        self.model = Actor("models/panda-model")
        self.model.reparentTo(render)
        self.model.setScale(.005)
        
        #things that matter
        self.model.setPos(x, y, 0)
        self.model.setH(h)
        self.vel = Velocity()
        self.hp = 100
        self.input = [False for i in range(5)]#left, right, up, down, space
        
        #taskMgr.add(self.move, "outtaThaWayImDrivingHere")
        #self.prevtime = 0
        
        self.setUpHeadlights()
    
    def setUpHeadlights(self):
        self.headlights = Spotlight("headlights")
        self.headlights.setColor(VBase4(1, 1, 1, 1))
        lens = PerspectiveLens()
        lens.setFov(90, 60)
        self.headlights.setLens(lens)
        slnp = self.model.attachNewNode(self.headlights)
        slnp.setPos(0, 0, 0)
        slnp.setHpr(0,0,0)
        render.setLight(slnp)
        self.lightsOn = True
    
    def toggleHeadlights(self):
        if self.lightsOn:
            self.headlights.setColor(VBase4(0, 0, 0, 1))
            self.lightsOn = False
        else:
            self.headlights.setColor(VBase4(1, 1, 1, 1))
            self.lightsOn = True
    
    def move(self, elapsed):
        #elapsed = task.time - self.prevtime
        
        #all these numbers need to be tested
        if self.input[0]:#left
            self.model.setH(self.model.getH() + elapsed * 200)#maybe multiply by speed?
        if self.input[1]:#right
            self.model.setH(self.model.getH() - elapsed * 200)
        tempmag = self.vel.getM()
        self.vel.addDM(self.model.getH(), elapsed * 1)
        self.vel.setDM(self.vel.getD(), tempmag)
        if self.input[2]:#up
            self.vel.addDM(self.model.getH(), elapsed * 4)
            self.vel.setDM(self.vel.getD(), min(self.vel.getM(), 2))#speed cap
        if self.input[3]:#down
            self.vel.addDM(self.model.getH(), elapsed * -4)
            self.vel.setDM(self.vel.getD(), min(self.vel.getM(), 2))#speed cap
        #self.vel.setDM(self.vel.getD(), self.vel.getM()*math.pow(1-(.02+.13*self.input[4]),elapsed))#friction
        if self.vel.getM() > 0:
            self.vel.setDM(self.vel.getD(), max(self.vel.getM() - (elapsed * (.5 + 1.5*self.input[4])),0))
        
        self.model.setPos(self.model.getX() + self.vel.x, self.model.getY() + self.vel.y, 0)
        
        #self.prevtime = task.time
        #return Task.cont