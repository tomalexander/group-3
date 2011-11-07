from terrain import terrain
from tile import *

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
        x_pos = 0
        for cell in line:
            if cell == '0':
                new_cell = tile(x_pos, y_pos, 0, self)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            else:
                new_cell = terrain(x_pos, y_pos, 0, self)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            x_pos = x_pos + self.cell_width
