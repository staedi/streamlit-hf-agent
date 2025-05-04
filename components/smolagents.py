# from langchain_community.retrievers import BM25Retriever
# import streamlit as st

# Initialize model (defaults to llama3.1)
def init_model(model:str='llama3.1:8b-instruct-q4_0'):
    from smolagents import LiteLLMModel

    llm_model = LiteLLMModel(
        model_id=f"ollama_chat/{model}",
        api_base="http://localhost:11434",
        num_ctx=8192,
        )

    return llm_model


# Load the dataset
def prepare_dataset(path="agents-course/unit3-invitees", split="train"):
    import datasets

    guest_dataset = datasets.load_dataset(path=path, split=split)

    return guest_dataset

# Create retriever
def create_retriever(dataset=None):
    from langchain.docstore.document import Document

    if not dataset:
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        # Simulate a knowledge base about party planning
        party_ideas = [
            {"text": "A superhero-themed masquerade ball with luxury decor, including gold accents and velvet curtains.", "source": "Party Ideas 1"},
            {"text": "Hire a professional DJ who can play themed music for superheroes like Batman and Wonder Woman.", "source": "Entertainment Ideas"},
            {"text": "For catering, serve dishes named after superheroes, like 'The Hulk's Green Smoothie' and 'Iron Man's Power Steak'.", "source": "Catering Ideas"},
            {"text": "Decorate with iconic superhero logos and projections of Gotham and other superhero cities around the venue.", "source": "Decoration Ideas"},
            {"text": "Interactive experiences with VR where guests can engage in superhero simulations or compete in themed games.", "source": "Entertainment Ideas"}
        ]

        source_docs = [
            Document(page_content=doc["text"], metadata={"source": doc["source"]})
            for doc in party_ideas
        ]
        
        # Split the documents into smaller chunks for more efficient search
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            add_start_index=True,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        docs = text_splitter.split_documents(source_docs)

    else:
        # Convert dataset entries into Document objects
        docs = [
            Document(
                page_content="\n".join([
                    f"Name: {item['name']}",
                    f"Relation: {item['relation']}",
                    f"Description: {item['description']}",
                    f"Email: {item['email']}"
                ]),
                metadata={"name": item['name']}
            )
            for item in dataset
        ]

    return docs

    # bm25_retriever = BM25Retriever.from_defaults(nodes=docs)

    # if "retriever" not in st.session_state:
    #     st.session_state.retriever = bm25_retriever
