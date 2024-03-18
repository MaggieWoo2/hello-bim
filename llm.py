import os
import requests
import json

from dotenv import load_dotenv
from openai import OpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
# from langchain_openai.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
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
    """Basic QA with LLMs"""
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



def get_response_with_history(user_message, llm, persona, tone, temperature, memory):
    """QA with local LLMs, adding conversation histiry"""
      
    template = """You are a chatbot having a conversation with a human.

        {chat_history}
        Human: {human_input}
        Chatbot:"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], template=template
    )

    llm = OpenAI()
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory,
    )
    return llm_chain.predict(human_input=user_message)