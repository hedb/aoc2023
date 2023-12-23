


SAMPLE_INPUT = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


class Grid:
    def __init__(self):
        self.grid = []
        self.dim = {'minx': 0,'miny': 0, 'maxx': 0, 'maxy': 0 }

    def add_row(self, row):
        self.grid.append(row)

    # def __getitem__(self, key):
    #     return self.grid[key]

    def update_dim(self, y, x):
        if x < self.dim['minx']:
            self.dim['minx'] = x
        if x > self.dim['maxx']:
            self.dim['maxx'] = x
        if y < self.dim['miny']:
            self.dim['miny'] = y
        if y > self.dim['maxy']:
            self.dim['maxy'] = y

    def get_cell(self,*, y, x):
        self.update_dim(y, x)
        new_x = x % self.width
        new_y = y % self.height
        if new_x < 0:
            new_x += self.width
        if new_y < 0:
            new_y += self.height
        if new_x == x and new_y == y:
            ret = self.grid[new_y][new_x]
        else :
            ret = Cell(x, y, self.grid[new_y][new_x].c)
        return ret


    @property
    def width(self):
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self):
        return len(self.grid)



class Cell:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.start_cell = False
        if c == 'S':
            self.start_cell = True
        self.id = f'{x},{y}'
        self.min_step_reached = None

    def __str__(self):
        return f'({self.x},{self.y},"{self.c}")'

    def mark(self, step):
        if self.min_step_reached is None or self.min_step_reached > step:
            self.min_step_reached = step


def parse_input1(input_str):
    grid = []
    start = None
    lines = input_str.splitlines()
    dimensions = { 'width': len(lines[0]), 'height': len(lines) }
    for y,l in enumerate(lines):
        grid.append([])
        for x,c in enumerate(l):
            grid[-1].append(Cell(x,y,c))
            if c == 'S':
                start = (x,y)
    return grid,start



def parse_input(input_str):
    grid = Grid()
    start = None
    lines = input_str.splitlines()
    dimensions = {'width': len(lines[0]), 'height': len(lines)}
    for y, l in enumerate(lines):
        row = []
        for x, c in enumerate(l):
            cell = Cell(x, y, c)
            row.append(cell)
            if c == 'S':
                start = (x, y)
        grid.add_row(row)
    return grid, start



class Path_Data_So_far:
    def __init__(self):
        self.step_used = 0
        self.tiles_covered = 0
        self.tiles_counted = set()

def get_roaming_options1(grid, start_cell, steps_left:int,step_counter:int, cache:set) -> int:

    if steps_left == 0:
        return 0

    cache.add(start_cell.id)
    cells_covered_so_far = len(cache)

    for diff in [(-1,0),(1,0),(0,-1),(0,1) ]:
        new_cell = move_cell(grid, start_cell, diff[0], diff[1])
        if new_cell is not None and new_cell.c == '.':
            tmp_cache = cache.copy()
            cell_covered_through_that_subtree = get_roaming_options(grid, new_cell, steps_left - 1,step_counter+1, tmp_cache)
            if cell_covered_through_that_subtree > cells_covered_so_far:
                cells_covered_so_far = cell_covered_through_that_subtree

    return cells_covered_so_far


def get_roaming_options2(grid, start_cell, steps_left:int, step_counter:int, cache:set) -> int:

    if steps_left == 0:
        return (len(cache))

    cache.add(start_cell.id)
    start_cell.mark(step_counter)

    for diff in [(-1,0),(1,0),(0,-1),(0,1) ]:
        new_cell = move_cell(grid, start_cell, diff[0], diff[1])
        if new_cell is not None and new_cell.c == '.':
            get_roaming_options(grid, new_cell, steps_left - 1,step_counter+1, cache)

    return len(cache)



def get_roaming_options(grid, start_cell, steps_left:int, step_counter:int, cache:set, previously_visited_cache:set):

    # print (f'[get_roaming_options] {start_cell} steps left: {steps_left}' )

    if (start_cell.id,steps_left) in previously_visited_cache:
        return
    previously_visited_cache.add((start_cell.id,steps_left))

    if steps_left == 0:
        cache.add(start_cell.id)
        start_cell.mark(step_counter)
        return

    for diff in [(-1,0),(1,0),(0,-1),(0,1) ]:
        new_cell = move_cell(grid, start_cell, diff[0], diff[1])
        if new_cell is not None and new_cell.c == '.':
            get_roaming_options(grid, new_cell, steps_left - 1,step_counter+1, cache,previously_visited_cache)


def move_cell(grid, start_cell, dx, dy):
    new_x = start_cell.x + dx
    new_y = start_cell.y + dy
    return grid.get_cell(y=new_y, x=new_x)

    # if 0 <= new_x < grid.width and 0 <= new_y < grid.height:
    #     return grid.get_cell(y = new_y,x = new_x)
    # else:
    #     return None


def part1(grid, start_point, step_number):
    start_cell = grid.get_cell(y=start_point[1],x=start_point[0])
    start_cell.c = '.'
    cache = set()
    previously_visited_cache = set()
    ret = get_roaming_options(grid, start_cell, step_number,0, cache, previously_visited_cache)
    return len(cache)

def print_grid(grid):
    for y in range(grid.dim['miny'],grid.dim['maxy']+1):
        for x in range( grid.dim['minx'],grid.dim['maxx']+1):
            cell = grid.get_cell(y=y,x=x)
            c = 'O' if cell.min_step_reached is not None else cell.c
            if cell.start_cell:
                c = '$' if cell.min_step_reached is not None else 'S'
            print(c,end='')
        print()

def _tests():
#
    test_input = """\
...#
#S##
....
"""
    grid,start_point = parse_input(test_input)
    ret = part1(grid, start_point,2 )
    assert ret == 7, ret


    for terms in [(6, 16)]:
        grid, start_point = parse_input(SAMPLE_INPUT)
        ret = part1(grid, start_point, terms[0])
        assert ret == terms[1], ret


    for terms in [ (10,50), (100,6536) ]:
        grid,start_point = parse_input(SAMPLE_INPUT)
        ret = part1(grid, start_point,terms[0])
        assert ret == terms[1], ret

        # print_grid(grid)
        # print( f'steps:{terms[0]},expected:{terms[1]}, got:{ret}' )

    # for i in range(1,1000):
    #     print (f'{i},', end='\t')
    #     with open('r21_input.txt') as f:
    #         grid, start_point = parse_input(f.read())
    #         ret = part1(grid, start_point, i)
    #         print(ret)


if __name__ == '__main__':

    _tests()

    # with open('r21_input.txt') as f:
    #     grid, start_point = parse_input(f.read())
    #     ret = part1(grid, start_point, 64)
    #     print (ret)