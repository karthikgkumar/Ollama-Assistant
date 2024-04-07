from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv
import webbrowser
import re
from googlesearch import search

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Task"
os.environ["LANGCHAIN_API_KEY"] = "ls__77f7c12d414c42b3acc75bc256e8c62a"

print(os.environ["LANGCHAIN_API_KEY"])
llm = Ollama(model="phi:latest", base_url="http://ollama-container:11435/", verbose=True)

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
    # Regular expression 
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, input_text)
    if "close" in input_text.lower():
        for url in urls:
            close_webpage(url)
        return f"Closing webpage(s): {', '.join(urls)}"
    elif "open" in input_text.lower():
        google_results = search(input_text, num=1, stop=1, pause=2)
        # Extract URL   search results
        for url in google_results:
            open_webpage(url)
            return f"Opening: {url}"
    else:
        return send_prompt(input_text)

def send_prompt(prompt):
    global llm
    response = llm.invoke(prompt)
    return response

print("Chat with Ollama")
while True:
    prompt = input("Your question: ")
    if prompt:
        print(f"User: {prompt}")
        response = handle_input(prompt)
        print(f"Assistant: {response}")
