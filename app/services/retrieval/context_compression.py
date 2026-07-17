from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)


def compress_chunks(question: str, chunks: list):

    if not chunks:
        return []

    prompt = f"""
You are an enterprise RAG context compressor.

User Question:
{question}

Below are retrieved chunks.

For EACH chunk:

- Keep ONLY the sentences useful for answering the question.
- Preserve the original wording.
- Remove unrelated information.
- Do NOT summarize.
- Do NOT rewrite.
- Do NOT add new information.

Return the compressed chunks in exactly the same order.

Separate every chunk using:

====================
"""

    for i, chunk in enumerate(chunks, start=1):

        prompt += f"""

Chunk {i}

{chunk["text"]}

====================
"""

    response = llm.invoke(prompt)
    print("\n===== COMPRESSED RESPONSE =====")
    print(response.content)

    compressed = response.content.strip().split(
        "===================="
    )

    compressed_chunks = []

    for chunk, text in zip(chunks, compressed):

        new_chunk = chunk.copy()
        new_chunk["text"] = text.strip()

        compressed_chunks.append(new_chunk)

    return compressed_chunks