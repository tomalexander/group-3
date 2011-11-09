import w_loader
from direct.actor.Actor import Actor #for animated models
from terrain import *

class edge_tile(terrain):
    def __init__(self, _x, _y, _type, _w_loader):
        terrain.__init__(self, _x, _y, _type, _w_loader)
        
    def load_model(self):
        self.model = loader.loadModel("models/end_tile.egg")
        #self.model = Actor("models/tile.egg", {})
        self.model.reparentTo(render)
        self.model.setScale(5.7)
        self.model.setPos(self.x, self.y, .001)
