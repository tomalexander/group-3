import socket
import urllib
import urllib2
from direct.task import Task
import threading

panda_settings = {}

class ping_handler(urllib2.HTTPHandler):
    def http_response(self, req, response):
        return response

def ping_server_browser(task):
    global panda_settings
    o = urllib2.build_opener(ping_handler())
    t = threading.Thread(target=o.open, args=('http://ip.paphus.com/browser.php?action=ping&name=' + urllib.quote(panda_settings["player_name"]),))
    t.start()
    return task.again

def set_panda_settings(data):
    global panda_settings
    panda_settings = data
