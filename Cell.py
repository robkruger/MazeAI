class Cell(object):

    def __init__(self, n, e, x, y):
        self.north = n
        self.east = e
        self.x = x
        self.y = y

    def toggle_north(self):
        self.north = not self.north

    def toggle_east(self):
        self.east = not self.east
