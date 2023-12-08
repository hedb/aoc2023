
import re
import time
import math
from dataclasses import dataclass


@dataclass
class MapLine:
    id: int
    start: str
    left: str
    right: str


def parse(input_line, i=0):
    # ZZZ = (ZZZ, ZZZ)
    if input_line.strip() == '':
        return None
    matches = re.match(' *([0-9A-Z]*) *= *\(([0-9A-Z]*) *, *([0-9A-Z]*)', input_line)
    ret = MapLine(i+1,matches.group(1), matches.group(2), matches.group(3))
    return ret


def part1_0():
    last_ts = time.time()
    with open('r8_input.txt') as f:
    # with open('r8_sample_input.txt') as f:
        data = f.read().splitlines()
        instructions = data[0]

        map = {}
        for line in data[1:]:
            map_line = parse(line)
            if map_line:
                map[map_line.start] = map_line

    number_of_steps = 0
    curr_step = map['AAA']

    while curr_step.start != 'ZZZ':
        for s in instructions:
            number_of_steps += 1
            if s == 'L':
                curr_step = map[curr_step.left]
            elif s == 'R':
                curr_step = map[curr_step.right]
            else:
                print('ERROR: wrong step: ', s)
                break
            if curr_step.start == 'ZZZ':
                break

    print (number_of_steps)


def part2_0():
    last_ts = time.time()
    with open('r8_input.txt') as f:
    # with open('r8_sample_input.txt') as f:
        data = f.read().splitlines()
        instructions = data[0]

        map = {}
        for i,line in enumerate(data[1:]):
            map_line = parse(line,i)
            if map_line:
                map[map_line.start] = map_line

    number_of_steps = 0
    starting_nodes = [ml for ml in map.values() if ml.start.endswith('A')]
    starting_nodes = [starting_nodes[5]]
    next_starting_nodes = []


    '''
    
1 [(61, 'BGA')]	1		
18962 [(296, 'LCZ')]	18962	18961	
37923 [(296, 'LCZ')]	37923	18961	67, 283,
			
1 [(67, 'SLA')]	1		
12170 [(501, 'LQZ')]	12170	12169	
24339 [(501, 'LQZ')]	24339	12169	43, 283
			
1 [(88, 'PTA')]	1		
17264 [(635, 'SNZ')]	17264	17263	
34527 [(635, 'SNZ')]	34527	17263	61, 283
			
1 [(115, 'AAA')]	1		
13302 [(272, 'ZZZ')]	13302	13301	
26603 [(272, 'ZZZ')]	26603	13301	47,283
			
1 [(402, 'XJA')]	1		
15000 [(66, 'PDZ')]	15000	14999	
29999 [(66, 'PDZ')]	29999	14999	 53, 283, 
			
1 [(419, 'JNA')]	1		
16698 [(62, 'PBZ')]	16698	16697	
33395 [(62, 'PBZ')]	33395	16697	59, 283, 
    
67*43*61*47*53*59*283
7309459565207
    '''

    while True:
        for s in instructions:
            number_of_steps += 1
            # print(', '.join(str(id) for id in sorted([n.id for n in starting_nodes])) )
            print (number_of_steps, [(n.id,n.start) for n in starting_nodes])
            for n in starting_nodes:
                if s == 'L':
                    next_starting_nodes.append(map[n.left])
                elif s == 'R':
                    next_starting_nodes.append(map[n.right])
                else:
                    print('ERROR: wrong step: ', s)
                    break
            starting_nodes = next_starting_nodes
            next_starting_nodes = []
            # if all(n.start.endswith('Z') for n in starting_nodes):
            if number_of_steps > 50000:
                break
        # if all(n.start.endswith('Z') for n in starting_nodes):
        if number_of_steps > 50000:
            break

    print (number_of_steps)


if __name__ == '__main__':
    part2_0()