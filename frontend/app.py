import streamlit as st
import requests
import uuid

API_URL = "http://backend:8000/api"

st.set_page_config(page_title="DocuMind", page_icon="🧠", layout="wide")
st.title("🧠 DocuMind — AI Document Research Assistant")

# Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar - Upload
with st.sidebar:
    st.header("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt"]
    )
    if uploaded_files:
        for file in uploaded_files:
            with st.spinner(f"Processing {file.name}..."):
                res = requests.post(
                    f"{API_URL}/upload",
                    data={"session_id": st.session_state.session_id},
                    files={"file": (file.name, file.getvalue())}
                )
                if res.status_code == 200:
                    st.success(res.json()["message"])
                else:
                    st.error("Upload failed!")

    st.divider()
    st.caption(f"Session: `{st.session_state.session_id[:8]}...`")
    if st.button("🔄 New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.rerun()

# Chat UI
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    st.write(f"• {s}")

# Input
if question := st.chat_input("Ask anything about your documents..."):
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = requests.post(
                f"{API_URL}/chat",
                json={"session_id": st.session_state.session_id, "question": question}
            )
            if res.status_code == 200:
                data = res.json()
                st.write(data["answer"])
                if data["sources"]:
                    with st.expander("📚 Sources"):
                        for s in data["sources"]:
                            st.write(f"• {s}")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data["sources"]
                })
            else:
                st.error("Something went wrong!")