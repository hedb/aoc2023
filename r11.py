
import re
import time
import math




def part1_0():
    last_ts = time.time()

    EXPENSION_FACTOR = 0

    cols_with_galaxy = set()
    # with open('r11_input.txt') as f:
    with open('r11_sample_input1.txt') as f:
        data = f.read().splitlines()
        lines = []
        for i,line in enumerate(data):
            if '#' in line:
                for c_pos,c in enumerate(line):
                    if c == '#':
                        cols_with_galaxy.add(c_pos)
            else:
                for times in range(EXPENSION_FACTOR):
                    lines.append(list(line)) # duplicate empty lines
            lines.append(list(line))

        offset = 0
        for col in range(len(data[0])):
            if col not in cols_with_galaxy:
                for line in lines:
                    for times in range(EXPENSION_FACTOR):
                        line.insert(col + offset,'.')
                offset += EXPENSION_FACTOR

        for line in lines:
            print(''.join(line))

        galaxies = {}
        for y,line in enumerate(lines):
            for x,c in enumerate(line):
                if c == '#':
                    id =  len(galaxies)
                    galaxies[id] = {'x':x,'y':y,'id': id}

        sum_distances = 0
        for i in range(len(galaxies)):
            for j in range(i,len(galaxies)):
                distance = abs(galaxies[i]['x'] - galaxies[j]['x']) + abs(galaxies[i]['y'] - galaxies[j]['y'])
                sum_distances += distance
                # print (f'{i} {j} {distance}')

        print(sum_distances)



if __name__ == '__main__':
    part1_0()