import re
import json

def parse_line_into_json(input_line:str, line_number:int) -> dict:
	output_dict = {"line": line_number, "numbers": [], "symbols": []}
	scanner = re.Scanner([
		(r"\d+", lambda scanner, token: output_dict["numbers"].append(
			{"token": token ,"start": scanner.match.start(), "end": scanner.match.end()})),
		(r"[*+#$]", lambda scanner, token: output_dict["symbols"].append(
			{"token": token, "position": scanner.match.start()})),
		(r".", lambda scanner, token: None),
	])

	scanner.scan(input_line)
	return output_dict

def parse_text_into_json(input_text: str):
	parsed_lines = [parse_line_into_json(line, i+1) for i, line in enumerate(input_text.split("\n"))]
	return parsed_lines

# Testing
result = parse_text_into_json("""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""")
json_output = json.dumps(result, indent=2)
print(json_output)