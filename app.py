import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# Streamlit interface

def main():
  
  st.title('Chat with Bim 笔木:)')
  client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

  # Text input for user message
  user_message = st.text_input("You:")

  if user_message:
      # Sending the user's message to GPT-3.5 and getting a response
      response = client.chat.completions.create(
          model="gpt-3.5-turbo",  # Use the appropriate engine for GPT-3.5
          messages=[
          {
              "role": "system", 
              "content": """
                      You are a helpful and resourceful assistant, your name is Bim. 
                      You will help users answer questions responsibly and reliably. 
                      Please give the best answer you can."""},
          {   
              "role": "user", 
              "content": user_message}
        ]
      )

      # Displaying the GPT-3.5 response
      st.text_area("GPT-3.5:", value=response.choices[0].message.content, height=150, max_chars=None, key=None)
      
if __name__ == "__main__":
  main()

