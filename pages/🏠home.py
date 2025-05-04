import streamlit as st

def get_main():
    st.header("Welcome to the LLM Playground 👋")
    st.write("This is a Streamlit ported version of the Huggingface Agent Course")

def get_sidebar():
    st.sidebar.markdown('Home')

def load_frontend():
    get_main()
    get_sidebar()

load_frontend()