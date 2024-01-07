
def parse_input(input_string):
    # Split the input string by lines and strip surrounding whitespace
    lines = [line.strip() for line in input_string.strip().split('\n')]

    # Initialize an array to hold the result and a temporary array for current chunk
    result = []
    current_chunk = []

    for line in lines:
        if line:
            # Add the line to the current chunk
            current_chunk.append(line)
        else:
            # If the line is empty, add the current chunk to the result and reset the chunk
            if current_chunk:
                result.append(current_chunk)
                current_chunk = []

    # Add any remaining chunk to the result (if input doesn't end with an empty line)
    if current_chunk:
        result.append(current_chunk)

    return result

def _test_transpose():
    # Test case 1: Square matrix
    matrix1 = ["abc", "def", "ghi"]
    expected1 = ["adg", "beh", "cfi"]
    assert transpose(matrix1) == expected1, "Test case 1 failed"

    # Test case 2: Rectangular matrix (more rows)
    matrix2 = ["ab", "cd", "ef"]
    expected2 = ["ace", "bdf"]
    assert transpose(matrix2) == expected2, "Test case 2 failed"

    # Test case 3: Rectangular matrix (more columns)
    matrix3 = ["abc", "def"]
    expected3 = ["ad", "be", "cf"]
    assert transpose(matrix3) == expected3, "Test case 3 failed"

    # Test case 4: Empty matrix
    matrix4 = []
    expected4 = []
    assert transpose(matrix4) == expected4, "Test case 4 failed"

    # Test case 5: Matrix with single-character strings
    matrix5 = ["a", "b", "c"]
    expected5 = ["abc"]
    assert transpose(matrix5) == expected5, "Test case 5 failed"



def _tests():
    _test_find_identical_lines()
    _test_verify_reflection_lines()
    _test_transpose()


def find_identical_lines(lines):
    result = []
    # Iterate through each line
    for i, line in enumerate(lines):
        # Initialize dictionary for the current line
        line_dict = {
            "id": i,
            "forward_identical": [],
            "backward_identical": [],
            "possible_mirror_line": False
        }

        # Check for identical lines after the current line
        for j in range(i + 1, len(lines)):
            if line == lines[j]:
                line_dict["forward_identical"].append(j)
                # Check if the immediate next line is identical
                if j == i + 1:
                    line_dict["possible_mirror_line"] = True

        # Check for identical lines before the current line
        for j in range(i):
            if line == lines[j]:
                line_dict["backward_identical"].append(j)

        # Add the dictionary to the result list
        result.append(line_dict)

    return result

def _test_verify_reflection_lines():
    # Test case 1: All lines identical
    lines1 = ["same", "same", "same"]
    expected1 = [0, 1]
    assert verify_reflection_lines(find_identical_lines(lines1)) == expected1, "Test case 1 failed"

    # Test case 2: First two lines identical, third different
    lines2 = ["same", "same", "different"]
    expected2 = [0]
    assert verify_reflection_lines(find_identical_lines(lines2)) == expected2, "Test case 2 failed"

    # Test case 3: No identical lines
    lines3 = ["line1", "line2", "line3"]
    expected3 = []
    assert verify_reflection_lines(find_identical_lines(lines3)) == expected3, "Test case 3 failed"

    # Test case 4: Mixed lines with valid reflection
    lines4 = ["same", "same1", "same1", "same", "same"]
    expected4 = [1, 3]
    assert verify_reflection_lines(find_identical_lines(lines4)) == expected4, "Test case 4 failed"

    # Test case 5: Running out of lines at the start
    lines5 = ["same", "same", "different1", "different2"]
    expected5 = [0]
    assert verify_reflection_lines(find_identical_lines(lines5)) == expected5, "Test case 5 failed"

    # Test case 6: Running out of lines at the end
    lines6 = ["different1", "different2", "same", "same"]
    expected6 = [2]
    assert verify_reflection_lines(find_identical_lines(lines6)) == expected6, "Test case 6 failed"


def _test_find_identical_lines():
    def assert_identical(actual, expected):
        assert len(actual) == len(expected), f"Expected {len(expected)} results, got {len(actual)}"
        for a, e in zip(actual, expected):
            assert a == e, f"Expected {e}, got {a}"

    # Test case 1: No identical lines
    lines1 = ["line1", "line2", "line3"]
    expected1 = [
        {"id": 0, "forward_identical": [], "backward_identical": [],'possible_mirror_line': False},
        {"id": 1, "forward_identical": [], "backward_identical": [],'possible_mirror_line': False},
        {"id": 2, "forward_identical": [], "backward_identical": [],'possible_mirror_line': False}
    ]
    assert_identical(find_identical_lines(lines1), expected1)

    # Test case 2: All lines identical
    lines2 = ["same", "same", "same"]
    expected2 = [
        {"id": 0, "forward_identical": [1, 2], "backward_identical": [],'possible_mirror_line': True},
        {"id": 1, "forward_identical": [2], "backward_identical": [0],'possible_mirror_line': True},
        {"id": 2, "forward_identical": [], "backward_identical": [0, 1],'possible_mirror_line': False}
    ]
    assert_identical(find_identical_lines(lines2), expected2)

    # Test case 3: Some identical lines
    lines3 = ["line1", "line2", "line1", "line3", "line2"]
    expected3 = [
        {"id": 0, "forward_identical": [2], "backward_identical": [],'possible_mirror_line': False},
        {"id": 1, "forward_identical": [4], "backward_identical": [],'possible_mirror_line': False},
        {"id": 2, "forward_identical": [], "backward_identical": [0],'possible_mirror_line': False},
        {"id": 3, "forward_identical": [], "backward_identical": [],'possible_mirror_line': False},
        {"id": 4, "forward_identical": [], "backward_identical": [1],'possible_mirror_line': False}
    ]
    assert_identical(find_identical_lines(lines3), expected3)

    # Test case 4: Empty input
    lines4 = []
    expected4 = []
    assert_identical(find_identical_lines(lines4), expected4)

    # Test case 5: Single line input
    lines5 = ["only line"]
    expected5 = [
        {"id": 0, "forward_identical": [], "backward_identical": [] ,'possible_mirror_line': False}
    ]
    assert_identical(find_identical_lines(lines5), expected5)


def verify_specific_reflection_line(lines_info, mirror_line_index):
    # Verify the reflection starting from the mirror line
    for offset in range(1, mirror_line_index + 1):
        # Check if the indices are within bounds
        if mirror_line_index - offset < 0 or mirror_line_index + offset + 1 >= len(lines_info):
            break

        # Get the ids of the lines before and after the mirror line
        line_before_id = lines_info[mirror_line_index - offset]['id']
        line_after_id = lines_info[mirror_line_index + offset + 1]['id']

        # Check if the line before is identical to the line after
        if line_before_id not in lines_info[line_after_id]['backward_identical']:
            return False

    return True


def verify_reflection_lines(lines_info):
    valid_mirror_lines = []

    for line_info in lines_info:
        if line_info['possible_mirror_line']:
            # Verify the specific reflection line
            if verify_specific_reflection_line(lines_info, line_info['id']):
                valid_mirror_lines.append(line_info['id'])

    return valid_mirror_lines

def _test_part_a(input_str:str):

    Sample = """\
    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.

    #...##..#
    #....#..#
    ..##..###
    #####.##.
    #####.##.
    ..##..###
    #....#..#   
    """

    parsed_input = parse_input(input_str)
    # parsed_input = parse_input(Sample)

    sum = 0
    for chunk_str in parsed_input:
        chunk = find_identical_lines(chunk_str)
        verified_reflection_lines_h = verify_reflection_lines(chunk)
        sum += 0 if len(verified_reflection_lines_h) == 0 else (verified_reflection_lines_h[0] + 1)*100
        chunk_str = transpose(chunk_str)
        chunk = find_identical_lines(chunk_str)
        verified_reflection_lines_v = verify_reflection_lines(chunk)
        sum += 0 if len(verified_reflection_lines_v) == 0 else (verified_reflection_lines_v[0] + 1)
        print(verified_reflection_lines_h , verified_reflection_lines_v)
    print(sum)

def transpose(lines: list[str]) -> list[str]:
    if len(lines) == 0:
        return []
    return  [''.join([line[i].strip() for line in lines]) for i in range(len(lines[0]))]



if __name__ == "__main__":
    _tests()

    with open("r13_input.txt", "r") as f:
        input_str = f.read()
        _test_part_a(input_str)

    # _test_part_a()
    # _test_part_b()
