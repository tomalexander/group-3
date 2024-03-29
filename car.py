from __future__ import division
from velocity import Velocity
from pandac.PandaModules import *#basic Panda modules
from direct.showbase.DirectObject import DirectObject#for event handling
from direct.actor.Actor import Actor#for animated models
import sys, os, math
from smoke_emitter import *

class Car():
    """This is a car."""
    def __init__ (self, x=0, y=0, h=0, car=0):
        #mydir = os.path.abspath(sys.path[0])
        #mydir = Filename.fromOsSpecific(mydir).getFullpath()
        if car == 0:
            self.model = loader.loadModel("cars/bluecar.egg")
        elif car == 1:
            self.model = loader.loadModel("cars/redcar.egg")
        elif car == 2:
            self.model = loader.loadModel("cars/greencar.egg")
        else:
            self.model = loader.loadModel("cars/yellowcar.egg")
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
        self.deaths = 0
        self.input = [False for i in range(5)]#left, right, up, down, space

        #Attach Smoke
        self.s1 = False
        self.s2 = False
        self.s3 = False
        self.smoke1 = smoke_emitter(self.model, 1, 1, 1)
        self.smoke2 = smoke_emitter(self.model, -1, 0, 1)
        self.smoke3 = smoke_emitter(self.model, 0, 1, 0)
        
        
        
        #taskMgr.add(self.move, "outtaThaWayImDrivingHere")
        #self.prevtime = 0
        
        self.setUpHeadlights()
    
    def makeCollisionSolid(self, cTrav, cHandler, num):
        cSphere = CollisionSphere((0,0,0), 3)
        cNode = CollisionNode("car%d"%num)
        cNode.addSolid(cSphere)
        cNodePath = self.model.attachNewNode(cNode)
        #cNodePath.show()
        #registers a from object with the traverser with a corresponding handler
        cTrav.addCollider(cNodePath, cHandler)
    
    def setUpHeadlights(self):
        self.headlights = Spotlight("headlights")
        self.headlights.setColor(VBase4(1.2, 1.2, 1.2, 1))
        #self.headlights.setShadowCaster(True, 512, 512)
        self.headlights.setAttenuation(Point3(0.0001, 0, 0.00001))
        print self.headlights.getAttenuation().getX()
        print self.headlights.getAttenuation().getY()
        print self.headlights.getAttenuation().getZ()
        lens = PerspectiveLens()
        lens.setFov(70, 90)
        lens.setNear(2.0)
        self.headlights.setLens(lens)
        slnp = self.model.attachNewNode(self.headlights)
        slnp.setPos(0, -0.35, 1)
        slnp.setHpr(0,-2.5,0)
        render.setLight(slnp)
        self.overlights = DirectionalLight("overhead lights")
        self.overlights.setColor(VBase4(1, 1, 1, 1))
        oslnp = self.model.attachNewNode(self.overlights)
        oslnp.setHpr(180,-75,0)
        self.model.setLight(oslnp)
        self.lightsOn = True
    
    def toggleHeadlights(self):
        if self.lightsOn:
            self.headlights.setColor(VBase4(0, 0, 0, 1))
            self.overlights.setColor(VBase4(0, 0, 0, 1))
            self.lightsOn = False
        else:
            self.headlights.setColor(VBase4(1.2, 1.2, 1.2, 1))
            self.overlights.setColor(VBase4(1, 1, 1, 1))
            self.lightsOn = True
    
    def setHeadlights(self, val):
        if val != self.lightsOn:
            if self.lightsOn:
                self.headlights.setColor(VBase4(0, 0, 0, 1))
                self.overlights.setColor(VBase4(0, 0, 0, 1))
                self.lightsOn = False
            else:
                self.headlights.setColor(VBase4(1, 1, 1, 1))
                self.overlights.setColor(VBase4(1, 1, 1, 1))
                self.lightsOn = True
                
    def takeDamage(self, num):
        self.hp -= num
    
    def move(self, elapsed):
        #all these numbers need to be tested
        if self.hp < 25 and not self.s3:
            self.smoke3.p.show()
            self.s3 = True
        if self.hp < 50 and not self.s2:
            self.smoke2.p.show()
            self.s2 = True
        if self.hp < 75 and not self.s1:
            self.smoke1.p.show()
            self.s1 = True
        
        #position change
        self.model.setPos(self.model.getX() + self.vel.x * elapsed/.02, self.model.getY() + self.vel.y * elapsed/.02, 0)
        tempmag = self.vel.getM()
        self.vel.addDM(self.model.getH(), elapsed * 1)
        self.vel.setDM(self.vel.getD(), tempmag)
        if self.vel.getM() > 0:
            self.vel.setDM(self.vel.getD(), max(self.vel.getM() - (elapsed * (.5 + 2.5*self.input[4])),0))
        if self.input[2]:#up
            self.vel.addDM(self.model.getH(), elapsed * 4)
            self.vel.setDM(self.vel.getD(), min(self.vel.getM(), 5))#speed cap
        if self.input[3]:#down
            self.vel.addDM(self.model.getH(), elapsed * -4)
            self.vel.setDM(self.vel.getD(), min(self.vel.getM(), 5))#speed cap
        
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
        
