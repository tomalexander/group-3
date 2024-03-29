import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random
from w_loader import w_loader
from w_loader import spawn_locations
from terrain import terrain
from fog import *
from smoke_emitter import *
from carData import CarData
import pythonServer, pythonClient
from ping_server_browser import *

global panda_window_settings

set_panda_settings(panda_window_settings)

class World(DirectObject): #subclassing here is necessary to accept events
    def __init__(self):
        #WxPandaShell.__init__(self, fStartDirect=True)
        #turn off default mouse control, otherwise can't reposition camera
        base.disableMouse()
        self.setupLights()
        render.setShaderAuto() #turns on per-pixel lighting, normal mapping, etc (you probably want to use this)
        base.camLens.setFar(1500)
        
    def setupLights(self):
        #ambient light
        self.ambientLight = AmbientLight("ambientLight") #parameter is a name
        #four values, RGBA, Alpha is largely irrelevant, value [0,1]
        self.ambientLight.setColor((.04, .04, .04, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        #the nodepath that calls setLight is what gets illuminated by the light
        render.setLight(self.ambientLightNP)
        #call clearLight() to turn it off
        
w = World()
game_fog()
init_smoke()
#smoke_emitter(w.panda, 0, 0, 500)
global spawn_locations
if panda_window_settings["action"] == "host":
    w.cars = CarData([], 0)
    w.connection = pythonServer.Network(w.cars, panda_window_settings["game_time"], panda_window_settings["selected_map"], panda_window_settings["num_players"], panda_window_settings["player_name"])
    taskMgr.doMethodLater(10, ping_server_browser, 'ping_server_browser_daemon')
elif panda_window_settings["action"] == "join":
    print "Made it to client creation"
    w.cars = CarData([], -1)
    w.connection = pythonClient.Client(w.cars, panda_window_settings["ip"], panda_window_settings["player_name"])
run()
