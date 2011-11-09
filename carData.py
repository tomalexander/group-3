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
        
    def addCar(self):
        pos = self.spos[len(self.carlist) % len(self.spos)]
        tempvel = Velocity(500 - pos[0], 500 - pos[1])
        newcar = Car(pos[0], pos[1], tempvel.getD())
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
        
    def move(self, task):
        elapsed = task.time - self.prevtime
        for i in range(len(self.carlist)):
            self.carlist[i].move(elapsed)
            if self.carlist[i].hp < 0:
                pos = self.spos[i%len(self.spos)]
                self.carlist[i].model.setPos(pos[0], pos[1], 0)
                self.carlist[i].model.setH((math.degrees(math.atan2(500-pos[0], 500-pos[1]))-90)%360)
                self.carlist[i].vel.setDM(0,0)
                self.carlist[i].deaths += 1
                self.carlist[i].hp = 100
        
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
        print firstString
        print secondString
        if secondString[:3] == "car":
            first = int(firstString[3])
            second = int(secondString[3])
            print "CRASH!!!!"
            for pair in self.collisionlist:
                if pair[0] == first and pair[1] == second:
                    break
            else:
                self.collisionlist.append((first, second))
                self.collisionlist.append((second, first))
        elif secondString == "spikes":
            if int(firstString[3]) == self.index:
                self.carlist[self.index].takeDamage(25)
        elif secondString == "sticky":
            self.carlist[self.index].vel.setDM(self.carlist[self.index].vel.getD(), self.carlist[self.index].vel.getM()/3)
        elif secondString == "bumper":
            collisions.bumperCollision(self.carlist[int(firstString[3])], cEntry.getIntoNodePath().getParent())
                
            