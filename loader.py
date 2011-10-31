from terrain import terrain

class loader:
    def __init__(self):
        pass

    def load_world(self, world_number):
        file_name = "worlds/world" + str(world_number) + ".txt"
        file_handle = open(file_name, 'r')
        for full_line in file_handle:
            line = full_line.strip()
            self.handle_line(line)

    def handle_line(self, line):
        for cell in line:
            pass
