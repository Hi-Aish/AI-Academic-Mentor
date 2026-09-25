import os
from google import genai
from google.genai import types


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


EMBEDDING_MODEL = "gemini-embedding-001"


def embed_documents(texts: list[str]):
    """
    Convert document chunks into embedding vectors.
    """

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768
        )
    )

    return [embedding.values for embedding in result.embeddings]


def embed_query(query: str):
    """
    Convert a student's question into an embedding vector.
    """

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values