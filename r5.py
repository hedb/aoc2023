
import re
import time
import math

def parse_line_into_json(input_line):
    ret = re.split(':| \| ', input_line)
    return ret


def part1_0():
    last_ts = time.time()
    with open('r5_input.txt') as f:
    # with open('r5_sample_input.txt') as f:
        lines = f.read().splitlines()
        seeds = re.match('seeds: *(.*)',lines[0])
        seeds = seeds.group(1).split(' ')
        seeds = [int(s) for s in seeds]

        maps = []
        for line in lines[1:]:
            if line == '': continue
            if line[0].isalpha():
                maps.append(curr_map := {'name': line, 'mapping': [] })
            else:
                mapping = line.split(' ')
                curr_map['mapping'].append({'source': int(mapping[1]), 'dest': int(mapping[0]), 'range': int(mapping[2]) })

        for m in maps:
            m['dest'] = sorted(m['mapping'], key=lambda x: x['dest'])
            m['source'] = sorted(m['mapping'], key=lambda x: x['source'])

        locations = []
        for seed in seeds:

            location = calc_location_per_seed(maps, seed)

            # print(f'{seed} -> {curr_source}')
            locations.append(location)

        print(min(locations))


def calc_location_per_seed(maps, seed):
    curr_source = seed
    # Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    for m in maps:
        # print("name", m['name'],'  curr-source', curr_source)
        # locate the right source range
        for mapping in m['source']:
            if curr_source < mapping['source']: continue
            if curr_source >= mapping['source'] and curr_source < mapping['source'] + mapping['range']:
                curr_source = mapping['dest'] + (curr_source - mapping['source'])
                break
    return curr_source


def safe_pop (l:list):
    ret = None
    if len(l) > 0 :
        ret = l.pop(0)
    return ret


def add_well_encapsulated_range(arr,shift:int ,range):
    arr.append({'start':range['start']+ shift, 'end': range['end']+ shift
                ,'source_start': range['start'], 'source_end': range['end']
                })

def explode_range(range,mapping):
    ret = []
    curr_range_start = range['start']
    for m in mapping:
        #diagram of cases in main.excalidraw
        if curr_range_start > m['source_end'] : continue # case 0

        # case 1
        elif curr_range_start <= m['source_end'] and curr_range_start > m['source_start'] \
            and range['end'] > m['source_end']:
            add_well_encapsulated_range(ret,m['shift'],{'start':curr_range_start, 'end': m['source_end']})
            curr_range_start = m['source_end'] + 1

        # case 2
        elif curr_range_start <= m['source_end'] and curr_range_start >= m['source_start'] \
            and range['end'] <= m['source_end']:
            add_well_encapsulated_range(ret,m['shift'],{'start':curr_range_start, 'end': range['end']})
            curr_range_start = range['end'] + 1 # signal not to add any more ranges
            break

        # case 3
        elif curr_range_start < m['source_start'] \
             and range['end'] > m['source_end']:

            add_well_encapsulated_range(ret,0,{'start':curr_range_start, 'end': m['source_start']-1})
            add_well_encapsulated_range(ret,m['shift'],{'start':m['source_start'], 'end': m['source_end']})
            curr_range_start = m['source_end'] + 1

        # case 4
        elif curr_range_start < m['source_start'] \
                and range['end'] >= m['source_start'] and range['end'] <= m['source_end']:
            add_well_encapsulated_range(ret,0,{'start':curr_range_start, 'end': m['source_start']-1})
            add_well_encapsulated_range(ret,m['shift'],{'start':m['source_start'], 'end': range['end']})
            curr_range_start = range['end'] + 1 # signal not to add any more ranges
            break

        elif range['end'] < m['source_start']: break # case 5

    if curr_range_start <= range['end']:
        add_well_encapsulated_range(ret,0,{'start':curr_range_start, 'end': range['end']})

    return ret




def part2_0():
    last_ts = time.time()
    with open('r5_input.txt') as f:
    # with open('r5_sample_input.txt') as f:
        lines = f.read().splitlines()
        seeds_and_ranges = re.match('seeds: *(.*)',lines[0])
        seeds_and_ranges = seeds_and_ranges.group(1).split(' ')
        seeds_and_ranges = [int(s) for s in seeds_and_ranges]

        seeds_m = [ [],[],[],[],[],[],[] ,[]]
        i = 0
        while i < len(seeds_and_ranges):
            # seeds.extend(range(seeds_and_ranges[i], seeds_and_ranges[i] +seeds_and_ranges[i+1]))
            seeds_m[0].append({'start':seeds_and_ranges[i],'end':seeds_and_ranges[i] +seeds_and_ranges[i+1] -1})
            i+= 2



        maps = []
        for line in lines[1:]:
            if line == '': continue
            if line[0].isalpha():
                maps.append(curr_map := {'name': line, 'mapping': [] })
            else:
                mapping = line.split(' ')
                new_mapping = {'source_start': int(mapping[1]),'dest': int(mapping[0]), 'range': int(mapping[2]) }
                new_mapping['source_end'] = new_mapping['source_start'] + new_mapping['range'] -1
                new_mapping['shift'] = new_mapping['dest'] - new_mapping['source_start']
                curr_map['mapping'].append(new_mapping)

        for m in maps:
            # m['dest'] = sorted(m['mapping'], key=lambda x: x['dest'])
            m['source'] = sorted(m['mapping'], key=lambda x: x['source_start'])


        locations = []

        for map_i,m in enumerate(maps):
            # print(map_i, " : ",m['name']," : ",m['source'])
            while (curr_source:=safe_pop(seeds_m[map_i])) != None:
                well_encapsulated_ranges = explode_range(curr_source,m['source'])
                seeds_m[map_i+1].extend(well_encapsulated_ranges)
                # print (well_encapsulated_ranges)

        min_location = math.inf
        for location in seeds_m[-1]:
            min_location = min(min_location,location['start'])
        print(min_location)




def test_exploded_part():

    range = {'start': 10, 'end': 15}
    mapping = [{'source_start': 0, 'source_end': 5}]
    # case 0
    ret = (explode_range(range, mapping ))
    assert ret == [{'start': 10, 'end': 15}]

    # case 1
    mapping.append({'source_start': 8, 'source_end': 12})
    ret = (explode_range(range, mapping))
    assert ret == [{'start': 10, 'end': 12}, {'start': 13, 'end': 15}]

    # case 2
    mapping =  [{'source_start': 0, 'source_end': 20}]
    ret = (explode_range(range, mapping))
    assert ret == [{'start': 10, 'end': 15}]

    # case 3
    mapping = [{'source_start': 12, 'source_end': 14}]
    ret = (explode_range(range, mapping))
    assert ret == [{'start': 10, 'end': 11}, {'start': 12, 'end': 14}, {'start': 15, 'end': 15}]

    # case 4
    mapping = [{'source_start': 12, 'source_end': 20}]
    ret = (explode_range(range, mapping))
    assert ret == [{'start': 10, 'end': 11}, {'start': 12, 'end': 15}]

    # case 5
    mapping = [{'source_start': 16, 'source_end': 20}]
    ret = (explode_range(range, mapping))
    assert ret == [{'start': 10, 'end': 15}]

    # print (ret)
    pass




if __name__ == '__main__':
    # part1_0()
    # test_exploded_part()
    part2_0()