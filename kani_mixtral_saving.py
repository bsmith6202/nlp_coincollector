import asyncio
import torch
from kani import Kani
from kani.engines.huggingface.llama2 import LlamaEngine

# Load Mixtral in fp16
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

# Query Mixtral
async def query_one(query):
    ai = Kani(engine)
    resp = await ai.chat_round_str(query)
    return resp

async def main():
    # Load queries here
    queries = ["How many connections does each stop on the Yamanote Line have?"]
    
    # Open file to save responses
    with open('responses.txt', 'w') as f:
        for query in queries:
            resp = await query_one(query)
            # Write query and response to file
            f.write(f"Query: {query}\n")
            f.write(f"Response: {resp}\n\n")
            
    print("RUNNING")

if __name__ == "__main__":
    asyncio.run(main())
