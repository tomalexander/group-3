from direct.actor.Actor import Actor #for animated models

class trap:
    def __init__(self, _x, _y, _type):
        self.x = _x
        self.y = _y
        self.type = _type

    def load_model(self):
        self.model = Actor("models/panda-model", {"walk":"panda-walk4"})
        self.model.reparentTo(render)
        self.model.setScale(0.005)
        self.model.setPos(self.x, self.y, 0)

    def set_up_collision_handler_event(self):
        self.collision_handler = CollisionHandlerEvent()
        self.collision_handler.setInPattern("trap-%in")

    def set_up_collisions(self):
        collision_sphere = CollisionSphere((0,0,0), 500)
        collision_node = CollisionNode("trap")
        collision_node.addSolid(collision_sphere)
        collision_node_path = self.model.attachNewNode(collision_node)
        collision_node_path.show()
        #TODO add collision_node_path to collision traverser
        # Ex: collision_traverser.addCollider(collision_node_path, collision_handler)

        #TODO accept collisions
        #  Ex: self.accept("trap-panda", self.hit)

    def hit(self, collision_entry):
        pass #https://www.panda3d.org/manual/index.php/Collision_Entries
