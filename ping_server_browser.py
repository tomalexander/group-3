import socket
import urllib2
from direct.task import Task
import threading

class ping_handler(urllib2.HTTPHandler):
    def http_response(self, req, response):
        return response

def ping_server_browser(task):
    o = urllib2.build_opener(ping_handler())
    t = threading.Thread(target=o.open, args=('http://ip.paphus.com/browser.php?action=ping',))
    t.start()
    return task.again
