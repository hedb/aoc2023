
SAMPLE_INPUT = '''
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''

class Cell:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f'({self.x},{self.y},{self.z})'

class Box:
    def __init__(self, start_cell_arr, end_cell_arr):
        self.id = None
        self.above_me = set()
        self.below_me = set()
        self.supporting = set()
        self.start_cell = Cell(int(start_cell_arr[0]), int(start_cell_arr[1]), int(start_cell_arr[2]))
        self.end_cell = Cell(int(end_cell_arr[0]), int(end_cell_arr[1]), int(end_cell_arr[2]))
        #verify that the box is valid
        diff_dim = (1 if self.start_cell.x != self.end_cell.x else 0) + \
                   (1 if self.start_cell.y != self.end_cell.y else 0)+ \
                   (1 if self.start_cell.z != self.end_cell.z else 0)
        if diff_dim > 1:
            raise Exception(f'Box is not valid {self}')

    def __repr__(self):
        return f'({self.id}: ({self.start_cell}, {self.end_cell}), supporting: { [b.id for b in self.supporting]})'

    def max_z(self):
        return max(self.start_cell.z, self.end_cell.z)
    def min_z(self):
        return min(self.start_cell.z, self.end_cell.z)

    def lower_to(self, z):
        lower_by = self.min_z() - z
        self.start_cell.z -= lower_by
        self.end_cell.z -= lower_by


class World:
    def __init__(self):
        self.boxes = []
        self.xy_grid = {}
        self.ID_COUNTER = 0
        self._max_z = 0
        self.z_levels = {}

    def add_box(self, box):
        box.id = chr(ord('A') + self.ID_COUNTER) if self.ID_COUNTER < 20 else "B" + str(self.ID_COUNTER)
        self.ID_COUNTER += 1
        self.boxes.append(box)
        for x in range(box.start_cell.x, box.end_cell.x + 1):
            for y in range(box.start_cell.y, box.end_cell.y + 1):
                if (x,y) not in self.xy_grid:
                    self.xy_grid[(x,y)] = list()
                self.xy_grid[(x,y)].append( box )
        if box.max_z() > self._max_z:
            self._max_z = box.max_z()

        if box.min_z() not in self.z_levels:
            self.z_levels[box.min_z()] = list()
        self.z_levels[box.min_z()].append(box)

    def max_z(self):
        return self._max_z

    def sort(self):
        for xy in self.xy_grid:
            self.xy_grid[xy].sort(key=lambda x: x.max_z() )

        for xy in self.xy_grid:
            for i,box in enumerate(self.xy_grid[xy][:-1]):
                box.above_me.add(self.xy_grid[xy][i+1])
                self.xy_grid[xy][i + 1].below_me.add(box)


    def gravity(self):
        for z in range(2, self.max_z() + 1):
            for box in self.z_levels.get(z,[]):
                if box.below_me:
                    max_z_below = max( [b.max_z() for b in box.below_me] )
                else:
                    max_z_below = 0
                box.lower_to(max_z_below + 1)

        #validate
        for box in self.boxes:
            if box.below_me:
                max_z_below = max( [b.max_z() for b in box.below_me] )
            else:
                max_z_below = 0
            if box.min_z() != max_z_below + 1:
                raise Exception(f'Box {box} is not at the right z level')


    def analyze_needed_blocks(self):
        needed = set()
        dependent = set()
        for b in self.boxes:
            for neighbor in b.above_me:
                if neighbor.min_z() == b.max_z() + 1:
                    # maybe needed
                    supporting_count = 0
                    for neighbor2 in neighbor.below_me:
                        if neighbor2.max_z() + 1 == neighbor.min_z() :
                            supporting_count += 1
                    if supporting_count == 1:
                        needed.add(b)
                        dependent.add(neighbor)
                        b.supporting.add(neighbor)
        return needed,dependent

    def count_redundant_blocks(self):
        needed,dependent = self.analyze_needed_blocks()
        return len(self.boxes) - len(needed)


    def calc_falling(self, box, falling_because_of_b_so_far):
        newlly_identified_falling = set()
        for neighbor in box.above_me:
            if neighbor.min_z() == box.max_z() + 1:
                # maybe needed
                supporting_count = 0
                for neighbor2 in neighbor.below_me:
                    if neighbor2.max_z() + 1 == neighbor.min_z() and neighbor2 not in falling_because_of_b_so_far:
                        supporting_count += 1
                if supporting_count <= 1:
                    if neighbor not in falling_because_of_b_so_far:
                        newlly_identified_falling.add(neighbor)
                    falling_because_of_b_so_far.add(neighbor)

        for neighbor in newlly_identified_falling:
            self.calc_falling(neighbor, falling_because_of_b_so_far)


    def sum_total_fallout(self):
        total_falling = set()
        dumb_counter = 0
        for b in self.boxes:
            falling_because_of_b = set()
            self.calc_falling(b, falling_because_of_b)
            dumb_counter += len(falling_because_of_b)
            total_falling.update(falling_because_of_b)
        return dumb_counter, len(total_falling)





    def print(self):
        for b in self.boxes:
            print(b)
        # for xy in self.xy_grid:
        #     print(f'{xy} : {self.xy_grid[xy]}')







def parse_input(input_data):
    print ('------------------------------------')
    world = World()
    lines = input_data.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        points = line.split('~')
        b = Box(points[0].split(','), points[1].split(','))
        world.add_box(b)
    world.sort()
    world.gravity()
    return world


def part1(world):
    print(world.xy_grid)

if __name__ == '__main__':

    world = parse_input(SAMPLE_INPUT)
    ret = world.count_redundant_blocks()
    assert ret == 5
    #
    # test_input = '''
    # 1,0,3~1,0,4
    # 1,2,5~1,2,5
    # 1,0,6~1,2,6
    # '''
    #
    # world = parse_input(test_input)
    # ret = world.count_redundant_blocks()
    # assert ret == 2, ret
    #
    #


    test_input = '''
            5,10,10~5,10,10
           0,10,12~5,10,12
            0,10,13~5,10,13
           '''

    test_input = '''
            0,0,10~0,0,10
            0,0,12~0,1,12
            0,0,13~0,1,13
           '''

    world = parse_input(test_input)
    ret = world.count_redundant_blocks()
    assert ret == 1, ret





    test_input = '''
        1,0,1~1,0,1
        2,0,1~2,0,1
        3,0,1~3,0,1        
        1,0,4~3,0,4  
        10,10,10~10,10,10
        10,10,11~10,10,11
        10,10,12~10,10,13  
        '''

    world = parse_input(test_input)
    ret = world.count_redundant_blocks()
    assert ret == 5, ret


    test_input = '''
        0,0,1~1,0,1
        0,0,2~0,0,2
        1,0,2~1,0,2
        0,0,3~1,0,3          
        '''
    world = parse_input(test_input)
    ret = world.sum_total_fallout()
    assert ret[0] == 3, ret


    world = parse_input(SAMPLE_INPUT)
    ret = world.sum_total_fallout()
    assert ret[0] == 7, ret

    with open('r22_input.txt') as f:
        input_data = f.read()
        world = parse_input(input_data)
        dumb_counter, smart_counter = world.sum_total_fallout()
        print(dumb_counter, smart_counter)