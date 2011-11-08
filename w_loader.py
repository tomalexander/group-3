from terrain import terrain
from tile import *
from spike import *
from sticky import *
from piston import *
from pit import *
from bumper import *

spawn_locations = []

class w_loader:
    def __init__(self):
        self.cell_height = 50
        self.cell_width = 50
        self.cell_list = []

    def load_world(self, world_number):
        file_name = "worlds/world" + str(world_number) + ".txt"
        file_handle = open(file_name, 'r')
        y_pos = 0
        for full_line in file_handle:
            line = full_line.strip()
            self.handle_line(line, y_pos)
            y_pos = y_pos + self.cell_height

    def handle_line(self, line, y_pos):
        global spawn_locations
        x_pos = 0
        for cell in line:
            if cell == 'l':#normal block
                new_cell = tile(x_pos, y_pos, 0, self)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            elif cell == 'v':#spike
                new_cell = spike(x_pos, y_pos)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            elif cell == 'r':#rumble
                new_cell = sticky(x_pos, y_pos)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            elif cell == 'p':#piston
                new_cell = piston(x_pos, y_pos)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            elif cell == '0':#empty
                new_cell = pit(x_pos, y_pos)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            elif cell == 'b':#barrier
                new_cell = bumper(x_pos, y_pos)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            elif cell == 's':#spawn
                spawn_locations.append((x_pos + 25, y_pos + 25),)
                print spawn_locations
                new_cell = tile(x_pos, y_pos, 0, self)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            else:
                pass
                # new_cell = terrain(x_pos, y_pos, 0, self)
                # new_cell.load_model()
                # self.cell_list.append(new_cell)
            x_pos = x_pos + self.cell_width
