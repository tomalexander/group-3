from direct.actor.Actor import Actor #for animated models
from direct.interval.ActorInterval import ActorInterval
from pandac.PandaModules import *    #basic Panda modules
from trap import *

class spike(trap):
    def __init__(self, _x, _y):
        trap.__init__(self, _x, _y, "spike")

    def load_model(self):
        self.model = Actor("models/spikes.egg", {"act":"models/spikes.egg"})
        self.model.reparentTo(render)
        self.model.setScale(5.7)
        self.model.setPos(self.x+25, self.y+25, 0)
        #self.act_control = self.model.getAnimControl('act')
        #self.act_control.setPlayRate(0.5)
        #self.act_control.loop('act')
        self.model.loop('act')
        self.set_up_collisions()
        #self.model.play("act")

    def set_up_collisions(self):
        self.collision_sphere = CollisionSphere((0,0,0), 4.5)
        self.collision_node = CollisionNode("spikes")
        self.collision_node.addSolid(self.collision_sphere)
        self.collision_node_path = self.model.attachNewNode(self.collision_node)
        #self.collision_node_path.show()
