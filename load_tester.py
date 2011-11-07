import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random
from w_loader import w_loader
from terrain import terrain
from fog import *
from smoke_emitter import *
from carData import CarData
import pythonServer, pythonClient

world_loader = w_loader()
world_loader.load_world(1)

class World(DirectObject): #subclassing here is necessary to accept events
    def __init__(self):
        #WxPandaShell.__init__(self, fStartDirect=True) 
        #turn off default mouse control, otherwise can't reposition camera
        base.disableMouse()
        camera.setPosHpr(0, -15, 7, 0, -15, 0)
        self.loadModels()
        self.setupLights()
        self.setupCollisions()
        render.setShaderAuto() #turns on per-pixel lighting, normal mapping, etc (you probably want to use this)
        self.keyMap = {"left":0, "right":0, "forward":0}
        taskMgr.add(self.move, "moveTask")
        self.prevtime = 0
        self.ismoving = False
        self.accept("escape", sys.exit)
        self.accept("arrow_up", self.setKey, ["forward", 1])
        self.accept("arrow_right", self.setKey, ["right", 1])
        self.accept("arrow_left", self.setKey, ["left", 1])
        self.accept("arrow_up-up", self.setKey, ["forward", 0])
        self.accept("arrow_right-up", self.setKey, ["right", 0])
        self.accept("arrow_left-up", self.setKey, ["left", 0])
        #"mouse1" is left mouse button is clicked
        #append "-up" for equivalent of for equivalent of KEYUP event
        self.accept("ate-smiley", self.eat)
        base.camLens.setFar(700)
    
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def loadModels(self):
        """loads initial models into the world."""
        self.panda = Actor("models/panda-model", {"walk":"panda-walk4", "eat":"panda-eat"})
        self.panda.reparentTo(render)
        self.panda.setScale(0.005)
        self.panda.setH(180)
        self.env = loader.loadModel("models/environment")
        self.env.reparentTo(render)
        self.env.setScale(.25)
        self.env.setPos(-8, 42, 0)
        self.env.hide()
        
        #load targets
        self.targets = []
        for i in range(10):
            target = loader.loadModel("smiley")
            target.setScale(.5)
            target.setPos(random.uniform(-20, 20), random.uniform(-15, 15), 2)
            target.reparentTo(render)
            self.targets.append(target)
    
    def setupLights(self):
        #ambient light
        self.ambientLight = AmbientLight("ambientLight") #parameter is a name
        #four values, RGBA, Alpha is largely irrelevant, value [0,1]
        self.ambientLight.setColor((.05, .05, .05, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        #the nodepath that calls setLight is what gets illuminated by the light
        render.setLight(self.ambientLightNP)
        #call clearLight() to turn it off
        
        self.keyLight = DirectionalLight("keyLight")
        self.keyLight.setColor((.1, .1, .1, 1))
        self.keyLightNP = render.attachNewNode(self.keyLight)
        self.keyLightNP.setHpr(0, -26, 0)
        render.setLight(self.keyLightNP)
        
        self.fillLight = DirectionalLight("fillLight")
        self.fillLight.setColor((.03, .03, .03, 1))
        self.fillLightNP = render.attachNewNode(self.fillLight)
        self.fillLightNP.setHpr(30, 0, 0)
        render.setLight(self.fillLightNP)
    
    def walk(self):
        """compound interval for walking"""
        #self.pandaWalk = self.panda.posInterval(1, (0, -5, 0))
        #some interval methods:
        #start(), loop(), pause(), resume(), finish()
        #start() can take arguments: start(starttime, endtime, playrate)
        dist = 5
        angle = deg2Rad(self.panda.getH())
        dx = dist * math.sin(angle)
        dy = dist * -math.cos(angle)
        pandaWalk = Parallel(self.panda.posInterval(1, (self.panda.getX()+dx, self.panda.getY()+dy, 0)), \
            self.panda.actorInterval("walk", loop=1, duration=1))
        pandaWalk.start()
    
    def turn(self, direction):
        pandaTurn = self.panda.hprInterval(.2, (self.panda.getH() - (10*direction), 0, 0))
        pandaTurn.start()
    
    def move(self, task):
        elapsed = task.time - self.prevtime
        #camera.lookAt(self.panda)
        if self.keyMap["left"]:
            self.panda.setH(self.panda.getH() + elapsed*100)
        if self.keyMap["right"]:
            self.panda.setH(self.panda.getH() - elapsed*100)
        if self.keyMap["forward"]:
            dist = 15 * elapsed
            angle = deg2Rad(self.panda.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.panda.setPos(self.panda.getX()+dx, self.panda.getY()+dy, 0)
        if self.keyMap["left"] or self.keyMap["right"] or self.keyMap["forward"]:
            if self.ismoving == False:
                self.ismoving = True
                self.panda.loop("walk")
        else:
            if self.ismoving:
                self.ismoving = False
                self.panda.stop()
                self.panda.pose("walk",4)
                
        self.prevtime = task.time
        return Task.cont
    
    def setupCollisions(self):
        #instantiates a collision traverser and sets it to the default
        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        #set pattern for event sent on collision
        #"%in" is substituted with the name of the into object
        self.cHandler.setInPattern("ate-%in")
        
        cSphere = CollisionSphere((0,0,0), 500)#because the panda is scaled way down, radius has to be huge
        cNode = CollisionNode("panda")
        cNode.addSolid(cSphere)
        cNode.setIntoCollideMask(BitMask32.allOff())#panda is *only* a from object
        cNodePath = self.panda.attachNewNode(cNode)
        #cNodePath.show()
        #registers a from object with the traverser with a corresponding handler
        base.cTrav.addCollider(cNodePath, self.cHandler)
        
        for target in self.targets:
            cSphere = CollisionSphere((0,0,0), 2)
            cNode = CollisionNode("smiley")
            cNode.addSolid(cSphere)
            cNodePath = target.attachNewNode(cNode)
            #cNodePath.show()
    
    def eat(self, cEntry):
        """handles panda eating a smiley"""
        #remove target from list of targets
        self.targets.remove(cEntry.getIntoNodePath().getParent())
        #remove from scene graph
        cEntry.getIntoNodePath().getParent().remove()
        self.panda.play("eat")


global panda_window_action, panda_window_ip_address
print panda_window_action, panda_window_ip_address
w = World()
game_fog()
init_smoke()
smoke_emitter(w.panda, 0, 0, 500)
if panda_window_action == "host":
    w.cars = CarData([(0,0), (0,5), (5,5), (5,0)], 0)
    w.connection = pythonServer.Network(w.cars)
elif panda_window_action == "connect":
    print "Made it to client creation"
    w.cars = CarData([(0,0), (0,5), (5,5), (5,0)], -1)
    w.connection = pythonClient.Client(w.cars, panda_window_ip_address)
run()
