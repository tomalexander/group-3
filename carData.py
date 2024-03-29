from __future__ import division
from velocity import Velocity
from car import Car
from direct.showbase.DirectObject import DirectObject#for event handling
from direct.interval.IntervalGlobal import *#for compound intervals
from pandac.PandaModules import *#basic Panda modules
from direct.task import Task#for update fuctions
from direct.actor.Actor import Actor#for animated models
import sys, math
import pythonServer
import collisions

MULCAM = 1.25

class CarData(DirectObject):
    """Holds all the cars. All of them."""
    def __init__ (self, spos, index):#takes in a list of x,y tuples, there should be 4 of these
        self.explosionSound = base.loader.loadSfx("Sounds/EXPLOSION.wav")
        self.headlightSound = base.loader.loadSfx("Sounds/HEADLIGHTS.WAV")
        self.rumbleSound = base.loader.loadSfx("Sounds/RUMBLE.wav")
        self.spikeSound = base.loader.loadSfx("Sounds/SPIKE.wav")
        self.boostSound = base.loader.loadSfx("Sounds/BOOST.wav")
        self.bumperSound = base.loader.loadSfx("Sounds/CRASH4.wav")
        
        self.spos = spos
        self.index = index
        self.carlist = []
        self.collisionlist = []
        
        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, [0,True])
        self.accept("arrow_right", self.setKey, [1,True])
        self.accept("arrow_up", self.setKey, [2,True])
        self.accept("arrow_down", self.setKey, [3,True])
        self.accept("z", self.setKey, [4,True])
        self.accept("arrow_left-up", self.setKey, [0,False])
        self.accept("arrow_right-up", self.setKey, [1,False])
        self.accept("arrow_up-up", self.setKey, [2,False])
        self.accept("arrow_down-up", self.setKey, [3,False])
        self.accept("z-up", self.setKey, [4,False])
        self.accept("space", self.toggleHeadlights)
        self.accept("hit-car", self.carCollision)
        
        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.setInPattern("hit-car")
        
        taskMgr.add(self.move, "outtaThaWayImDrivingHere")
        self.prevtime = 0
        self.go = False
        
    def addCar(self):
        pos = self.spos[len(self.carlist) % len(self.spos)]
        tempvel = Velocity(500 - pos[0], 500 - pos[1])
        newcar = Car(pos[0], pos[1], tempvel.getD(), len(self.carlist)%4)
        self.carlist.append(newcar)
        if self.index >= 0 and self.index == len(self.carlist) - 1:
            tempvel.setDM(newcar.model.getH(), -75)
            camera.setPos(\
                newcar.model.getX() + tempvel.x,\
                newcar.model.getY() + tempvel.y,\
                newcar.model.getZ() + 40)
            camera.lookAt(newcar.model)
            camera.setP(camera.getP() + 5)
            newcar.makeCollisionSolid(base.cTrav, self.cHandler, self.index)
        elif self.index == 0:
            newcar.makeCollisionSolid(base.cTrav, self.cHandler, len(self.carlist)-1)
        return newcar
        
    def setKey(self, ind, value):
        if self.index >= 0 and self.index < len(self.carlist):
            self.carlist[self.index].input[ind] = value
    
    def toggleHeadlights(self):
        if self.index >= 0 and self.index < len(self.carlist):
            self.carlist[self.index].toggleHeadlights()
            self.headlightSound.play()
        
    def move(self, task):
        if self.go:
            elapsed = task.time - self.prevtime
            for i in range(len(self.carlist)):
                self.carlist[i].move(elapsed)
                if self.carlist[i].hp <= 0:
                    self.carlist[i].smoke3.p.hide()
                    self.carlist[i].smoke2.p.hide()
                    self.carlist[i].smoke1.p.hide()
                    self.carlist[i].s1 = False
                    self.carlist[i].s2 = False
                    self.carlist[i].s3 = False
                    pos = self.spos[i%len(self.spos)]
                    self.carlist[i].model.setPos(pos[0], pos[1], 0)
                    tempvel = Velocity(500 - pos[0], 500 - pos[1])
                    self.carlist[i].model.setH(tempvel.getD())
                    self.carlist[i].vel.setXY(0,0)
                    self.carlist[i].deaths += 1
                    self.carlist[i].hp = 100
                    if i == self.index:
                        self.explosionSound.play()
            
            if self.index >= 0 and self.index < len(self.carlist):
                tempvel = Velocity()
                tempvel.setDM(self.carlist[self.index].model.getH(), -75 * MULCAM)
                tempvel.addDM(self.carlist[self.index].vel.getD(), self.carlist[self.index].vel.getM() * -10 / MULCAM)
                camera.setPos(\
                    self.carlist[self.index].model.getX() + tempvel.x,\
                    self.carlist[self.index].model.getY() + tempvel.y,\
                    self.carlist[self.index].model.getZ() + 40 + self.carlist[self.index].vel.getM() * -5 / MULCAM)
                camera.lookAt(self.carlist[self.index].model)
                camera.setP(camera.getP() + 5)
            
            self.prevtime = task.time
        return Task.cont

    def carCollision(self, cEntry):
        firstString = cEntry.getFromNodePath().getName()
        secondString = cEntry.getIntoNodePath().getName()
        first = int(firstString[3])
        print firstString
        print secondString
        if secondString[:3] == "car":
            second = int(secondString[3])
            print "CRASH!!!!"
            for pair in self.collisionlist:
                if pair[0] == first and pair[1] == second:
                    break
            else:
                self.collisionlist.append((first, second))
                self.collisionlist.append((second, first))
        elif secondString == "spikes":
            if first == self.index:
                self.carlist[self.index].takeDamage(25)
                self.spikeSound.play()
        elif secondString == "sticky":
            self.carlist[first].vel.setDM(self.carlist[first].vel.getD(), min(self.carlist[first].vel.getM(), 5/3))
            if first == self.index:
                self.rumbleSound.play()
        elif secondString == "boost":
            self.carlist[first].vel.addDM(self.carlist[first].model.getH(), 5)
            self.carlist[first].vel.setDM(self.carlist[first].vel.getD(), 5)
            if first == self.index:
                self.boostSound.play()
        elif secondString == "bumper":
            collisions.bumperCollision(self.carlist[first], cEntry.getIntoNodePath().getParent())
            if first == self.index:
                self.bumperSound.play()
        elif secondString == "pit":
            if first == self.index:
                self.carlist[self.index].takeDamage(125)
                
            
