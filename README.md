# 🎓 AI Academic Mentor (RAG Backend)

An intelligent, production-ready Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **ChromaDB**, **Google Gemini** (for vector embeddings), and **Groq** (for ultra-fast LLM text generation). 

This application allows students and researchers to upload academic PDF documents, automatically indexes and vectorizes the text content, and enables precise semantic Q&A with exact source page citations.

## 🚀 Key Features

- **Document Ingestion & Processing**: Automatically parses PDF documents page-by-page.

- **Smart Text Chunking**: Splits academic text logically to preserve context and metadata (filenames, page numbers).

- **Dual-Provider Architecture**:

  -Uses **Google Gemini** for high-quality text embedding generation.

  -Uses **Groq (Llama/OpenAI-OSS models)** for instantaneous, free-tier LLM response generation.

- **Persistent Vector Storage**: Leverages ChromaDB for fast, persistent semantic similarity searches.

- **Grounded Answers**: Strict system constraints prevent hallucinations and force the AI to cite exact document pages.

- **Interactive API Docs**: Built-in Swagger UI via FastAPI for seamless testing.

## 🛠️ Tech Stack

- **Framework**: FastAPI, Uvicorn

- **Database & Vector Search**: ChromaDB

- **Embeddings**: Google Gemini API (gemini-embed-001 / standard embedding endpoints)

- **Generation**: Groq API (openai/gpt-oss-20b or Llama models)

- **PDF Processing**: PyPDF / custom loaders

- **Environment Management**: python-dotenv

## 📂 Project Directory Structure

```
AI-Academic-Mentor/
│
├── backend/
│   ├── app/
│   │   ├── rag/
│   │   │   ├── pdf_loader.py
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── vector_store.py
│   │   │   ├── retriever.py
│   │   │   └── generator.py
│   │   └── main.py
│   ├── data/
│   │   └── chroma/       # Persistent vector database store
│   ├── uploads/          # Uploaded PDF files
│   ├── .env              # Environment configuration (Secret Keys)
│   └── requirements.txt  # Python dependencies
│
└── README.md
```

## ⚙️ Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Hi-Aish/AI-Academic-Mentor.git
cd AI-Academic-Mentor/backend
```

### 2. Create and Activate a Virtual Environment

Windows (CMD / PowerShell):
```powershell
python -m venv venv
venv\Scripts\activate
```

Mac / Linux:
```Bash
python3 -m venv venv
source venv/bin/activate
```
## 3. Install Dependencies

```Bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables

Create a `.env` file inside the `backend/ ` directory and add your API keys:

Code snippet
```
GEMINI_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
``` 

## 🚀 Running the Application

Start the FastAPI development server with live-reload:

```Bash
uvicorn app.main:app --reload
```

Once running, open your browser and navigate to:

Interactive API Docs (Swagger UI): `http://127.0.0.1:8000/docs`

Root Health Check: `http://127.0.0.1:8000/`

## 🔌 API Endpoints Reference

## 1. Upload Academic Document

- **Endpoint**: `POST /documents/upload`

- **Content-Type**: `multipart/form-data`

- **Description** : Uploads a `.pdf` file, extracts text, chunks it, embeds it, and stores vectors in ChromaDB.

### 2. Chat / Query Assistant

- **Endpoint**: `POST /chat`

- **Content-Type**: `application/json`

- **Request Body Example**:

JSON
```
{
  "question": "What are the core concepts covered in chapter 1?",
  "top_k": 5
}
```

- ***Response***: Returns a grounded answer along with source document names, page numbers, and distance scores.

