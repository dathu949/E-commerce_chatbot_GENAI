import streamlit as st
import os
from  google import genai
from dotenv import load_dotenv

load_dotenv()

#configure  Api key 
os.environ['GEMINI_API_KEY'] = os.getenv('gemini_key')

#Initialize client once in session state
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

client = st.session_state.client

system_prompt = system_prompt = '''You are a expert in E-commerce Domain. ' \
'Respond to the user queries in 1 to 2 sentences.You should respond to user queries 
related to only E-commerce.If not E-commerce domain then say to user that you are only 
eligible to answer for E-commerce queries not for other domains.'''

st.title('E-commerce Chatbot')
st.write('Type your message below to chat with the model')

#Initialize the chat session only once
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model = 'gemini-2.5-flash',
        config = genai.types.GenerateContentConfig(
            system_instruction = system_prompt
        )
    )
if "messages" not in st.session_state:
    st.session_state.messages = []
print(st.session_state)

#Display past messages
for role,text in st.session_state.messages:
    if role == 'user':
        st.markdown(f"**you:** {text}")
    else:
        st.markdown(f"**Bot:{text}")

#chat input 
user_input = st.chat_input('Type your message here...')
if user_input:
    st.session_state.messages.append(("user",user_input))

    #send messsgae safely
    chat = st.session_state.chat_session
    response = chat.send_message(user_input)

    bot_reply = response.text
    st.session_state.messages.append(('bot',bot_reply))
    st.rerun()