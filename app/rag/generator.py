import os
from groq import Groq


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Using openai (Versatile & smart for academic mentoring)
GENERATION_MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are an AI Academic Mentor.
Answer the student's question using the provided academic context.

Rules:
1. Use the provided context as the primary source of truth.
2. Do not invent facts that are not supported by the context.
3. If the context does not contain enough information, clearly say that
   the uploaded study material does not contain enough information.
4. Explain concepts clearly for a student.
5. When possible, mention the source page.
"""


def generate_answer(question: str, retrieved_chunks):
    """
    Generate a grounded answer using Groq based on retrieved chunks.
    """
    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]
        context_parts.append(
            f"""
SOURCE {index}
Document: {metadata["filename"]}
Page: {metadata["page"]}

Content:
{chunk["text"]}
"""
        )

    context = "\n\n".join(context_parts)

    user_prompt = f"""
ACADEMIC CONTEXT:

{context}

STUDENT QUESTION:

{question}

Answer the question using the academic context following the system rules.
"""

    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content