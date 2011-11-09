# Look at /usr/share/panda3d/samples/Particles
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup

def init_smoke():
    base.enableParticles()

class smoke_emitter():
    def __init__(self, parent, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z
        self.parent = parent
        self.p = ParticleEffect()
        self.load_config('steam.ptf')
        self.p.setScale(2)
        self.p.hide()

    def load_config(self, file_name):
        self.p.cleanup()
        self.p = ParticleEffect()
        self.p.loadConfig(file_name)
        self.p.start(render)
        self.p.setPos(self.x, self.y, self.z)
        self.p.reparentTo(self.parent)
