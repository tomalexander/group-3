from __future__ import division
from car import Car
from direct.showbase.DirectObject import DirectObject#for event handling
from direct.interval.IntervalGlobal import *#for compound intervals
from pandac.PandaModules import *#basic Panda modules
from direct.task import Task#for update fuctions
from direct.actor.Actor import Actor#for animated models
import sys, math
import pythonServer

class CarData(DirectObject):
    """Holds all the cars. All of them."""
    def __init__ (self, spos, index):#takes in a list of x,y tuples, there should be 4 of these
        self.spos = spos
        self.index = index
        self.carlist = []
        
        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, [0,True])
        self.accept("arrow_right", self.setKey, [1,True])
        self.accept("arrow_up", self.setKey, [2,True])
        self.accept("arrow_down", self.setKey, [3,True])
        self.accept("space", self.setKey, [4,True])
        self.accept("arrow_left-up", self.setKey, [0,False])
        self.accept("arrow_right-up", self.setKey, [1,False])
        self.accept("arrow_up-up", self.setKey, [2,False])
        self.accept("arrow_down-up", self.setKey, [3,False])
        self.accept("space-up", self.setKey, [4,False])
        
        taskMgr.add(self.move, "outtaThaWayImDrivingHere")
        self.prevtime = 0
        
    def addCar(self):
        pos = self.spos.pop()
        newcar = Car(pos[0], pos[1], (math.degrees(math.atan2(15-pos[0], 15-pos[1]))-90)%360)
        self.carlist.append(newcar)
        return newcar
        
    def setKey(self, ind, value):
        if self.index >= 0 and self.index < len(self.carlist):
            self.carlist[self.index].input[ind] = value
        
    def move(self, task):
        elapsed = task.time - self.prevtime
        for car in self.carlist:
            car.move(elapsed)
        
        #put in camera stuff car.x+ carvel.x*modify, similar for y , 2 + carvel.getM * modify
        if self.index >= 0 and self.index < len(self.carlist):
            camera.setPos(\
                self.carlist[self.index].model.getX() - self.carlist[self.index].vel.x * 4,\
                self.carlist[self.index].model.getY() - self.carlist[self.index].vel.y * 4,\
                self.carlist[self.index].model.getZ() + 75 - self.carlist[self.index].vel.getM()*15/2)
            camera.lookAt(self.carlist[self.index].model)
            camera.setP(camera.getP() + self.carlist[self.index].vel.getM()*2)
        
        self.prevtime = task.time
        return Task.cont
