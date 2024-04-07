from langchain_community.llms import Ollama
import streamlit as st
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv
import webbrowser
import re
from googlesearch import search

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

print(os.environ["LANGCHAIN_API_KEY"])
llm = Ollama(model="phi:latest", base_url="http://ollama-container:11434", verbose=True)




def open_webpage(url):
    webbrowser.open_new_tab(url)


def close_webpage(url_to_close):
    browser_windows = webbrowser._browsers.values()
    for browser in browser_windows:
        for tab in browser:
            if tab.url == url_to_close:
                tab.close()
                return f"Closed tab: {url_to_close}"



def handle_input(input_text):
    # Regular expression to identify URLs in the input_text
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Find all URLs in the input_text
    urls = re.findall(url_pattern, input_text)
    if "close" in input_text.lower():
        for url in urls:
            for i in input_text.split():
                if i in url:
                    close_webpage(url)
        return f"Closing webpage(s): {', '.join(urls)}"
    elif "open" in input_text.lower():
        google_results = search(input_text, num=1, stop=1, pause=2)
        # Extract the first URL from the search results
        for url in google_results:
            open_webpage(url)
            return f"Opening: {url}"
    else:
        return sendPrompt(input_text)


def sendPrompt(prompt):
    global llm
    response = llm.invoke(prompt)
    return response

st.title("Chat with Ollama")
if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question !"}
    ]

if prompt := st.chat_input("Your question"): 
    st.session_state.messages.append({"role": "user", "content": prompt})


for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = handle_input(prompt)
            print(response)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) 


