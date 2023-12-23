import re
import copy

SAMPLE_INPUT = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

def parse_input(input):
    lines = input.splitlines()
    rules = {}
    parts = []

    for i,l in enumerate(lines):
        l = l.strip()
        if l == '':
            break
        m = re.split(r'([a-z]*)\{(.*)\}', l)
        conds = m[2].split(',')
        default_state = conds[-1]
        conds1 = []
        for c in conds[:-1]:
            c = c.strip()
            m2 = re.split(r'([xmas])([><])([0-9]*):(.*)', c)
            conds1.append( {'name': m2[1], 'op': m2[2], 'value': int(m2[3]), 'res': m2[4] } )
        rules[m[1]] = { 'id': m[1] ,'conditions': conds1, 'default_state':default_state }


    for l in lines[i+1:]:
        l = l.strip()
        if l == '':
            break
        m = l[1:-1].split(',')
        values = {}
        for p in m:
            m2 = re.split(r'([xmas])=([0-9]*)', p)
            values[m2[1]] = int(m2[2])
        parts.append(values)

    return rules, parts

def part1(rules, parts):

    end_lists = {'A':[], 'R':[]}

    for p in parts:
        current_workflow = rules['in']
        while True:
            part_state = 'no_matched_conditions'
            for c in current_workflow['conditions']:
                if c['op'] == '>':
                    if p[c['name']] > c['value']:
                        if c['res'] in end_lists:
                            end_lists[c['res']].append(p)
                            part_state = 'part_sorted'
                            break
                        else:
                            current_workflow = rules[c['res']]
                            part_state = 'new_workflow'
                            break
                elif c['op'] == '<':
                    if p[c['name']] < c['value']:
                        if c['res'] in end_lists:
                            end_lists[c['res']].append(p)
                            part_state = 'part_sorted'
                            break
                        else:
                            current_workflow = rules[c['res']]
                            part_state = 'new_workflow'
                            break
                else:
                    raise Exception('Unknown operator')

            if part_state == 'no_matched_conditions':
                next_station = current_workflow['default_state']
                if next_station in end_lists:
                    end_lists[next_station].append(p)
                    part_state = 'part_sorted'
                else:
                    current_workflow = rules[  next_station ]
                    part_state = 'new_workflow'

            if part_state == 'new_workflow':
                continue
            elif part_state == 'part_sorted':
                break
            else:
                raise Exception('Unknown state')

    ret = 0
    for p in end_lists['A']:
        for v in p.values():
            ret += v
    return ret


class Range:
    start_inc: int = 0
    end_exc: int = 0

    def __init__(self, start_inc, end_exc):
        self.start_inc = start_inc
        self.end_exc = end_exc

def add_well_encapsulated_range(arr,shift:int ,range):
    arr.append({'start':range['start']+ shift, 'end': range['end']+ shift
                ,'source_start': range['start'], 'source_end': range['end']
                })

#
# def intersect_range_and_range_list(range:Range, sorted_range_list: list[Range]) -> list[Range]:
#     new_ranges : list[Range] = []
#
#
#     curr_start_inc = range.start_inc
#
#     for m in sorted_range_list: # type: Range
#         #diagram of cases in main.excalidraw
#
#         if range.start_inc >= m.end_exc : continue # case 0
#
#         # case 1
#         elif range.start_inc >= m.start_inc and range.start_inc < m.end_exc \
#             and range.end_exc > m.end_exc:
#
#             curr_start_inc = m.end_exc
#
#         # case 2
#         elif curr_start_inc >= m.start_inc and curr_start_inc < m.end_exc and \
#             range.end_exc >= m.start_inc and range.end_exc < m.end_exc:
#
#             break
#
#         # case 3
#         elif curr_start_inc < m.start_inc and curr_start_inc > m.end_exc:
#
#             m.start_inc = curr_start_inc
#             curr_start_inc = m.end_exc
#
#         # case 4
#         elif curr_start_inc < m.start_inc \
#                 and range.end_exc >= m.start_inc and range.end_exc < m.end_exc:
#
#             m.start_inc = curr_start_inc
#             break
#
#         elif range['end'] < m['source_start']:
#
#             break # case 5
#
#     if curr_start_inc <= range['end']:
#         add_well_encapsulated_range(ret,0,{'start':curr_start_inc, 'end': range['end']})
#
#     return ret
#

class Optional_Path:
    workflow: dict
    ranges: dict

    def __init__(self, workflow, ranges):
        self.workflow = workflow
        self.ranges = ranges

    def split_on_condition(self, condition, end_lists,rules):
        # 'px': {'id': 'px', 'conditions': [{'name': 'a', 'op': '<', 'value': 2006, 'res': 'qkq'},
        on_match, on_fail = None, None

        # case 0 All In
        if  condition['op'] == '>' and condition['value'] < self.ranges[condition['name']][0] \
            or condition['op'] == '<' and condition['value'] >= self.ranges[condition['name']][1]:
            on_match = self

    # case 1    All Out
        elif condition['op'] == '>' and (condition['value']+1) >= self.ranges[condition['name']][1] \
            or condition['op'] == '<' and condition['value'] <= self.ranges[condition['name']][0]:
            on_fail = self

        elif (condition['op'] == '>'
              and condition['value'] >= self.ranges[condition['name']][0] ):

            on_match = Optional_Path( self.workflow, copy.deepcopy(self.ranges))
            on_match.ranges[condition['name']][0] = condition['value'] + 1

            on_fail = Optional_Path(self.workflow, self.ranges)
            on_fail.ranges[condition['name']][1] = condition['value'] +1

        elif condition['op'] == '<' and condition['value'] > self.ranges[condition['name']][0] :

            on_match = Optional_Path( self.workflow, copy.deepcopy(self.ranges))
            on_match.ranges[condition['name']][1] = condition['value']

            on_fail = Optional_Path(self.workflow, self.ranges)
            on_fail.ranges[condition['name']][0] = condition['value']




        if on_match is not None:
            if condition['res'] in end_lists:
                end_lists[condition['res']].append(on_match.ranges)
                on_match = None
            else:
                on_match.workflow = rules[condition['res']]

        return on_match, on_fail

def calc_score(ranges_list:list):
    ret = 0
    for ranges in ranges_list:
        range_options = 1
        for r in ranges.values():
            range_options *= (r[1] - r[0])
        ret += range_options

    return ret



def part2(rules):

    end_lists = {'A':[], 'R':[]}
    possible_paths = []
    possible_paths.append(Optional_Path(rules['in'], {'x':[1,4001], 'm':[1,4001],'a':[1,4001],'s':[1,4001] } ))

    while len(possible_paths) > 0 :
        curr_path = possible_paths.pop()
        for c in curr_path.workflow['conditions']:
            cond_match_path , curr_path = curr_path.split_on_condition(c,end_lists,rules)
            if cond_match_path is not None:
                possible_paths.append(cond_match_path)
            elif curr_path is None:
                break
        if curr_path is not None:
            next_station = curr_path.workflow['default_state']
            if next_station in end_lists:
                end_lists[next_station].append(curr_path.ranges)
                continue
            else:
                possible_paths.append(Optional_Path(rules[next_station], curr_path.ranges))

    return calc_score(end_lists['A']),end_lists['A']

def _tests():
    rules, parts = parse_input(SAMPLE_INPUT)
    ret = part1(rules, parts)
    assert ret == 19114

    test_input = ''' \
        in{x<2001:A,R}    
    '''
    rules, parts = parse_input(test_input)
    ret = part2(rules)
    assert ret[0] == 128000000000000, ret

    test_input = ''' \
            in{x<2:A,m<2:A,R}    
        '''
    rules, parts = parse_input(test_input)
    ret = part2(rules)
    assert ret[0] == 127984000000, ret


    test_input = ''' \
            in{x<2:A,m<2:ctwo,R}
            ctwo{a<2:A,R}    
        '''
    rules, parts = parse_input(test_input)
    ret = part2(rules)
    assert ret[0] == 64015996000, ret



    test_input = ''' \
                in{x<3:ctwo,R}
                ctwo{x>2:A,R}    
            '''
    rules, parts = parse_input(test_input)
    ret = part2(rules)
    assert ret[0] == 0, ret



    test_input = ''' \
                in{x>10:ctwo,R}
                ctwo{x<11:A,R}    
            '''
    rules, parts = parse_input(test_input)
    ret = part2(rules)
    assert ret[0] == 0, ret

    rules, parts = parse_input(SAMPLE_INPUT)
    ret = part2(rules)
    assert ret[0]  == 167409079868000, ret



if __name__ == '__main__':
    _tests()

    with open('r19_input.txt') as f:
        rules, parts = parse_input(f.read())
        # ret = part1(rules, parts)
        ret = part2(rules)
        print(ret)
