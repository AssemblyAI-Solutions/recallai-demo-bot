import requests
import os
from dotenv import load_dotenv

load_dotenv()

def answer_question(query):
    url = f"https://api.retool.com/v1/workflows/{os.getenv('RETOOL_WORKFLOW_ID')}/startTrigger"
    headers = {
        'Content-Type': 'application/json',
        'X-Workflow-Api-Key': os.getenv('RETOOL_WORKFLOW_TOKEN')
    }
    data = {
        "query": query
    }

    response = requests.post(url, json=data, headers=headers)
    return response.text

if __name__ == "__main__":
    print(answer_question("what languages does assemlyai support for nano?"))