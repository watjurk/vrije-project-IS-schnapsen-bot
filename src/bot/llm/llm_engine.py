import json
from typing import Optional
import requests
from os import path

MODEL_TYPE = "openhermes"  # Update this for your model

CURRENT_FOLDER = path.dirname(path.abspath(__file__))
MODEL_TYPE = "openhermes"  # Update this for your model

# read the master prompt from a file
PLAYING_PROMPT = open(path.join(CURRENT_FOLDER, "playing_prompt.txt")).read()

# read the expert prompt from a file
EXPERT_PROMPT = open(path.join(CURRENT_FOLDER, "expert_prompt.txt")).read()

def expert(history):
    full_expert_prompt = EXPERT_PROMPT + history
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_TYPE,
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



def generate(game_representation: str, feedback: Optional[str] = None) -> str:
    full_prompt = f"{PLAYING_PROMPT}\n\n{game_representation}"
    if feedback is not None:
        full_prompt += f"\n\n{feedback}"

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_TYPE,
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
