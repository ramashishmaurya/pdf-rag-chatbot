import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def get_embeddings():
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=OLLAMA_URL
    )


def get_or_create_collection(session_id: str):
    return Chroma(
        collection_name=session_id,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_PATH
    )


def add_documents(session_id: str, documents):
    vectorstore = get_or_create_collection(session_id)
    vectorstore.add_documents(documents)
    return vectorstore