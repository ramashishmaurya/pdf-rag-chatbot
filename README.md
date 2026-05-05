# 🧠 DocuMind — AI-Powered Document Research Assistant

> Upload your documents and chat with them using local AI — no API keys, no cloud, full privacy.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-1.2.17-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-latest-red?logo=streamlit)
![Ollama](https://img.shields.io/badge/Ollama-local-black)
![Redis](https://img.shields.io/badge/Redis-latest-red?logo=redis)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)

---

## 📌 What is DocuMind?

DocuMind is a **production-grade RAG (Retrieval-Augmented Generation)** application that lets you upload multiple documents (PDF, DOCX, TXT) and have an intelligent conversation with them — powered entirely by **local LLMs via Ollama**.

No OpenAI. No API costs. No data leaving your machine.

---

## ✨ Features

- 📄 **Multi-document upload** — PDF, DOCX, TXT supported
- 🤖 **Local LLM** — Powered by Ollama (qwen2.5 / llama2)
- 🧠 **Conversational RAG** — Follow-up questions with full context awareness
- 📚 **Source citations** — Every answer shows which document it came from
- 🗂️ **Redis chat history** — Conversation history persisted across sessions (24hr TTL)
- 🔒 **Session isolation** — Each user gets their own document collection
- 🐳 **Docker ready** — Run everything with one command
- ⚡ **FastAPI backend** — Clean REST API with Swagger docs

---

## 🏗️ Architecture

```
User (Browser)
      │
      ▼
┌─────────────┐
│  Streamlit  │  ← Frontend UI (Port 8501)
│   Frontend  │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   FastAPI   │  ← REST API Backend (Port 8000)
│   Backend   │
└──────┬──────┘
       │
   ┌───┴────────────────┐
   │                    │
   ▼                    ▼
┌──────────┐     ┌─────────────┐
│ ChromaDB │     │    Redis    │
│ (Vectors)│     │  (History)  │
└──────────┘     └─────────────┘
       │
       ▼
┌─────────────┐
│   Ollama    │  ← Local LLM (Port 11434)
│  (qwen2.5)  │
└─────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Chat UI |
| Backend | FastAPI | REST API |
| RAG Framework | LangChain 1.2.17 | RAG pipeline |
| LLM | Ollama + qwen2.5 | Answer generation |
| Embeddings | nomic-embed-text | Document vectorization |
| Vector Store | ChromaDB | Document storage & retrieval |
| Chat History | Redis | Session persistence |
| Containerization | Docker + Docker Compose | Deployment |

---

## 📁 Project Structure

```
pdf-rag-chatbot/
├── backend/
│   ├── main.py                   # FastAPI app entry point
│   ├── .env                      # Environment variables
│   ├── requirements.txt          # Python dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py             # Document upload endpoint
│   │   └── chat.py               # Chat & history endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag_pipeline.py       # LangChain RAG logic
│   │   ├── vector_store.py       # ChromaDB operations
│   │   ├── document_loader.py    # File loading & chunking
│   │   └── chat_history.py       # Redis chat history
│   └── models/
│       ├── __init__.py
│       └── schemas.py            # Pydantic request/response models
├── frontend/
│   └── app.py                    # Streamlit UI
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed
- Docker (optional, for Redis)
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pdf-rag-chatbot.git
cd pdf-rag-chatbot
```

---

### 2. Setup Virtual Environment

```bash
python -m venv myvenv

# Windows
myvenv\Scripts\activate

# Mac/Linux
source myvenv/bin/activate
```

---

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
pip install streamlit requests  # for frontend
```

---

### 4. Pull Ollama Models

```bash
ollama pull qwen2.5
ollama pull nomic-embed-text
```

---

### 5. Start Redis (via Docker)

```bash
docker run -d -p 6379:6379 --name redis redis
```

---

### 6. Configure Environment

Create `backend/.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5
CHROMA_DB_PATH=./chroma_db
REDIS_URL=redis://localhost:6379
```

---

### 7. Run the Application

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
streamlit run app.py
```

---

### 8. Open in Browser

| Service | URL |
|---|---|
| 🖥️ Streamlit UI | http://localhost:8501 |
| 📖 API Docs (Swagger) | http://localhost:8000/docs |
| 🔌 API Base | http://localhost:8000/api |

---

## 🐳 Docker Deployment

Run everything with a single command:

```bash
docker-compose up --build
```

Then pull models inside Ollama container:

```bash
docker exec -it ollama ollama pull qwen2.5
docker exec -it ollama ollama pull nomic-embed-text
```

---

## 📡 API Reference

### Upload Document
```http
POST /api/upload
Content-Type: multipart/form-data

session_id: string
file: File (PDF / DOCX / TXT)
```

**Response:**
```json
{
  "message": "✅ 'document.pdf' uploaded successfully!",
  "chunks": 42,
  "session_id": "abc-123"
}
```

---

### Chat with Documents
```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "abc-123",
  "question": "What is this document about?"
}
```

**Response:**
```json
{
  "answer": "The document is about...",
  "sources": ["document.pdf"],
  "session_id": "abc-123"
}
```

---

### Clear Chat History
```http
DELETE /api/chat/{session_id}/history
```

---

## 🔄 How RAG Works

```
1. UPLOAD PHASE
   PDF/DOCX/TXT
        ↓
   Text Extraction (PyPDF / Docx2txt)
        ↓
   Chunking (500 chars, 50 overlap)
        ↓
   Embeddings (nomic-embed-text via Ollama)
        ↓
   ChromaDB (stored per session)

2. CHAT PHASE
   User Question
        ↓
   Load chat history from Redis
        ↓
   History-Aware Retriever
   (rephrase question with context)
        ↓
   ChromaDB similarity search (top 4 chunks)
        ↓
   LLM (qwen2.5) generates answer
        ↓
   Save to Redis + return answer + sources
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `qwen2.5` | LLM model name |
| `CHROMA_DB_PATH` | `./chroma_db` | Vector DB storage path |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection URL |

---

## 🧪 Supported Models

Any Ollama model works! Recommended:

| Model | Size | Best For |
|---|---|---|
| `qwen2.5` | 4.7GB | Best quality (default) |
| `llama2` | 3.8GB | Alternative |
| `mistral` | 4.1GB | Fast responses |
| `phi3` | 2.3GB | Low resource systems |

Change model in `.env`:
```env
OLLAMA_MODEL=mistral
```

---

## 🐛 Common Issues

**Ollama connection refused:**
```bash
ollama serve  # manually start ollama
```

**ChromaDB error:**
```bash
pip install chromadb --upgrade
```

**Redis connection failed:**
```bash
docker start redis  # if container exists
# or
docker run -d -p 6379:6379 --name redis redis
```

**Module not found:**
```bash
# Make sure venv is activated
myvenv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — feel free to use this project for learning and production.

---

## 👨‍💻 Author

Built with ❤️ using LangChain, FastAPI, and Ollama.

> *"The goal was to build a production-grade RAG system that works completely offline, respects privacy, and demonstrates real-world AI engineering skills."*
