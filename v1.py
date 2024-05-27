import streamlit as st
import replicate
import os
from dotenv import load_dotenv
from utils import replicate_run  # Import the debounced function
import time
import webbrowser

# Load environment variables
load_dotenv(dotenv_path="api.env")

# Pre-prompt for the Llama model
PRE_PROMPT = "You are a helpful personal assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as a Personal Assistant."

# Set page title
st.set_page_config(page_title="🤖💬 CareerCompass")

replicate_api = os.getenv('REPLICATE_API_TOKEN')

# Sidebar with API token and model selection
with st.sidebar:
    st.title('🤖💬 CareerCompass')
    st.write('This chatbot is created to assist in making career choices.')


    if replicate_api:
        st.success('API key loaded from environment!', icon='✅')
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    st.subheader('Models and parameters')
    selected_model = st.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    
    st.markdown("📖 Explore our career-focused social blog app for expert advice, valuable insights, and connections to fuel your professional growth. Join us now @ [Four3](https://tr7j.github.io/Blogging-app)!")

    # Button to navigate back to the blog app
    if st.button("Click ☝️"):
        st.markdown("<a href='https://tr7j.github.io/Blogging-app/' target='_blank'>Click here</a>", unsafe_allow_html=True)
# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to display chat history
def display_chat_history():
    for i, (user, assistant) in enumerate(st.session_state.chat_history):
        st.text_area(f"User [{i}]", value=user, height=50, max_chars=None, key=f"user_{i}", disabled=True)
        st.text_area(f"Assistant [{i}]", value=assistant, height=50, max_chars=None, key=f"assistant_{i}", disabled=True)

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.session_state.chat_history = []

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = PRE_PROMPT + "\n\n"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate_run(llm, {"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                 "repetition_penalty": 1})
    return output

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            full_response = ''
            for item in response:
                full_response += item
            st.write(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
    st.session_state.chat_history.append((prompt, full_response))
