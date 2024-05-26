import streamlit as st
import replicate
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Set page title
st.set_page_config(page_title="🤖💬 𝕮𝖆𝖗𝖊𝖊𝖗𝕮𝖔𝖒𝖕𝖆𝖘𝖘")

# Sidebar with API token and model selection
with st.sidebar:
    st.title('🤖💬 𝕮𝖆𝖗𝖊𝖊𝖗𝕮𝖔𝖒𝖕𝖆𝖘𝖘')
    st.write('This chatbot is created to assist in navigation through Four3.')
    replicate_api = st.secrets.get('REPLICATE_API_TOKEN', '')
    
    if replicate_api:
        st.success('API key already provided!', icon='✅')
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
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
    temperature = st.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('max_length', min_value=32, max_value=128, value=120, step=8)
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

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
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    try:
        output = replicate.run(
            llm,
            input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                   "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1}
        )
        return output
    except replicate.exceptions.ReplicateError as e:
        st.error(f"ReplicateError: {e}")
        return None

# User-provided prompt
prompt = st.chat_input(disabled=not replicate_api)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant" and prompt:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            if response:
                full_response = ''.join(response)
                st.write(full_response)
                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)
                st.session_state.chat_history.append((prompt, full_response))
            else:
                st.error("Failed to generate a response. Please check your API key and input parameters.")

# Button to navigate back to the blog app
if st.button("Back to Blog App"):
    st.write("You will be redirected to the blog app.")
    # Implement the redirection logic if needed

