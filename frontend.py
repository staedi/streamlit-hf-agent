from helpers import utils
import streamlit as st

depths = {"smolagents": ["💻code_agent.py","🔨tool_calling_agent.py","🔎agentic_RAG.py"],
          "llamaindex": ["🔨tools.py","🕵️agents.py","workflows.py"],
          "use-case": ["Complete"]}

def get_nav(pages):
    utils.init_async()
    nav = st.navigation(pages)
    nav.run()


def get_sidebar(work_type:str, model_lists:dict, task_lists:dict, framework:str):
    # with st.sidebar:
    # Framework: llamaindex
    # global framework
    # framework = st.sidebar.selectbox('Framework is',options=['smolagents','llamaindex'],index=0,disabled=True)
    framework = st.sidebar.selectbox('Framework is',options=[framework],index=0,disabled=True)

    # Model: llama3.1 and qwen2.5-coder
    model = st.sidebar.selectbox('Choose an LLM model',options=model_lists.keys())

    if model.lower().find('choose') == -1:
        task = st.sidebar.selectbox('Choose a task',options=task_lists[framework].keys())

        # get_chat_view(framework=framework,work_type=work_type,task_type=task,task_lists=task_lists)
        init_agent = st.sidebar.button('Init agent')

        if init_agent: #or not utils.validate_agent(framework=framework,agent_type=work_type,task_type=task):
            if framework == 'smolagents':
            # if is_agent:
                import agent.smolagents
                agent.smolagents.init_agent(init=True,model=model_lists[model],work_type=work_type,task_type=task)
            elif framework == 'llamaindex':
                import agent.llamaindex
                agent.llamaindex.init_agent(init=True,model=model_lists[model],work_type=work_type,task_type=task)

        get_chat_view(framework=framework,work_type=work_type,task_type=task,task_lists=task_lists)


def get_chat_view(framework:str, work_type:str, task_type:str, task_lists:dict):
    if not utils.validate_agent(framework=framework,work_type=work_type):
        st.session_state.messages = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if utils.validate_agent(framework=framework,work_type=work_type,task_type=task_type):
        query = task_lists[framework][task_type]

        # st.write(query)
        # query = st.chat_input('Enter a query.')

        if query:
            with st.chat_message("user"):
                st.markdown(f"***Task type: `{task_type}`***")
                st.write(query)
                st.session_state.messages.append({'role':'user','content':query})

            with st.chat_message("assistant"):
                try:
                    if framework == 'smolagents':
                        import agent.smolagents
                        agent.smolagents.await_result(query)
                    elif framework == 'llamaindex':
                        import agent.llamaindex
                        utils.run_async_task(agent.llamaindex.await_result,query)
                except Exception as e:
                    st.error(e)
                    st.error(f"An error ocurred")


# def load_frontend():
#     # get_main()
#     get_sidebar()
#     # get_chat_view()

# load_frontend()