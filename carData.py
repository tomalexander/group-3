from __future__ import division
from pandac.PandaModules import *#basic Panda modules
from direct.interval.IntervalGlobal import *#for compound intervals
from direct.task import Task#for update fuctions
import math

class CarData():
    """Holds all the cars. All of them."""
    def __init__ (self, spos):#takes in a list of x,y tuples, there should be 4 of these
        self.spos = spos
        self.carlist = [Car(spos[0][0], spos[0][1], (math.degrees(math.atan2(15-spos[0][0], 15-spos[0][1]))-90)%360)]
        self.spos.pop(0)
        
        taskMgr.add(self.move, "outtaThaWayImDrivingHere")
        self.prevtime = 0
        
        return self.carlist[0]
        
    def addCar(self):
        pos = self.spos.pop()
        newcar = Car(pos[0][0], pos[0][1], (math.degrees(math.atan2(15-pos[0][0], 15-pos[0][1]))-90)%360)
        self.carlist.append(newcar)
        return newcar
        
    def move(self, task):
        elapsed = task.time - self.prevtime
        for car in self.carlist:
            car.move(elapsed)
        
        self.prevtime = task.time
        return Task.cont