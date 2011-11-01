from __future__ import division
import math

#0 degrees is in the direction of increasing y

####################
#^        0        #
#|        |        #
#|        |        #
#y 90-----O----270 #
#|        |        #
#|        |        #
#|       180       #
#0--------x------> #
####################

class Velocity():
    """A class for holding a two dimentional velocity"""
    def __init__(self, x=0, y=0):
        self.setXY(x, y)
        
    def setXY(self, x, y):
        self.x = x
        self.y = y
        
    def setDM(self, deg, mag):
        rad = math.radians((deg+90) % 360)#plus 90 because of what panda3d thinks is 0 degrees
        self.setXY(mag*math.cos(rad), mag*math.sin(rad))
        
    def getXY(self):
        return (self.x, self.y)
        
    def getD(self):
        return (math.degrees(math.atan2(self.y,self.x))-90) % 360
        
    def getM(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
        
    def getDM(self):
        return (self.getD(), self.getM())
        
    def addXY(self, x, y):
        self.x += x
        self.y += y
        
    def addDM(self, deg, mag):
        temp = ocity()
        temp.setDM(deg, mag)
        self.addXY(temp.x, temp.y)