import re

def analyze_line(line,only_asterisk=False):
    numbers = []
    symbols = set()
    curr_index = 0
    # {'&', '@', '=', '+', '-', '*', '#', '%', '$', '/'}
    split_parts = re.split('(\&|\@|\=|\+|\-|\*|\#|\%|\$|\/|\.)',line)
    for p in split_parts:
        if p == '':
            continue
        elif p[0].isdigit():
            numbers.append({'v':int(p),'start':curr_index,'end':curr_index+len(p)-1})
        elif p[0] != '.':
            if not only_asterisk or p[0] == '*':
                symbols.add(curr_index)
        curr_index += len(p)

    return numbers, symbols

def print_all_different_chars(lines):
    chars = set()
    for line in lines:
        for c in line:
            if not c.isdigit() and c != '.':
                chars.add(c)
    print(chars)

def as_matix_has_symbol(symbol_lines,y,x):
    ret = False
    if y >= 0 and y < len(symbol_lines):
        ret = x in symbol_lines[y]
    return ret


def attempt2():
    # tests()
    number_lines = []
    symbol_lines = []
    with open('r3_input.txt') as f:
    # with open('r3_sample_input.txt') as f:
        data = f.read().splitlines()
        # print_all_different_chars(data)
        # exit()
        for line in data:
            n,s = analyze_line(line)
            number_lines.append(n)
            symbol_lines.append(s)
        # number_lines.append([]);number_lines.insert(0,[])
        # symbol_lines.append(set());symbol_lines.insert(0,set())

    sum = 0
    for i,number_line in enumerate(number_lines):
        for n in number_line:
            number_added = False
            for y_diff in [-1,0,1]:
                for x in range(n['start']-1,n['end']+2):
                    if as_matix_has_symbol(symbol_lines,i+y_diff,x):
                        print(f"number {n} is touching symbol at {i+y_diff},{x}")
                        sum += n['v']
                        number_added = True
                        break
                if number_added:
                    break
    print(sum)



def part2_1():
    # tests()
    number_lines = []
    asterisk_lines = []
    with open('r3_input.txt') as f:
    # with open('r3_sample_input.txt') as f:
        data = f.read().splitlines()
        # print_all_different_chars(data)
        # exit()
        for line in data:
            n,s = analyze_line(line,only_asterisk=True)
            number_lines.append(n)
            asterisk_lines.append(s)

    asterisk_map = {}
    for i,number_line in enumerate(number_lines):
        for n in number_line:
            number_added = False
            for y_diff in [-1,0,1]:
                for x in range(n['start']-1,n['end']+2):
                    if as_matix_has_symbol(asterisk_lines,i+y_diff,x):
                        print(f"number {n} is touching asterisk at {i+y_diff},{x}")
                        asterisk_key = (i+y_diff,x)
                        if asterisk_key not in asterisk_map:
                            asterisk_map[asterisk_key] = {'numbers':[]}
                        asterisk_map[asterisk_key]['numbers'].append(n)

    sum = 0
    for k,v in asterisk_map.items():
        # print(k,v)
        if len(v['numbers']) == 2:
            sum += v['numbers'][0]['v'] * v['numbers'][1]['v']
        elif len(v['numbers']) > 2:
            print(f"too many numbers for asterisk at {k}")
            exit()
    print(sum)


def attempt1():
    # tests()
    # with open('r3_input.txt') as f:
    number_lines = []
    symbol_lines = []
    with open('r3_sample_input.txt') as f:
        data = f.read().splitlines()
        # print_all_different_chars(data)
        for line in data:
            n,s = analyze_line(line)
            number_lines.append(n)
            symbol_lines.append(s)
        number_lines.append([]);number_lines.insert(0,[])
        symbol_lines.append(set());symbol_lines.insert(0,set())


        for i,s in enumerate(symbol_lines[:-1]):
            if i == 0 : continue
            current_influencing_sumbols = symbol_lines[i - 1].union(symbol_lines[i]).union(symbol_lines[i + 1])
            sorted_influencing_symbols = sorted(list(current_influencing_sumbols))
            numbers = number_lines[i]
            numbers_index = 0
            touched_numbers = []
            for s in sorted_influencing_symbols:
                while numbers_index <len(numbers) and numbers[numbers_index]['end'] < s-1:
                    numbers_index +=1
                if s >= numbers[numbers_index]['start']-1 and s <= numbers[numbers_index]['end']+1:
                    touched_numbers.append(numbers[numbers_index])

            print(touched_numbers)

if __name__ == '__main__':
    # attempt2()
    part2_1()