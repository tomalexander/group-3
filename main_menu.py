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
panda_window_settings["num_players"] = 4

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
        self.update_map_list()
        self.get_ip_address()
        


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
        self.text_name = wx.TextCtrl(self.join_panel)
        self.join_hbox2.Add(self.label_name, 1, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.join_hbox2.Add(self.text_name, 3, wx.TOP | wx.RIGHT, 0)

        #row 4
        self.join_hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_ip = wx.StaticText(self.join_panel, label="IP Address:")
        self.label_ip.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.text_ip = wx.TextCtrl(self.join_panel)
        self.join_hbox4.Add(self.label_ip, 0, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.join_hbox4.Add(self.text_ip, 3, wx.TOP | wx.RIGHT, 0)

        #row 3
        #row 3 column 1
        self.join_vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.join_hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_running = wx.StaticText(self.join_panel, label="Running\nServers:")
        self.label_running.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.button_refresh = wx.Button(self.join_panel, 3, label="Refresh")
        wx.EVT_BUTTON(self, 3, self._update_host_list)
        self.button_start = wx.Button(self.join_panel, 4, label="Start")
        wx.EVT_BUTTON(self, 4, self.join_start_game)
        self.server_list = wx.ListBox(self.join_panel, id=7)
        wx.EVT_LISTBOX(self, 7, self.ip_selected)
        self.join_vbox1.Add(self.label_running, 1, wx.ALL | wx.EXPAND, 5)
        self.join_vbox1.Add(self.button_refresh, 1, wx.ALL | wx.EXPAND, 5)
        self.join_vbox1.Add(self.button_start, 1, wx.ALL | wx.EXPAND, 5)
        self.join_hbox3.Add(self.join_vbox1, 2, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.join_hbox3.Add(self.server_list, 3, wx.TOP | wx.RIGHT | wx.EXPAND, 10)

        #rack em up
        self.join_vbox.Add(self.join_hbox1, 0, wx.ALL | wx.EXPAND, 10)
        self.join_vbox.Add(self.join_hbox2, 0, wx.ALL | wx.EXPAND, 10)
        self.join_vbox.Add(self.join_hbox4, 0, wx.ALL | wx.EXPAND, 10)
        self.join_vbox.Add(self.join_hbox3, 1, wx.ALL | wx.EXPAND, 10)

        #Interactivtize me baby
        wx.EVT_BUTTON(self, 2, self._set_host_ui)

        self.join_panel.SetSizer(self.join_vbox)
        self.update_host_list()
        #self.join_vbox.Add(self.join_panel)
        

    def init_host_ui(self):
        self.host_vbox = wx.BoxSizer(wx.VERTICAL)

        #row 1
        self.host_hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.host_label_title = wx.StaticText(self.host_panel, label="Rezolution")
        self.host_label_title.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.button_host = wx.Button(self.host_panel, 5, label="Join")
        self.host_hbox1.Add(self.host_label_title, 3, wx.TOP | wx.LEFT | wx.EXPAND, 10)
        self.host_hbox1.Add(self.button_host, 1, wx.TOP | wx.RIGHT, 10)

        #row 2
        self.host_hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.host_label_name = wx.StaticText(self.host_panel, label="Name:")
        self.host_label_name.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.host_text_name = wx.TextCtrl(self.host_panel)
        self.host_hbox2.Add(self.host_label_name, 1, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.host_hbox2.Add(self.host_text_name, 3, wx.TOP | wx.RIGHT, 0)

        #row 4
        self.host_hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.host_label_ip = wx.StaticText(self.host_panel, label="IP Address:")
        self.host_label_ip.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.host_text_ip = wx.TextCtrl(self.host_panel)
        self.host_hbox4.Add(self.host_label_ip, 0, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.host_hbox4.Add(self.host_text_ip, 3, wx.TOP | wx.RIGHT, 0)

        #row 5
        self.host_hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.host_label_world = wx.StaticText(self.host_panel, label="World:")
        self.host_label_world.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.map_list = wx.ComboBox(self.host_panel, id=6, style=wx.CB_DROPDOWN)
        self.host_hbox5.Add(self.host_label_world, 1, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.host_hbox5.Add(self.map_list, 3, wx.TOP | wx.RIGHT, 0)

        #row 6
        self.host_hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.host_label_time = wx.StaticText(self.host_panel, label="Time:")
        self.host_label_time.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.host_text_time = wx.TextCtrl(self.host_panel)
        self.host_text_time.SetValue("3")

        self.host_label_players = wx.StaticText(self.host_panel, label="Players:")
        self.host_label_players.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.host_players = wx.ComboBox(self.host_panel, id=7, style=wx.CB_DROPDOWN)
        self.host_players.SetItems(["1","2","3","4"])
        self.host_players.SetSelection(3)
        
        self.host_hbox6.Add(self.host_label_time, 0, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.host_hbox6.Add(self.host_text_time, 3, wx.TOP | wx.RIGHT, 03)
        self.host_hbox6.Add(self.host_label_players, 0, wx.TOP | wx.RIGHT, 03)
        self.host_hbox6.Add(self.host_players, 3, wx.TOP | wx.RIGHT, 0)

        #row 7
        self.host_hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.host_start_button = wx.Button(self.host_panel, 10, label="Start")
        wx.EVT_BUTTON(self, 10, self.host_start_game)
        self.host_hbox7.Add(self.host_start_button, 0, wx.LEFT | wx.TOP, 0)

        #rack em up
        self.host_vbox.Add(self.host_hbox1, 1, wx.ALL | wx.EXPAND, 10)
        self.host_vbox.Add(self.host_hbox2, 1, wx.ALL | wx.EXPAND, 10)
        self.host_vbox.Add(self.host_hbox4, 1, wx.ALL | wx.EXPAND, 10)
        self.host_vbox.Add(self.host_hbox5, 1, wx.ALL | wx.EXPAND, 10)
        self.host_vbox.Add(self.host_hbox6, 1, wx.ALL | wx.EXPAND, 10)
        self.host_vbox.Add(self.host_hbox7, 1, wx.ALL | wx.EXPAND, 10)

        #Interactivtize me baby
        wx.EVT_BUTTON(self, 5, self._set_join_ui)

        self.host_panel.SetSizer(self.host_vbox)
        
    def _set_join_ui(self, event):
        self.set_join_ui()

    def _set_host_ui(self, event):
        self.set_host_ui()

    def set_join_ui(self):
        self.host_panel.Hide()
        self.join_panel.Show()
        self.sizer.Layout()
        self.text_name.SetValue(self.host_text_name.GetValue())
        self.text_ip.SetValue(self.host_text_ip.GetValue())
        self.update_host_list()
        

    def set_host_ui(self):
        self.host_panel.Show()
        self.join_panel.Hide()
        self.sizer.Layout()
        self.host_text_name.SetValue(self.text_name.GetValue())
        self.get_ip_address()

    def get_ip_address(self):
        response = urllib2.urlopen('http://ip.paphus.com/')
        ip = response.read()
        self.text_ip.SetValue(ip)
        self.host_text_ip.SetValue(ip)

    def join_start_game(self, event):
        global panda_window_settings
        panda_window_settings["action"] = "join"
        self.start_game()

    def host_start_game(self, event):
        global panda_window_settings
        panda_window_settings["action"] = "host"
        self.start_game()

    def start_game(self):
        global panda_window_settings
        panda_window_settings["ip"] = self.text_ip.GetValue()
        panda_window_settings["player_name"] = self.text_name.GetValue()
        panda_window_settings["selected_map"] = self.maps[self.map_list.GetSelection()]
        panda_window_settings["game_time"] = int(self.host_text_time.GetValue())
        panda_window_settings["num_players"] = self.host_players.GetSelection()+1
        self.Close(True)
        self.Destroy()

    def click_host(self, event):
        global panda_window_action
        panda_window_action = "host"
        self.get_ip_address()
        self.start_game()

    def click_refresh(self, event):
        self.update_host_list()

    def _update_host_list(self, event):
        self.update_host_list()

    def update_host_list(self):
        self.hosts = []
        response = urllib2.urlopen('http://ip.paphus.com/browser.php?action=gethosts')
        ip = response.read()
        self.hosts = [i for i in ip.split(" ") if i != ""]
        self.server_list.Set(self.hosts)

    def ip_selected(self, event):
        self.text_ip.SetValue(self.hosts[self.server_list.GetSelection()])
        self.host_text_ip.SetValue(self.hosts[self.server_list.GetSelection()])

    def update_map_list(self):
        self.maps = map(strip_txt, os.listdir("worlds/"))
        self.map_list.SetItems(self.maps)
        self.map_list.SetSelection(0)


    def load_username(self):
        file_handle = open("username.txt", 'r')
        name = file_handle.readline()
        
    
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
    execfile("load_tester.py", {"panda_window_settings" : panda_window_settings})

run_main_menu()
