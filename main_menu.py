import wx
import socket
import urllib2
import os

panda_window_settings = {}
panda_window_settings["action"] = "none"
panda_window_settings["ip"] = "none"
panda_window_settings["player_name"] = "none"
panda_window_settings["selected_map"] = "none"
panda_window_settings["game_time"] = 5

class panda_window(wx.Frame):

    def __init__(self, parent, title):
        super(panda_window, self).__init__(parent, title=title, size=(600,560))
        global panda_window_settings
        panda_window_settings["action"] = "none"

        self.init_ui()
        self.Show()
        self.Centre()

    def init_ui(self):
        self.panel = wx.Panel(self, -1)
        self.init_join_ui()
        self.init_host_ui()
        self.set_join_ui()

    def init_join_ui(self):
        self.join_vbox = wx.BoxSizer(wx.VERTICAL)

        #row 1
        self.join_hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_title = wx.StaticText(self.panel, label="Rezolution")
        self.label_title.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.button_host = wx.Button(self.panel, 2, label="Host")
        self.join_hbox1.Add(self.label_title, 3, wx.TOP | wx.LEFT | wx.EXPAND, 10)
        self.join_hbox1.Add(self.button_host, 1, wx.TOP | wx.RIGHT, 10)

        #row 2
        self.join_hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_name = wx.StaticText(self.panel, label="Name:")
        self.label_name.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.text_ip_address = wx.TextCtrl(self.panel)
        self.join_hbox2.Add(self.label_name, 1, wx.TOP | wx.LEFT | wx.EXPAND, 10)
        self.join_hbox2.Add(self.text_ip_address, 3, wx.TOP | wx.RIGHT, 10)

        #row 3
        #row 3 column 1
        self.join_vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.join_hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_running = wx.StaticText(self.panel, label="Running\nServers:")
        self.label_running.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.button_refresh = wx.Button(self.panel, 3, label="Refresh")
        self.button_start = wx.Button(self.panel, 3, label="Start")
        self.server_list = wx.ListBox(self.panel, id=4)
        self.join_vbox1.Add(self.label_running, 1, wx.ALL, 5)
        self.join_vbox1.Add(self.button_refresh, 1, wx.ALL, 5)
        self.join_vbox1.Add(self.button_start, 1, wx.ALL, 5)
        self.join_hbox3.Add(self.join_vbox1, 2, wx.TOP | wx.LEFT | wx.EXPAND, 10)
        self.join_hbox3.Add(self.server_list, 3, wx.TOP | wx.RIGHT | wx.EXPAND, 10)

        #rack em up
        self.join_vbox.Add(self.join_hbox1, 1, wx.ALL | wx.EXPAND, 10)
        self.join_vbox.Add(self.join_hbox2, 1, wx.ALL | wx.EXPAND, 10)
        self.join_vbox.Add(self.join_hbox3, 2, wx.ALL | wx.EXPAND, 10)
        

    def init_host_ui(self):
        pass

    def set_join_ui(self):
        self.panel.SetSizer(self.join_vbox)

    def set_host_ui(self):
        pass

    
def strip_txt(inp):
    if (inp[-4:] == ".txt"):
        return inp[:-4]


def run_main_menu():
    global panda_window_settings
    app = wx.App()
    main_menu = panda_window(None, title='Main Selection')
    app.MainLoop()
    if (panda_window_settings["action"] == "none"):
        return
    #execfile("load_tester.py", {"panda_window_action" : panda_window_action, "panda_window_ip_address" : panda_window_ip_address})

run_main_menu()
