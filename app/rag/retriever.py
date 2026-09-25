from .embeddings import embed_query
from .vector_store import search


def retrieve(question: str, top_k: int = 5):
    """
    Retrieve the top-k most relevant chunks for a student's question.
    """

    query_embedding = embed_query(question)

    results = search(
        query_embedding=query_embedding,
        top_k=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved_chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        retrieved_chunks.append({
            "text": document,
            "metadata": metadata,
            "distance": distance
        })

    return retrieved_chunks