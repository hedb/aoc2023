
import re
import time
import math


def parse_line_into_json(input_line):
    ret = re.split(':| \| ', input_line)
    return ret


def part1_0():
    last_ts = time.time()
    # with open('rX_input.txt') as f:
    with open('rX_sample_input.txt') as f:
        data = f.read().splitlines()
        lines = []
        for line in data:
            line = parse_line_into_json(line)
            lines.append(line)

    for l in lines:
        print(l)
    print(time.time() - last_ts,' seconds')



if __name__ == '__main__':
    part1_0()