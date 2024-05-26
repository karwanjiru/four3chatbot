import streamlit as st
import os
from dotenv import load_dotenv
from utils import replicate_run
import webbrowser

# Load environment variables
load_dotenv()

# Pre-prompt for the Llama model
PRE_PROMPT = "You are a helpful personal assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as a Personal Assistant."

# Set page title
st.set_page_config(page_title="🤖💬 CareerCompass")

# Sidebar with API token and model selection
with st.sidebar:
    st.title('🤖💬 CareerCompass')
    st.write('This chatbot is created to assist in navigation through Four3.')

    replicate_api = os.getenv('REPLICATE_API_TOKEN')
    if replicate_api:
        st.success('API key loaded from environment!', icon='✅')
    else:
        st.warning('API key not found in environment. Please check your .env file.', icon='⚠️')

    st.subheader('Models and parameters')
    selected_model = st.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    # Add more model selection options if needed

    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

    # Button to navigate back to the blog app
    if st.button("Back to Blog App"):
        webbrowser.open_new_tab('https://github.com/TR7J/Blogging-app/tree/master/src')

# Store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = PRE_PROMPT + "\n\n"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    try:
        output = replicate_run(llm, {
            "prompt": f"{string_dialogue} {prompt_input} Assistant: ",
            "repetition_penalty": 1
        })
        return output
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# User-provided prompt
if prompt := st.text_input(label="Input prompt"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(st.session_state.messages[-1]["content"])
            if response:
                for item in response:
                    st.write(item)
                st.session_state.messages.append({"role": "assistant", "content": response})
