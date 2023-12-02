import re



# {'id': 1, 'resutls': [ {'r':4,'g':0,'b':3}, {'r':1,'g':2,'b':6}, {'r':0,'g':2,'b':0} ]
def analyze_line(line):
    ret = {'id':None,'results':[]}
    matches = re.match(r'Game ([0-9]*):(.*)',line)
    ret['id'] = int(matches.group(1))
    rounds = matches.group(2).split(';')
    rounds = [round.split(',') for round in rounds]
    for round_str in rounds:
        round = {'r':0,'g':0,'b':0}
        ret['results'].append(round)
        for colour in round_str:
            colour = colour.strip()
            match = re.match(r'^([0-9]*) ([r|g|b])',colour)
            count = int(match.group(1))
            colour = match.group(2)
            round[colour] = count
    return ret

def calc_max(rounds):
    max_per_color = {'r':0,'g':0,'b':0}
    for round in rounds['results']:
        for colour in ['r','g','b']:
            if round[colour] > max_per_color[colour]:
                max_per_color[colour] = round[colour]
    return max_per_color

if __name__ == '__main__':
    # tests()
    with open('r2_input.txt') as f:
    # with open('r2_sample_input.txt') as f:
        data = f.read().splitlines()
        max_res_calc = 0

        for line in data:
            r = analyze_line(line)
            max_per_color = calc_max(r)

            #r21
            #     #  only 12 red cubes, 13 green cubes, and 14 blue cubes.
            #     if max_per_color['r'] <= 12 and max_per_color['g'] <= 13 and max_per_color['b'] <= 14: #condition is possible
            #         # print(r['id'], max_per_color)
            #         max_res_calc += r['id']
            #         pass
            #     else:
            #         # print(r['id'], max_per_color)
            #         pass

            #r22
            cube_power = max_per_color['r']*max_per_color['g']*max_per_color['b']
            max_res_calc += cube_power

        print(max_res_calc)

