import wx
import socket
import urllib2
import os

panda_window_action = "none"
panda_window_ip_address = ""

class panda_window(wx.Frame):

    def __init__(self, parent, title):
        super(panda_window, self).__init__(parent, title=title, 
            size=(600, 560))
        global panda_window_action
        panda_window_action = "none"
        self.init_ui()
        self.Show()
        self.Centre()

    def init_ui(self):
        self.panel = wx.Panel(self, -1)
        self.set_join_gui()
        
        self.ln = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL, pos=(300,0))
        self.ln.SetSize((30,560))

        self.set_host_gui()
        
        self.hosts = []
        self.maps = []
        self.update_map_list()
        self.get_ip_address()
        self.update_host_list()
        self.update_map_list()

    def set_host_gui(self):
        self.map_list = wx.ComboBox(self.panel, id=5, pos=(330,160), size=(150,50), style=wx.CB_DROPDOWN)
        self.label_host = wx.StaticText(self.panel, label="Hosting", pos=(318,3))
        self.label_host.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.label_game_name = wx.StaticText(self.panel, label="Game Name:", pos=(318,23))
        self.button_host = wx.Button(self.panel, 1, label="Host", pos=(312,140), size=(90, 28))
        self.Bind(wx.EVT_BUTTON, self.click_host, id=1)
        

    def set_join_gui(self):
        self.label_join = wx.StaticText(self.panel, label="Join", pos=(18,3))
        self.label_join.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.label_ip_address = wx.StaticText(self.panel, label="Please Enter IP Address:", pos=(12,60))
        self.text_ip_address = wx.TextCtrl(self.panel, pos=(12,83), size=(290, 50))
        self.button_connect = wx.Button(self.panel, 2, label="Connect", pos=(12,140), size=(100, 28))
        self.button_refresh = wx.Button(self.panel, 3, label="Refresh", pos=(203,140), size=(90, 28))
        self.Bind(wx.EVT_BUTTON, self.click_host, id=1)
        self.Bind(wx.EVT_BUTTON, self.click_connect, id=2)
        self.label_ip_address = wx.StaticText(self.panel, label="Running Servers:", pos=(12,180))
        self.server_list = wx.ListBox(self.panel, id=4, pos=(12,210), size=(260,200))
        wx.EVT_LISTBOX(self, 4, self.ip_selected)

        
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

    def update_map_list(self):
        self.maps = map(strip_txt, os.listdir("worlds/"))
        self.map_list.SetItems(self.maps)
        self.map_list.SetSelection(0)
        

def strip_txt(inp):
    if (inp[-4:] == ".txt"):
        return inp[:-4]
        
def run_main_menu():
    app = wx.App()
    main_menu = panda_window(None, title='Main Selection')
    app.MainLoop()
    if (panda_window_action == "none"):
        return
    execfile("load_tester.py", {"panda_window_action" : panda_window_action, "panda_window_ip_address" : panda_window_ip_address})

run_main_menu()
