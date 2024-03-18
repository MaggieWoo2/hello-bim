import os

import streamlit as st

from llm import *

def main():
    # App title
    st.set_page_config(page_title="Chat with Bim 笔木:)")

    # Sidebar for model parameters and clear chat history
    with st.sidebar:
        st.title('🐤Chat with Bim 笔木:)')
        st.write('This chatbot is powered by versatile LLM backend.')

        st.subheader('Choose an agent:')
        persona = st.radio("Select one:", ["🐹Donald Trump", "🏴‍☠️Jack Sparrow", "🕵️‍♂️John Smith", "中文"])
        
        st.subheader('Response type:')
        response_tone = st.selectbox("Choose the response type:", ["neutral", "aggressive", "soft"])
        
        st.subheader('Adjust creativity:')
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.01)


        # st.subheader('Clear Chat History')
        def clear_chat_history():
            st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        st.button('Clear Chat History', on_click=clear_chat_history)

    # Initialize session_state to keep track of messages
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    if "memory" not in st.session_state.keys():
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")
        
    prompt = st.chat_input("Your message:")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_response_with_history(prompt, llm="llama2", persona=persona, tone=response_tone, temperature=temperature, memory=st.session_state.memory)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
   

if __name__ == "__main__":
    main()