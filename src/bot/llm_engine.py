import json
import requests
import sys

model = 'openhermes'  # Update this for your model

# Read the master prompt from a file
prompt_path = "/Users/julespadova/Documents/Intelligent System Project/lmm shcnapsen/bot with plain text/prompt.txt"
with open(prompt_path, 'r') as file:
    master_prompt = file.read()


#read the expert prompt from a file 
expert_prompt_path = "/Users/julespadova/Documents/Intelligent System Project/lmm shcnapsen/bot with plain text/expert_prompt.txt"
with open(expert_prompt_path, 'r') as file:
    expert_prompt = file.read()



def expert(history):
    full_expert_prompt = expert_prompt + history
    r = requests.post('http://localhost:11434/api/generate',
                    json={
                        'model': model,
                        'prompt': full_expert_prompt,
                        'context': [],
                    },
                    stream=True)
    r.raise_for_status()

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        output += response_part

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return output

def generate(user_input):
    full_prompt = master_prompt + "\n\n" + user_input
    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          'model': model,
                          'prompt': full_prompt,
                          'context': [],
                      },
                      stream=True)
    r.raise_for_status()

    output = ""
    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        output += response_part

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return output

def main():
    game_state = ""
    for line in sys.stdin:
        if line.strip() == "END_OF_GAME_STATE":  # Assuming this is the delimiter
            if game_state:
                move = generate(game_state)
                print(move)  # Write bot's move to stdout
                sys.stdout.flush()  # Ensure the move is sent to the engine immediately
                game_state = ""  # Reset game state
        else:
            game_state += line

if __name__ == "__main__":
    main()
 