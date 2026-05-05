from langchain_ollama import ChatOllama
from .vector_store import get_or_create_collection
import os

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")

# session memory (manual)
session_memories = {}

# 🔥 Wrapper class (same feel as old chain)
class ConversationalRAGWrapper:
    def __init__(self, llm, retriever, memory):
        self.llm = llm
        self.retriever = retriever
        self.memory = memory

    def invoke(self, inputs: dict):
        question = inputs.get("question", "")

        # 1. retrieve docs
        docs = self.retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in docs])

        # 2. build prompt (with memory)
        history_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in self.memory]
        )

        prompt = f"""
You are a helpful assistant.

Chat History:
{history_text}

Context:
{context}

Question:
{question}
"""

        # 3. LLM call
        response = self.llm.invoke(prompt)
        answer = response.content

        # 4. save memory
        self.memory.append({"role": "user", "content": question})
        self.memory.append({"role": "assistant", "content": answer})

        return {
            "answer": answer,
            "source_documents": docs
        }


# ✅ SAME FUNCTION NAME
def get_rag_chain(session_id: str):
    vectorstore = get_or_create_collection(session_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    if session_id not in session_memories:
        session_memories[session_id] = []

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_URL,
        temperature=0.2
    )

    # 🔥 return wrapper (same interface)
    return ConversationalRAGWrapper(
        llm,
        retriever,
        session_memories[session_id]
    )


# ✅ SAME FUNCTION NAME
def ask_question(session_id: str, question: str):
    chain = get_rag_chain(session_id)

    result = chain.invoke({"question": question})

    sources = list(set([
        doc.metadata.get("source", "Unknown")
        for doc in result.get("source_documents", [])
    ]))

    return result["answer"], sources