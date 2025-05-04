import os
import sys

ref_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0,ref_dir)

import frontend
import streamlit as st

def get_main():
    global framework, work_type, model_lists, task_lists
    
    framework, work_type = 'llamaindex', 'Agent'

    st.subheader(f"Welcome to `{framework} - {work_type}()` Playground 👋")

    model_lists = {
        "Choose a model": None,
        "llama3.1": "llama3.1:8b-instruct-q4_0",
        "qwen2.5-coder": "qwen2.5-coder:7b-instruct"
    }

    task_lists = {
        "llamaindex":
        {
            "Calculation": "What is (2 + 2) * 2?",
            "QueryEngine": "Search the database for 'science fiction' and return some persona descriptions."
        }
    }

def load_frontend():
    get_main()
    frontend.get_sidebar(work_type=work_type,model_lists=model_lists,task_lists=task_lists,framework=framework)
    # get_chat_view()

load_frontend()