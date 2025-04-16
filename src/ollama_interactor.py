import json
from src.printer import *
from urllib import request


def generate_commit_message_body(diff: str):
    try:
        ollama_url = 'http://localhost:11434/api/chat'
        myobj = {
            'model': 'mistral',
            "messages": [
                {
                    "content": "Write a professional git commit message based on the a diff."
                               "Do not preface the commit with anything, use the present tense, return the full sentence, "
                               "separate different topic to new lines "
                               f"and use the conventional commits specification:\n {diff}",
                    "role": "user"
                },
            ],
            "stream": False,
        }
        json_data = json.dumps(myobj)
        json_data = json_data.encode()
        req = request.Request(ollama_url, data=json_data, method='POST')  # this will make the method "POST"
        req.add_header('Content-Type', 'application/json')
        with request.urlopen(req) as df:
            content = df.read()
        response_data = json.loads(content)['message']['content']
        return str(response_data).strip()
    except Exception as e:
        warn(e)
        warn("Generating commit message body failed, either ollama not running or something went wrong")
        return ""
