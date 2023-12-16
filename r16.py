

SAMPLE_INPUT = """
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....\
"""

def print_tiles(tiles):
    for line in tiles:
        for tile in line:
            print(f'T:{tile.symbol}, ', end='')
        print()

def _tests():
    with open('r16_sample_input1', 'r') as f:
        input_str = f.read()
        tiles = parse_input(input_str)
        traverse_ray(tiles,Ray(x=0, y=0, dir=(1,0)))
        assert calc_energy(tiles) == 46

        tiles = parse_input(input_str)
        traverse_ray(tiles, Ray(x=3, y=0, dir=(0, 1)))
        assert calc_energy(tiles) == 51


    with open('r16_input.txt', 'r') as f:
        input_str = f.read()
        tiles = parse_input(input_str)
        print(  calc_energy_and_clean_after(tiles,Ray(x=107, y=109, dir=(0,-1))) )

transitions = {
    '\\': {
        (1,0): (0,1),
        (-1,0): (0,-1),
        (0,1): (1,0),
        (0,-1): (-1,0),
    },
    '/': {
        (1,0): (0,-1),
        (-1,0): (0,1),
        (0,1): (-1,0),
        (0,-1): (1,0),
    },
    '|': {
        (1,0): ( (0,1), (0,-1)),
        (-1,0): ( (0,1), (0,-1)),
        (0,1): (0,1),
        (0,-1): (0,-1),
    },
    '-': {
        (1,0): (1,0),
        (-1,0): (-1,0),
        (0,1): ( (1,0), (-1,0)),
        (0,-1): ( (1,0), (-1,0)),
    }
}

def traverse_ray(tiles, starting_ray):

    rays_to_compute = []
    rays_to_compute.append(starting_ray)

    while len(rays_to_compute) != 0:
        ray = rays_to_compute.pop()
        while True:
            #end condition 1
            if ray.x < 0 or ray.x >= len(tiles[0]) or ray.y < 0 or ray.y >= len(tiles) :
                break

            tile = tiles[ray.y][ray.x]

            # end condition 2
            if ray.dir in tile.already_traversed_directions:
                break

            tile.energized = 1
            tile.already_traversed_directions.add(ray.dir)

            if tile.symbol == '.':
                ray.x += ray.dir[0]
                ray.y += ray.dir[1]
                continue

            dir_post_pass = transitions[tile.symbol][ray.dir]
            if isinstance(dir_post_pass[0], tuple):
                new_ray = Ray(x=ray.x + dir_post_pass[1][0], y=ray.y + dir_post_pass[1][1], dir=dir_post_pass[1])
                rays_to_compute.append(new_ray)
                dir_post_pass = dir_post_pass[0]
            ray.x += dir_post_pass[0]
            ray.y += dir_post_pass[1]
            ray.dir = dir_post_pass



def calc_energy(tiles):
    ret = 0
    for line in tiles:
        for tile in line:
            ret += tile.energized
    return ret



class Tile:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.energized = 0
        self.already_traversed_directions = set()

    def __str__(self):
        return f'[T: {self.symbol}]'

class Ray:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def __str__(self):
        return f'[R: {self.x}, {self.y}, {self.dir}]'

def parse_input(input_str) -> list[str] :
    ret = []
    input_str = input_str.strip().replace('\\','%')
    for y, line in enumerate(input_str.splitlines()):
        ret.append([None] * len(line))
        for x, symbol in enumerate(line):
            ret[y][x] = Tile(x, y, symbol if symbol != '%' else '\\')
    return ret


def calc_energy_and_clean_after(tiles,ray):
    traverse_ray(tiles, ray)
    energy = calc_energy(tiles)
    for line in tiles:
        for tile in line:
            tile.energized = 0
            tile.already_traversed_directions = set()
    return energy

def calc_max_energy(tiles):

    max_energy = 0
    for y in range(len(tiles)):
        e1  = calc_energy_and_clean_after(tiles,Ray(0 , y, (1,0)))
        e2  = calc_energy_and_clean_after(tiles,Ray(len(tiles[0])-1 , y, (-1,0)))
        if max_energy < max(e1,e2):
            max_energy = max(e1,e2)
            print (Ray(0 , y, (1,0)) , e1)
            print (Ray(len(tiles[0])-1 , y, (-1,0)) , e2)

    for x in range(len(tiles[0])):
        e1  = calc_energy_and_clean_after(tiles,Ray(x , 0, (0,1)))
        e2  = calc_energy_and_clean_after(tiles,Ray(x , len(tiles)-1, (0,-1)))
        if max_energy < max(e1,e2):
            max_energy = max(e1,e2)
            print (Ray(x , 0, (0,1)) , e1)
            print (Ray(x , len(tiles)-1, (0,-1)) , e2)


    return max_energy


if __name__ == '__main__':
    _tests()


    with open('r16_input.txt', 'r') as f:
        input_str = f.read()
        tiles = parse_input(input_str)
        print(  calc_max_energy(tiles) )
