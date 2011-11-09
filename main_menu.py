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
        self.main_panel = wx.Panel(self)
        self.host_panel = wx.Panel(self.main_panel)
        self.join_panel = wx.Panel(self.main_panel)
        
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.host_panel, 1, wx.EXPAND)
        self.sizer.Add(self.join_panel, 1, wx.EXPAND)
        self.host_panel.Hide()
        
        self.main_panel.SetSizer(self.sizer)
        
        self.init_join_ui()
        self.init_host_ui()


    def init_join_ui(self):
        self.join_vbox = wx.BoxSizer(wx.VERTICAL)

        #row 1
        self.join_hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_title = wx.StaticText(self.join_panel, label="Rezolution")
        self.label_title.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.button_host = wx.Button(self.join_panel, 2, label="Host")
        self.join_hbox1.Add(self.label_title, 3, wx.TOP | wx.LEFT | wx.EXPAND, 10)
        self.join_hbox1.Add(self.button_host, 1, wx.TOP | wx.RIGHT, 10)

        #row 2
        self.join_hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_name = wx.StaticText(self.join_panel, label="Name:")
        self.label_name.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.text_ip_address = wx.TextCtrl(self.join_panel)
        self.join_hbox2.Add(self.label_name, 1, wx.TOP | wx.LEFT | wx.EXPAND, 10)
        self.join_hbox2.Add(self.text_ip_address, 3, wx.TOP | wx.RIGHT, 10)

        #row 3
        #row 3 column 1
        self.join_vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.join_hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_running = wx.StaticText(self.join_panel, label="Running\nServers:")
        self.label_running.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.button_refresh = wx.Button(self.join_panel, 3, label="Refresh")
        self.button_start = wx.Button(self.join_panel, 4, label="Start")
        self.server_list = wx.ListBox(self.join_panel, id=4)
        self.join_vbox1.Add(self.label_running, 1, wx.ALL | wx.EXPAND, 5)
        self.join_vbox1.Add(self.button_refresh, 1, wx.ALL | wx.EXPAND, 5)
        self.join_vbox1.Add(self.button_start, 1, wx.ALL | wx.EXPAND, 5)
        self.join_hbox3.Add(self.join_vbox1, 2, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.join_hbox3.Add(self.server_list, 3, wx.TOP | wx.RIGHT | wx.EXPAND, 10)

        #rack em up
        self.join_vbox.Add(self.join_hbox1, 1, wx.ALL | wx.EXPAND, 10)
        self.join_vbox.Add(self.join_hbox2, 1, wx.ALL | wx.EXPAND, 10)
        self.join_vbox.Add(self.join_hbox3, 2, wx.ALL | wx.EXPAND, 10)

        #Interactivtize me baby
        wx.EVT_BUTTON(self, 2, self._set_host_ui)

        self.join_panel.SetSizer(self.join_vbox)
        #self.join_vbox.Add(self.join_panel)
        

    def init_host_ui(self):
        self.host_vbox = wx.BoxSizer(wx.VERTICAL)

        #row 1
        self.host_hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.host_label_title = wx.StaticText(self.host_panel, label="Rezolution")
        self.host_label_title.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.button_host = wx.Button(self.host_panel, 2, label="Join")
        self.host_hbox1.Add(self.host_label_title, 3, wx.TOP | wx.LEFT | wx.EXPAND, 10)
        self.host_hbox1.Add(self.button_host, 1, wx.TOP | wx.RIGHT, 10)

        #rack em up
        self.host_vbox.Add(self.host_hbox1, 1, wx.ALL | wx.EXPAND, 10)

        self.host_panel.SetSizer(self.host_vbox)
        
    def _set_join_ui(self, event):
        self.set_join_ui()

    def _set_host_ui(self, event):
        self.set_host_ui()

    def set_join_ui(self):
        self.host_panel.Hide()
        self.join_panel.Show()
        self.sizer.Layout()

    def set_host_ui(self):
        self.host_panel.Show()
        self.join_panel.Hide()
        self.sizer.Layout()

    
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
