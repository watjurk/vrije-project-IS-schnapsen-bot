import json
from os import path
from typing import Optional

import requests

MODEL_TYPE = "openhermes"


CURRENT_FOLDER = path.dirname(path.abspath(__file__))
PLAYING_PROMPT_EXPERT = open(path.join(CURRENT_FOLDER, "playing_prompt_expert.txt")).read()
PLAYING_PROMPT_NO_EXPERT = open(path.join(CURRENT_FOLDER, "playing_prompt_no_expert.txt")).read()

EXPERT_PROMPT = open(path.join(CURRENT_FOLDER, "expert_prompt.txt")).read()


def llm_expert(ollama_port, game_history: str, game_representation_without_history: str):
    full_expert_prompt = f"{EXPERT_PROMPT}\n\nHISTORY:\n{game_history}\n\nSTATE:\n{game_representation_without_history}"
    return api_generate(ollama_port, full_expert_prompt)


def llm_player(
    ollama_port,
    game_representation: str,
    expert_advice: str,
    use_expert: bool = False,
    feedback: Optional[str] = None,
) -> str:
    if use_expert:
        full_prompt = f"{PLAYING_PROMPT_EXPERT}"
    else:
        full_prompt = f"{PLAYING_PROMPT_NO_EXPERT}"

    full_prompt += f"\n\nSTATE:\n{game_representation}"

    if use_expert:
        full_prompt += f"\n\nEXPERT ADVICE:\n{expert_advice}"

    if feedback is not None:
        full_prompt += f"\n\nFEEDBACK:\n{feedback}"

    return api_generate(ollama_port, full_prompt)


def api_generate(ollama_port, prompt: str) -> str:
    r = requests.post(
        f"http://localhost:{ollama_port}/api/generate",
        json={
            "model": MODEL_TYPE,
            "prompt": prompt,
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
