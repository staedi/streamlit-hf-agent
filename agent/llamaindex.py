from helpers import utils
import tools.llamaindex
import components.llamaindex
import streamlit as st

# Create Tools
def create_tool(task_type:str, work_type:str):
    tool_list = []

    # Tool only
    if task_type == 'Weather':
        tool_list = tools.llamaindex.weather_tool

    # Tool and Agent
    elif task_type == 'QueryEngine':
        tool_list = tools.llamaindex.query_engine_tool

    # Agent only
    elif task_type == 'Calculation':
        if work_type == 'Agent':
            tool_list = [tools.llamaindex.add, tools.llamaindex.subtract, tools.llamaindex.multiply, tools.llamaindex.divide]
        elif work_type == 'Workflow':
            tool_list = [tools.llamaindex.add, tools.llamaindex.multiply]

    # RAG
    elif task_type == 'RAG':
        dataset = components.llamaindex.prepare_dataset()
        components.llamaindex.create_retriever(dataset=dataset)
        tool_list = [tools.llamaindex.weather_info_tool,tools.llamaindex.hub_stats_tool,tools.llamaindex.guest_info_tool]

    # Only Agent accept list (tool_list being converted to list)
    if work_type != 'Tool' and not isinstance(tool_list,list):
        tool_list = [tool_list]

    return tool_list

# Initialize the Agent (Tools, AgentWorkflow)
def init_agent(init:bool, model:str='llama3.1:8b-instruct-q4_0', work_type:str='Tool', task_type=None):
    # # Agent can be initialized only under the following conditions
    # 1) New (init)
    # 2) Different framework (agent['framework'] == 'llamaindex)
    # 3) Different agent_type (agent['work_type'] != work_type)
    # 4) Different task_type (agent['task_type'] != task_type)

    # if init and not utils.validate_agent(framework='smolagents',work_type=agent_type,task_type=task_type):

    # Init model
    llm_model = components.llamaindex.init_model(model=model)

    # Call Tool
    tools = create_tool(task_type=task_type,work_type=work_type)

    # Tools (w/o Agent)
    if work_type == 'Tool':
        agent = tools

    # AgentWorkflow (Multi Agent)
    elif work_type == 'Workflow':
        from llama_index.core.agent.workflow import ReActAgent, AgentWorkflow

        if task_type == 'Calculation':
            agent_list = [
                ReActAgent(
                    name="add_agent",
                    description="Is able to add two integers",
                    system_prompt="A helpful assistant that can use a tool to add numbers.",
                    tools=[tools[0]],
                    llm=llm_model,
                ),
                ReActAgent(
                    name="multiply_agent",
                    description="Is able to multiply two integers",
                    system_prompt="A helpful assistant that can use a tool to multiply numbers.",
                    tools=[tools[1]], 
                    llm=llm_model,
                )
            ]
  
            agent = AgentWorkflow(
                agents=agent_list,
                root_agent=agent_list[-1].name
            )
  
    # AgentWorkflow (Single Agent)
    else:
        from llama_index.core.agent.workflow import AgentWorkflow

        # Init system_prompt
        if task_type in ('Calculation', 'QueryEngine'):
            if task_type == 'Calculation':
                system_prompt = "You are a math agent that can add, subtract, multiply, and divide numbers using provided tools. Show the step-by-step reasoning before providing the answer."
            elif task_type == 'QueryEngine':
                system_prompt = "You are a helpful assistant that has access to a database containing persona descriptions."

            agent = AgentWorkflow.from_tools_or_functions(
                tools,
                llm=llm_model,
                system_prompt=system_prompt
            )

        else:
            agent = AgentWorkflow.from_tools_or_functions(
                tools,
                llm=llm_model
            )

    # Store to the session_state
    st.session_state['agent'] = {'framework':'llamaindex','work_type':work_type,'task_type':task_type,'agent':agent}

# Run the agent
async def run_agent(query:str):
    if utils.validate_agent(framework='llamaindex'):
    # if 'agent' in st.session_state and \
    #     st.session_state.agent['framework'] == 'smolagents' and \
    #     st.session_state.agent['agent']:

        if st.session_state.agent['work_type'] == 'Tool':
            response = await st.session_state.agent['agent'].acall(query)
        else:
            response = await st.session_state.agent['agent'].run(query)

        return response

async def await_result(query:str):
    response = await run_agent(query)

    # Tool
    if utils.validate_agent(framework='llamaindex') and st.session_state.agent['work_type'] == 'Tool':
        st.write(response.content)
        st.session_state.messages.append({'role':'assistant','content':response.content})

    # Agent
    else:
        st.write(response.response.blocks[0].text)
        st.session_state.messages.append({'role':'assistant','content':response.response.blocks[0].text})