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
        self.model = loader.loadModel("models/car.egg")
        #self.model = Actor("models/panda-model")
        self.model.reparentTo(render)
        #self.model.setScale(.005)
        self.model.setScale(5.7)
        
        #things that matter
        self.model.setPos(x, y, 0)
        self.model.setH(h)
        self.vel = Velocity()
        self.turn = 0
        self.hp = 100
        self.input = [False for i in range(5)]#left, right, up, down, space
        
        #taskMgr.add(self.move, "outtaThaWayImDrivingHere")
        #self.prevtime = 0
        
        self.setUpHeadlights()
    
    def makeCollisionSolid(self, cTrav, cHandler, num):
        cSphere = CollisionSphere((0,0,0), 3)#because the panda is scaled way down, radius has to be huge
        cNode = CollisionNode("car%d"%num)
        cNode.addSolid(cSphere)
        cNodePath = self.model.attachNewNode(cNode)
        cNodePath.show()
        #registers a from object with the traverser with a corresponding handler
        cTrav.addCollider(cNodePath, cHandler)
    
    def setUpHeadlights(self):
        self.headlights = Spotlight("headlights")
        self.headlights.setColor(VBase4(1, 1, 1, 1))
        lens = PerspectiveLens()
        lens.setFov(90, 90)
        lens.setNear(2.0)
        self.headlights.setLens(lens)
        slnp = self.model.attachNewNode(self.headlights)
        slnp.setPos(0, -0.35, 0)
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
        #all these numbers need to be tested
        
        #position change
        self.model.setPos(self.model.getX() + self.vel.x * elapsed/.02, self.model.getY() + self.vel.y * elapsed/.02, 0)
        tempmag = self.vel.getM()
        self.vel.addDM(self.model.getH(), elapsed * 1)
        self.vel.setDM(self.vel.getD(), tempmag)
        if self.vel.getM() > 0:
            self.vel.setDM(self.vel.getD(), max(self.vel.getM() - (elapsed * (.5 + 2.5*self.input[4])),0))
        if self.input[2]:#up
            self.vel.addDM(self.model.getH(), elapsed * 4)
            self.vel.setDM(self.vel.getD(), min(self.vel.getM(), 4))#speed cap
        if self.input[3]:#down
            self.vel.addDM(self.model.getH(), elapsed * -4)
            self.vel.setDM(self.vel.getD(), min(self.vel.getM(), 4))#speed cap
        
        #turning
        self.model.setH(self.model.getH() + self.turn * elapsed/.02)
        if self.input[0]:#left
            self.turn += elapsed * (100 + self.vel.getM()*100/4) / 4
            self.turn = min(.02 * (100 + self.vel.getM()*100/4), self.turn)
            #self.model.setH(self.model.getH() + elapsed * (100 + self.vel.getM()*100/4))
        elif self.input[1]:#right
            self.turn -= elapsed * (100 + self.vel.getM()*100/4) / 4
            self.turn = max(-.02 * (100 + self.vel.getM()*100/4), self.turn)
            #self.model.setH(self.model.getH() - elapsed * (100 + self.vel.getM()*100/4))
        else:
            self.turn -= math.copysign(elapsed, self.turn) * (100 + self.vel.getM()*100/4) / 4
            if abs(self.turn) <= (elapsed * (100 + self.vel.getM()*100/4) / 4):
                self.turn = 0
        