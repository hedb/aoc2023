
import re
import time
import math

def parse_line_into_json(input_line):
    ret = re.split(':| \| ', input_line)
    return ret


def part1_0():
    last_ts = time.time()
    # with open('r6_input.txt') as f:
    with open('r7_sample_input.txt') as f:
        data = f.read().splitlines()
        lines = []
        for line in data:
            line = parse_line_into_json(line)
            lines.append(line)

    for l in lines:
        print(l)
    print(time.time() - last_ts,' seconds')


def calc_races_options(t,d) :

    root1 = (t - math.sqrt(t**2 -4*d) ) /2 + .000000000001
    root2 = (t + math.sqrt(t**2 -4*d) ) /2 -.000000000001
    ret = math.floor(root2) - math.ceil(root1) +1
    return ret

    # speed = (hold*hold+1) / 2
    # travel_time = time - hold
    # distance = speed * travel_time = (hold*hold+1) / 2 * (time - hold)


if __name__ == '__main__':

    # races = [(7,9), (15,40), (30,200)]
    # races = [(41, 249), (77, 1362), (70, 1127), (96, 1011)]
    races =  [(41777096,249136211271011)]

    calc_races_options_arr = [calc_races_options(r[0],r[1]) for r in races]
    #multiply all scores
    ret = 1
    for s in calc_races_options_arr:
        ret *= s
    print (ret)



