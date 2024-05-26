import replicate
import streamlit as st
import os
from dotenv import load_dotenv
import webbrowser

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Finance Bot💵 ", page_icon="💵")

# REPLICATE_API_URL = "https://replicate.com/account/api-tokens"
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

with st.sidebar:
    st.title("💵💬CareerCompass")
    st.write("Explore our career-focused social blog app for expert advice, valuable insights, and connections to fuel your professional growth. Join us now!")
    headers = {
    "Authorization": f"Token {REPLICATE_API_TOKEN}",
    "Content-Type": "application/json"
}

    st.subheader('Models and Parameters')
    selected_model = st.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
            llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
            llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'

    temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=32, max_value=128, value=120, step=8)
       
# first message to be initialized 
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to The Hub Bot! I'm here to help you with any questions about finance. What can I assist you with today?"}]

st.subheader("chats")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
     st.session_state.messages = [{"role": "assistant", "content": "Welcome to The Hub Bot! I'm here to help you with any questions about finance. What can I assist you with today?"}]
st.sidebar.button("Delete chats", on_click=clear_chat_history)


#answer 
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.\n\n"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    output = replicate.run(
        llm,  
        input={"prompt": f"{string_dialogue} {prompt_input}\nAssistant: ", "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1.0}
    )
    return output


# Chat input and response generation
if prompt := st.chat_input(placeholder="hello friend"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gathering best info..."):
            response = generate_llama2_response(prompt)
            full_response = ''.join(response)
            st.write(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

with st.sidebar:
    st.write()
    if st.button("Four3"):
         st.markdown("Click me to go back to back to [The Hub]()")
          

    if st.button("Live Stock"):
        st.markdown("Get to see [live stocks](https://fib.co.ke/live-markets/) get to understand the current  market") 

    if st.button("Live Stock"):
        st.markdown("Get to see [live stocks](https://fib.co.ke/live-markets/) get to understand the current  market") 
