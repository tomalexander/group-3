from direct.actor.Actor import Actor #for animated models
from direct.interval.ActorInterval import ActorInterval
from trap import *

class spike(trap):
    def __init__(self, _x, _y):
        trap.__init__(self, _x, _y, "spike")

    def load_model(self):
        self.model = Actor("models/spikeanimation.egg", {"act":"models/spikeanimation.egg"})
        self.model.reparentTo(render)
        self.model.setScale(5.7)
        self.model.setPos(self.x+25, self.y+25, -28)
        self.act_control = self.model.getAnimControl('act')
        self.act_control.setPlayRate(0.1)
        self.act_control.loop('act')
        #self.walkInterval = ActorInterval(self.model, 'act') 
        #loop and pause the animation from the beginning 
        #self.walkInterval.loop() 
        #self.model.play("act")
