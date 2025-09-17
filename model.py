import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"
}

data = {
    "model": "meta-llama/llama-4-scout-17b-16e-instruct",
    "messages": [
        {"role": "user", "content": "Explain the importance of fast language models"}
    ]
}

response = requests.post(url, headers=headers, json=data)

result = response.json()
print(json.dumps(result, indent=2))
