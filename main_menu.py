import wx
import socket
import urllib2

panda_window_action = "none"
panda_window_ip_address = ""

class panda_window(wx.Frame):

    def __init__(self, parent, title):
        super(panda_window, self).__init__(parent, title=title, 
            size=(300, 360))
        global panda_window_action
        panda_window_action = "none"
        self.init_ui()
        self.Show()
        self.Centre()

    def init_ui(self):
        self.panel = wx.Panel(self, -1)
        self.label_ip_address = wx.StaticText(self.panel, label="Please Enter IP Address:", pos=(3,3))
        self.text_ip_address = wx.TextCtrl(self.panel, pos=(3,33), size=(290, 50))
        self.button_host = wx.Button(self.panel, 1, label="Host", pos=(3,90), size=(90, 28))
        self.button_connect = wx.Button(self.panel, 2, label="Connect", pos=(103,90), size=(90, 28))
        self.button_refresh = wx.Button(self.panel, 3, label="Refresh", pos=(203,90), size=(90, 28))
        self.Bind(wx.EVT_BUTTON, self.click_host, id=1)
        self.Bind(wx.EVT_BUTTON, self.click_connect, id=2)
        self.Bind(wx.EVT_BUTTON, self.click_refresh, id=3)
        self.server_list = wx.ListBox(self.panel, id=4, pos=(3,140), size=(280,200))
        wx.EVT_LISTBOX(self, 4, self.ip_selected)
        self.hosts = []
        self.get_ip_address()
        self.update_host_list()
        
    def get_ip_address(self):
        response = urllib2.urlopen('http://ip.paphus.com/')
        ip = response.read()
        self.text_ip_address.SetValue(ip)

    def start_game(self):
        self.Close(True)
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

    def click_refresh(self, event):
        self.update_host_list()

    def update_host_list(self):
        self.hosts = []
        response = urllib2.urlopen('http://ip.paphus.com/browser.php?action=gethosts')
        ip = response.read()
        self.hosts = [i for i in ip.split(" ") if i != ""]
        self.server_list.Set(self.hosts)

    def ip_selected(self, event):
        self.text_ip_address.SetValue(self.hosts[self.server_list.GetSelection()])
        
def run_main_menu():
    app = wx.App()
    main_menu = panda_window(None, title='Main Selection')
    app.MainLoop()
    execfile("load_tester.py", {"panda_window_action" : panda_window_action, "panda_window_ip_address" : panda_window_ip_address})

run_main_menu()
