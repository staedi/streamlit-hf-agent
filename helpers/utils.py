import os
import glob
import asyncio

import streamlit as st
import re

def get_filename():
    # Return the current filename
    return os.path.realpath('__').split('/')[-1]

def set_page_meta(path):
    # Set title
    title = path[path.rfind('/')+1:path.rfind('.py')].title().replace('_','')
    
    # Remove emoji from the title
    title = re.sub(r'[^a-zA-Z]','',title)

    # Generate the Page properties
    return st.Page(path,title=title)

# Filter out unavailable framework (i.e., smolagents or llamaindex)
def filter_framework():
    framework_filter = []

    try:
        import smolagents

    except:
        framework_filter.append('smolagents')
        try:
            import llama_index
        except:
            framework_filter.append('llamaindex')

    finally:
        try:
            import llama_index
        except:
            framework_filter.append('llamaindex')

    return framework_filter

def get_paths(root:str = 'pages'):
    # Get the path structure (dir/file)
    paths = glob.glob(f'{root}/**/*.py',recursive=True)

    # Available framework only
    framework_filter = filter_framework()

    paths = [path for path in paths for framework in framework_filter if path.find(framework)==-1]

    # Prepare key for each navigation
    keys = [path[path.rfind('/')+1:path.rfind('.py')] if '/' not in path[path.find('/')+1:] else path[path.find('/')+1:path.rfind('/')] for path in paths]
    # Replace emoji in the Category
    keys = [re.sub(r'[^a-zA-Z]','',key) for key in keys]

    # Initialize dictionary
    page_dict = {key:[] for key in keys}

    # Populate the dictionary
    for key, path in zip(keys, paths):
        page_dict.get(key).append(set_page_meta(path))

    # Convert key to title()
    pages = {key.title():value for key, value in page_dict.items()}

    return pages

# Validate if the tool/agent (namely, work) has been created
def validate_agent(framework:str,work_type=None,task_type=None) -> bool:
    status = False

    if work_type and task_type:
        if 'agent' in st.session_state and \
            st.session_state.agent['framework'] == framework and \
            st.session_state.agent['work_type'] == work_type and \
            st.session_state.agent['task_type'] == task_type and \
            st.session_state.agent['agent']:
            status = True

    # task_type (tools) not specified
    elif work_type:
        if 'agent' in st.session_state and \
            st.session_state.agent['framework'] == framework and \
            st.session_state.agent['work_type'] == work_type and \
            st.session_state.agent['agent']:
            status = True

    else:
        if 'agent' in st.session_state and \
            st.session_state.agent['framework'] == framework and \
            st.session_state.agent['agent']:
            status = True

    return status

# Silence the torch error
def init_async():
    import torch
    torch.classes.__path__ = [] # add this line to manually set it to empty. 


def run_async_task(async_func, *args):
    """
    Run an asynchronous function in a new event loop.

    Args:
    async_func (coroutine): The asynchronous function to execute.
    *args: Arguments to pass to the asynchronous function.

    Returns:
    None
    """
    
    loop = None

    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(async_func(*args))
    except:
        # Close the existing loop if open
        if loop is not None:
            loop.close()

        # Create a new loop for retry
        loop = asyncio.new_event_loop()

        loop.run_until_complete(async_func(*args))
    finally:
        if loop is not None:
            loop.close()