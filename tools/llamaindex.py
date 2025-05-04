import random
from llama_index.core.tools import FunctionTool, QueryEngineTool
import components.llamaindex

# Call via Tool (w/o Agent)
def get_weather(location: str) -> str:
    """Useful for getting the weather for a given location."""
    # print(f"Getting weather for {location}")
    return f"The weather in {location} is sunny"

# Initialize the tool
weather_tool = FunctionTool.from_defaults(
    get_weather,
    # name="weather tool",
    # description="Useful for getting the weather for a given location."
)

# Call via Agent
def get_weather_info(location: str) -> str:
    """Fetches dummy weather information for a given location."""
    # Dummy weather data
    weather_conditions = [
        {"condition": "Rainy", "temp_f": 60},
        {"condition": "Clear", "temp_f": 80},
        {"condition": "Windy", "temp_f": 70}
    ]
    # Randomly select a weather condition
    data = random.choice(weather_conditions)
    return f"Weather in {location}: {data['condition']}, {data['temp_f']}°F"

# Initialize the tool
weather_info_tool = FunctionTool.from_defaults(get_weather_info)

def init_query_engine(model:str='llama3.1:8b-instruct-q4_0'):
    vector_store = components.llamaindex.init_vector_store()
    embed_model = components.llamaindex.init_embed_model()
    llm_model = components.llamaindex.init_model(model)
    
    vector_index = components.llamaindex.init_vector_index(vector_store=vector_store,embed_model=embed_model)
    query_engine = vector_index.as_query_engine(llm=llm_model)

    return query_engine

# Initialize the tool
query_engine_tool = QueryEngineTool.from_defaults(
    query_engine=init_query_engine(),
)

def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

def divide(a: int, b: int) -> int:
    """Divide two numbers"""
    return a / b

def get_hub_stats(author: str) -> str:
    """Fetches the most downloaded model from a specific author on the Hugging Face Hub."""

    from huggingface_hub import list_models

    try:
        # List models from the specified author, sorted by downloads
        models = list(list_models(author=author, sort="downloads", direction=-1, limit=1))

        if models:
            model = models[0]
            return f"The most downloaded model by {author} is {model.id} with {model.downloads:,} downloads"
        else:
            return f"No models found for author {author}."
        
    except Exception as e:
        return f"Error fetching models for {author}: {str(e)}"
    
# Initialize the tool
hub_stats_tool = FunctionTool.from_defaults(get_hub_stats)

# Create guest_info_tool
def get_guest_info_retriever(query: str) -> str:
    """Retrieves detailed information about gala guests based on their name or relation."""

    import streamlit as st

    results = st.session.retriever.retrieve(query)
    if results:
        return "\n\n".join([doc.text for doc in results[:3]])
    else:
        return "No matching guest information found."
        
# Initialize the tool
guest_info_tool = FunctionTool.from_defaults(get_guest_info_retriever)