# RagBot — RAG-based PDF Chatbot

RagBot is a Retrieval-Augmented Generation (RAG) application that lets you upload PDF documents and chat with them. It combines a FastAPI backend for document ingestion and question-answering with a Streamlit frontend for an interactive chat experience, and cites the source documents behind every answer.

## Features

- 📄 **Multi-PDF upload** — upload and index multiple PDFs at once
- 🔍 **Semantic search** — documents are chunked and embedded for retrieval-based Q&A
- 💬 **Conversational chat UI** — ask questions in natural language and get grounded answers
- 📚 **Source attribution** — every answer lists the source document(s) it was drawn from
- 💾 **Persistent vector store** — embeddings persist across sessions via Chroma
- ⬇️ **Chat history export** — download the conversation as a text file

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Uvicorn |
| LLM | Groq (`ChatGroq`, `openai/gpt-oss-20b`) via LangChain |
| Orchestration | LangChain (`RetrievalQA` chain) |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| Vector store | ChromaDB |
| Document loading | `PyPDFLoader`, `RecursiveCharacterTextSplitter` |
| Frontend | Streamlit |
| Logging | Loguru |

## Architecture

```
client/                    # Streamlit frontend
├── app.py                 # Entry point
├── config.py               # API URL config
├── components/
│   ├── upload.py           # PDF upload UI
│   ├── chatUI.py            # Chat interface
│   └── history_download.py  # Chat history export
└── utils/api.py             # HTTP client for backend calls

server/                    # FastAPI backend
├── main.py                 # API routes (/upload_pdfs/, /ask/, /test)
├── logger.py                # Loguru logger setup
└── modules/
    ├── load_vectorstore.py  # PDF parsing, chunking, embedding, Chroma indexing
    ├── llm.py                 # Groq LLM + RetrievalQA chain setup
    └── query_handlers.py      # Query execution and response formatting
```

**Flow:** PDFs uploaded via the Streamlit UI → sent to `/upload_pdfs/` → parsed and split into chunks → embedded and stored in a local Chroma vector store → user questions sent to `/ask/` → top-k relevant chunks retrieved → passed to the Groq LLM along with the question → answer + source documents returned to the UI.

## Getting Started

### Prerequisites

- Python 3.12+
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
git clone https://github.com/riteshsal/RagBot-.git
cd RagBot-

# using uv (recommended, repo includes a uv.lock)
uv sync

# or with pip
pip install -r requirements.txt
```

### Configuration

Create a `.env` file inside `server/`:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Running the app

Start the backend:

```bash
cd server
uvicorn main:app --reload
```

In a separate terminal, start the frontend:

```bash
cd client
streamlit run app.py
```

The backend runs at `http://127.0.0.1:8000` and the Streamlit UI opens automatically in your browser.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload_pdfs/` | Upload one or more PDFs to be chunked, embedded, and indexed |
| `POST` | `/ask/` | Ask a question; returns an answer with source document references |
| `GET` | `/test` | Health check |

## Possible Improvements

- Add authentication and per-user document scoping
- Support additional file types (docx, txt, web pages)
- Add streaming responses for the chat UI
- Containerize with Docker Compose for one-command setup
- Add automated tests for the ingestion and query pipeline

## License

Add a license of your choice (e.g., MIT) if you plan to share this publicly.
