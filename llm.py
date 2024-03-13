import os
import requests
import json

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()


# system_message = """
# You are a helpful and resourceful assistant, your name is Bim. 
# You will help users answer questions responsibly and reliably. 
# Please give the best answer you can.
# """

def get_system_message(persona, tone):
    system_message = f"""
    You are {persona}, please use an {tone} tone to answer users questions."""
    return system_message

def get_response(user_message, llm, persona, tone, temperature):
    
    if llm == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the appropriate engine for GPT-3.5
            messages=[
                {
                    "role": "system",
                    "content": get_system_message(persona, tone)},
                {
                    "role": "user",
                    "content": user_message}
            ]
        )

        # Return the model response
        return response.choices[0].message.content

    else:
        url = "http://localhost:11434/api/generate"
        headers = {
                    'Content-Type': 'application/json',
                    }
        full_prompt = user_message
        data = {
                "model": llm,
                "stream": False,
                "prompt": full_prompt,
                "system": get_system_message(persona, tone),
                "temperature": temperature
                    }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
        else:
            actual_response = "Sorry, try another time~"
            
        return actual_response