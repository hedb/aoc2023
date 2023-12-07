
import re
import time
import math


def parse_line_into_json(input_line):
    ret = re.split(' ', input_line)
    ret = {'hand': ret[0], 'bid':int(ret[1])}
    return ret

def analyze_hand(line):
    m = {}
    m1 = {}
    for c in line['hand']:
        m[c] = m.get(c, 0) + 1
    for v in m.values():
        m1[v] = m1.get(v, 0) + 1

    if 5 in m1:
        line['hand_type'] = 'Five of a kind'
        line['hand_value'] = 7
    elif 4 in m1:
        line['hand_type'] = 'Four of a kind'
        line['hand_value'] = 6
    elif 3 in m1 and 2 in m1:
        line['hand_type'] = 'Full house'
        line['hand_value'] = 5
    elif 3 in m1:
        line['hand_type'] = 'Three of a kind'
        line['hand_value'] = 4
    elif 2 in m1 and m1[2] == 2:
        line['hand_type'] = 'Two pair'
        line['hand_value'] = 3
    elif 2 in m1:
        line['hand_type'] = 'One pair'
        line['hand_value'] = 2
    else:
        line['hand_type'] = 'Nothing'
        line['hand_value'] = 1

    card_values_b13 = {'A':12, 'K':11, 'Q':10, 'J':9, 'T':8, '9':7, '8':6, '7':5, '6':4, '5':3, '4':2, '3':1, '2':0}
    card_value = \
        card_values_b13[line['hand'][0]] * 13**4 + \
        card_values_b13[line['hand'][1]] * 13**3 + \
        card_values_b13[line['hand'][2]] * 13**2 + \
        card_values_b13[line['hand'][3]] * 13**1 + \
        card_values_b13[line['hand'][4]] * 13**0
    line['cards_value'] = card_value

    line['combined_value'] = line['hand_value'] * 13**5 + card_value

    return line


def analyze_hand2(line):
    m = {}
    m1 = {}
    for c in line['hand']:
        m[c] = m.get(c, 0) + 1

    if 'J' in m:
        joker_count = m['J']
        m['J'] = 0
        top_one_to_join = max(m.values())
        for k in m:
            if m[k] == top_one_to_join:
                m[k] += joker_count
                break

    for v in m.values():
        m1[v] = m1.get(v, 0) + 1


    if 5 in m1:
        line['hand_type'] = 'Five of a kind'
        line['hand_value'] = 7
    elif 4 in m1:
        line['hand_type'] = 'Four of a kind'
        line['hand_value'] = 6
    elif 3 in m1 and 2 in m1:
        line['hand_type'] = 'Full house'
        line['hand_value'] = 5
    elif 3 in m1:
        line['hand_type'] = 'Three of a kind'
        line['hand_value'] = 4
    elif 2 in m1 and m1[2] == 2:
        line['hand_type'] = 'Two pair'
        line['hand_value'] = 3
    elif 2 in m1:
        line['hand_type'] = 'One pair'
        line['hand_value'] = 2
    else:
        line['hand_type'] = 'Nothing'
        line['hand_value'] = 1

    card_values_b13 = {'A':12, 'K':11, 'Q':10, 'T':9, '9':8, '8':7, '7':6, '6':5, '5':4, '4':3, '3':2, '2':1, 'J':0 }
    card_value = \
        card_values_b13[line['hand'][0]] * 13**4 + \
        card_values_b13[line['hand'][1]] * 13**3 + \
        card_values_b13[line['hand'][2]] * 13**2 + \
        card_values_b13[line['hand'][3]] * 13**1 + \
        card_values_b13[line['hand'][4]] * 13**0
    line['cards_value'] = card_value

    line['combined_value'] = line['hand_value'] * 13**5 + card_value

    return line


def part1_0():
    last_ts = time.time()
    with open('r7_input.txt') as f:
    # with open('r7_sample_input.txt') as f:
        data = f.read().splitlines()
        hands = []
        for line in data:
            line = parse_line_into_json(line)
            line = analyze_hand2(line)
            hands.append(line)


    hands.sort(key=lambda x: x['combined_value'], reverse=False)

    win_sum = 0
    for i,hand in enumerate(hands):
        win_sum += hand['bid'] * (i+1)

    print(win_sum)


if __name__ == '__main__':
    part1_0()