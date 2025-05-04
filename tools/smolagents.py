import random
from smolagents import Tool, tool
from huggingface_hub import list_models
# import components.smolagents
# import streamlit as st

# RAG
# from langchain.docstore.document import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever

@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for a casual party.
                        - "formal": Menu for a formal party.
                        - "superhero": Menu for a superhero party.
                        - "custom": Custom menu.
    """

    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."

@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.

    Args:
        query: A search term for finding catering services.
    """

    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }

    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)

    return best_service

class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""

    inputs = {
        "category":
        {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic gotham')."
        }
    }

    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic gotham": "Non-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }

        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic gotham'.")
    
class PartyPlanningRetrieverTool(Tool):
    name = "party_planning_retriever"
    description = "Uses semantic search to retrieve relevant party planning ideas for Alfred's superhero-themed party at Wayne Manor."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be related to party planning or superhero themes.",
        }
    }
    output_type = "string"

    def __int__(self, docs, **kwargs):
        super().__init__(**kwargs)
        self.retriever = BM25Retriever.from_documents(
            docs, k=5 # Retrieve the top 5 documents
        )

    def forward(self, query:str) -> str:
        assert isinstance(query, str), "Your search must be a string"

        docs = self.retriever.invoke(
            query,
        )

        return "\nRetrieved ideas:\n" + "".join(
            [
                f"\n\n===== Idea {str(i)} =====\n" + doc.page_content
                for i, doc in enumerate(docs)
            ]
        )

class WeatherInfoTool(Tool):
    name = "weather_info"
    description = "Fetches dummy weather information for a given location."
    inputs = {
        "location": {
            "type": "string",
            "description": "The location to get weather information for."
        }
    }
    output_type = "string"

    def forward(self, location: str):
        # Dummy weather data
        weather_conditions = [
            {"condition": "Rainy", "temp_f": 60},
            {"condition": "Clear", "temp_f": 80},
            {"condition": "Windy", "temp_f": 70}
        ]
        # Randomly select a weather condition
        data = random.choice(weather_conditions)
        return f"Weather in {location}: {data['condition']}, {data['temp_f']}°F"

class HubStatsTool(Tool):
    name = "hub_stats"
    description = "Fetches the most downloaded model from a specific author on the Hugging Face Hub."
    inputs = {
        "author": {
            "type": "string",
            "description": "The username of the model author/organization to find models from."
        }
    }
    output_type = "string"

    def forward(self, author: str):
        try:
            # List models from the specified author, sorted by downloads
            models = list(list_models(author=author, sort="downloads", direction=-1, limit=1))

            if models:
                model = models[0]
                return f"The most downloaded model by {author} is {model.id} with {model.downloads:,} downloads."
            else:
                return f"No models found for author {author}."
        except Exception as e:
            return f"Error fetching models for {author}: {str(e)}"

class GuestInfoRetrieverTool(Tool):
    name = "guest_info_retriever"
    description = "Retrieves detailed information about gala guests based on their name or relation."
    inputs = {
        "query": {
            "type": "string",
            "description": "The name or relation of the guest you want information about.",
        }
    }
    output_type = "string"

    def __int__(self, docs):
        self.is_initialized = False
        self.retriever = BM25Retriever.from_documents(docs)

    def forward(self, query:str) -> str:
        # assert isinstance(query, str), "Your search must be a string"
        results = self.retriever.get_relevant_documents(query)

        if results:
            return "\n\n".join([doc.page_content for doc in results[:3]])
        else:
            return "No matching guest information found."