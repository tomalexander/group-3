from direct.actor.Actor import Actor #for animated models
from direct.interval.ActorInterval import ActorInterval
from pandac.PandaModules import *    #basic Panda modules
from trap import *

class sticky(trap):
    def __init__(self, _x, _y):
        trap.__init__(self, _x, _y, "sticky")

    def load_model(self):
        self.model = loader.loadModel("models/sticky.egg")
        self.model.reparentTo(render)
        self.model.setScale(5.7)
        self.model.setPos(self.x+25, self.y+25, -28.5)
        self.set_up_collisions()

    def set_up_collisions(self):
        self.collision_sphere = CollisionSphere((0,0,0), 6.5)
        self.collision_node = CollisionNode("sticky")
        self.collision_node.addSolid(self.collision_sphere)
        self.collision_node_path = self.model.attachNewNode(self.collision_node)
        #self.collision_node_path.show()
