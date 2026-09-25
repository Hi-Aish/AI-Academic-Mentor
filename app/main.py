import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel


load_dotenv()


from app.rag.pdf_loader import extract_pages
from app.rag.chunker import chunk_pages
from app.rag.embeddings import embed_documents
from app.rag.vector_store import add_chunks
from app.rag.retriever import retrieve
from app.rag.generator import generate_answer


app = FastAPI(
    title="AI Academic Mentor",
    description="RAG-based academic study assistant",
    version="1.0.0"
)


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "AI Academic Mentor RAG is running"
    }


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    document_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}.pdf"
    )

    file_data = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(file_data)

    # 1. Extract text
    pages = extract_pages(file_path)

    if not pages:
        raise HTTPException(
            status_code=400,
            detail="No readable text found in PDF."
        )

    # 2. Chunk text
    chunks = chunk_pages(pages)

    # 3. Generate embeddings
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embed_documents(texts)

    # 4. Store in vector DB
    stored_count = add_chunks(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document_id,
        filename=file.filename
    )

    return {
        "message": "Document successfully indexed",
        "document_id": document_id,
        "filename": file.filename,
        "pages": len(pages),
        "chunks": stored_count
    }


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5


@app.post("/chat")
def chat(request: QuestionRequest):
    # 1. Retrieve relevant chunks
    retrieved_chunks = retrieve(
        question=request.question,
        top_k=request.top_k
    )

    if not retrieved_chunks:
        return {
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": []
        }

    # 2. Generate answer
    answer = generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    # 3. Return sources
    sources = []

    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]
        sources.append({
            "document": metadata["filename"],
            "page": metadata["page"],
            "distance": chunk["distance"]
        })

    return {
        "answer": answer,
        "sources": sources
    }