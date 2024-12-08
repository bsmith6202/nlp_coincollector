import asyncio

import torch
from kani import Kani
from kani.engines.huggingface.llama2 import LlamaEngine

# load mixtral in fp16
common_hf_model_args = dict(
    device_map="auto",
    torch_dtype=torch.float16,
)

engine = LlamaEngine(
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    max_context_size=32768,
    model_load_kwargs=common_hf_model_args,
    do_sample=False,
)


# query mixtral
async def query_one(query):
    # fewshot = [
    #     ChatMessage.user("thank you"),
    #     ChatMessage.assistant("arigato"),
    #     ChatMessage.user("good morning"),
    #     ChatMessage.assistant("ohayo"),
    # ]
    # ai = Kani(engine, chat_history=fewshot)
    ai = Kani(engine)
    resp = await ai.chat_round_str(query)
    print(resp)
    return resp


async def main():
    # load queries here
    queries = ["How many connections does each stop on the Yamanote Line have?"]
    for query in queries:
        resp = await query_one(query)
        # save response here


if __name__ == "__main__":
    asyncio.run(main())