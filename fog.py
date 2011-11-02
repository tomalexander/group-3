import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions

class game_fog():
    def __init__(self):
        self.fog = Fog("Fog Name")
        self.fog.setColor(.2,.2,.2)
        self.set_density(0.005)
        render.setFog(self.fog)

    def set_density(self, alpha):
        self.fog.setExpDensity(alpha)

    def clear_fog(self):
        render.clearFog()
