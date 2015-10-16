import re
import heapq
import sys
import md5


re_rect = re.compile('\<rect\s+fill="(?P<type>\w+)"\s+height="(?P<height>\d+)"\s+width="(?P<width>\d+)"\s+x="(?P<x>\d+)"\s+y="(?P<y>\d+)"')
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = 'maze.html'

maze_html = open(file_name, 'r')

walls = []
red = None
green = None

maze_width = 0
maze_height = 0
for type, height, width, x, y in re_rect.findall(maze_html.read()):
    x = int(x)
    y = int(y)
    height = int(height)
    if type == 'black':
        walls.append((x/height, y/height))
    elif type == 'green':
        green = (x/height, y/height)
    elif type == 'red':
        red = (x/height, y/height)
    maze_width = max(maze_width, x/height)
    maze_height = max(maze_height, y/height)



class Cell(object):
    def __init__(self, x, y, reachable):
        """
        Initialize new cell
        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __repr__(self):
        return '%s,%s - %s' %(self.x, self.y, self.reachable)

class AStar(object):
    def __init__(self, walls, start, end, grid_height, grid_width):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.walls = walls
        self.start = start
        self.end = end

        self.grid_height = grid_height
        self.grid_width = grid_width

        print self.grid_height
        print self.grid_width

    def init_grid(self):
        # walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
        #      (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in self.walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        print self.start
        print self.end
        self.start = self.get_cell(*self.start)
        self.end = self.get_cell(*self.end)

    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.
        @param cell
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list
        """
        cells = []
        if cell.x < self.grid_width - 1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.grid_height - 1:
            cells.append(self.get_cell(cell.x, cell.y + 1))
        return cells

    def what_move(self, old, new):

        if old.x == new.x:
            if old.y > new.y:
                return 'B'
            else:
                return 'T'
        else:
            if old.x > new.x:
                return 'R'
            else:
                return 'L'


    def display_path(self):
        steps = []
        cell = self.end
        while cell.parent is not self.start:
            old, new = cell.parent, cell
            steps.append(self.what_move(old, new))
            cell = cell.parent
            # print 'path: cell: %d,%d' % (cell.x, cell.y)

        steps.append(self.what_move(self.start, cell))

        return steps

    def compare(self, cell1, cell2):
        """
        Compare 2 cells F values
        @param cell1 1st cell
        @param cell2 2nd cell
        @returns -1, 0 or 1 if lower, equal or greater
        """
        if cell1.f < cell2.f:
            return -1
        elif cell1.f > cell2.f:
            return 1
        return 0

    def update_cell(self, adj, cell):
        """
        Update adjacent cell
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                return self.display_path()
                # break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


a = AStar(walls, red, green, maze_height, maze_width)
a.init_grid()
steps = a.process()

steps = "".join(steps)

print steps

print md5.md5(steps).hexdigest()


