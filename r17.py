from enum import Enum


SAMPLE_INPUT = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

def get_neighbors(cell, grid):
    neighbors = []
    if cell.x > 0:
        neighbors.append(grid[cell.y][cell.x - 1])
    if cell.x < len(grid[0]) - 1:
        neighbors.append(grid[cell.y][cell.x + 1])
    if cell.y > 0:
        neighbors.append(grid[cell.y - 1][cell.x])
    if cell.y < len(grid) - 1:
        neighbors.append(grid[cell.y + 1][cell.x])
    return neighbors



def standard_dijkstra(grid):
    for row in grid:
        for cell in row:
            cell.distance = float("inf")
            cell.previous = None
    start = grid[0][0]
    start.distance = 0
    unvisited = set()
    for row in grid:
        for cell in row:
            unvisited.add(cell)
    while len(unvisited) > 0:
        current = min(unvisited, key=lambda x: x.distance)
        unvisited.remove(current)
        for neighbor in get_neighbors(current, grid):
            if neighbor in unvisited:
                alt = current.distance + neighbor.value
                if alt < neighbor.distance:
                    neighbor.distance = alt
                    neighbor.previous = current
    return grid[-1][-1].distance

def get_possible_arrival_routes(cell, grid):
    routes = []
    if cell.x > 0:
        routes.extend( [ (cell,Direction.left,1),(cell,Direction.left,2),(cell,Direction.left,3) ]   )
    if cell.x < len(grid[0]) - 1:
        routes.extend( [ (cell,Direction.right,1),(cell,Direction.right,2),(cell,Direction.right,3) ]   )
    if cell.y > 0:
        routes.extend( [ (cell,Direction.up,1),(cell,Direction.up,2),(cell,Direction.up,3) ]   )
    if cell.y < len(grid) - 1:
        routes.extend( [ (cell,Direction.down,1),(cell,Direction.down,2),(cell,Direction.down,3) ]   )
    return routes

def modified_dijkstra(grid):
    for row in grid:
        for mcell in row:
            mcell.distances = {Direction.up: [float("inf")]*3, Direction.down: [float("inf")]*3, Direction.left: [float("inf")]*3, Direction.right: [float("inf")]*3}
    start = grid[0][0]
    start.distances = {Direction.up: [0,0,0], Direction.down: [0,0,0], Direction.left: [0,0,0], Direction.right: [0,0,0]}
    unvisited = list[tuple]()
    for row in grid:
        for cell in row:
            unvisited.extend( get_possible_arrival_routes(cell, grid) )
    while len(unvisited) > 0:
        current = min(unvisited, key=lambda x: x.distance)
        unvisited.remove(current)
        for neighbor in get_neighbors(current, grid):
            if neighbor in unvisited:
                alt = current.distance + neighbor.value
                if alt < neighbor.distance:
                    neighbor.distance = alt
    return grid[-1][-1].distance



class CELL:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __str__(self):
        return "CELL(%s, %s, %s)" % (self.x, self.y, self.value)


class MCELL:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __str__(self):
        return "CELL(%s, %s, %s)" % (self.x, self.y, self.value)

class Direction(Enum):
    up = 0
    down = 1
    left = 2
    right = 3


def parse_input(input):
    grid = []
    for y, line in enumerate(input.strip().split("\n")):
        line = line.strip()
        if line == "":
            continue
        row = []
        for x, value in enumerate(line):
            row.append(CELL(x, y, int(value)))
        grid.append(row)
    return grid


def _tests():

    test_input = """
    11
    21
    """

    grid = parse_input(test_input)
    distance = standard_dijkstra(grid)
    assert distance == 2, distance

    test_input = """
    111
    919
    119
    191
    111
    """

    grid = parse_input(test_input)
    distance = standard_dijkstra(grid)
    assert distance == 8, distance

    test_input = """
        11111111
        22222221
        """
    grid = parse_input(test_input)
    distance = modified_dijkstra(grid)
    assert distance > 8, 'should be larger than 8 because cant go straight'

    # grid = parse_input(SAMPLE_INPUT)
    # distance = modified_dijkstra(grid)
    # assert distance == 102, distance

if __name__ == "__main__":
    _tests()