import json
from os import path
from typing import Optional

import requests
#from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex

MODEL_TYPE = "mixtral"


CURRENT_FOLDER = path.dirname(path.abspath(__file__))
PLAYING_PROMPT = open(path.join(CURRENT_FOLDER, "playing_prompt_v3.txt")).read()
EXPERT_PROMPT = open(path.join(CURRENT_FOLDER, "expert_prompt_v3.txt")).read()

#rag_documents = SimpleDirectoryReader(path.join(CURRENT_FOLDER, "rag_data")).load_data()

#service_context = ServiceContext.from_defaults(llm=None, embed_model="local")
#rag_index = VectorStoreIndex.from_documents(rag_documents, service_context=service_context)
#rag_retriever_engine = rag_index.as_retriever()


def llm_expert(game_history: str, game_representation_without_history: str):
    full_expert_prompt = f"{EXPERT_PROMPT}\n\nHISTORY:\n{game_history}\n\nSTATE:\n{game_representation_without_history}"
    return api_generate(full_expert_prompt)


def llm_player(
    game_representation_without_history: str,
    game_history: str,
    feedback: Optional[str] = None,
) -> str:
    history = game_history
    expert_advice = llm_expert(history, game_representation_without_history)

    #rag_response = ""
    #rag_responses = rag_retriever_engine.retrieve(expert_advice)
    #for response in rag_responses:
        #rag_response += f"{response.get_text()}\n"
    # Remove tailing enter
    #rag_response = rag_response[:-1]

    full_prompt = f"{PLAYING_PROMPT}"
    full_prompt += f"\n\nSTATE:\n{game_representation_without_history}"
    full_prompt += f"\n\nEXPERT ADVICE:\n{expert_advice}"
    #full_prompt += f"\n\nBOOK ADVICE:\n{rag_response}"
    if feedback is not None:
        full_prompt += f"\n\nFEEDBACK:\n{feedback}"
    
    #print(full_prompt)

    return api_generate(full_prompt)


def api_generate(prompt: str) -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
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
