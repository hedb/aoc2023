import re
import time

def parse_line_into_json(input_line):
    # Splitting the line into id, wins, have parts
    card, elements = input_line.split(':')
    card_id = re.match('Card *([0-9]*)',card)[1]
    elements = elements.split(' | ')
    wins = [int(x) for x in elements[0].split()]
    have = [int(x) for x in elements[1].split()]

    # Creating the dictionary
    dict_line = {"id": int(card_id), "wins": wins, "have": have, 'type':'orig'}

    return dict_line

def part1():
    # tests()
    with open('r4_input.txt') as f:
    # with open('r4_sample_input.txt') as f:
        data = f.read().splitlines()
        sum = 0
        for line in data:
            print(line)
            l_obj = parse_line_into_json(line)
            actual_wins = set(l_obj['wins']).intersection(set(l_obj['have']))
            points = pow(2,len(actual_wins)-1) if len(actual_wins) > 0 else 0
            sum += points
        print(sum)


def safe_pop(l):
    if len(l) > 0:
        return l.pop(0)
    else:
        return None

def part2_1():
    # tests()
    with open('r4_input.txt') as f:
    # with open('r4_sample_input.txt') as f:
        data = f.read().splitlines()
        cards = []
        for line in data:
            l_obj = parse_line_into_json(line)
            actual_wins = len(set(l_obj['wins']).intersection(set(l_obj['have'])))
            cards.append({'id':l_obj['id']-1, 'wins':actual_wins, 'cards_of_type':1})

        sum_cards = 0
        for c in cards:
            sum_cards += c['cards_of_type']
            for i in range(c['wins']):
                cards[c['id'] + i + 1]['cards_of_type'] += c['cards_of_type']
        print(sum_cards)




def part2():
    # tests()
    # with open('r4_input.txt') as f:
    with open('r4_sample_input.txt') as f:
        data = f.read().splitlines()
        cards = {}
        for line in data:
            l_obj = parse_line_into_json(line)
            cards[l_obj['id']]  = [l_obj]

    last_ts = time.time()
    cur_ind = 1
    cards_res = {}
    cards_played = 0
    while cur_ind <= len(cards):
        cur_card = safe_pop(cards[cur_ind])
        if cur_card == None:
            cur_ind += 1
            print('Moving to:', cur_ind, 'cards played:', cards_played, 'time taken:', time.time() - last_ts)
            last_ts = time.time()
            continue
        else:
            cards_played += 1
            if cur_card['type'] == 'orig':
                cards_res[cur_ind] = len(set(cur_card['wins']).intersection(set(cur_card['have'])))
            copies_won = cards_res[cur_ind]
            for i in range(copies_won):
                cards[cur_ind + i + 1].append({'id':cur_card['id'], 'type':'copy'})

    print(cards_played)




if __name__ == '__main__':
    part2_1()