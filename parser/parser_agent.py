import json
from enum import Enum
from openai import OpenAI
from openai.types.chat import ChatCompletion


class InputType(Enum):
    FEEDBACK = 1
    MOVE_TO_CODE = 2
    EXIT = 3

def receive_multiline_input(prompt):
    print(prompt)

    input_lines = []
    input_type = InputType.FEEDBACK  # Default input type

    while True:
        line = input()
        input_lines.append(line)

        # Check for special commands
        if line == "-code":
            input_type = InputType.MOVE_TO_CODE
            input_lines.pop()  # Remove the command line
            break
        elif line == "-end":
            input_type = InputType.EXIT
            input_lines.pop()  # Remove the command line
            break

        # Check for two consecutive empty lines
        if len(input_lines) >= 2 and input_lines[-1] == '' and input_lines[-2] == '':
            input_lines = input_lines[:-2]  # Remove the last two empty lines
            break

    print("input received. processing...")
    return (input_type, "\n".join(input_lines))


def openai_call(prompt):


    client = OpenAI()
    messages = [{"role": "user", "content": prompt}]

    # print("\033[91m{}\033[00m".format(prompt))

    response: ChatCompletion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages
    )

    res_str = response.choices[0].message.content
    is_valid_json = False
    try:
        res_json = json.loads(res_str)
        is_valid_json = True
    except:
        print("failed to parse the result as json")
        pass
    return {"str": res_str, "is_valid_json": is_valid_json}

def analyze_initial_input(input_data):

    prompt = f"""
    I'd like you to parse the following input text into a valid JSON.
    We will do it in a few steps process.

    First, I'll supply the input and I'd like you to read it and attempt to analyze yourself the intended JSONs.
    I'll later supply you with modification requests.

    I'll provide a few lines but please return just the first two ones.
    please return them as a valid JSON list with two dicts one per line.
    No explanation, no comments, just the JSONs.    

    the Input:
    {input_data}
    """

    ret = openai_call(prompt)
    return ret

def analyze_feedbacks(*,original_input_data,last_parsing_result,feedback_data):
    prompt = f"""\
    Previously I asked you to parse the following input:
    {original_input_data}
    
you've replied me with the following JSONs:
{last_parsing_result}

for the first two lines.

This is my feedback:
{feedback_data}

please take in my feedback and return again the first two lines as a valid JSON list with two dicts one per line.
No explanation, no comments, just the JSONs.
"""

    ret = openai_call(prompt)
    return ret


def initial_ask_for_code(*,original_input_data, last_parsing_result):

    prompt = f"""
    I'd like you to write a python script that parses the following input text into a valid JSON.
    this is the input:
    {original_input_data} 
    
    we agreed in the last session on this format ( it's a parsing of the first two lines ):
    {last_parsing_result} 
    
    please write the code that parses the input into the JSONs.
    the signature is as follows:
    def parse_line_into_json(input_line:str) -> dict    
    """

    ret = openai_call(prompt)
    return ret

def main():
    initial_text = \
"""\nI'm your friendly parser agent.
Let's start by just entering an input text sample.
I expect up to 10 lines of input.
I'll start by trying to deduce what needed on my own and answer with the first two lines parsed into JSONs
take me with feedbacks from there.
Enter your input here (Enter two consecutive empty lines to finish input, ^c to quit):)
"""

    (input_type, input_str) = receive_multiline_input(prompt=initial_text)
    if input_type != InputType.FEEDBACK:
        print("No input received. exiting.")
        return
    data_lines = [line for line in input_str.splitlines() if line.strip() != '']
    result = analyze_initial_input(input_str)

    while True:
        if result['is_valid_json']:
            json_obj = json.loads(result['str'])
            print( f"Parsing attempt:\n{data_lines[0]}\n{json_obj[0]}\n\n{data_lines[1]}\n{json_obj[1]}\n")
        else:
            print( f"Parsing attempt:\n{data_lines[0]}\n{data_lines[1]}\n{result}\n")

        print("Now, please provide me with feedbacks on the first two lines.")
        (input_type, feedback_data) = receive_multiline_input(prompt="Enter your feedbacks here (Enter two consecutive empty lines to finish input, -code to accept the json format and move to code, -end to exit):)")
        if input_type == InputType.EXIT:
            print("Exiting.")
            return
        elif input_type == InputType.MOVE_TO_CODE:
            break
        result = analyze_feedbacks(feedback_data=feedback_data, original_input_data=input_str, last_parsing_result=result['str'])

    result = initial_ask_for_code(original_input_data=input_str, last_parsing_result=result['str'])
    print (result['str'])





if __name__ == "__main__":
    main()
