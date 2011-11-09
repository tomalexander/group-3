from terrain import terrain
from tile import *
from edge_tile import *
from spike import *
from sticky import *
from piston import *
from pit import *
from bumper import *
from boost import *

spawn_locations = []

class w_loader:
    def __init__(self):
        self.cell_height = 50
        self.cell_width = 50
        self.cell_list = []

    def load_world(self, world_number):
        file_name = "worlds/" + world_number + ".txt"
        file_handle = open(file_name, 'r')
        y_pos = 950
        for full_line in file_handle:
            line = full_line.strip()
            self.handle_line(line, y_pos)
            y_pos = y_pos - self.cell_height
        plane1 = CollisionPlane(Plane(Vec3(0, 1, 0), Point3(0, -25, 0)))
        plane2 = CollisionPlane(Plane(Vec3(0, -1, 0), Point3(0, 1025, 0)))
        plane3 = CollisionPlane(Plane(Vec3(1, 0, 0), Point3(-25, 0, 0)))
        plane4 = CollisionPlane(Plane(Vec3(-1, 0, 0), Point3(1025, 0, 0)))
        boundary_node = CollisionNode("pit")
        boundary_node.addSolid(plane1)
        boundary_node.addSolid(plane2)
        boundary_node.addSolid(plane3)
        boundary_node.addSolid(plane4)
        boundary_node_path = render.attachNewNode(boundary_node)
        #boundary_node_path.show()
        wall_model = loader.loadModel("models/roomtiles.egg")
        wall_model.reparentTo(render)
        wall_model.setPos(500, 500, 0)
        wall_model.setScale(36)
        wambientLight = AmbientLight("ambientLightForWall")
        wambientLight.setColor((.1, .1, .1, 3))
        wambientLightNP = wall_model.attachNewNode(wambientLight)
        wall_model.setLight(wambientLightNP)

    def handle_line(self, line, y_pos):
        global spawn_locations
        x_pos = 0
        for cell in line:
            if cell == 'l':#normal block
                new_cell = tile(x_pos, y_pos, 0, self)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            elif cell == 'e':#edge block
                new_cell = edge_tile(x_pos, y_pos, 0, self)
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
            elif cell == '+':#boost
                new_cell = boost(x_pos, y_pos)
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
            elif cell == '_':#barrier
                new_cell = bumper(x_pos, y_pos)
                new_cell.load_model()
                self.cell_list.append(new_cell)
            elif cell == '-':#barrier
                new_cell = bumper(x_pos, y_pos)
                new_cell.load_model()
                new_cell.model.setH(180)
                self.cell_list.append(new_cell)
            elif cell == '[':#barrier
                new_cell = bumper(x_pos, y_pos)
                new_cell.load_model()
                new_cell.model.setH(270)
                self.cell_list.append(new_cell)
            elif cell == ']':#barrier
                new_cell = bumper(x_pos, y_pos)
                new_cell.load_model()
                new_cell.model.setH(90)
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
