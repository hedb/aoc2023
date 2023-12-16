import re

INPUT_SAMPLE = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,
pc=
6,ot=7
"""

def parse_input(input_str) -> list[str] :
    return ''.join(input_str.splitlines()).split(',')


def calc_for_str(input_str):
    ret = 0
    for c in input_str:
        ret += ord(c)
        ret *= 17
        ret %= 256
    return ret

def part_1(lines):
    ret = 0
    for line in lines:
        ret += calc_for_str(line)
    return ret

def _tests():
    assert calc_for_str('HASH') == 52
    assert part_1(parse_input(INPUT_SAMPLE)) == 1320

    part_2(parse_input(INPUT_SAMPLE))


class Box:
    def __init__(self,id)  :
        self.id = id
        self.lenses : list[Lens] = []

    def __str__(self):
        ret = ''
        if len(self.lenses) != 0:
            ret = f'Box {self.id}'
            for lens in self.lenses:
                ret += f' {lens}'
            ret += '\n'
        return ret

class Lens:
    def __init__(self,label,value) :
        self.label = label
        self.value = value

    def __str__(self):
        return f'[{self.label} {self.value}]'

def print_boxes(boxes):
    # Box 0: [rn 1] [cm 2]
    for box in boxes:
        print(box, end='')


def part_2(lines):
    boxes : list[Box] = []
    for i in range(256):
        boxes.append(Box(i))

    for line in lines:
        m = re.split(r'([-=])',line)
        box_id = calc_for_str(m[0])
        op = m[1]
        lenses = boxes[box_id].lenses
        if op == '=':
            value = int(m[2])
            found = False
            for lens in lenses:
                if lens.label == m[0]:
                    lens.value = value
                    found = True
            if not found:
                lenses.append(Lens(m[0],value))
        elif op == '-':
            for lens in lenses:
                if lens.label == m[0]:
                    lenses.remove(lens)

    print_boxes(boxes)
    ret = 0
    for i,box in enumerate(boxes):
        for j,lens in enumerate(box.lenses):
            ret += (1+i)*(1+j)*lens.value
    print(ret)


if __name__ == '__main__':
    # _tests()

    with open('r15_input.txt') as f:
        lines = parse_input(f.read())
        part_2(lines)


    pass