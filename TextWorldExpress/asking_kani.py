import asyncio
import torch
from kani import Kani
from kani.engines.huggingface.llama2 import LlamaEngine
import json

history_file = 'observations_moves_kani.json'

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
    pad_token_id=2,
)

# Query Mixtral with conversation history
def query_conversation(conversation_history, user_input):
    ai = Kani(engine)
    # Combine history with the current user input
    conversation_history.append(f"User: {user_input}")
    # Join the conversation history into a single string
    full_conversation = "\n".join(conversation_history)
    # Get AI's response
    resp = ai.chat_round_str(full_conversation)
    conversation_history.append(f"AI: {resp}")
    return resp, conversation_history

def main():
    # Initialize conversation history
    conversation_history = []
    # User queries (simulating a 10-step conversation: 5 user inputs, 5 AI responses)
    user_queries = [
        "Hello! How are you today?",
        "Can you tell me something interesting about space?",
        "What do you know about black holes?",
        "How do black holes affect time?",
        "What's your favorite topic to discuss?"
    ]
    
    # Open file to save responses
    with open('responses.txt', 'w') as f:
        for i, user_input in enumerate(user_queries):
            resp, conversation_history = query_conversation(conversation_history, user_input)
            # Write conversation step to file
            f.write(f"Step {i+1} - User: {user_input}\n")
            f.write(f"Step {i+1} - AI: {resp}\n\n")
    
    print("Conversation complete.")

if __name__ == "__main__":
    asyncio.run(main())
    
def createJSON():
    empty_history = []
    with open(history_file, 'w') as f:
        json.dump(empty_history, f)
    print("History has been reset.")
    
def save_history(observation, move):
    # Load existing history
    history = load_history()

    # Determine the current step number
    step_number = len(history) + 1

    # Append the new observation and move with a step number
    history.append(f"Step #{step_number} observation: {observation} and move: {move}")

    # Save the updated history back to the file
    with open(history_file, 'w') as f:
        json.dump(history, f)
        
def load_history():
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
            return history
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

# query mixtral
async def get_move(obs, infos):
    
    history = load_history()
    # move = queryLLM(obs, infos, history)

    # Save the observation and move to the history file
    

    # return move
    history_text = "\n".join(history) if history else "No previous history. This is the first move"
    
    question = (
        "You are playing the coin collector game. Your goal is to find a coin in one of the rooms by traversing." 
        + "Here is the current environment information: "
        + infos['observation']
        + " Please pick one of these valid options: "
        + ', '.join(infos['validActions'])
        + ". You must respond with only the words from the actions, "
        + "such as 'move east' or 'open door to north'. Only respond with the current move you want to take, and no other words. It should be few words all lowercase for example take coin or look around."
        + "Please do not add words such as 'I choose to' or 'blank' and avoid punctuation. If there is the option to take coin, always do that. Do not go to rooms already seen. You may not take the coin if it is not explicitly in the observation that there is a coin in the room, or you will fail."
    )
    ai = Kani(engine)
    # inputs = ai.tokenizer(question, return_tensors="pt", padding=True, truncation=True)
    # attention_mask = inputs['attention_mask']
    
    resp = await ai.chat_round_str(question)
    print(resp)
    save_history(infos['observation'], resp)
    return resp


def main():
    # load queries here
    queries = ["How many connections does each stop on the Yamanote Line have?"]
    for query in queries:
        resp = query_one(query)
        # save response here