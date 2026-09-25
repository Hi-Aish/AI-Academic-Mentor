import chromadb


CHROMA_PATH = "./data/chroma"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name="academic_documents"
)


def add_chunks(chunks, embeddings, document_id, filename):
    ids = []
    documents = []
    metadatas = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        chunk_id = f"{document_id}_{index}"

        ids.append(chunk_id)

        documents.append(chunk["text"])

        metadatas.append({
            "document_id": document_id,
            "filename": filename,
            "page": chunk["page"],
            "chunk_index": chunk.get("chunk_index", index)
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(ids)


def search(query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    return results