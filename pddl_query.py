import requests
import time
import pandas as pd
import os
from openai import OpenAI
import json

client = OpenAI(
    organization='org-ZWMRC3KJT3026wx9IKBrgqU7',
    project='proj_IzxXsMn4fy7agRMpFqCPXOqX',
)


def run_solver():
    print("in solver")
    domain_file = open('coin_df.pddl').read()
    problem_file = open('coin_pf.pddl').read()
    plan_found = None
    # print("df is", domain_file)
    # print("pf is", problem_file)
    req_body = {"domain" : domain_file, "problem" : problem_file}
    # print("2")
    # Send job request to solve endpoint
    solve_request_url=requests.post(f"https://solver.planning.domains:5001/package/lama-first/solve", json=req_body).json()
    # print("3")
    # Query the result in the job
    celery_result=requests.post('https://solver.planning.domains:5001' + solve_request_url['result'])
    # print("here")
    while celery_result.json().get("status","")== 'PENDING':
        # Query the result every 0.5 seconds while the job is executing
        celery_result=requests.post('https://solver.planning.domains:5001' + solve_request_url['result'])
        # print("celery result", celery_result)
        time.sleep(0.5)
    if celery_result.json()['result']:
        return celery_result.json()['result']
    # print("out of while loop")
    else:
        print("no result")
        return ""
    
def parse_result(result):
    # print("result is", result)
    if (result['output']):
        steps = result['output']['sas_plan']
        steps_array = [step.strip() for step in steps.strip().split('\n')]
    else:
        print("invalid output: ", result)
        print("found invalid")
        return "invalid"
    # print(steps_array)
    return steps_array

#def query_forjson(query):
    

def initialize_pf(obs, infos):
    print("initializing pf")
    problem_file_ex = open('coin_pf_example.pddl').read()
    domain_file = open('coin_df.pddl').read()
    
    # print("current obs", obs)
    
    question = (
        "Here is an example of a problem file in PDDL for the coin collector game:\n"
        + problem_file_ex + "\n"
        + "I want you to recreate one for your current observations.\n"
        + "You are to only use predicates defined in this domain file:\n"
        + domain_file + "\n"
        + "Ignore any objects in the pf, just focus on current locations, surrounding locations, and doors.\n"
        + "Here are your observations:\n"
        + obs + "\n"
        + "The goal should always be to visit a not-yet-visited room.\n"
        + "Return the response in this JSON format: {\"pf\": \"(insert pf solution)\"}\n"
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": question}
        ],
        response_format={"type": "json_object"}
    )
    
    currResponse = response.choices[0].message.content
    response_dict = json.loads(currResponse)
    pf_answer = response_dict["pf"]
    with open("coin_pf.pddl", "w") as file:
        file.write(pf_answer)
    print("\nLLM INIITAL PF:", pf_answer)
        
    # print("initial pf is ", currResponse)

def update_pf(obs, infos, move):
    print("updating pf")
    problem_file = open('coin_pf.pddl').read()
    domain_file = open('coin_df.pddl').read()
    
    print("obs to update pf with", obs)
    # print("infos to update pf with", infos)
    
    coin_str = 'coin'
    
    if coin_str in obs:
        print("coin here!")
        print("here is observations", obs)
    
    question = (
        "Here is the old problem file for the coin collector game: "
        + problem_file 
        + " and here are the current problem observations "
        + obs 
        + " and this is the move you just took to get to these observations (to help you get from the old problem file to the current problem file). "
        + move
        + "Please return an updated version of the problem file based on the move and your now current observations."
        + "It must reflect only the parameters listed in this domain file"
        + domain_file
        + "The goal should always be the exact same as the problem file you were given, which is to visit not yet visited rooms."
        + "Answer in the form of a json {pf: your ansewr}"
    )
    
    # need to use chat gpt again to update pf
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": question}
        ],
        response_format={"type": "json_object"}
    )
    
    currResponse = response.choices[0].message.content
    response_dict = json.loads(currResponse)
    pf_answer = response_dict["pf"]
    with open("coin_pf.pddl", "w") as file:
        file.write(pf_answer)
    print("\nLLM RESPONSE PF:", pf_answer)
    # return currResponse

def get_move_from_chat(step, validActions):
    question = (
        "From this description of a step in a coin collector game"
        + step 
        + " please return the move of the string that matches the format an action here"
        + (', '.join(validActions))
        + " return it all lowercase, no puncutation, no extra words like for instance do not say the move is look around, instead just say look around"
        + " no quotation marks, parentheses, or extra words"
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    
    currResponse = response.choices[0].message.content
    return currResponse
    
    # returns an array of the move strings 
def get_next_moves(obs, infos):
    validActions = ['move east', 'move south', 'move north', 'move west', 
                        'open door to east', 'open door to west','open door to north','open door to south',
                        'inventory', 'look around', 'close door to east', 'close door to north', 'close door to south', 'close door to west',
                        'take coin']
    result = run_solver()

    step_arr = parse_result(result)[:-1]
    if (step_arr == "invali"):
        return "invalid"
    print("result array from solver", step_arr)
    plan = []
    for step in step_arr:
        print("curr step", step)
        single_move = get_move_from_chat(step, validActions)
        print("step from chat", single_move)
        plan.append(single_move)
    print("result plan", plan)
    return plan

    
def main():
    get_next_moves([])
    
if __name__ == "__main__":
    main()