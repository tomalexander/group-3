from __future__ import division
from velocity import Velocity
from pandac.PandaModules import *#basic Panda modules
from direct.showbase.DirectObject import DirectObject#for event handling
from direct.actor.Actor import Actor#for animated models

class Car():
    """This is a car."""
    def __init__ (self, x=0, y=0, h=0):
        self.model = Actor("models/panda-model")
        self.model.reparentTo(render)
        self.model.setScale(.005)
        
        self.model.setPos(x, y, 0)
        self.model.setH(h)
        self.vel = Velocity()
        self.hp = 100
        self.input = [False for i in range(5)]#left, right, up, down, space
        
        #taskMgr.add(self.move, "outtaThaWayImDrivingHere")
        #self.prevtime = 0
        
    def move(self, elapsed):
        #elapsed = task.time - self.prevtime
        
        #all these numbers need to be tested
        if self.input[0]:#left
            self.model.setH(self.model.getH() + elapsed * 200)#maybe multiply by speed?
        if self.input[1]:#right
            self.model.setH(self.model.getH() - elapsed * 200)
        if self.input[2]:#up
            self.vel.addDM(self.model.getH(), elapsed * 150)
            self.vel.setDM(self.vel.getD(), min(self.vel.getM(), 50))#speed cap
        if self.input[3]:#down
            self.vel.addDM(self.model.getH(), elapsed * -150)
            self.vel.setDM(self.vel.getD(), min(self.vel.getM(), 50))#speed cap
        self.vel.setDM(self.vel.getD(), self.vel.getM()*(1-.1-.2*self.input[4]))#friction
            
        self.model.setPos(self.model.getX() + self.vel.x, self.model.getY() + self.vel.y, 0)
        
        #self.prevtime = task.time
        return Task.cont