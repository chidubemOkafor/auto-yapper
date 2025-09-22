import json
from dotenv import load_dotenv
import os
from main import client
from openai import OpenAI
import datetime

load_dotenv()

url = os.getenv('GROQ_URL')
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"
}

cl = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv('HF_TOKEN'),
)

with open("aboutProject.txt", "r") as file:
    project_description = file.read().replace("\n", " ")

with open("context.txt", "r") as file:
    context = file.read()

data = {
    "messages": [
        {
            "role": "system",
            "content": f"{context} {project_description} and remember that Geverlyn is only in the morning 'current time {datetime.time}'"
        },
        {
            "role": "user",
            "content": f"yap about {os.getenv('ACCOUNT_USERNAME')}"
        }
    ]
}

completion = cl.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct:nebius",
    messages=data["messages"]
)
