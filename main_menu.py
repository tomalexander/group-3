import wx
import socket
import urllib2

panda_window_action = "none"
panda_window_ip_address = ""

class panda_window(wx.Frame):

    def __init__(self, parent, title):
        super(panda_window, self).__init__(parent, title=title, 
            size=(260, 180))
        global panda_window_action
        panda_window_action = "none"
        self.init_ui()
        self.Show()
        self.Centre()

    def init_ui(self):
        self.panel = wx.Panel(self, -1)
        self.label_ip_address = wx.StaticText(self.panel, label="Please Enter IP Address:", pos=(3,3))
        self.text_ip_address = wx.TextCtrl(self.panel, pos=(3,33), size=(250, 50))
        self.button_host = wx.Button(self.panel, 1, label="Host", pos=(3,90), size=(90, 28))
        self.button_connect = wx.Button(self.panel, 2, label="Connect", pos=(103,90), size=(90, 28))
        self.Bind(wx.EVT_BUTTON, self.click_host, id=1)
        self.Bind(wx.EVT_BUTTON, self.click_connect, id=2)
        self.get_ip_address()
        
    def get_ip_address(self):
        response = urllib2.urlopen('http://ip.paphus.com/')
        ip = response.read()
        self.text_ip_address.SetValue(ip)

    def start_game(self):
        self.Destroy()

    def click_host(self, event):
        global panda_window_action
        panda_window_action = "host"
        self.start_game()

    def click_connect(self, event):
        global panda_window_action
        global panda_window_ip_address
        panda_window_ip_address = self.text_ip_address.GetValue()
        panda_window_action = "connect"
        self.start_game()

def run_main_menu():
    app = wx.App()
    main_menu = panda_window(None, title='Main Selection')
    app.MainLoop()
    print panda_window_action, panda_window_ip_address
    addr = socket.gethostbyname(socket.gethostname())
    print addr
