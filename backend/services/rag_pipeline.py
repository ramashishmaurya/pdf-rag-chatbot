import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from services.vector_store import get_or_create_collection

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")

session_histories: dict[str, list] = {}


def get_llm():
    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_URL,
        temperature=0.2
    )


def get_chat_history(session_id: str) -> list:
    return session_histories.get(session_id, [])


def build_rag_chain(session_id: str):
    vectorstore = get_or_create_collection(session_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = get_llm()

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Given the chat history and the latest user question, "
         "rewrite it as a standalone question. "
         "Do NOT answer it, just rephrase if needed, otherwise return as is."
         ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful assistant. "
         "Use the following retrieved context to answer the question. "
         "If you don't know the answer, say you don't know. "
         "Keep the answer concise.\n\n"
         "Context:\n{context}"
         ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain


def ask_question(session_id: str, question: str):
    try:
        print(f"[INFO] Building RAG chain for session: {session_id}")
        rag_chain = build_rag_chain(session_id)
        chat_history = get_chat_history(session_id)

        print(f"[INFO] Invoking chain with question: {question}")
        result = rag_chain.invoke({
            "input": question,
            "chat_history": chat_history
        })

        print(f"[INFO] Result keys: {result.keys()}")
        answer = result.get("answer", "Sorry, I could not generate an answer.")

        if session_id not in session_histories:
            session_histories[session_id] = []

        session_histories[session_id].extend([
            HumanMessage(content=question),
            AIMessage(content=answer)
        ])

        sources = list(set([
            doc.metadata.get("source", "Unknown")
            for doc in result.get("context", [])
        ]))

        return answer, sources

    except Exception as e:
        print(f"[ERROR] ask_question failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e