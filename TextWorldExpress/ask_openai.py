import sys
from openai import OpenAI
import json
import openai

# description: list of functions queried by textworldexpress runner using GPT4

history_file = 'observations_moves.json'

# def query():
#     # Check if a question was provided as a command-line argument
#     if len(sys.argv) < 2:
#         print("Usage: python ask_openai.py 'Your question here'")
#         return

#     # Get the question from the command-line arguments
#     question = sys.argv[1]

#     # Initialize the OpenAI client
#     client = OpenAI(
#     organization='org-ZWMRC3KJT3026wx9IKBrgqU7',
#     project='$PROJECT_ID',
#     )

#     # Send the question to the OpenAI API
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {"role": "user", "content": question}
#         ]
#     )
# #     response = client.chat.completions.create(
# #     model="gpt-3.5-turbo",
# #     messages=[
# #         {"role": "user", "content": question}
# #     ]
# # )

#     # Print the API's response
#     print("\nResponse:", response.choices[0].message.content)
#     #print("\nResponse:", response.choices[0].message["content"])
    
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
    
def queryLLM(obs, infos, history):
    history_text = "\n".join(history) if history else "No previous history. This is the first move"
    
    question = (
        "You are playing the coin collector game. Your goal is to find a coin in one of the rooms. Try to explore new rooms. So far: "
        + history_text
        + "Here is the current environment information: "
        + infos['observation']
        + " Please pick one of these valid options: "
        + ', '.join(infos['validActions'])
        + ". You must respond with only the words from the actions, "
        + "such as 'move east' or 'open door to north'. "
        + "Please do not add words such as 'I choose to' or 'blank' and avoid punctuation. If there is the open take coin, always do that. Do not go to rooms already seen. "
    )
    
    with open("question.txt", "a") as file:
        file.write(f"question: {question}\n")
    
    client = OpenAI(
        organization='org-ZWMRC3KJT3026wx9IKBrgqU7',
        project='proj_IzxXsMn4fy7agRMpFqCPXOqX',
    )

    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    
    currResponse = response.choices[0].message.content
    print("\nLLM RESPONSE ANSWER:", currResponse)
    return currResponse

        #openai.organization = "org-ZWMRC3KJT3026wx9IKBrgqU7"
    
    

    #UNCOMMENT VERSION OF GPT TO USE
    
    # # Send the question to the OpenAI API
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "user", "content": question}
    #     ]
    # )
    # currResponse = response.choices[0].message.content
    # print("\nLLM RESPONSE ANSWER:", currResponse)
    # return currResponse

    # response = client.completions.create(
    #     model="text-davinci-003",
    #     prompt=question
    # )

    # currResponse = response.choices[0].text
    # print("\nLLM RESPONSE ANSWER:", currResponse)
    # return currResponse
    
    
def coinMove(obs, infos):
    # print("Current observation:", infos['observation'])
    # print("Current valid actions:", infos['validActions'])

    # Get LLM's response (next move)
    history = load_history()
    move = queryLLM(obs, infos, history)

    # Save the observation and move to the history file
    save_history(infos['observation'], move)

    return move

if __name__ == "__main__":
    print('in main')
    query()
