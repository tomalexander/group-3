from direct.actor.Actor import Actor #for animated models
from direct.interval.ActorInterval import ActorInterval
from pandac.PandaModules import *    #basic Panda modules
from trap import *

class boost(trap):
    def __init__(self, _x, _y):
        trap.__init__(self, _x, _y, "boost")

    def load_model(self):
        self.model = loader.loadModel("models/booster.egg")
        self.model.reparentTo(render)
        self.model.setScale(5.7)
        self.model.setPos(self.x, self.y, 0)
        self.set_up_collisions()

    def set_up_collisions(self):
        self.collision_sphere = CollisionSphere((4.3,4.3,0), 4)
        self.collision_node = CollisionNode("boost")
        self.collision_node.addSolid(self.collision_sphere)
        self.collision_node_path = self.model.attachNewNode(self.collision_node)
        #self.collision_node_path.show()
