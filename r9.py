
import re
import time
import math


def parse(input_line):
    ret = re.split(' ', input_line)
    ret = [int(x) for x in ret]
    return ret


def part1_0():
    last_ts = time.time()
    with open('r9_input.txt') as f:
    # with open('r9_sample_input.txt') as f:
        data = f.read().splitlines()
        lines = []
        for line in data:
            line = parse(line)
            lines.append(line)


    ret = 0
    ret1 = 0
    for orig_line in lines:
        diff_series = []
        solved = False

        l = orig_line
        while not solved:
            diffs = []
            for i,n in enumerate(l[:-1]):
                diffs.append(l[i+1]-l[i] )
            if len(diffs) == 1 or all([d == 0 for d in diffs]):
                solved = True
            diff_series.append(diffs)
            l = diffs

        next_value = sum([s[-1] for s in diff_series]) + orig_line[-1]

        tmp = 0
        for i in range(len(diff_series)):
            tmp += pow(-1,i) * diff_series[i][0]
        prev_value = orig_line[0] - tmp

        ret += next_value
        ret1 += prev_value


    print(ret , ret1)
    print(time.time() - last_ts,' seconds')



if __name__ == '__main__':
    part1_0()