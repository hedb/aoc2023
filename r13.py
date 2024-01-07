

SAMPLE_INPUT_1 = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

SAMPLE_INPUT_2 = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
"""

SAMPLE_INPUT_3 = """\
.#...####.##..#
..#.###...#.##.
..#.###...#.##.
.#...####.##..#
.####..##.##..#
.####.#.###.##.
####..#.#######
#.......####..#
####.#.#.......
..#....##.#####
.##.##...##.###
..#.#.#.##.....
.....##.#..####
##..#.###..####
.##..#...######"""

SAMPLE_INPUT_4 = """\
##....##.
##.##.###
.#.##.#.#
..#..#..#
........#
........#
..#..#..#
.#.##.#.#
##.##.###
##....##.
.##..#..."""

def calc_reflection(lines: list[str]) -> int :
    if len(lines) == 0:
        return 0

    str_map = {}
    id_map = {}

    for i,line in enumerate(lines):
        if line in str_map:
            str_map[line]['ids'].append(i)
        else:
            str_map[line] = {'str': line, 'ids': [i] }

        id_map[i] = str_map[line]


    h_verifications = []
    first_line_matcher = str_map[lines[0]]
    if len(first_line_matcher['ids']) >= 2:
        for i in first_line_matcher['ids']:
            if i != 0:
                h_verifications.append( [0, i] )

    last_line_matcher = str_map[lines[-1]]
    if len(last_line_matcher['ids']) >= 2:
        for i in last_line_matcher['ids']:
            if i != len(lines)-1:
                h_verifications.append( [i, len(lines)-1] )

    sum = 0
    for h_ver in h_verifications:
        confirmed = True
        contribution = (h_ver[1] - h_ver[0] + 1) / 2 + h_ver[0]
        mirrored_rows = h_ver
        for i in range(len(lines)):
            mirrored_rows[0] += 1
            mirrored_rows[1] -= 1
            if mirrored_rows[0] >= mirrored_rows[1]:
                break
            if lines[mirrored_rows[0]] != lines[mirrored_rows[1]]:
                confirmed = False
                break
        if confirmed:
            # print (" receiving contribution: ", contribution, " from ", h_ver)
            sum += contribution

    return sum

def transpose(lines: list[str]) -> list[str]:
    if len(lines) == 0:
        return []
    return  [''.join([line[i].strip() for line in lines]) for i in range(len(lines[0]))]


def part_a(lines: list[str]):

    sum_vertical = 0
    sum_horizontal = 0

    lines.append("")
    current_part_start = 0
    for i,line in enumerate(lines):
        if line.strip() == "":
            sum_vertical += calc_reflection(lines[current_part_start:i])
            lines_t = transpose(lines[current_part_start:i])
            sum_horizontal += calc_reflection(lines_t)
            current_part_start = i + 1

    return sum_vertical*100 + sum_horizontal

def _tests():
    input = """\
.#.#
.#.#
.#.#
.#.#"""
    output = """\
....
####
....
####"""
    assert transpose(input.splitlines()) == output.splitlines()

    input = """\
1234567890
1234567890
"""
    output = """\
11
22
33
44
55
66
77
88
99
00
"""
    assert transpose(input.splitlines()) == output.splitlines()

    input = """\
#.######.#..###
.#..##....#..##
####..####.##..
###.##.####....
####..#######..
.#......#.#.#..
.#......#..#...
#..#..#..#...##
#.#.##.#.##.###
"""

    print (transpose(input.splitlines()))



def _test_part_a():
    ret = part_a(SAMPLE_INPUT_1.splitlines())
    assert ret == 405, ret

    # print(part_a(SAMPLE_INPUT_2.splitlines()))
    # print(part_a(SAMPLE_INPUT_3.splitlines()))
    # print(part_a(SAMPLE_INPUT_4.splitlines()))

    # with open('r13_sample_input1.txt') as f:
    with open('r13_input.txt') as f:
        lines = f.read().splitlines()
        ret = part_a(lines)
        print(ret)

if __name__ == "__main__":

    # with open('r13_sample_input1.txt') as f:
    #     lines = f.read().splitlines()
    #     lines = transpose(lines)
    #     for line in lines:
    #         print(line)
    # tests()

    _test_part_a()