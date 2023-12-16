
import re
import time
import math
import copy
import itertools

def parse(input_line,is_part2 = False):
    tmp = re.split(' ', input_line)
    text_line = tmp[0]
    counters = re.split(',', tmp[1])

    if is_part2:
        mutlplier = ['?','?','?','?','?','?']
        text_line = text_line.join(mutlplier)[1:-1]
        counters = counters * ( len(mutlplier) -1 )

    ret = {'orig': text_line, 'arrange': text_line, 'counters': counters}
    # ret = {}
    ret['str_as_list'] = list(text_line)
    ret['arrange'] = [x for x in re.split('\.', ret['arrange']) if x != '']
    ret['counters'] = [int(x) for x in counters]
    return ret

def calc_options(o):

    ret = 0

    if sum(o['counters']) == 0:
        if '#' in ''.join(o['arrange']):
            return 0 # not valid, finished countes bet there is still a thing
        else:
            return 1

    elif sum(o['counters']) > sum ([len(x) for x in o['arrange']]):
        return 0
    else:
        # trying to match first at first place
        if len(o['arrange'][0]) < o['counters'][0]: # not enough space
            o1 = copy.deepcopy(o)
            o1['arrange'].pop(0)
            ret += calc_options(o1)
        elif len(o['arrange'][0]) == o['counters'][0]: # exact match
                o1 = copy.deepcopy(o)
                o1['arrange'].pop(0)
                o1['counters'].pop(0)
                ret += calc_options(o1)
        else: # enough space
            for i in range(len(o['arrange'][0]) - o['counters'][0] + 1):
                if (i > 0) and (o['arrange'][0][i-1] == '#'):
                    break; # no need to check further beacuse we leave something like 1,X
                elif (i < len(o['arrange'][0]) - o['counters'][0]) and (o['arrange'][0][i+o['counters'][0]] == '#'):
                    continue; # we are swallowing some #
                o1 = copy.deepcopy(o)
                o1['arrange'][0] = o1['arrange'][0][o['counters'][0]+i+1:]
                o1['counters'].pop(0)
                ret += calc_options(o1)

    return ret

def calc_line_counters(line):
    ret = []
    current_section = 0
    for c in line:
        if c not in '#.':
            raise Exception('Wrong input :' + line)
        if c == '#':
            current_section += 1
        elif current_section > 0:
            ret.append(current_section)
            current_section = 0
    if current_section > 0:
        ret.append(current_section)
    return ret

def tests():
    assert calc_line_counters('.#.###.#.######') == [1, 3, 1, 6]
    assert calc_line_counters('..##.##.##.##.##') == [2, 2, 2, 2, 2]
    assert calc_line_counters('##.##.##.##.##..') == [2, 2, 2, 2, 2]
    assert calc_line_counters('##.##.##.##.##') == [2, 2, 2, 2, 2]
    assert calc_line_counters('####.#...#...') == [4,1,1]


    ret = parse('.# 1',True)
    assert ret['orig'] == '.#?.#?.#?.#?.#'
    assert ret['counters'] == [1,1,1,1,1]

    ret = parse('???.### 1,1,3',True)
    assert ret['orig'] == '???.###????.###????.###????.###????.###'
    assert ret['counters'] == [1,1,3,1,1,3,1,1,3,1,1,3,1,1,3]



def calc_options_BF(line,target_counters):
    ret = 0
    if '?' in line:
        ret += calc_options_BF(line.replace('?','#',1),target_counters)
        ret += calc_options_BF(line.replace('?','.',1),target_counters)
    else: # is the path up till here valid ?
        line_counters = calc_line_counters(line)
        if line_counters == target_counters:
            # print(line)
            ret = 1
        else:
            ret = 0

    return ret










def part1_BF(is_part2):
    last_ts = time.time()
    # with open('r12_input.txt') as f:
    with open('r12_sample_input1.txt') as f:
        data = f.read().splitlines()
        lines = []
        sum = 0
        for line in data:
            line = parse(line,is_part2)
            line_options = calc_options_BF(line['orig'],line['counters'])
            print(line, line_options)
            sum += line_options
            lines.append(line)

    print(sum)
    print(time.time() - last_ts,' seconds')

def calc_options_1(o):
    '''
    {'orig': '???.###', 'arrange': ['???', '###'], 'counters': [1, 1, 3]}
    {'orig': '.??..??...?##.', 'arrange': ['??', '??', '?##'], 'counters': [1, 1, 3]}
    {'orig': '?#?#?#?#?#?#?#?', 'arrange': ['?#?#?#?#?#?#?#?'], 'counters': [1, 3, 1, 6]}
    {'orig': '????.#...#...', 'arrange': ['????', '#', '#'], 'counters': [4, 1, 1]}
    {'orig': '????.######..#####.', 'arrange': ['????', '######', '#####'], 'counters': [1, 6, 5]}
    {'orig': '?###????????', 'arrange': ['?###????????'], 'counters': [3, 2, 1]}
    '''

    ret = 0
    num_of_diez_to_fill = sum(o['counters'])  - o['str_as_list'].count('#')
    working_list = o['str_as_list'].copy()
    q_indices = set()
    for i in range(len(working_list)):
        if working_list[i] == '?':
            q_indices.add(i)

    combinations_iter = itertools.combinations(q_indices,num_of_diez_to_fill)
    for combination in combinations_iter:
        for i in q_indices:
            if i in combination:
                working_list[i] = '#'
            else:
                working_list[i] = '.'
        if calc_line_counters(''.join(working_list)) == o['counters']:
            ret += 1

    return ret


def part1_0():
    last_ts = time.time()
    # with open('r12_input.txt') as f:
    with open('r12_sample_input1.txt') as f:
        data = f.read().splitlines()
        lines = []
        sum = 0
        for line in data:
            line = parse(line)
            line_options = calc_options(line)
            print(line, line_options )
            sum += line_options
            lines.append(line)

    print(sum)
    print(time.time() - last_ts,' seconds')

def part1_1():
    last_ts = time.time()
    with open('r12_input.txt') as f:
    # with open('r12_sample_input1.txt') as f:
        data = f.read().splitlines()
        lines = []
        sum = 0
        for line in data:
            line = parse(line)
            line_options = calc_options_1(line)

            print(line, line_options )
            sum += line_options
            lines.append(line)

    print(sum)
    print(time.time() - last_ts,' seconds')



if __name__ == '__main__':

    # tests()

    #Candidate
    # failed because of ?????????#?#.#?.?.# 4,3,1,1,1
    part1_0()

    # part1_1()

    # Proven
    part1_BF(False)
