from direct.actor.Actor import Actor #for animated models
from trap import *

class spike(trap):
    def __init__(self, _x, _y):
        trap.__init__(self, _x, _y, "spike")

    def load_model(self):
        self.model = Actor("models/spikeanimation.egg", {"act":"spikeanimation_temp"})
        self.model.reparentTo(render)
        self.model.setScale(5.7)
        self.model.setPos(self.x+25, self.y+25, -28)
