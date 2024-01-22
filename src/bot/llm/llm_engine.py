import json
import requests
from os import path

model = "openhermes"  # Update this for your model
CURRENT_FOLDER = path.dirname(path.abspath(__file__))

# Read the master prompt from a file
prompt_path = path.join(CURRENT_FOLDER, "prompt.txt")
with open(prompt_path, "r") as file:
    master_prompt = file.read()


# read the expert prompt from a file
expert_prompt_path = "/Users/julespadova/Documents/Intelligent System Project/lmm shcnapsen/bot with plain text/expert_prompt.txt"
with open(expert_prompt_path, "r") as file:
    expert_prompt = file.read()


def expert(history):
    full_expert_prompt = expert_prompt + history
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": full_expert_prompt,
            "context": [],
        },
        stream=True,
    )
    r.raise_for_status()

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get("response", "")
        output += response_part

        if "error" in body:
            raise Exception(body["error"])

        if body.get("done", False):
            return output


def generate(game_state: str) -> str:
    full_prompt = master_prompt + "\n\n" + game_state
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": full_prompt,
            "context": [],
        },
        stream=True,
    )
    r.raise_for_status()

    output = ""
    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get("response", "")
        output += response_part

        if "error" in body:
            raise Exception(body["error"])

        if body.get("done", False):
            return output
