

def r1() :

    sum_first  = 0
    sum_second  = 0

    with open('r1_1_input.txt') as f:
        data = f.read().splitlines()
        for line in data:
            # print(line)
            already_met_first_digit = None
            last_char = 0
            for c in line:
                #check if c is a digit
                if c.isdigit():
                    if not already_met_first_digit:
                        already_met_first_digit = True
                        sum_first += int(c)
                    last_char = int(c)
            sum_second += last_char

    sum = sum_first*10 + sum_second
    print(sum)

def r2(lines):
    sum_first  = 0
    sum_second  = 0

    digits = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    for line in lines:
        kl =  keyword_listener(digits.keys())
        already_met_first_digit = None
        last_char = 0
        c_int_val = None
        for c in line:
            if c.isdigit():
                kl.accept_char(c) # just to reset the state
                c_int_val = int(c)
            else :
                ret = kl.accept_char(c)
                if (ret != None):
                    c_int_val = digits[ret]
            if c_int_val != None:
                if not already_met_first_digit:
                    already_met_first_digit = True
                    sum_first += c_int_val
                last_char = c_int_val
        sum_second += last_char

    sum = sum_first*10 + sum_second
    print(sum)



class keyword_listener:
    def __init__(self, possible_keywords):
        self.keyword_data = {}
        for keyword in possible_keywords:
            self.keyword_data[keyword] = {'current_index': 0, 'len': len(keyword)}

    def accept_char(self, c):
        ret = None
        for keyword, v in self.keyword_data.items():
            if keyword[v['current_index']] == c:
                v['current_index'] += 1
                if v['current_index'] == v['len']:
                    ret = keyword
                    v['current_index'] = 0
            else:
                v['current_index'] = 1 if keyword[0] == c else 0

        return ret


def tests():
    keyword_listener_test = keyword_listener(['abc'])
    assert(keyword_listener_test.accept_char('a') == None)
    assert(keyword_listener_test.accept_char('b') == None)
    assert(keyword_listener_test.accept_char('c') == 'abc')

    assert(keyword_listener_test.accept_char('a') == None)
    assert(keyword_listener_test.accept_char('b') == None)
    assert(keyword_listener_test.accept_char('b') == None)
    assert(keyword_listener_test.accept_char('c') == None)


    keyword_listener_test = keyword_listener(['abce', 'bcd'])
    assert(keyword_listener_test.accept_char('a') == None)
    assert(keyword_listener_test.accept_char('b') == None)
    assert(keyword_listener_test.accept_char('c') == None)
    assert(keyword_listener_test.accept_char('d') == 'bcd')

    keyword_listener_test = keyword_listener(['ab'])
    assert (keyword_listener_test.accept_char('a') == None)
    assert (keyword_listener_test.accept_char('a') == None)
    assert (keyword_listener_test.accept_char('b') == 'ab')

    keyword_listener_test = keyword_listener(['nine'])
    assert(keyword_listener_test.accept_char('n') == None)
    assert(keyword_listener_test.accept_char('n') == None)
    assert(keyword_listener_test.accept_char('i') == None)
    assert(keyword_listener_test.accept_char('n') == None)
    assert(keyword_listener_test.accept_char('e') == 'nine')






if __name__ == '__main__':

    # tests()

    # r1()
    #
    with open('r1_1_input.txt') as f:
        data = f.read().splitlines()
        # data = ['two1nine','eightwothree','abcone2threexyz','xtwone3four','4nineeightseven2','zoneight234','7pqrstsixteen']
        # data = ['fiveh1eight']
        # data = ['two75four85']
        # data = ['afasdtwosasda']
        # data = ['5aaatwo']
        # data = ['zspb1sevennine76one']
        # data = ['sevennine']
        r2 (data)