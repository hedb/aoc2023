
import re
import time
import math
import hashlib

possible_steps = {
    ('-', -1, 0): (-1, 0),
    ('-', 1, 0): (1, 0),

    ('|', 0, -1): (0, -1),
    ('|', 0, 1): (0, 1),

    ('7', 0, -1): (-1, 0),
    ('7', 1, 0): (0, 1),

    ('J', 0, 1): (-1, 0),
    ('J', 1, 0): (0, -1),

    ('L', 0, 1): (1, 0),
    ('L', -1, 0): (0, -1),

    ('F', 0, -1): (1, 0),
    ('F', -1, 0): (0, 1),
}

def calc_next_step(lines,current_symbol,current_place,prev_place):
    x_diff = current_place[0] - prev_place[0]
    y_diff = current_place[1] - prev_place[1]
    ret = [0,0]
    next_move = possible_steps[ (current_symbol,x_diff,y_diff)]

    next_place = (current_place[0]+next_move[0], current_place[1]+next_move[1])
    return next_place




def part1_0():
    last_ts = time.time()

    S_POS = [0,0]

    with open('r10_input.txt') as f:
    # with open('r10_sample_input1.txt') as f: # encloses 4
    # with open('r10_sample_input2.txt') as f: # encloses 8
    # with open('r10_sample_input3.txt') as f: # encloses
        data1 =f.read()
        data_hash = hashlib.sha256(data1.encode('utf-8')).digest()
        data = data1.splitlines()
        print ('data hash = ' + str(data_hash))
        lines = []
        for i,line in enumerate(data):
            lines.append(line)
            if 'S' in line:
                S_POS[1] = i
                S_POS[0] = line.index('S')

    #[119, 30]
    #-S7
    looped = False
    current_place = S_POS

    start_settings = {
        b'O:\xfe\xed|9?\xc9\x98\xf6\xb7\xb1!\x8c\xb0\x1d\x82T:\xccI\x10z\xfea\xa9\xf8lH\xb4>\xe7': (1,0,'F'),
        b'`a\xf4\xa9By\xf4\xab\x9a\xe1\x9f\x1c\xfd\x8eWn\xdce\x19a\xb5\xc2\xc3K\x9bay\x80\x1fZZl': (-1,0,'-'),
        b'\xcf\x058\x1c\xdd\x8b\xae\x0e\xef\x01f\xdf\xe5\x1ak\xae\xf4\x82h\xb8\xff\x02\xff\rl\x19\xaf\xce\x1e\xc1$\xe6':(1,0,'F'),
        b'\xd7\xc5e\xb61\xd8\x1f\x8e\x9av"\x85rB\xc1G\xec\xb4\x11:\xb8?o\xa5\xf7l\x80\x1e\xbf\x89\x8e\xed':(-1,0,'7')
    }
    start_settings = start_settings[data_hash]
    prev_place = [S_POS[0]+start_settings[0],S_POS[1] + start_settings[1]]

    current_symbol = start_settings[2]
    loop_mark = [[0 for i in range(len(lines[0]))] for j in range(len(lines))]

    step_number = 0
    while not looped:
        if current_symbol in '|L7JF-':
            loop_mark[current_place[1]][current_place[0]] = 1
        # print(current_symbol, current_place)
        step_number += 1
        tmp = current_place
        current_place = calc_next_step(lines,current_symbol,current_place,prev_place)
        prev_place = tmp
        current_symbol = lines[current_place[1]][current_place[0]]
        if current_symbol == 'S':
            break


    #replacing the S sign
    tmp_tist = list(lines[S_POS[1]])
    tmp_tist[S_POS[0]] = start_settings[2]
    lines[S_POS[1]] = ''.join(tmp_tist)

    trapped_cells = 0

    state_change = {
        ('L','J') : 0,
        ('L','7') : 1,
        ('F','7') : 0,
        ('F','J') : 1,
        ('','F') : 0,
        ('','L') : 0,
    }
    trapped_cells_dict = set()
    for i,line in enumerate(loop_mark):
        is_in = False
        prev_symbol = ''

        for j,v in enumerate(line):
            current_symbol = lines[i][j]
            if v :
                if current_symbol == '|':
                    is_in = not is_in
                else:
                    if state_change.get((prev_symbol,current_symbol),0) :
                        is_in = not is_in

                    if current_symbol in 'J7':
                        prev_symbol = ''
                    elif current_symbol != '-' :
                        prev_symbol = current_symbol

            elif is_in:
                # print('Trapped cell at: line:',i,' char:',j  )
                trapped_cells_dict.add( (i,j) )
                trapped_cells += 1

    for i, line in enumerate(loop_mark):
        for j, v in enumerate(line):
            print ( lines[i][j] if v else ('O' if (i,j) in trapped_cells_dict else '.') ,end='')
        print()


    print(trapped_cells)
    print(time.time() - last_ts,' seconds')



if __name__ == '__main__':
    part1_0()