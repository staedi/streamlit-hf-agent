# Initialize model (defaults to llama3.1)
def init_model(model:str='llama3.1:8b-instruct-q4_0'):
    from llama_index.llms.ollama import Ollama

    llm_model = Ollama(
        model=model,
        request_timeout=360.0
        )

    return llm_model

# Initialize embedding model for vector store (defaults to huggingface)
def init_embed_model(model:str='BAAI/bge-small-en-v1.5'):
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    embed_model = HuggingFaceEmbedding(model_name=model)

    return embed_model

# Initialize vector store (chroma DB)
def init_vector_store(path:str='alfred_chroma_db',db_name:str='alfred'):
    import chromadb
    from llama_index.vector_stores.chroma import ChromaVectorStore

    db = chromadb.PersistentClient(path=path)
    chroma_collection = db.get_or_create_collection(db_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    return vector_store

# Initialize vector index
def init_vector_index(vector_store,embed_model):
    from llama_index.core import VectorStoreIndex

    vector_index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,embed_model=embed_model
    )

    return vector_index

# Load the dataset
def prepare_dataset(path="agents-course/unit3-invitees", split="train"):
    import datasets

    guest_dataset = datasets.load_dataset(path=path, split=split)

    return guest_dataset

# Create retriever
def create_retriever(dataset):
    from llama_index.core.schema import Document
    from llama_index.retrievers.bm25 import BM25Retriever
    import streamlit as st

    # Convert dataset entries into Document objects
    docs = [
        Document(
            text="\n".join([
                f"Name: {dataset['name'][i]}",
                f"Relation: {dataset['relation'][i]}",
                f"Description: {dataset['description'][i]}",
                f"Email: {dataset['email'][i]}"
            ]),
            metadata={"name": dataset['name'][i]}
        )
        for i in range(len(dataset))
    ]

    bm25_retriever = BM25Retriever.from_defaults(nodes=docs)

    if "retriever" not in st.session_state:
        st.session_state.retriever = bm25_retriever
