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


class CELL:
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

class MCell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.distances_by_incoming_dir = {Direction.up: [float("inf")] * 3, Direction.down: [float("inf")] * 3, Direction.left: [float("inf")] * 3, Direction.right: [float("inf")] * 3}

    def __str__(self):
        return "MCELL(%s, %s)" % (self.x, self.y)

    def get_distance(self,dir:Direction, stretch_used:int):
        return self.distances_by_incoming_dir[dir][stretch_used - 1]

    def min_distance(self):
        return min( [min(self.distances_by_incoming_dir[Direction.up]),min(self.distances_by_incoming_dir[Direction.down]),min(self.distances_by_incoming_dir[Direction.left]),min(self.distances_by_incoming_dir[Direction.right])] )


class ArrivalMove:
    def __init__(self, cell:MCell, arrival_direction:Direction, stretch_used:int):
        self.cell = cell
        self.arrival_direction = arrival_direction
        self.stretch_used = stretch_used

    def __str__(self):
        return "ArrivalMove(%s, %s, %s)" % (self.cell, self.direction, self.stretch_used)



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

def get_possible_arrival_moves(cell, grid):
    routes = []
    if cell.x > 0:
        routes.extend( [ (cell,Direction.right,1),(cell,Direction.right,2),(cell,Direction.right,3) ]   )
    if cell.x < len(grid[0]) - 1:
        routes.extend( [ (cell,Direction.left,1),(cell,Direction.left,2),(cell,Direction.left,3) ]   )
    if cell.y > 0:
        routes.extend( [ (cell,Direction.down,1),(cell,Direction.down,2),(cell,Direction.down,3) ]   )
    if cell.y < len(grid) - 1:
        routes.extend( [ (cell,Direction.up,1),(cell,Direction.up,2),(cell,Direction.up,3) ]   )
    return routes



def modified_get_neighbors(cell:MCell, incoming_dir:Direction, stretch_used_input:int, grid) -> list[MCell]:

    neighbors = []
    if cell.x > 0 and not (incoming_dir == Direction.left and stretch_used_input == 3) and dir != Direction.right:
        neighbors.append( (grid[cell.y][cell.x - 1],Direction.left,stretch_used_input+1 if incoming_dir == Direction.left else 1) )

    if cell.x < len(grid[0]) - 1 and not (incoming_dir == Direction.right and stretch_used_input == 3) and dir != Direction.left:
        neighbors.append((grid[cell.y][cell.x + 1],Direction.right,stretch_used_input+1 if incoming_dir == Direction.right else 1))

    if cell.y > 0 and not (incoming_dir == Direction.up and stretch_used_input == 3) and dir != Direction.down:
        neighbors.append((grid[cell.y - 1][cell.x],Direction.up,stretch_used_input+1 if incoming_dir == Direction.up else 1))

    if cell.y < len(grid) - 1 and not (incoming_dir == Direction.down and stretch_used_input == 3) and dir != Direction.up:
        neighbors.append((grid[cell.y + 1][cell.x],Direction.down,stretch_used_input+1 if incoming_dir == Direction.down else 1))
        
    return neighbors



def modified_dijkstra(grid):
    start = grid[0][0]
    start.distances_by_incoming_dir[Direction.down][0] = 0
    unvisited = set[tuple[MCell,Direction,int]]()
    for row in grid:
        for cell in row:
            arrival_routes = get_possible_arrival_moves(cell, grid)
            unvisited.update( arrival_routes )
    unvisited.add( (start,Direction.down,1) )
    while len(unvisited) > 0: # TODO: We need to initalize the first one manually so the stretch would be 0
        current = min(unvisited, key=lambda x: x[0].get_distance(x[1],x[2]) )
        unvisited.remove(current)
        possible_movements = modified_get_neighbors(current[0],current[1], current[2], grid)
        for possible_movement in possible_movements:
            if possible_movement in unvisited:
                alt = current[0].get_distance(current[1],current[2]) + possible_movement[0].value
                if alt < possible_movement[0].get_distance(possible_movement[1],possible_movement[2]):
                    possible_movement[0].distances_by_incoming_dir[possible_movement[1]][possible_movement[2] - 1] = alt
    return grid[-1][-1]



def get_neighboors_simple(cell, grid):
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

def print_minimal_path(grid):
    current = grid[-1][-1]
    path = []
    while current is not grid[0][0]:
        path.append(current)
        distance = current.min_distance()
        neighbors = get_neighboors_simple(current, grid)
        for neighbor in neighbors:
            if neighbor.min_distance() == distance - current.value:
                current = neighbor
                break
        if current == path[-1]:
            raise Exception("No path found")

    path.reverse()
    for cell in path:
        print(cell)

def print_minimal_path1(grid):
    for row in grid:
        for cell in row:
            print(f'({cell.min_distance()},{cell.value}) ' , end=" ")
        print("")


def parse_input(input, version=None):
    grid = []
    for y, line in enumerate(input.strip().split("\n")):
        line = line.strip()
        if line == "":
            continue
        row = []
        for x, value in enumerate(line):
            if version == "modified_version":
                row.append(MCell(x, y, int(value)))
            else:
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
    11
    21
    """

    grid = parse_input(test_input, "modified_version")
    exit_point = modified_dijkstra(grid)
    assert  exit_point.min_distance() == 2, exit_point.distances_by_incoming_dir
    #
    test_input = """
        11111111
        22222221
        """
    grid = parse_input(test_input, "modified_version" )
    exit_point = modified_dijkstra(grid)
    assert exit_point.min_distance() > 8, 'should be larger than 8 because cant go straight' + str(exit_point)

    grid = parse_input(SAMPLE_INPUT,"modified_version" )
    exit_point = modified_dijkstra(grid)
    print(exit_point.distances_by_incoming_dir)
    print_minimal_path1(grid)
    print_minimal_path(grid)
    # assert exit_point.min_distance() == 102




if __name__ == "__main__":
    _tests()