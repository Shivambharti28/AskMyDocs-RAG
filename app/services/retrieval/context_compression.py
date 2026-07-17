from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)


def compress_chunks(question: str, chunks: list):
    """
    Compress retrieved chunks using a single Gemini call.

    If compression fails, the original chunks are returned.
    """

    if not chunks:
        return []

    prompt = f"""
You are an Enterprise RAG Context Compressor.

User Question:
{question}

Below are retrieved chunks.

For EACH chunk:

- Keep ONLY the sentences directly useful for answering the user's question.
- Preserve the original wording.
- Remove unrelated information.
- Do NOT summarize.
- Do NOT rewrite.
- Do NOT add new information.
- Do NOT change the order.

Return the compressed chunks in EXACTLY the same order.

Separate every chunk using the following delimiter exactly:

====================
"""

    for i, chunk in enumerate(chunks, start=1):

        prompt += f"""

Chunk {i}

{chunk["text"]}

====================
"""


    try:
        response = llm.invoke(prompt)

    except Exception as e:
        print("\nContext Compression Failed")
        print(e)
        print("Using original retrieved chunks.\n")

        return chunks


    print("\n========== COMPRESSED RESPONSE ==========\n")
    print(response.content)
    print("\n=========================================\n")

    # ------------------------------
    # Split Response
    # ------------------------------

    compressed = [
        text.strip()
        for text in response.content.split("====================")
        if text.strip()
    ]


    if len(compressed) != len(chunks):

        print(
            f"\nCompression returned {len(compressed)} chunks "
            f"but expected {len(chunks)}."
        )

        print("Using original chunks instead.\n")

        return chunks

    compressed_chunks = []

    for original_chunk, compressed_text in zip(chunks, compressed):

        new_chunk = original_chunk.copy()

        if compressed_text:
            new_chunk["text"] = compressed_text
        else:
            new_chunk["text"] = original_chunk["text"]

        compressed_chunks.append(new_chunk)

    print(
        f"Successfully compressed {len(compressed_chunks)} chunks.\n"
    )

    return compressed_chunks