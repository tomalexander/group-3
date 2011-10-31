import w_loader

class terrain:
    def __init__(self, _x, _y, _type, _w_loader):
        self.x = _x
        self.y = _y
        self.type = _type
        self.w_loader = _w_loader;

    def load_model(self):
        self.model = Actor("models/panda-model", {"walk":"panda-walk4"})
        self.model.reparentTo(self.w_loader)
        self.model.setScale(0.005)
        self.model.setPos(self.x, self.y, 0)
