import json
from typing import Optional
import requests
from os import path

MODEL_TYPE = "openhermes"  

CURRENT_FOLDER = path.dirname(path.abspath(__file__))

# read the master prompt from a file
PLAYING_PROMPT = open(path.join(CURRENT_FOLDER, "playing_prompt_v3.txt")).read()

# read the expert prompt from a file
EXPERT_PROMPT = open(path.join(CURRENT_FOLDER, "expert_prompt_v3.txt")).read()

def expert(history, game_representation_without_history):
    full_expert_prompt = EXPERT_PROMPT + "HISTORY:" + history + "GAME STATE:" + game_representation_without_history
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
    output = ""
    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get("response", "")
        output += response_part

        if "error" in body:
            raise Exception(body["error"])

        if body.get("done", False):
            return output



def generate(game_representation, game_representation_without_history, game_history: str, feedback: Optional[str] = None) -> str:

    # LLM expert 
    history = game_history

    expert_advice = expert(history, game_representation_without_history)

    print(expert_advice)
    # LLM player
    full_prompt = f"{PLAYING_PROMPT}\n\n{game_representation_without_history}\n\nExpert Advice:\n{expert_advice}"
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
