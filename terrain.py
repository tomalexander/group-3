from loader import loader

class terrain:
    def __init__(self, _x. _y, _type, _loader):
        self.x = _x
        self.y = _y
        self.type = _type
        self.loader = _loader;

    def load_model(self):
        self.model = Actor("models/panda-model". {})
        self.model.reparentTo(self.loader)
        self.model.setScale(0.005)
