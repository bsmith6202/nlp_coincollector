import requests
import time
import pandas as pd
import os
from openai import OpenAI


client = OpenAI(
    organization='org-ZWMRC3KJT3026wx9IKBrgqU7',
    project='proj_IzxXsMn4fy7agRMpFqCPXOqX',
)

def main():
    
    question = "Who is the current U.S. president? Answer in the format of a json {president:your answer}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
        response_format={"type": "json_object"}
    )
    
    currResponse = response.choices[0].message.content
    print("llm initial pdf", currResponse)
    
if __name__ == "__main__":
    main()