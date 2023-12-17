from enum import Enum
import heapq


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
        if self.x == 0 and self.y == 0 and dir == Direction.down and stretch_used == 0:
            return 0
        return self.distances_by_incoming_dir[dir][stretch_used - 1]

    def min_distance(self):
        return min( [min(self.distances_by_incoming_dir[Direction.up]),min(self.distances_by_incoming_dir[Direction.down]),min(self.distances_by_incoming_dir[Direction.left]),min(self.distances_by_incoming_dir[Direction.right])] )


    def __eq__(self, other):
        if not isinstance(other, ArrivalMove):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(  ( self.x , self.y )  )


class ArrivalMove:
    def __init__(self, cell:MCell, arrival_direction:Direction, stretch_used:int):
        self.cell = cell
        self.arrival_direction = arrival_direction
        self.stretch_used = stretch_used

    def __eq__(self, other):
        if not isinstance(other, ArrivalMove):
            return NotImplemented
        return self.arrival_direction == other.arrival_direction and self.cell == other.cell and self.stretch_used == other.stretch_used

    def __hash__(self):
        return hash(  (self.cell.x,self.cell.y,self.arrival_direction,self.stretch_used)  )

    def __str__(self):
        return "ArrivalMove(%s, %s, %s)" % (self.cell, self.arrival_direction, self.stretch_used)

    def __repr__(self):
        return str(self)


    def __lt__(self, other):
        return hash(self) < hash(other)


class HeapQSet:
    def __init__(self):
        self.heap = []
        self.set = set()

    def push(self, item: ArrivalMove):
        if item not in self.set:
            tmp_item = (item.cell.min_distance() ,item)
            heapq.heappush(self.heap, tmp_item )
            self.set.add( tmp_item )

    def update(self, items):
        for item in items:
            self.push(item)

    def pop(self):
        item = heapq.heappop(self.heap)
        self.set.remove(item)
        return item[1]

    def remove(self, item: ArrivalMove):
        tmp_item = (item.cell.min_distance() ,item)
        self.heap.remove(tmp_item)
        self.set.remove(tmp_item)
        heapq.heapify(self.heap)

    def __len__(self):
        return len(self.heap)

    def __contains__(self, item: ArrivalMove):
        tmp_item = (item.cell.min_distance() ,item)
        return tmp_item in self.set


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
        routes.extend( [ ArrivalMove(cell,Direction.right,1),ArrivalMove(cell,Direction.right,2),ArrivalMove(cell,Direction.right,3) ]   )
    if cell.x < len(grid[0]) - 1:
        routes.extend( [ ArrivalMove(cell,Direction.left,1),ArrivalMove(cell,Direction.left,2),ArrivalMove(cell,Direction.left,3) ]   )
    if cell.y > 0:
        routes.extend( [ ArrivalMove(cell,Direction.down,1),ArrivalMove(cell,Direction.down,2),ArrivalMove(cell,Direction.down,3) ]   )
    if cell.y < len(grid) - 1:
        routes.extend( [ ArrivalMove(cell,Direction.up,1),ArrivalMove(cell,Direction.up,2),ArrivalMove(cell,Direction.up,3) ]   )
    return routes



def modified_get_neighbors(move:ArrivalMove, grid) -> list[MCell]:

    neighbors = []
    if move.cell.x > 0 and not (move.arrival_direction == Direction.left and move.stretch_used == 3) and move.arrival_direction != Direction.right:
        neighbors.append( ArrivalMove(grid[move.cell.y][move.cell.x - 1],Direction.left,move.stretch_used+1 if move.arrival_direction == Direction.left else 1) )

    if move.cell.x < len(grid[0]) - 1 and not (move.arrival_direction == Direction.right and move.stretch_used == 3) and move.arrival_direction != Direction.left:
        neighbors.append( ArrivalMove(grid[move.cell.y][move.cell.x + 1],Direction.right,move.stretch_used+1 if move.arrival_direction == Direction.right else 1))

    if move.cell.y > 0 and not (move.arrival_direction == Direction.up and move.stretch_used == 3) and move.arrival_direction != Direction.down:
        neighbors.append( ArrivalMove(grid[move.cell.y - 1][move.cell.x],Direction.up,move.stretch_used+1 if move.arrival_direction == Direction.up else 1))

    if move.cell.y < len(grid) - 1 and not (move.arrival_direction == Direction.down and move.stretch_used == 3) and move.arrival_direction != Direction.up:
        neighbors.append( ArrivalMove(grid[move.cell.y + 1][move.cell.x],Direction.down,move.stretch_used+1 if move.arrival_direction == Direction.down else 1))

    return neighbors



def modified_dijkstra(grid):
    start = grid[0][0]
    start.distances_by_incoming_dir[Direction.down][0] = 0
    unvisited = HeapQSet()
    for row in grid:
        for cell in row:
            arrival_routes = get_possible_arrival_moves(cell, grid)
            unvisited.update( arrival_routes )
    unvisited.push( ArrivalMove(start,Direction.down,0) ) # there is a special code for handling the stretch = 0 for cell 0,0
    while len(unvisited) > 0: # TODO: We need to initalize the first one manually so the stretch would be 0
        # print (len(unvisited))

        curr_move = unvisited.pop()
        # min(unvisited1, key=lambda m: m.cell.get_distance(m.arrival_direction,m.stretch_used) )

        possible_movements = modified_get_neighbors(curr_move, grid)
        for possible_movement in possible_movements:
            if possible_movement in unvisited:
                alt = curr_move.cell.get_distance(curr_move.arrival_direction,curr_move.stretch_used) + possible_movement.cell.value
                if alt < possible_movement.cell.get_distance(possible_movement.arrival_direction ,possible_movement.stretch_used ):
                    unvisited.remove(possible_movement)
                    possible_movement.cell.distances_by_incoming_dir[possible_movement.arrival_direction ][possible_movement.stretch_used - 1] = alt
                    unvisited.push(possible_movement)

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
    assert exit_point.min_distance() == 102


    test_input = """
        19
        19
        19
        11
        """
    grid = parse_input(test_input, "modified_version" )
    exit_point = modified_dijkstra(grid)
    assert exit_point.min_distance() == 4, exit_point.distances_by_incoming_dir



if __name__ == "__main__":
    _tests()

    # with open("r17_intput.txt") as f:
    #     grid = parse_input(f.read().strip(), "modified_version")
    #     exit_point = modified_dijkstra(grid)
    #     print(exit_point.min_distance())
    #     print(exit_point.distances_by_incoming_dir)
