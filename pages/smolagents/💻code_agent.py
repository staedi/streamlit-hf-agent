import os
import sys

ref_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0,ref_dir)

import frontend
import streamlit as st

def get_main():
    global framework, work_type, model_lists, task_lists
    
    framework, work_type = 'smolagents', 'CodeAgent'

    st.subheader(f"Welcome to `{framework} - {work_type}()` Playground 👋")

    model_lists = {
        "Choose a model": None,
        "llama3.1": "llama3.1:8b-instruct-q4_0",
        "qwen2.5-coder": "qwen2.5-coder:7b-instruct"
    }

    task_lists = {
        "smolagents":
        {
            "DuckDuckGo": "Search for the best music recommendations for a party at the Wayne's mansion.",
            "Tool_decorator": "Prepare a formal menu for the party.",
            "Python_imports": 
            """
            Alfred needs to prepare for the party. Here are the tasks:
            1. Prepare the drinks - 30 minutes
            2. Decorate the mansion - 60 minutes
            3. Set up the menu - 45 minutes
            4. Prepare the music and playlist - 45 minutes
            
            If we start right now, at what time will the party be ready?
            """,
            "Tool_complete": "Give me best playlist for a party at the Wayne's mansion. The party idea is a 'villain masquerade' theme"
        }
    }

def load_frontend():
    get_main()
    frontend.get_sidebar(work_type=work_type,model_lists=model_lists,task_lists=task_lists,framework=framework)
    # get_chat_view()

load_frontend()