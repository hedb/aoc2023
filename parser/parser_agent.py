import json

from openai import OpenAI
from openai.types.chat import ChatCompletion


def receive_multiline_input(prompt):
    print(prompt)

    # Reading multiple lines of input
    input_lines = []
    while True:
        line = input()
        input_lines.append(line)
        if len(input_lines) >= 2 and input_lines[-1] == '' and input_lines[-2] == '':
            # Remove the last two empty lines
            input_lines = input_lines[:-2]
            break

    print("input received. processing...")
    return "\n".join(input_lines)


def openai_call(prompt):


    client = OpenAI()
    messages = [{"role": "user", "content": prompt}]

    print("\033[91m{}\033[00m".format(prompt))

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


def main():
    initial_text = \
"""\nI'm your friendly parser agent.
Let's start by just entering an input text sample.
I expect up to 10 lines of input.
I'll start by trying to deduce what needed on my own and answer with the first two lines parsed into JSONs
take me with feedbacks from there.
Enter your input here (Enter two consecutive empty lines to finish input, ^c to quit):)
"""

    input_data = receive_multiline_input(prompt=initial_text)
    data_lines = [line for line in input_data.splitlines() if line.strip() != '']
    result = analyze_initial_input(input_data)

    while True:
        if result['is_valid_json']:
            json_obj = json.loads(result['str'])
            print( f"Parsing attempt:\n{data_lines[0]}\n{json_obj[0]}\n\n{data_lines[1]}\n{json_obj[1]}\n")
        else:
            print( f"Parsing attempt:\n{data_lines[0]}\n{data_lines[1]}\n{result}\n")

        print("Now, please provide me with feedbacks on the first two lines.")
        feedback_data = receive_multiline_input(prompt="Enter your feedbacks here (Enter two consecutive empty lines to finish input, ^c to quit):)")

        result = analyze_feedbacks(feedback_data=feedback_data, original_input_data=input_data, last_parsing_result=result['str'])





if __name__ == "__main__":
    main()
