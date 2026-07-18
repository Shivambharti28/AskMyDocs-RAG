import logfire

MAX_CONTEXT_CHARS = 10000


# def build_prompt(question: str, retrieved_chunks: list[dict]) -> str:
def build_prompt(question: str,retrieved_chunks: list[dict],conversation_history: list[dict] | None = None,) -> str:
    """
    Build a grounded prompt for the LLM using retrieved chunks.

    Args:
        question: User's question.
        retrieved_chunks: List of retrieved chunks from Qdrant.

    Returns:
        A formatted prompt ready to send to the LLM.
    """

    with logfire.span(
        "📝 Building Prompt",
        retrieved_chunks=len(retrieved_chunks),
    ):
        # Remove duplicate chunks

        seen = set()
        unique_chunks = []

        for chunk in retrieved_chunks:
            text = chunk.get("text") or chunk.get("content", "")

            if text in seen:
                continue

            seen.add(text)
            unique_chunks.append(chunk)


        # System Instructions

        instruction = """
You are an Enterprise AI Assistant.

You must answer the user's question ONLY using the provided context.

Rules:
1. Use ONLY the retrieved context.
2. Do NOT use outside knowledge.
3. Do NOT hallucinate or invent facts.
4. If the answer cannot be found in the context, respond exactly:
   "I couldn't find this information in the provided documents."
5. If multiple documents contain useful information, combine them into one coherent answer.
6. When possible, cite the document name and page number naturally.
7. Keep the answer clear, concise, and well-structured.
"""


        


        # Build Conversation History

        history = ""

        if conversation_history:

            history += (
                "==================================================\n"
                    "CONVERSATION HISTORY\n"
                "==================================================\n\n"
            )

            for message in conversation_history:

                role = message["role"].upper()
                content = message["content"]

                history += f"{role}: {content}\n\n"

        else:

            history = (
                "==================================================\n"
                "CONVERSATION HISTORY\n"
                "==================================================\n\n"
                "No previous conversation.\n\n"
            )
        # Build Context


        context = ""

        for i, chunk in enumerate(unique_chunks, start=1):

            source = chunk.get("source", "Unknown")
            page = chunk.get("page", "Unknown")
            section = chunk.get("section")
            text = chunk.get("text") or chunk.get("content", "")

            # Skip empty chunks
            if not text.strip():
                continue

            # Show section only if meaningful
            section_text = ""
            if section and not str(section).startswith("Page"):
                section_text = f"\nSection : {section}"

            next_chunk = f"""
==================================================
DOCUMENT {i}
==================================================

Source : {source}
Page   : {page}{section_text}

Content:
{text}


--------------------------------------------------

"""

            # Prevent prompt from exceeding context budget
            if len(context) + len(next_chunk) > MAX_CONTEXT_CHARS:
                logfire.warning(
                    "Maximum context size reached.",
                    max_context_chars=MAX_CONTEXT_CHARS,
                )
                break

            context += next_chunk


        # Final Prompt

        prompt = f"""
{instruction}

{history}

==================================================
RETRIEVED CONTEXT
==================================================

{context}

==================================================
CURRENT QUESTION
==================================================

{question}

==================================================
ANSWER
==================================================
"""

#         prompt = f"""
# {instruction}

# ==================================================
# CONTEXT
# ==================================================

# {context}

# ==================================================
# QUESTION
# ==================================================

# {question}

# ==================================================
# ANSWER
# ==================================================
# """

        logfire.info(
            "Prompt built successfully.",
            unique_chunks=len(unique_chunks),
            context_length=len(context),
            prompt_length=len(prompt),
        )

        return prompt