from helpers import utils
import tools.smolagents
import components.smolagents
import streamlit as st

# Create Tools
def create_tool(task_type:str, work_type:str):
    tool_list = []

    if task_type.find('Tool') != -1:
        tool_list = [tools.smolagents.suggest_menu]

    if task_type in ('DuckDuckGo', 'Tool_complete'):
        from smolagents import DuckDuckGoSearchTool

        if task_type == 'DuckDuckGo':
            tool_list = [DuckDuckGoSearchTool()]

        elif task_type == 'Python_imports':
            from smolagents import VisitWebpageTool

            tool_list = [
                DuckDuckGoSearchTool(),
                VisitWebpageTool(),
                tools.smolagents.suggest_menu,
                tools.smolagents.catering_service_tool,
                tools.smolagents.SuperheroPartyThemeTool(),
            ]

        elif task_type == 'Custom_KB':
            docs = components.smolagents.create_retriever()
            # Create the retriever tool
            party_planning_retriever = tools.smolagents.PartyPlanningRetrieverTool(docs)
            tool_list = [party_planning_retriever]

    elif task_type == 'RAG':
        dataset = components.smolagents.prepare_dataset()
        docs = components.smolagents.create_retriever(dataset)
        tool_list = [
            tools.smolagents.GuestInfoRetrieverTool(docs),
            tools.smolagents.WeatherInfoTool(),
            tools.smolagents.HubStatsTool()
        ]

    return tool_list

# Initialize the Agent (CodeAgent, ToolCallAgent)
def init_agent(init:bool, model:str='llama3.1:8b-instruct-q4_0', work_type:str='CodeAgent', task_type=None):
    # # Agent can be initialized only under the following conditions
    # 1) New (init)
    # 2) Different framework (agent['framework'] != 'smolagents)
    # 3) Different agent_type (agent['agent_type'] != work_type)
    # 4) Different task_type (agent['task_type'] != task_type)

    # if init and not utils.validate_agent(framework='smolagents',work_type=agent_type,task_type=task_type):

    # Init model
    llm_model = components.smolagents.init_model(model=model)

    # Call Tool
    tools = create_tool(task_type=task_type,work_type=work_type)

    # ToolCallingAgent (JSON)
    if work_type == 'ToolCallingAgent':
        from smolagents import ToolCallingAgent

        agent = ToolCallingAgent(
            model=llm_model,
            tools=tools,
        )

    # CodeAgent (by default)
    else:
        from smolagents import CodeAgent

        if task_type == 'Python_imports':
            agent = CodeAgent(
                model=llm_model,
                tools=tools,
                additional_authorized_imports=['datetime']
            )

        elif task_type == 'Tool_complete':
            agent = CodeAgent(
                model=llm_model,
                tools=tools,
                max_steps=10,
                verbosity_level=2
            )

        # elif task_type == 'RAG':
        #     agent = CodeAgent(
        #         model=llm_model,
        #         tools=tools,
        #         add_base_tools=True,  # Add any additional base tools
        #         planning_interval=3   # Enable planning every 3 steps
        #     )

        else:
            agent = CodeAgent(
                model=llm_model,
                tools=tools,
                # add_base_tools=True
            )

    # Store to the session_state
    st.session_state['agent'] = {'framework':'smolagents','work_type':work_type,'task_type':task_type,'agent':agent}

# Run the agent
def run_agent(query:str):
    if utils.validate_agent(framework='smolagents'):
    # if 'agent' in st.session_state and \
    #     st.session_state.agent['framework'] == 'smolagents' and \
    #     st.session_state.agent['agent']:

        response = st.session_state.agent['agent'].run(query)
        return response

def await_result(query:str):
    response = run_agent(query)
    st.write(response)
    st.session_state.messages.append({'role':'assistant','content':response})