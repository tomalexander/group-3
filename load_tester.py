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
from ping_server_browser import *

world_loader = w_loader()
world_loader.load_world(1)

class World(DirectObject): #subclassing here is necessary to accept events
    def __init__(self):
        #WxPandaShell.__init__(self, fStartDirect=True)
        #turn off default mouse control, otherwise can't reposition camera
        base.disableMouse()
        self.setupLights()
        render.setShaderAuto() #turns on per-pixel lighting, normal mapping, etc (you probably want to use this)
        base.camLens.setFar(700)
        
    def setupLights(self):
        #ambient light
        self.ambientLight = AmbientLight("ambientLight") #parameter is a name
        #four values, RGBA, Alpha is largely irrelevant, value [0,1]
        self.ambientLight.setColor((.04, .04, .04, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        #the nodepath that calls setLight is what gets illuminated by the light
        render.setLight(self.ambientLightNP)
        #call clearLight() to turn it off
        
global panda_window_action, panda_window_ip_address
print panda_window_action, panda_window_ip_address
w = World()
game_fog()
init_smoke()
#smoke_emitter(w.panda, 0, 0, 500)
if panda_window_action == "host":
    w.cars = CarData([(0,0), (0,5), (5,5), (5,0)], 0)
    w.connection = pythonServer.Network(w.cars)
    taskMgr.doMethodLater(10, ping_server_browser, 'ping_server_browser_daemon')
elif panda_window_action == "connect":
    print "Made it to client creation"
    w.cars = CarData([(0,0), (0,5), (5,5), (5,0)], -1)
    w.connection = pythonClient.Client(w.cars, panda_window_ip_address)
run()
