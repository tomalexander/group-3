from direct.actor.Actor import Actor #for animated models
from direct.interval.ActorInterval import ActorInterval
from pandac.PandaModules import *    #basic Panda modules
from trap import *

class bumper(trap):
    def __init__(self, _x, _y):
        trap.__init__(self, _x, _y, "bumper")

    def load_model(self):
        self.model = loader.loadModel("models/bumperforeal.egg")
        self.model.reparentTo(render)
        self.model.setScale(5.7)
        self.model.setPos(self.x+25, self.y+25, 0)
        self.set_up_collisions()

    def set_up_collisions(self):
        self.collision_body = CollisionTube(-3.5,-3.5,.5,3.5,-3.5,.5,1.2)
        #self.collision_sphere = CollisionSphere((0,0,0), 6.5)
        self.collision_node = CollisionNode("bumper")
        self.collision_node.addSolid(self.collision_body)
        self.collision_node_path = self.model.attachNewNode(self.collision_node)
        self.collision_node_path.show()
