import copy
import functools
import time

SAMPLE_INPUT_1 = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....\
"""


def  parse(lines: list[str]) -> list[list[str]]:
    ret = []
    max_len = 0
    for line in lines:
        line = line.strip()
        if len(line) > max_len:
            max_len = len(line)
        ret.append(list(line))
    for line in ret:
        line += ['.'] * (max_len - len(line))

    return ret

def tests():
    test_input = """\
    O.
    OOO#\
"""
    parse_ret = parse(test_input.splitlines())
    assert parse_ret == [['O', '.','.','.'], ['O', 'O', 'O', '#']]

    test_input = """\
    .
    O\
    """
    assert ((part_a(parse(test_input.splitlines())))[0]
            == [['O'], ['.']])

    test_input = """\
        .
        .
        O\
        """
    assert ((part_a(parse(test_input.splitlines())))[0]
            == [['O'], ['.'], ['.']])

    test_input = """\
            .
            #
            O\
            """
    assert ((part_a(parse(test_input.splitlines())))[0]
            == [['.'], ['#'], ['O']])

    test_input = """\
                #
                .
                OO\
                """
    grid = part_a(parse(test_input.splitlines()))[0]
    # print_grid(grid)
    assert grid == [['#','O'], ['O','.'], ['.','.']]

    test_input = """\
                    #
                    O
                    .
                    O\
                    """
    grid = part_a(parse(test_input.splitlines()))[0]
    # print_grid(grid)
    assert grid == [['#'], ['O'], ['O'], ['.']]

    test_input = """\
                OO
                .
                OO\
                """
    score = calc_score(parse(test_input.splitlines()))
    assert score == 8, score



    test_input = """\
                    #
                    O
                    .
                    O\
                    """
    grid = tilt_right(parse(test_input.splitlines()))
    assert grid == [['O', '.', 'O', '#']]

    test_input = """\
                        #
                        OO
                        .
                        OO\
                        """
    grid = tilt_right(parse(test_input.splitlines()))
    # print_grid(grid)
    assert grid == [['O', '.', 'O', '#'],['O', '.', 'O', '.']]

    lines, score = part_b(parse(SAMPLE_INPUT_1.splitlines()), 1)
    # print_grid(lines)
    assert score == 87, score

    lines, score = part_b(parse(SAMPLE_INPUT_1.splitlines()), 2)
    # print_grid(lines)
    assert score == 69, score

    lines, score = part_b(parse(SAMPLE_INPUT_1.splitlines()), 3)
    # print_grid(lines)
    assert score == 69, score


    # for l in parse_ret:
    #     print(l)

def print_grid(grid: list[list[str]]):
    for line in grid:
        print(''.join(line))

def calc_score(grid: list[list[str]]) -> int:
    ret = 0
    line_count = len(grid)
    for i,line in enumerate(grid):
        rocks = line.count('O')
        ret += rocks * (line_count - i)
    return ret


def push_up(lines: list[list[str]]):

    # Assumption: all lines are the same length
    for j in range(len(lines[0])):
        next_available_slot = 0
        for i in range(len(lines)):
            tmp_for_debug = lines[i][j]
            if lines[i][j] == '#':
                next_available_slot = i + 1
            elif lines[i][j] == 'O':
                if next_available_slot < i:
                    lines[i][j] = '.'
                    lines[next_available_slot][j] = 'O'
                next_available_slot = next_available_slot + 1

    return lines


def part_a(lines: list[list[str]]):
    lines = push_up(lines)
    score = calc_score(lines)
    return lines,score

def tilt_right(lines: list[list[str]]):
    # Assumption: all lines are the same length
    ret = []
    for i in range(len(lines[0])):
        ret.append([line[i] for line in reversed(lines)])
    return ret



def make_key(lines: list[list[str]]) -> str:
    return ','.join([''.join(line) for line in lines])

def part_b_one_cycle(lines: list[list[str]]):

    lines = copy.deepcopy(lines)

    lines = push_up(lines)
    lines = tilt_right(lines)  # west is up
    lines = push_up(lines)
    lines = tilt_right(lines)  # south is up
    lines = push_up(lines)
    lines = tilt_right(lines)  # east is up
    lines = push_up(lines)
    lines = tilt_right(lines)  # north is up

    return lines


class PatternRecognizer:
    def __init__(self, target: int, type):
        self.target = target
        self.type = type
        self.steps_map = {}
        self.steps = []

        self._is_in_loop:bool = False
        self.loop_start_key = None

    class Type:
        DETERMINISTIC = 1

    class Step:
        def __init__(self, key: str, score: int):
            self.key:str = key
            self.score:int = score



    def add_step(self, key: str, score: int):
        step = self.Step(key=key, score=score)

        if key not in self.steps_map:
            self.steps_map[key] = []
        else:
            self._is_in_loop = True
            self.loop_start_key = key

        self.steps.append(step)
        self.steps_map[key].append(len(self.steps) - 1)

    def is_in_loop(self, key: str) -> bool:
        return self._is_in_loop

    def get_expected_result(self) -> int:
        if not self._is_in_loop:
            return None

        loop_size = self.steps_map[self.loop_start_key][-1] - self.steps_map[self.loop_start_key][-2]
        needed_mod = self.target % loop_size
        loop_start_mod = (self.steps_map[self.loop_start_key][-2]+1) % loop_size
        diff = (needed_mod - loop_start_mod) % loop_size
        needed_index = self.steps_map[self.loop_start_key][-2] + diff
        return self.steps[needed_index].score


def part_b(lines: list[list[str]],cycle_num: int):
    cache = {}

    pr = PatternRecognizer(target=1000*1000*1000,type = PatternRecognizer.Type.DETERMINISTIC)

    for i in range(cycle_num):
        key = make_key(lines)

        if key not in cache:
            next_lines = part_b_one_cycle(lines)
            cache[key] = next_lines
        else :
            next_lines = cache[key]

        lines = next_lines

        score = calc_score(lines)
        # print ('\n ------------------')
        # print()
        print (i, score)

        pr.add_step(key=key, score=score)

        if pr.is_in_loop(key):
            print('pattern found at', i, ' expected result at ' , pr.target , ' is ', pr.get_expected_result() )
            break

        # print_grid(lines)

    return lines,score





if __name__ == '__main__':
    # tests()

    # with open('r14_input.txt', 'r') as f:
    #     lines, score = part_a(parse(f.readlines()))
    #     assert score == 108857, score
    #
    # lines, score = part_b(parse(SAMPLE_INPUT_1.splitlines()), 100)
    # print (score)

    with open('r14_input.txt', 'r') as f:
        lines, score = part_b(parse(f.read().splitlines()), 10000)
        # print(score)
