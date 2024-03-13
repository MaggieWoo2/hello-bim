import os

import streamlit as st

from llm import get_response

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

    # Initialize chat messages if not already present
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        
    # User input
    prompt = st.chat_input("Your message:")

    # Process user input
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Generating a response using the get_response function from llm.py
        response = get_response(prompt, llm="llama2", persona=persona, tone=response_tone, temperature=temperature)
        # Displaying the assistant's response
        st.session_state.messages.append({"role": "assistant", "content": response})
        # st.text_area("Bim:", value=response, height=150, max_chars=None, key=None)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
   

if __name__ == "__main__":
    main()